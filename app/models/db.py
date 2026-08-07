"""
SQLAlchemy 2.x async ORM models — all tables.

TWO ENGINES — never mix them:
  async_engine  → FastAPI route handlers (AsyncSession)
  sync_engine   → Celery tasks (Session) — Celery workers are synchronous

RELATIONSHIP LOADING STRATEGY:
  lazy="selectin" on all relationships — avoids N+1 without requiring
  explicit joinedload() calls everywhere. Best default for this access pattern.

IMMUTABILITY RULES (enforced at app layer, not DB):
  documents.file_url, documents.sha256_hash  — never UPDATE after insert
  paragraphs.text_original                   — never UPDATE after insert
  case_facts where human_confirmed=True      — upsert skips these rows
"""

from __future__ import annotations

import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    BigInteger, Boolean, CheckConstraint, Column, Date,
    DateTime, Float, ForeignKey, Index, Integer, Numeric,
    String, Text, UniqueConstraint, func, text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID, ARRAY
from sqlalchemy.ext.asyncio import (
    AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship, Session,
    sessionmaker,
)
from sqlalchemy import create_engine as create_sync_engine
from contextlib import asynccontextmanager, contextmanager

from app.config import settings


# ─── ENGINES ─────────────────────────────────────────────────────────────────

async_engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

_sync_url = settings.database_url.replace(
    "postgresql+asyncpg://", "postgresql+psycopg2://"
)
sync_engine = create_sync_engine(
    _sync_url,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


# ─── BASE ─────────────────────────────────────────────────────────────────────

class Base(AsyncAttrs, DeclarativeBase):
    pass


# ─── SESSION DEPENDENCIES ─────────────────────────────────────────────────────

@asynccontextmanager
async def get_async_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@contextmanager
def get_sync_db() -> Session:
    session = SyncSessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Alias used in blueprint Celery task code
get_sync_session = get_sync_db


# ─── MODELS ──────────────────────────────────────────────────────────────────

class Bank(Base):
    __tablename__ = "banks"

    id:         Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:       Mapped[str]       = mapped_column(Text, nullable=False)
    short_code: Mapped[str]       = mapped_column(String(20), nullable=False, unique=True)
    active:     Mapped[bool]      = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime]  = mapped_column(DateTime(timezone=True), server_default=func.now())

    users: Mapped[list[User]]  = relationship("User", back_populates="bank", lazy="selectin")
    cases: Mapped[list[Case]]  = relationship("Case", back_populates="bank", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Bank {self.short_code}>"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "role IN ('BANK_OFFICER','BANK_ADMIN','SYSTEM_ADMIN')",
            name="users_role_check"
        ),
    )

    id:            Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bank_id:       Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("banks.id", ondelete="RESTRICT"), nullable=False)
    email:         Mapped[str]       = mapped_column(Text, nullable=False, unique=True)
    password_hash: Mapped[str]       = mapped_column(Text, nullable=False)
    role:          Mapped[str]       = mapped_column(String(20), nullable=False)
    active:        Mapped[bool]      = mapped_column(Boolean, default=True)
    created_at:    Mapped[datetime]  = mapped_column(DateTime(timezone=True), server_default=func.now())

    bank:  Mapped[Bank]        = relationship("Bank", back_populates="users", lazy="selectin")
    cases: Mapped[list[Case]]  = relationship("Case", back_populates="created_by_user", lazy="selectin", foreign_keys="Case.created_by")

    def __repr__(self) -> str:
        return f"<User {self.email} [{self.role}]>"


