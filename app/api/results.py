"""Compliance & Results API — compliance rule outcomes, ground scores,
judgment applicability, and live corpus win-rate stats for a case.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import CurrentUser, DbDep, OfficerDep, verify_case_bank_access
from app.models.db import ComplianceResult, GroundScore, JudgmentApplicability, SAGround

router = APIRouter()


# ─── SCHEMAS ──────────────────────────────────────────────────────────────────

class ComplianceResultResponse(BaseModel):
    id: uuid.UUID
    rule_id: str
    module: str
    status: str
    severity: Optional[str]
    message: Optional[str]
    judgment_tags: Optional[list[str]]
    evaluated_at: datetime


class GroundScoreResponse(BaseModel):
    ground_code: str
    factual_score: Optional[float]
    judicial_score: Optional[float]
    ground_strength: Optional[float]
    corpus_total: int
    corpus_borrower_wins: int
    corpus_bank_wins: int
    corpus_confidence: str
    full_corpus_total: int
    full_corpus_borrower_wins: int
    full_corpus_bank_wins: int
    evaluated_at: datetime


class JudgmentApplicabilityResponse(BaseModel):
    ground_code: Optional[str]
    status: str
    reason: Optional[str]
    citation: str
    title: str
    short_name: Optional[str]
    court: str
    favor: Optional[str]
    holding_summary: Optional[str]
    evaluated_at: datetime


class CorpusStatBucket(BaseModel):
    total: int
    borrower_wins: int
    bank_wins: int
    neutral: int
    borrower_win_pct: Optional[float]
    bank_win_pct: Optional[float]


class CorpusStatResponse(BaseModel):
    ground_code: str
    verified: CorpusStatBucket
    full: CorpusStatBucket
    data_confidence: str


# ─── ENDPOINTS ────────────────────────────────────────────────────────────────

@router.get("/{case_id}/results/compliance", response_model=list[ComplianceResultResponse])
async def get_compliance_results(
    case_id: uuid.UUID,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> list[ComplianceResultResponse]:
    await verify_case_bank_access(case_id, current_user, db)
    result = await db.execute(
        select(ComplianceResult).where(ComplianceResult.case_id == case_id).order_by(ComplianceResult.rule_id)
    )
    return [
        ComplianceResultResponse(
            id=r.id, rule_id=r.rule_id, module=r.module, status=r.status,
            severity=r.severity, message=r.message, judgment_tags=r.judgment_tags,
            evaluated_at=r.evaluated_at,
        )
        for r in result.scalars().all()
    ]


@router.get("/{case_id}/results/grounds", response_model=list[GroundScoreResponse])
async def get_ground_scores(
    case_id: uuid.UUID,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> list[GroundScoreResponse]:
    await verify_case_bank_access(case_id, current_user, db)
    result = await db.execute(
        select(GroundScore).where(GroundScore.case_id == case_id).order_by(GroundScore.ground_code)
    )
    return [
        GroundScoreResponse(
            ground_code=g.ground_code,
            factual_score=g.factual_score, judicial_score=g.judicial_score,
            ground_strength=g.ground_strength,
            corpus_total=g.corpus_total, corpus_borrower_wins=g.corpus_borrower_wins,
            corpus_bank_wins=g.corpus_bank_wins, corpus_confidence=g.corpus_confidence,
            full_corpus_total=g.full_corpus_total,
            full_corpus_borrower_wins=g.full_corpus_borrower_wins,
            full_corpus_bank_wins=g.full_corpus_bank_wins,
            evaluated_at=g.evaluated_at,
        )
        for g in result.scalars().all()
    ]


@router.get("/{case_id}/results/judgments", response_model=list[JudgmentApplicabilityResponse])
async def get_judgment_applicability(
    case_id: uuid.UUID,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> list[JudgmentApplicabilityResponse]:
    """Verified (APPLICABLE/PARTIAL/NOT_APPLICABLE/LEGAL_UNCERTAINTY, Class A)
    and similarity-retrieved (SIMILARITY_RETRIEVED, Class B) judgments —
    see report Section A/B honesty distinction, same split shown here."""
    await verify_case_bank_access(case_id, current_user, db)

    # JudgmentApplicability.judgment has no lazy="selectin" — explicit
    # eager-load avoids a MissingGreenlet when accessing r.judgment below.
    from sqlalchemy.orm import selectinload
    result = await db.execute(
        select(JudgmentApplicability)
        .where(JudgmentApplicability.case_id == case_id)
        .options(selectinload(JudgmentApplicability.judgment))
        .order_by(JudgmentApplicability.ground_code)
    )
    rows = result.scalars().all()

    return [
        JudgmentApplicabilityResponse(
            ground_code=r.ground_code, status=r.status, reason=r.reason,
            citation=r.judgment.citation, title=r.judgment.title,
            short_name=r.judgment.short_name, court=r.judgment.court,
            favor=r.judgment.favor, holding_summary=r.judgment.holding_summary,
            evaluated_at=r.evaluated_at,
        )
        for r in rows
    ]


@router.get("/{case_id}/results/corpus-stats", response_model=list[CorpusStatResponse])
async def get_corpus_stats(
    case_id: uuid.UUID,
    current_user: CurrentUser = OfficerDep,
    db: AsyncSession = DbDep,
) -> list[CorpusStatResponse]:
    """Live Qdrant win-rate stats (verified + full counts) for every ground
    raised in this case. Degrades to all-zero/NO_DATA per ground if the
    judgment corpus isn't loaded yet or Qdrant is unreachable — never 500s."""
    await verify_case_bank_access(case_id, current_user, db)
    from app.services.judgments.statistics import get_ground_statistics

    result = await db.execute(select(SAGround.ground_code).where(SAGround.case_id == case_id).distinct())
    ground_codes = [row[0] for row in result.all()]

    stats = []
    for ground_code in ground_codes:
        s = get_ground_statistics(ground_code)
        stats.append(CorpusStatResponse(
            ground_code=ground_code,
            verified=CorpusStatBucket(**s["verified"]),
            full=CorpusStatBucket(**s["full"]),
            data_confidence=s["data_confidence"],
        ))
    return stats
