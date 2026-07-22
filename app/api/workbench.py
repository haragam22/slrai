"""Workbench API — fact review and confirmation.

Three item types (see confidence_router.py + fact_persistence.py):
  LOW_CONFIDENCE — extracted but confidence < threshold or nlp_implied or ALWAYS_HUMAN_CONFIRM
  NOT_FOUND      — required field never extracted (no case_facts row at all)
  CONFLICT       — two documents disagree (fact_conflicts row, unresolved)

The workbench is a live query, not a materialized table — items are derived
from case_facts/fact_conflicts state at read time.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import CurrentUser, DbDep, OfficerDep, get_client_ip, verify_case_bank_access
from app.models.db import CaseFact, FactConflict, Paragraph, write_audit_log
from app.services.extraction.confidence_router import ALWAYS_HUMAN_CONFIRM, CONFIDENCE_THRESHOLD

router = APIRouter()

# Fields the compliance engine requires that must exist as a case_fact somewhere.
# Minimal set for H4 — expands as YAML rule modules (H5) define their own field deps.
REQUIRED_FIELDS: dict[str, str] = {
    "notice_served": "M1 — Demand notice service",
    "objection_filed": "M1 — Borrower objection under 13(3A)",
    "bank_reply_given": "M1 — Bank reply to objection",
    "valuer_rbi_empanelled": "M4 — Valuation compliance",
    "demand_notice_date": "M1 — Demand notice date",
    "sa_filing_date": "M4 — SA filing date",
    "sa_applicant_type": "Routing — applicant relationship to property",
    "total_borrowers_in_loan": "M7 — Total borrowers in loan",
    "npa_classification_date": "M8 — NPA classification date",
    "date_of_last_payment": "M8 — Date of last payment",
}

FIELD_LABELS: dict[str, str] = {
    "notice_served": "Demand notice served",
    "objection_filed": "Objection filed by borrower",
    "bank_reply_given": "Bank reply given",
    "lease_claimed": "Lease claimed",
    "lease_registered": "Lease registered",
    "valuation_disputed": "Valuation disputed",
    "valuation_challenged_by_borrower": "Valuation challenged by borrower",
    "valuer_section_247_registered": "Valuer registered under Companies Act s.247",
    "valuer_rbi_empanelled": "Valuer RBI empanelled",
    "all_parties_served": "All parties served",
    "npa_premature_alleged": "NPA classification premature (alleged)",
    "msme_status_claimed": "MSME status claimed",
    "udyam_cert_in_bank_file": "Udyam certificate in bank file",
    "total_borrowers_in_loan": "Total borrowers in loan",
    "total_guarantors_in_loan": "Total guarantors in loan",
    "ibc_moratorium_active": "IBC moratorium active",
    "demand_notice_date": "Demand notice date",
    "sa_filing_date": "SA filing date",
    "sa_applicant_type": "SA applicant type",
    "npa_classification_date": "NPA classification date",
    "date_of_last_payment": "Date of last payment",
}


def _label(field_name: str) -> str:
    return FIELD_LABELS.get(field_name, field_name.replace("_", " ").title())


def _why_flagged(fact: CaseFact) -> str:
    if fact.field_name in ALWAYS_HUMAN_CONFIRM:
        return "Always requires human confirmation."
    if fact.extraction_method == "nlp_implied":
        return "Fact was implied, not explicitly stated."
    if (fact.confidence or 0.0) < CONFIDENCE_THRESHOLD:
        return f"Confidence below {int(CONFIDENCE_THRESHOLD * 100)}%."
    return "Flagged for review."


def _is_low_confidence(fact: CaseFact) -> bool:
    if fact.human_confirmed:
        return False
    if fact.extraction_method == "regex":
        return False
    if fact.field_name in ALWAYS_HUMAN_CONFIRM:
        return True
    if fact.extraction_method == "nlp_implied":
        return True
    return (fact.confidence or 0.0) < CONFIDENCE_THRESHOLD


# ─── SCHEMAS ──────────────────────────────────────────────────────────────────

class WorkbenchFactItem(BaseModel):
    fact_id: uuid.UUID
    field_name: str
    field_label: str
    extracted_value: Optional[str]
    confidence: float
    source_page: Optional[int]
    source_text: Optional[str]
    extraction_method: str
    module: str
    why_flagged: str


class WorkbenchNotFoundItem(BaseModel):
    field_name: str
    field_label: str
    module: str
    why_needed: str
    input_type: str
    hint: str


class WorkbenchConflictItem(BaseModel):
    conflict_id: uuid.UUID
    field_name: str
    field_label: str
    candidate_a_value: Optional[str]
    candidate_a_source: str
    candidate_b_value: Optional[str]
    candidate_b_source: str
    module: str


class WorkbenchResponse(BaseModel):
    low_confidence_items: list[WorkbenchFactItem]
    not_found_items: list[WorkbenchNotFoundItem]
    conflict_items: list[WorkbenchConflictItem]
    total_pending: int
    all_resolved: bool


class FactResponse(BaseModel):
    id: uuid.UUID
    field_name: str
    field_value: Optional[str]
    confidence: Optional[float]
    extraction_method: Optional[str]
    human_confirmed: bool
    source_page: Optional[int]
    requires_workbench: bool


class ConfirmFactRequest(BaseModel):
    corrected_value: Optional[str] = None
    human_confirmed: bool = True


class ConflictResolutionRequest(BaseModel):
    resolution: Literal["candidate_a", "candidate_b", "custom"]
    custom_value: Optional[str] = None


class WorkbenchCompleteRequest(BaseModel):
    trigger_analysis: bool = True


class WorkbenchCompleteResponse(BaseModel):
    case_id: uuid.UUID
    trigger_analysis: bool
    chain_b_task_id: Optional[str] = None


def _fact_to_response(fact: CaseFact) -> FactResponse:
    return FactResponse(
        id=fact.id,
        field_name=fact.field_name,
        field_value=fact.field_value,
        confidence=fact.confidence,
        extraction_method=fact.extraction_method,
        human_confirmed=fact.human_confirmed,
        source_page=fact.source_page,
        requires_workbench=_is_low_confidence(fact),
    )


# ─── ENDPOINTS ────────────────────────────────────────────────────────────────

@router.get("/{case_id}/workbench", response_model=WorkbenchResponse)
async def get_workbench(
    case_id: uuid.UUID,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> WorkbenchResponse:
    await verify_case_bank_access(case_id, current_user, db)

    facts_result = await db.execute(select(CaseFact).where(CaseFact.case_id == case_id))
    facts = facts_result.scalars().all()

    para_ids = {fact.source_paragraph_id for fact in facts if fact.source_paragraph_id}
    paragraphs_by_id: dict[uuid.UUID, Paragraph] = {}
    if para_ids:
        paras_result = await db.execute(select(Paragraph).where(Paragraph.id.in_(para_ids)))
        paragraphs_by_id = {p.id: p for p in paras_result.scalars().all()}

    low_confidence_items = []
    present_fields = set()
    for fact in facts:
        present_fields.add(fact.field_name)
        if not _is_low_confidence(fact):
            continue
        source_text = None
        if fact.source_paragraph_id:
            para = paragraphs_by_id.get(fact.source_paragraph_id)
            if para:
                source_text = para.get_text()
        low_confidence_items.append(WorkbenchFactItem(
            fact_id=fact.id,
            field_name=fact.field_name,
            field_label=_label(fact.field_name),
            extracted_value=fact.field_value,
            confidence=fact.confidence or 0.0,
            source_page=fact.source_page,
            source_text=source_text,
            extraction_method=fact.extraction_method or "unknown",
            module="COMPLIANCE",
            why_flagged=_why_flagged(fact),
        ))

    not_found_items = [
        WorkbenchNotFoundItem(
            field_name=field_name,
            field_label=_label(field_name),
            module="COMPLIANCE",
            why_needed=why_needed,
            input_type="boolean",
            hint="Check the relevant document and confirm manually.",
        )
        for field_name, why_needed in REQUIRED_FIELDS.items()
        if field_name not in present_fields
    ]

    conflicts_result = await db.execute(
        select(FactConflict).where(FactConflict.case_id == case_id, FactConflict.resolved == False)  # noqa: E712
    )
    conflicts = conflicts_result.scalars().all()
    conflict_items = [
        WorkbenchConflictItem(
            conflict_id=c.id,
            field_name=c.field_name,
            field_label=_label(c.field_name),
            candidate_a_value=c.candidate_a_value,
            candidate_a_source=f"Page {c.candidate_a_source_page}" if c.candidate_a_source_page else "Unknown source",
            candidate_b_value=c.candidate_b_value,
            candidate_b_source=f"Page {c.candidate_b_source_page}" if c.candidate_b_source_page else "Unknown source",
            module="COMPLIANCE",
        )
        for c in conflicts
    ]

    total_pending = len(low_confidence_items) + len(not_found_items) + len(conflict_items)
    return WorkbenchResponse(
        low_confidence_items=low_confidence_items,
        not_found_items=not_found_items,
        conflict_items=conflict_items,
        total_pending=total_pending,
        all_resolved=(total_pending == 0),
    )


@router.get("/{case_id}/facts", response_model=list[FactResponse])
async def get_all_facts(
    case_id: uuid.UUID,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> list[FactResponse]:
    await verify_case_bank_access(case_id, current_user, db)
    result = await db.execute(select(CaseFact).where(CaseFact.case_id == case_id))
    return [_fact_to_response(f) for f in result.scalars().all()]


@router.patch("/{case_id}/facts/{fact_id}", response_model=FactResponse)
async def confirm_fact(
    case_id: uuid.UUID,
    fact_id: uuid.UUID,
    body: ConfirmFactRequest,
    request: Request,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> FactResponse:
    """Confirm or correct a single fact. Writes an audit_log entry."""
    await verify_case_bank_access(case_id, current_user, db)

    result = await db.execute(
        select(CaseFact).where(CaseFact.id == fact_id, CaseFact.case_id == case_id)
    )
    fact = result.scalar_one_or_none()
    if fact is None:
        raise HTTPException(status_code=404, detail="Fact not found.")

    if body.corrected_value is not None:
        fact.field_value = body.corrected_value
        fact.extraction_method = "human_confirmed"
    fact.human_confirmed = body.human_confirmed
    fact.confirmed_by = current_user.user_id
    fact.confirmed_at = datetime.now(timezone.utc)
    fact.confidence = 1.0

    await write_audit_log(
        db, action="FACT_CONFIRM",
        user_id=current_user.user_id,
        case_id=case_id,
        detail={"field_name": fact.field_name, "corrected": body.corrected_value is not None},
        ip_address=get_client_ip(request),
    )
    await db.commit()
    await db.refresh(fact)
    return _fact_to_response(fact)


@router.patch("/{case_id}/workbench/conflicts/{conflict_id}", response_model=FactResponse)
async def resolve_conflict(
    case_id: uuid.UUID,
    conflict_id: uuid.UUID,
    body: ConflictResolutionRequest,
    request: Request,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> FactResponse:
    await verify_case_bank_access(case_id, current_user, db)

    result = await db.execute(
        select(FactConflict).where(FactConflict.id == conflict_id, FactConflict.case_id == case_id)
    )
    conflict = result.scalar_one_or_none()
    if conflict is None:
        raise HTTPException(status_code=404, detail="Conflict not found.")
    if conflict.resolved:
        raise HTTPException(status_code=409, detail="Conflict already resolved.")

    if body.resolution == "candidate_a":
        resolved_value = conflict.candidate_a_value
    elif body.resolution == "candidate_b":
        resolved_value = conflict.candidate_b_value
    else:
        if body.custom_value is None:
            raise HTTPException(status_code=422, detail="custom_value required when resolution is 'custom'.")
        resolved_value = body.custom_value

    conflict.resolved = True
    conflict.resolved_value = resolved_value
    conflict.resolved_by = current_user.user_id
    conflict.resolved_at = datetime.now(timezone.utc)

    fact_result = await db.execute(
        select(CaseFact).where(CaseFact.case_id == case_id, CaseFact.field_name == conflict.field_name)
    )
    fact = fact_result.scalar_one_or_none()
    if fact is None:
        fact = CaseFact(case_id=case_id, field_name=conflict.field_name)
        db.add(fact)

    fact.field_value = resolved_value
    fact.human_confirmed = True
    fact.confirmed_by = current_user.user_id
    fact.confirmed_at = datetime.now(timezone.utc)
    fact.confidence = 1.0
    fact.extraction_method = "human_confirmed"

    await write_audit_log(
        db, action="CONFLICT_RESOLVE",
        user_id=current_user.user_id,
        case_id=case_id,
        detail={"field_name": conflict.field_name, "resolution": body.resolution},
        ip_address=get_client_ip(request),
    )
    await db.commit()
    await db.refresh(fact)
    return _fact_to_response(fact)


@router.post("/{case_id}/workbench/confirm-all", response_model=WorkbenchCompleteResponse)
async def confirm_all(
    case_id: uuid.UUID,
    body: WorkbenchCompleteRequest,
    request: Request,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> WorkbenchCompleteResponse:
    """Validates preconditions (all workbench items resolved), then fires Chain B."""
    case = await verify_case_bank_access(case_id, current_user, db)

    workbench = await get_workbench(case_id, current_user, db)
    if not workbench.all_resolved:
        raise HTTPException(
            status_code=422,
            detail=f"{workbench.total_pending} workbench item(s) still pending review.",
        )

    task_id = None
    if body.trigger_analysis:
        from app.tasks.chain_b import run_chain_b

        async_result = run_chain_b.delay(str(case_id))
        task_id = async_result.id

    await write_audit_log(
        db, action="WORKBENCH_CONFIRM_ALL",
        user_id=current_user.user_id,
        case_id=case_id,
        detail={"trigger_analysis": body.trigger_analysis},
        ip_address=get_client_ip(request),
    )
    await db.commit()

    return WorkbenchCompleteResponse(
        case_id=case_id,
        trigger_analysis=body.trigger_analysis,
        chain_b_task_id=task_id,
    )