class Case(Base):
    __tablename__ = "cases"
    __table_args__ = (
        CheckConstraint(
            """status IN (
                'DRAFT','INTAKE_REJECTED','PROCESSING',
                'PENDING_HUMAN_REVIEW','ANALYSING',
                'PENDING_JUDGMENT_REVIEW','COMPLETE','FAILED','DELETED'
            )""",
            name="cases_status_check"
        ),
        Index("idx_cases_bank_id", "bank_id"),
        Index("idx_cases_status", "status"),
    )

    id:                       Mapped[uuid.UUID]        = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bank_id:                  Mapped[uuid.UUID]        = mapped_column(UUID(as_uuid=True), ForeignKey("banks.id", ondelete="RESTRICT"), nullable=False)
    created_by:               Mapped[uuid.UUID]        = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    case_ref:                 Mapped[Optional[str]]    = mapped_column(Text)
    drt_case_number:          Mapped[Optional[str]]    = mapped_column(Text)
    drt_bench:                Mapped[Optional[str]]    = mapped_column(Text)
    borrower_name:            Mapped[str]              = mapped_column(Text, nullable=False)
    property_description:     Mapped[Optional[str]]    = mapped_column(Text)
    loan_account_number:      Mapped[Optional[str]]    = mapped_column(Text)
    principal_amount:         Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2))
    status:                   Mapped[str]              = mapped_column(String(30), nullable=False, default="DRAFT")
    pipeline_stage:           Mapped[Optional[str]]    = mapped_column(Text)
    pipeline_step_current:    Mapped[int]              = mapped_column(Integer, nullable=False, default=0)
    pipeline_step_total:      Mapped[int]              = mapped_column(Integer, nullable=False, default=0)
    intake_filter_result:     Mapped[Optional[dict]]   = mapped_column(JSONB)
    judgment_coverage_alerts: Mapped[Optional[list]]   = mapped_column(JSONB)
    created_at:               Mapped[datetime]         = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:               Mapped[datetime]         = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    bank:               Mapped[Bank]                    = relationship("Bank", back_populates="cases")
    created_by_user:    Mapped[User]                    = relationship("User", back_populates="cases", foreign_keys=[created_by])
    documents:          Mapped[list[Document]]          = relationship("Document", back_populates="case", lazy="selectin")
    case_facts:         Mapped[list[CaseFact]]          = relationship("CaseFact", back_populates="case", lazy="selectin")
    sa_grounds:         Mapped[list[SAGround]]          = relationship("SAGround", back_populates="case", lazy="selectin")
    compliance_results: Mapped[list[ComplianceResult]]  = relationship("ComplianceResult", back_populates="case", lazy="selectin")
    ground_scores:      Mapped[list[GroundScore]]       = relationship("GroundScore", back_populates="case", lazy="selectin")
    reports:            Mapped[list[Report]]            = relationship("Report", back_populates="case", lazy="selectin")
    audit_logs:         Mapped[list[AuditLog]]          = relationship("AuditLog", back_populates="case", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Case {self.id} [{self.status}] borrower={self.borrower_name}>"


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = (
        CheckConstraint("ocr_status IN ('PENDING','PROCESSING','COMPLETE','FAILED')", name="documents_ocr_status_check"),
        Index("idx_documents_case_id", "case_id"),
        UniqueConstraint("case_id", "sha256_hash", name="documents_case_id_sha256_hash_key"),
    )

    id:                Mapped[uuid.UUID]      = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id:           Mapped[uuid.UUID]      = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    uploaded_by:       Mapped[uuid.UUID]      = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    doc_type:          Mapped[str]            = mapped_column(Text, nullable=False)
    original_filename: Mapped[Optional[str]]  = mapped_column(Text)
    file_url:          Mapped[str]            = mapped_column(Text, nullable=False)
    sha256_hash:       Mapped[str]            = mapped_column(Text, nullable=False)
    file_size:         Mapped[Optional[int]]  = mapped_column(Integer)
    version:           Mapped[int]            = mapped_column(Integer, default=1)
    language:    Mapped[str]            = mapped_column(String(10), default="en")
    page_count:  Mapped[Optional[int]]  = mapped_column(Integer)
    ocr_status:  Mapped[str]            = mapped_column(String(20), default="PENDING")
    uploaded_at: Mapped[datetime]       = mapped_column(DateTime(timezone=True), server_default=func.now())

    case:       Mapped[Case]            = relationship("Case", back_populates="documents")
    uploader:   Mapped[User]            = relationship("User")
    paragraphs: Mapped[list[Paragraph]] = relationship("Paragraph", back_populates="document", lazy="selectin")
    case_facts: Mapped[list[CaseFact]]  = relationship("CaseFact", back_populates="source_document", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Document {self.doc_type} [{self.ocr_status}]>"


class Paragraph(Base):
    __tablename__ = "paragraphs"
    __table_args__ = (Index("idx_paragraphs_document_id", "document_id"),)

    id:              Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id:     Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    page_number:     Mapped[int]             = mapped_column(Integer, nullable=False)
    para_sequence:   Mapped[int]             = mapped_column(Integer, nullable=False)
    text_original:   Mapped[str]             = mapped_column(Text, nullable=False)
    text_translated: Mapped[Optional[str]]   = mapped_column(Text)
    language:        Mapped[str]             = mapped_column(String(10), default="en")
    is_heading:      Mapped[bool]            = mapped_column(Boolean, default=False)
    is_numbered:     Mapped[bool]            = mapped_column(Boolean, default=False)
    is_handwritten:  Mapped[bool]            = mapped_column(Boolean, default=False)
    bbox:            Mapped[Optional[dict]]  = mapped_column(JSONB)
    ocr_confidence:  Mapped[Optional[float]] = mapped_column(Float)
    created_at:      Mapped[datetime]        = mapped_column(DateTime(timezone=True), server_default=func.now())

    document: Mapped[Document] = relationship("Document", back_populates="paragraphs")

    def get_text(self) -> str:
        return self.text_translated or self.text_original

    def __repr__(self) -> str:
        return f"<Paragraph page={self.page_number} seq={self.para_sequence}>"


ALWAYS_HUMAN_CONFIRM_FIELDS = {
    "valuer_rbi_empanelled",
    "valuer_section_247_registered",
    "udyam_cert_in_bank_file",
    "total_borrowers_in_loan",
    "total_guarantors_in_loan",
    "ibc_moratorium_active",
    "sa_applicant_type",
    "ats_payments_made_to_loan_account",
    "auction_conducted_despite_stay",
    "sale_certificate_issued",
}


class CaseFact(Base):
    __tablename__ = "case_facts"
    __table_args__ = (
        UniqueConstraint("case_id", "field_name", name="case_facts_case_id_field_name_key"),
        CheckConstraint(
            "extraction_method IN ('regex','nlp_explicit','nlp_implied','human_confirmed')",
            name="case_facts_extraction_method_check"
        ),
        Index("idx_case_facts_case_id", "case_id"),
        Index("idx_case_facts_field", "case_id", "field_name"),
    )

    id:                  Mapped[uuid.UUID]           = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id:             Mapped[uuid.UUID]           = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    field_name:          Mapped[str]                 = mapped_column(Text, nullable=False)
    field_value:         Mapped[Optional[str]]       = mapped_column(Text)
    confidence:          Mapped[Optional[float]]     = mapped_column(Float)
    source_document_id:  Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"))
    source_page:         Mapped[Optional[int]]       = mapped_column(Integer)
    source_paragraph_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("paragraphs.id", ondelete="SET NULL"))
    extraction_method:   Mapped[Optional[str]]       = mapped_column(String(20))
    human_confirmed:     Mapped[bool]                = mapped_column(Boolean, default=False)
    confirmed_by:        Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    confirmed_at:        Mapped[Optional[datetime]]  = mapped_column(DateTime(timezone=True))
    created_at:          Mapped[datetime]            = mapped_column(DateTime(timezone=True), server_default=func.now())

    case:             Mapped[Case]               = relationship("Case", back_populates="case_facts")
    source_document:  Mapped[Optional[Document]] = relationship("Document", back_populates="case_facts")
    source_paragraph: Mapped[Optional[Paragraph]] = relationship("Paragraph")
    confirming_user:  Mapped[Optional[User]]     = relationship("User")

    @property
    def requires_workbench(self) -> bool:
        if self.human_confirmed:
            return False
        if self.extraction_method == "nlp_implied":
            return True
        if self.field_name in ALWAYS_HUMAN_CONFIRM_FIELDS:
            return True
        if self.confidence is not None and self.confidence < 0.80:
            return True
        return False

    def __repr__(self) -> str:
        return f"<CaseFact {self.field_name}={self.field_value!r} confirmed={self.human_confirmed}>"


class FactConflict(Base):
    __tablename__ = "fact_conflicts"
    __table_args__ = (
        UniqueConstraint("case_id", "field_name", name="fact_conflicts_case_id_field_name_key"),
        Index("idx_fact_conflicts_case", "case_id", "resolved"),
    )

    id:                            Mapped[uuid.UUID]        = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id:                       Mapped[uuid.UUID]        = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    field_name:                    Mapped[str]              = mapped_column(Text, nullable=False)
    candidate_a_value:             Mapped[Optional[str]]    = mapped_column(Text)
    candidate_a_source_doc_id:     Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"))
    candidate_a_source_page:       Mapped[Optional[int]]    = mapped_column(Integer)
    candidate_a_extraction_method: Mapped[Optional[str]]    = mapped_column(Text)
    candidate_b_value:             Mapped[Optional[str]]    = mapped_column(Text)
    candidate_b_source_doc_id:     Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"))
    candidate_b_source_page:       Mapped[Optional[int]]    = mapped_column(Integer)
    candidate_b_extraction_method: Mapped[Optional[str]]    = mapped_column(Text)
    resolved:                      Mapped[bool]             = mapped_column(Boolean, default=False)
    resolved_value:                Mapped[Optional[str]]    = mapped_column(Text)
    resolved_by:                   Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    resolved_at:                   Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at:                    Mapped[datetime]         = mapped_column(DateTime(timezone=True), server_default=func.now())


class SAGround(Base):
    __tablename__ = "sa_grounds"
    __table_args__ = (Index("idx_sa_grounds_case_id", "case_id"),)

    id:                      Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id:                 Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    ground_code:             Mapped[str]             = mapped_column(Text, nullable=False)
    statutory_basis:         Mapped[Optional[str]]   = mapped_column(Text)
    source_paragraph_id:     Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("paragraphs.id", ondelete="SET NULL"))
    factual_claim_extracted: Mapped[Optional[str]]   = mapped_column(Text)
    documents_cited:         Mapped[Optional[list]]  = mapped_column(ARRAY(Text))
    confidence:              Mapped[Optional[float]] = mapped_column(Float)
    created_at:              Mapped[datetime]        = mapped_column(DateTime(timezone=True), server_default=func.now())

    case:             Mapped[Case]               = relationship("Case", back_populates="sa_grounds")
    source_paragraph: Mapped[Optional[Paragraph]] = relationship("Paragraph")

    def __repr__(self) -> str:
        return f"<SAGround {self.ground_code}>"


