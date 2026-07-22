"""Idempotent upsert helper for case_facts — Chain A safe to re-run.

Plain INSERT on case_id+field_name UNIQUE constraint = IntegrityError on retry.
This upsert makes Chain A safe to retry after a crash and handles the three
workbench item types: LOW_CONFIDENCE (routed at insert), NOT_FOUND (absence
is visible as a missing case_facts row), CONFLICT (fact_conflicts row).
"""
from sqlalchemy import select

from app.models.db import CaseFact, FactConflict
from app.services.compliance.engine import COMPUTED_FIELD_RESOLVERS


def upsert_case_fact(db, case_id: str, field_name: str, fact_data: dict) -> None:
    """
    Upsert with conflict detection.

    If a value already exists for this field AND the new value is different
    AND the existing value is not human_confirmed:
        -> Create a fact_conflict record. Do NOT overwrite the existing value.
    If existing value IS human_confirmed: never overwrite.
    If no existing value: insert normally.
    """
    if field_name in COMPUTED_FIELD_RESOLVERS:
        raise ValueError(
            f"Attempted to store computed field '{field_name}' in case_facts. "
            f"Computed fields must never be persisted — they are derived at rule engine time."
        )

    existing = db.execute(
        select(CaseFact).where(
            CaseFact.case_id == case_id,
            CaseFact.field_name == field_name,
        )
    ).scalar_one_or_none()

    if existing is None:
        db.add(CaseFact(case_id=case_id, field_name=field_name, **fact_data))
        return

    if existing.human_confirmed:
        return

    new_value = fact_data.get("field_value")
    if existing.field_value == new_value or new_value is None:
        return

    conflict_exists = db.execute(
        select(FactConflict).where(
            FactConflict.case_id == case_id,
            FactConflict.field_name == field_name,
            FactConflict.resolved == False,  # noqa: E712 — SQLAlchemy needs `== False`, not `is False`
        )
    ).scalar_one_or_none()

    if conflict_exists:
        return

    conflict = FactConflict(
        case_id=case_id,
        field_name=field_name,
        candidate_a_value=existing.field_value,
        candidate_a_source_doc_id=existing.source_document_id,
        candidate_a_source_page=existing.source_page,
        candidate_a_extraction_method=existing.extraction_method,
        candidate_b_value=new_value,
        candidate_b_source_doc_id=fact_data.get("source_document_id"),
        candidate_b_source_page=fact_data.get("source_page"),
        candidate_b_extraction_method=fact_data.get("extraction_method"),
    )
    db.add(conflict)


def aggregate_metadata(case_id: str, extraction_results: list[dict], db) -> None:
    """
    Aggregate metadata fields across all extraction results.
    Takes first non-null value per field (SA header is usually paragraph 0-3).
    """
    fields = {
        "meta_drt_jurisdiction": None,
        "meta_sa_number": None,
        "meta_primary_borrower": None,
    }
    for result in extraction_results:
        if not result:
            continue
        meta = result.get("metadata", {})
        if meta.get("drt_jurisdiction") and not fields["meta_drt_jurisdiction"]:
            fields["meta_drt_jurisdiction"] = meta["drt_jurisdiction"]
        if meta.get("sa_number") and not fields["meta_sa_number"]:
            fields["meta_sa_number"] = meta["sa_number"]
        if meta.get("primary_borrower") and not fields["meta_primary_borrower"]:
            fields["meta_primary_borrower"] = meta["primary_borrower"]

    for field_name, value in fields.items():
        if value:
            upsert_case_fact(db, case_id, field_name, {
                "field_value": value,
                "confidence": 0.85,
                "extraction_method": "nlp_explicit",
                "human_confirmed": False,
            })
