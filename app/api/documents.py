"""
Document upload API.

SECURITY:
  - bank_id scoping via verify_case_bank_access (never trust case_id alone)
  - only application/pdf accepted (storage.validate_file_type)
  - duplicate detection: same sha256_hash + case_id = 409
"""

from __future__ import annotations

import asyncio
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import iterate_in_threadpool

from app.dependencies import CurrentUser, DbDep, OfficerDep, verify_case_bank_access
from app.models.db import Document
from app.services import storage
from app.services.extraction.doc_classifier import classify_document

router = APIRouter()

UPLOAD_RATE_LIMIT_SECONDS = 30


def _check_upload_rate_limit(case_id: uuid.UUID) -> bool:
    """One upload per case_id per 30s — Redis SET NX with TTL as the counter.
    Fails open (allows upload) if Redis itself is down; a stuck upload lock
    is worse than a missed rate-limit window."""
    import redis
    from app.config import settings

    key = f"upload_rate_limit:{case_id}"
    try:
        client = redis.from_url(settings.redis_url, socket_connect_timeout=3)
        return bool(client.set(key, "1", nx=True, ex=UPLOAD_RATE_LIMIT_SECONDS))
    except Exception:
        import logging
        logging.getLogger(__name__).exception("rate limit check failed for case=%s — failing open", case_id)
        return True


class DocumentResponse(BaseModel):
    id: uuid.UUID
    case_id: uuid.UUID
    doc_type: str
    original_filename: Optional[str]
    sha256_hash: str
    file_size: Optional[int]
    ocr_status: str
    uploaded_at: datetime


def _to_response(doc: Document) -> DocumentResponse:
    return DocumentResponse(
        id=doc.id,
        case_id=doc.case_id,
        doc_type=doc.doc_type,
        original_filename=doc.original_filename,
        sha256_hash=doc.sha256_hash,
        file_size=doc.file_size,
        ocr_status=doc.ocr_status,
        uploaded_at=doc.uploaded_at,
    )


@router.post("/{case_id}/documents", status_code=status.HTTP_201_CREATED, response_model=DocumentResponse)
async def upload_document(
    case_id: uuid.UUID,
    file: UploadFile = File(...),
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> DocumentResponse:
    from app.tasks.chain_a import run_chain_a

    case = await verify_case_bank_access(case_id, current_user, db)

    if not _check_upload_rate_limit(case_id):
        raise HTTPException(
            status_code=429,
            detail="Only one document upload per case allowed every 30 seconds.",
        )

    if case.status == "INTAKE_REJECTED":
        raise HTTPException(
            status_code=422,
            detail="This case was rejected at intake. Documents cannot be uploaded.",
        )

    try:
        storage.validate_file_type(file.content_type)
    except storage.UnsupportedMediaTypeError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc

    file_bytes = await file.read()

    sha256 = storage.compute_sha256(file_bytes)

    existing = await db.execute(
        select(Document).where(
            Document.case_id == case_id,
            Document.sha256_hash == sha256,
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="This document has already been uploaded for this case.")

    doc_id = uuid.uuid4()
    try:
        s3_key, sha256 = await asyncio.to_thread(
            storage.upload_document, file_bytes, str(case_id), str(doc_id), file.content_type
        )
    except storage.FileTooLargeError as exc:
        raise HTTPException(status_code=413, detail=str(exc)) from exc
    except storage.StorageUploadError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    first_500_chars = file_bytes[:2000].decode("utf-8", errors="ignore")[:500]
    doc_type = classify_document(first_500_chars)

    is_first_document = (await db.execute(
        select(Document).where(Document.case_id == case_id)
    )).scalar_one_or_none() is None

    document = Document(
        id=doc_id,
        case_id=case_id,
        uploaded_by=current_user.user_id,
        doc_type=doc_type,
        original_filename=file.filename,
        file_url=s3_key,
        sha256_hash=sha256,
        file_size=len(file_bytes),
    )
    db.add(document)

    if is_first_document:
        case.status = "PROCESSING"

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="This document has already been uploaded for this case.")
    await db.refresh(document)

    if is_first_document:
        run_chain_a.delay(str(case_id), str(doc_id))

    return _to_response(document)


@router.get("/{case_id}/documents", response_model=list[DocumentResponse])
async def list_documents(
    case_id: uuid.UUID,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> list[DocumentResponse]:
    await verify_case_bank_access(case_id, current_user, db)
    result = await db.execute(select(Document).where(Document.case_id == case_id).order_by(Document.uploaded_at))
    return [_to_response(d) for d in result.scalars().all()]


@router.get("/{case_id}/documents/{doc_id}", response_model=DocumentResponse)
async def get_document(
    case_id: uuid.UUID,
    doc_id: uuid.UUID,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> DocumentResponse:
    await verify_case_bank_access(case_id, current_user, db)
    result = await db.execute(
        select(Document).where(Document.id == doc_id, Document.case_id == case_id)
    )
    doc = result.scalar_one_or_none()
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found.")
    return _to_response(doc)


@router.get("/{case_id}/documents/{doc_id}/download")
async def download_document(
    case_id: uuid.UUID,
    doc_id: uuid.UUID,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
):
    from fastapi.responses import StreamingResponse

    await verify_case_bank_access(case_id, current_user, db)
    result = await db.execute(
        select(Document).where(Document.id == doc_id, Document.case_id == case_id)
    )
    doc = result.scalar_one_or_none()
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found.")
    try:
        return StreamingResponse(
            iterate_in_threadpool(storage.stream_document(doc.file_url)),
            media_type="application/pdf",
        )
    except storage.DocumentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except storage.StorageError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