class ComplianceResult(Base):
    __tablename__ = "compliance_results"
    __table_args__ = (
        CheckConstraint("status IN ('PASS','FAIL','UNKNOWN','REVIEW')", name="compliance_results_status_check"),
        CheckConstraint(
            """severity IN (
                'FATAL','ABSOLUTE_BAR','CURABLE','MINOR',
                'ADVISORY','REVIEW_REQUIRED','UNKNOWN','HIGH'
            )""",
            name="compliance_results_severity_check"
        ),
        CheckConstraint("outcome_favors IN ('BANK','BORROWER','NEUTRAL')", name="compliance_results_outcome_favors_check"),
        Index("idx_compliance_case_id", "case_id"),
    )

    id:           Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id:      Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    rule_id:      Mapped[str]             = mapped_column(Text, nullable=False)
    module:       Mapped[str]             = mapped_column(Text, nullable=False)
    status:       Mapped[str]             = mapped_column(String(10), nullable=False)
    severity:     Mapped[Optional[str]]   = mapped_column(String(20))
    # Who this finding favors — decoupled from `status` (a rule author's status
    # label like PASS/FAIL is not a reliable signal of direction, see H14(c)).
    outcome_favors: Mapped[str]           = mapped_column(String(10), nullable=False, server_default="BANK")
    message:      Mapped[Optional[str]]   = mapped_column(Text)
    detail_json:  Mapped[Optional[dict]]  = mapped_column(JSONB)
    judgment_tags: Mapped[Optional[list]] = mapped_column(ARRAY(Text))
    evaluated_at: Mapped[datetime]        = mapped_column(DateTime(timezone=True), server_default=func.now())

    case: Mapped[Case] = relationship("Case", back_populates="compliance_results")

    def __repr__(self) -> str:
        return f"<ComplianceResult {self.rule_id} [{self.status}/{self.severity}]>"


