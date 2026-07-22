"""
Case management endpoints.

SECURITY:
  - bank_id comes from JWT only, never request body
  - All queries filter by bank_id
  - Soft-delete only — legal documents have retention requirements
  - verify_case_bank_access raises 404 (not 403) to avoid leaking case existence
"""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.dependencies import (
    AdminDep, CurrentUser, DbDep, OfficerDep,
    get_client_ip, get_current_user, verify_case_bank_access,
)
from app.models.db import Case, write_audit_log
from app.services.compliance.pre_intake import run_f2_filter

router = APIRouter()


STAGE_PROGRESS: dict[str, int] = {
    "OCR": 10,
    "LANGUAGE_DETECTION": 20,
    "TRANSLATION": 30,
    "REGEX_EXTRACTION": 40,
    "NLP_EXTRACTION": 60,
    "POPULATING_WORKBENCH": 70,
    "PENDING_HUMAN_REVIEW": 80,
    "ANALYSING": 85,
    "PENDING_JUDGMENT_REVIEW": 90,
    "COMPLETE": 100,
}

STAGE_MESSAGES: dict[str, str] = {
    "OCR": "Running OCR on uploaded documents…",
    "LANGUAGE_DETECTION": "Detecting document language…",
    "TRANSLATION": "Translating documents to English…",
    "REGEX_EXTRACTION": "Extracting structured fields from documents…",
    "NLP_EXTRACTION": "Extracting facts for each ground and classifying SA grounds raised…",
    "POPULATING_WORKBENCH": "Populating officer workbench for review…",
    "PENDING_HUMAN_REVIEW": "Awaiting officer review of extracted facts.",
    "ANALYSING": "Running compliance engine and judgment retrieval…",
    "PENDING_JUDGMENT_REVIEW": "Awaiting judgment coverage review.",
    "COMPLETE": "Analysis complete.",
}


# ─── SCHEMAS ──────────────────────────────────────────────────────────────────

class CreateCaseRequest(BaseModel):
    borrower_name: str
    case_ref: Optional[str] = None
    drt_case_number: Optional[str] = None
    drt_bench: Optional[str] = None
    property_description: Optional[str] = None
    loan_account_number: Optional[str] = None
    principal_amount: Optional[Decimal] = None


class UpdateCaseRequest(BaseModel):
    borrower_name: Optional[str] = None
    case_ref: Optional[str] = None
    drt_case_number: Optional[str] = None
    drt_bench: Optional[str] = None
    property_description: Optional[str] = None
    loan_account_number: Optional[str] = None
    principal_amount: Optional[Decimal] = None


class CaseResponse(BaseModel):
    id: uuid.UUID
    bank_id: uuid.UUID
    created_by: uuid.UUID
    case_ref: Optional[str]
    drt_case_number: Optional[str]
    drt_bench: Optional[str]
    borrower_name: str
    property_description: Optional[str]
    loan_account_number: Optional[str]
    principal_amount: Optional[Decimal]
    status: str
    pipeline_stage: Optional[str]
    intake_filter_result: Optional[dict]
    judgment_coverage_alerts: Optional[list]
    created_at: datetime
    updated_at: datetime


class CaseSummaryResponse(BaseModel):
    id: uuid.UUID
    borrower_name: str
    case_ref: Optional[str]
    status: str
    pipeline_stage: Optional[str]
    principal_amount: Optional[Decimal]
    created_at: datetime


class CaseListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[CaseSummaryResponse]


class PipelineStatusResponse(BaseModel):
    case_id: uuid.UUID
    status: str
    pipeline_stage: Optional[str]
    progress_pct: int
    stage_message: str
    intake_filter_result: Optional[dict]


def _to_response(case: Case) -> CaseResponse:
    return CaseResponse(
        id=case.id,
        bank_id=case.bank_id,
        created_by=case.created_by,
        case_ref=case.case_ref,
        drt_case_number=case.drt_case_number,
        drt_bench=case.drt_bench,
        borrower_name=case.borrower_name,
        property_description=case.property_description,
        loan_account_number=case.loan_account_number,
        principal_amount=case.principal_amount,
        status=case.status,
        pipeline_stage=case.pipeline_stage,
        intake_filter_result=case.intake_filter_result,
        judgment_coverage_alerts=case.judgment_coverage_alerts,
        created_at=case.created_at,
        updated_at=case.updated_at,
    )


# ─── ENDPOINTS ────────────────────────────────────────────────────────────────

