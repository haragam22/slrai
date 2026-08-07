"""
Report endpoints — JSON, PDF download, and on-demand regeneration.

SECURITY:
  - bank_id scoping via verify_case_bank_access (never trust case_id alone)
"""

from __future__ import annotations

import asyncio
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import iterate_in_threadpool

from app.dependencies import CurrentUser, DbDep, OfficerDep, verify_case_bank_access
from app.models.db import Report
from app.services import storage

router = APIRouter()


async def _latest_report(case_id: uuid.UUID, db: AsyncSession) -> Report:
    result = await db.execute(
        select(Report).where(Report.case_id == case_id).order_by(Report.generated_at.desc())
    )
    report = result.scalars().first()
    if report is None:
        raise HTTPException(status_code=404, detail="No report generated for this case yet.")
    return report


@router.get("/{case_id}/report")
async def get_report(
    case_id: uuid.UUID,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
):
    await verify_case_bank_access(case_id, current_user, db)
    report = await _latest_report(case_id, db)
    return report.report_json


@router.get("/{case_id}/report/pdf")
async def download_report_pdf(
    case_id: uuid.UUID,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
):
    await verify_case_bank_access(case_id, current_user, db)
    report = await _latest_report(case_id, db)
    if not report.pdf_url:
        raise HTTPException(status_code=404, detail="PDF not available for this report.")
    try:
        return StreamingResponse(
            iterate_in_threadpool(storage.stream_document(report.pdf_url)),
            media_type="application/pdf",
        )
    except storage.DocumentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except storage.StorageError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/{case_id}/report")
async def regenerate_report(
    case_id: uuid.UUID,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
):
    await verify_case_bank_access(case_id, current_user, db)
    from app.reports.generator import generate_report

    result = await asyncio.to_thread(generate_report, str(case_id), str(current_user.user_id))
    return result