class Judgment(Base):
    __tablename__ = "judgments"
    __table_args__ = (
        CheckConstraint("court IN ('SUPREME_COURT','HIGH_COURT','DRAT','DRT')", name="judgments_court_check"),
        CheckConstraint("favor IN ('BANK','BORROWER','NEUTRAL')", name="judgments_favor_check"),
    )

    id:                    Mapped[uuid.UUID]        = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    citation:              Mapped[str]              = mapped_column(Text, nullable=False, unique=True)
    title:                 Mapped[str]              = mapped_column(Text, nullable=False)
    short_name:            Mapped[Optional[str]]    = mapped_column(Text)
    court:                 Mapped[str]              = mapped_column(String(20), nullable=False)
    high_court_state:      Mapped[Optional[str]]    = mapped_column(Text)
    bench_strength:        Mapped[int]              = mapped_column(Integer, default=1)
    judgment_date:         Mapped[Optional[date]]   = mapped_column(Date)
    overruled:             Mapped[bool]             = mapped_column(Boolean, default=False)
    overruled_by:          Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("judgments.id", ondelete="SET NULL"))
    favor:                 Mapped[Optional[str]]    = mapped_column(String(10))
    favor_verified:        Mapped[bool]             = mapped_column(Boolean, default=False)
    ground_codes:          Mapped[Optional[list]]   = mapped_column(ARRAY(Text))
    statutory_basis:       Mapped[Optional[str]]    = mapped_column(Text)
    holding_summary:          Mapped[Optional[str]]  = mapped_column(Text)
    has_verified_conditions:  Mapped[bool]           = mapped_column(Boolean, default=False)
    source:                   Mapped[Optional[str]]  = mapped_column(
        String(20),
        CheckConstraint(
            "source IN ('SC_FULL_TEXT','HC_FULL_TEXT','DRAT_FULL_TEXT','IBC_LAW_SUMMARY','IK_SUMMARY')",
            name="judgments_source_check",
        ),
    )
    chunk_type:               Mapped[Optional[str]]  = mapped_column(Text)
    applicable_conditions:    Mapped[Optional[list]] = mapped_column(JSONB)
    exclusion_conditions:     Mapped[Optional[list]] = mapped_column(JSONB)
    # v2.0 judgment format (JUDGMENT_SUMMARY_PROMPT_v2.md) additions
    distinguished_by:      Mapped[Optional[list]]   = mapped_column(ARRAY(Text))
    act_sections:           Mapped[Optional[list]]   = mapped_column(ARRAY(Text))
    rules_sections:          Mapped[Optional[list]]   = mapped_column(ARRAY(Text))
    slrai_modules:            Mapped[Optional[list]]   = mapped_column(ARRAY(Text))
    keywords:                 Mapped[Optional[list]]   = mapped_column(ARRAY(Text))
    ik_doc_id:                Mapped[Optional[str]]    = mapped_column(Text)
    ik_url:                   Mapped[Optional[str]]    = mapped_column(Text)
    borrower_claim:           Mapped[Optional[str]]    = mapped_column(Text)
    applicable_conditions_text: Mapped[Optional[str]]  = mapped_column(Text)
    exclusion_conditions_text:  Mapped[Optional[str]]  = mapped_column(Text)
    added_by:              Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    added_at:              Mapped[datetime]         = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_reviewed_at:      Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    def __repr__(self) -> str:
        return f"<Judgment {self.citation}>"