@router.post("", status_code=status.HTTP_201_CREATED, response_model=CaseResponse)
async def create_case(
    body: CreateCaseRequest,
    request: Request,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> CaseResponse:
    intake_result = None
    case_status = "DRAFT"

    if body.principal_amount is not None:
        intake_result = run_f2_filter(body.principal_amount)
        if intake_result is not None:
            case_status = intake_result.action

    case = Case(
        bank_id=current_user.bank_id,
        created_by=current_user.user_id,
        borrower_name=body.borrower_name,
        case_ref=body.case_ref,
        drt_case_number=body.drt_case_number,
        drt_bench=body.drt_bench,
        property_description=body.property_description,
        loan_account_number=body.loan_account_number,
        principal_amount=body.principal_amount,
        status=case_status,
        intake_filter_result=intake_result.model_dump() if intake_result else None,
    )
    db.add(case)
    await db.flush()

    await write_audit_log(
        db, action="CASE_CREATE",
        user_id=current_user.user_id,
        case_id=case.id,
        detail={"borrower_name": body.borrower_name, "status": case_status},
        ip_address=get_client_ip(request),
    )
    await db.commit()
    await db.refresh(case)
    return _to_response(case)


@router.get("", response_model=CaseListResponse)
async def list_cases(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> CaseListResponse:
    query = select(Case).where(Case.bank_id == current_user.bank_id)

    if status_filter:
        query = query.where(Case.status == status_filter)
    else:
        query = query.where(Case.status != "DELETED")

    if search:
        like = f"%{search}%"
        query = query.where(
            or_(
                Case.borrower_name.ilike(like),
                Case.case_ref.ilike(like),
                Case.drt_case_number.ilike(like),
            )
        )

    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar_one()

    query = query.order_by(Case.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    cases = result.scalars().all()

    return CaseListResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[
            CaseSummaryResponse(
                id=c.id,
                borrower_name=c.borrower_name,
                case_ref=c.case_ref,
                status=c.status,
                pipeline_stage=c.pipeline_stage,
                principal_amount=c.principal_amount,
                created_at=c.created_at,
            )
            for c in cases
        ],
    )


@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(
    case_id: uuid.UUID,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> CaseResponse:
    case = await verify_case_bank_access(case_id, current_user, db)
    return _to_response(case)


@router.patch("/{case_id}", response_model=CaseResponse)
async def update_case(
    case_id: uuid.UUID,
    body: UpdateCaseRequest,
    request: Request,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> CaseResponse:
    case = await verify_case_bank_access(case_id, current_user, db)

    if case.status not in ("DRAFT", "INTAKE_REJECTED"):
        raise HTTPException(
            status_code=409,
            detail="Case metadata can only be updated while in DRAFT or INTAKE_REJECTED status."
        )

    updated_fields = {}
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(case, field, value)
        updated_fields[field] = str(value)

    await write_audit_log(
        db, action="CASE_UPDATE",
        user_id=current_user.user_id,
        case_id=case.id,
        detail=updated_fields,
        ip_address=get_client_ip(request),
    )
    await db.commit()
    await db.refresh(case)
    return _to_response(case)


@router.get("/{case_id}/pipeline-status", response_model=PipelineStatusResponse)
async def get_pipeline_status(
    case_id: uuid.UUID,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> PipelineStatusResponse:
    case = await verify_case_bank_access(case_id, current_user, db)
    stage = case.pipeline_stage or case.status
    progress = STAGE_PROGRESS.get(stage, 0)
    message = STAGE_MESSAGES.get(stage, f"Status: {case.status}")
    return PipelineStatusResponse(
        case_id=case.id,
        status=case.status,
        pipeline_stage=case.pipeline_stage,
        progress_pct=progress,
        stage_message=message,
        intake_filter_result=case.intake_filter_result,
    )


@router.post("/{case_id}/resume", status_code=status.HTTP_202_ACCEPTED)
async def resume_analysis(
    case_id: uuid.UUID,
    request: Request,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> dict:
    """Officer-triggered — starts Chain B. NEVER called automatically."""
    from app.tasks.chain_b import run_chain_b_from_judgments

    case = await verify_case_bank_access(case_id, current_user, db)

    if case.status != "PENDING_HUMAN_REVIEW":
        raise HTTPException(
            status_code=409,
            detail=f"Chain B can only be started from PENDING_HUMAN_REVIEW status. Current: {case.status}."
        )

    run_chain_b_from_judgments.delay(str(case_id), str(current_user.user_id))

    await write_audit_log(
        db, action="CHAIN_B_TRIGGERED",
        user_id=current_user.user_id,
        case_id=case.id,
        ip_address=get_client_ip(request),
    )
    await db.commit()
    return {"detail": "Analysis started.", "case_id": str(case_id)}


@router.delete("/{case_id}", status_code=status.HTTP_200_OK)
async def delete_case(
    case_id: uuid.UUID,
    request: Request,
    current_user: CurrentUser = AdminDep,
    db: AsyncSession = DbDep,
) -> dict:
    """Soft delete only — legal documents have retention requirements."""
    case = await verify_case_bank_access(case_id, current_user, db)

    if case.status in ("PROCESSING", "ANALYSING"):
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a case while it is actively processing."
        )

    case.status = "DELETED"
    case.pipeline_stage = None

    await write_audit_log(
        db, action="CASE_SOFT_DELETE",
        user_id=current_user.user_id,
        case_id=case.id,
        ip_address=get_client_ip(request),
    )
    await db.commit()
    return {"detail": "Case marked as deleted.", "case_id": str(case_id)}