class JudgmentApplicability(Base):
    __tablename__ = "judgment_applicability"
    __table_args__ = (
        CheckConstraint(
            """status IN (
                'APPLICABLE','PARTIAL','NOT_APPLICABLE',
                'LEGAL_UNCERTAINTY','UNAVAILABLE'
            )""",
            name="judgment_applicability_status_check"
        ),
    )

    id:           Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id:      Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    judgment_id:  Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), ForeignKey("judgments.id", ondelete="CASCADE"), nullable=False)
    ground_code:  Mapped[Optional[str]]   = mapped_column(Text)
    status:       Mapped[Optional[str]]   = mapped_column(String(25))
    reason:       Mapped[Optional[str]]   = mapped_column(Text)
    evaluated_at: Mapped[datetime]        = mapped_column(DateTime(timezone=True), server_default=func.now())

    judgment: Mapped[Judgment] = relationship("Judgment")


class GroundScore(Base):
    __tablename__ = "ground_scores"
    __table_args__ = (Index("idx_ground_scores_case_id", "case_id"),)

    id:                   Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id:              Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    ground_code:          Mapped[str]             = mapped_column(Text, nullable=False)
    factual_score:        Mapped[Optional[float]] = mapped_column(Float)
    judicial_score:       Mapped[Optional[float]] = mapped_column(Float)
    ground_strength:      Mapped[Optional[float]] = mapped_column(Float)
    corpus_total:         Mapped[int]             = mapped_column(Integer, default=0)
    corpus_borrower_wins: Mapped[int]             = mapped_column(Integer, default=0)
    corpus_bank_wins:     Mapped[int]             = mapped_column(Integer, default=0)
    corpus_confidence:    Mapped[str]             = mapped_column(Text, default="NO_DATA")
    full_corpus_total:         Mapped[int]        = mapped_column(Integer, default=0)
    full_corpus_borrower_wins: Mapped[int]        = mapped_column(Integer, default=0)
    full_corpus_bank_wins:     Mapped[int]        = mapped_column(Integer, default=0)
    evaluated_at:         Mapped[datetime]        = mapped_column(DateTime(timezone=True), server_default=func.now())

    case: Mapped[Case] = relationship("Case", back_populates="ground_scores")

    def __repr__(self) -> str:
        return f"<GroundScore {self.ground_code}={self.ground_strength}>"


class Report(Base):
    __tablename__ = "reports"

    id:                  Mapped[uuid.UUID]        = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id:             Mapped[uuid.UUID]        = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    compliance_score:    Mapped[Optional[int]]    = mapped_column(Integer)
    litigation_exposure: Mapped[Optional[float]]  = mapped_column(Float)
    recommendation:      Mapped[Optional[str]]    = mapped_column(Text)
    report_json:         Mapped[Optional[dict]]   = mapped_column(JSONB)
    pdf_url:             Mapped[Optional[str]]    = mapped_column(Text)
    content_hash:        Mapped[Optional[str]]    = mapped_column(Text)
    generated_by:        Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    generated_at:        Mapped[datetime]         = mapped_column(DateTime(timezone=True), server_default=func.now())

    case:           Mapped[Case]          = relationship("Case", back_populates="reports")
    generated_user: Mapped[Optional[User]] = relationship("User")

    def __repr__(self) -> str:
        return f"<Report {self.id} score={self.compliance_score}>"


class AuditLog(Base):
    __tablename__ = "audit_log"
    __table_args__ = (
        Index("idx_audit_case_id", "case_id"),
        Index("idx_audit_user_id", "user_id"),
    )

    id:         Mapped[uuid.UUID]           = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id:    Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="SET NULL"))
    user_id:    Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    action:     Mapped[str]                 = mapped_column(Text, nullable=False)
    detail:     Mapped[Optional[dict]]      = mapped_column(JSONB)
    ip_address: Mapped[Optional[str]]       = mapped_column(String(45))
    created_at: Mapped[datetime]            = mapped_column(DateTime(timezone=True), server_default=func.now())

    case: Mapped[Optional[Case]] = relationship("Case", back_populates="audit_logs")
    user: Mapped[Optional[User]] = relationship("User")

    def __repr__(self) -> str:
        return f"<AuditLog {self.action} user={self.user_id}>"


class CaseStatute(Base):
    __tablename__ = "case_statutes"
    __table_args__ = (Index("idx_case_statutes_case_id", "case_id"),)

    id:             Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id:        Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    rule_id:        Mapped[str]       = mapped_column(Text, nullable=False)
    section_number: Mapped[str]       = mapped_column(Text, nullable=False)
    act_name:       Mapped[str]       = mapped_column(Text, nullable=False)
    statute_text:   Mapped[str]       = mapped_column(Text, nullable=False)
    retrieved_at:   Mapped[datetime]  = mapped_column(DateTime(timezone=True), server_default=func.now())

    case: Mapped[Case] = relationship("Case")

    def __repr__(self) -> str:
        return f"<CaseStatute {self.rule_id} -> {self.act_name} Sec {self.section_number}>"


# ─── AUDIT LOG HELPERS ────────────────────────────────────────────────────────

async def write_audit_log(
    db: AsyncSession,
    action: str,
    user_id: uuid.UUID | None = None,
    case_id: uuid.UUID | None = None,
    detail:  dict | None = None,
    ip_address: str | None = None,
) -> None:
    log = AuditLog(
        action=action,
        user_id=user_id,
        case_id=case_id,
        detail=detail or {},
        ip_address=ip_address,
    )
    db.add(log)
