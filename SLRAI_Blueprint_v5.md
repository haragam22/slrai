# PROJECT SLRAI — AI-IDE-Ready Technical Blueprint
## SARFAESI Legal Risk & Auction Intelligence Platform
**Version:** 5.0 (V2 — All Bugs Fixed, Rules Expanded, Dockerfile Added)
**Status:** Implementation Ready — Reviewed and Patched

> **What changed from v4.0:**
> - Claude model string corrected (`claude-sonnet-4-6`)
> - Anthropic SDK updated (`anthropic==0.56.0`)
> - Embedding model replaced (`law-ai/InLegalBERT` — verified Indian legal model on HuggingFace)
> - `defaultdict` lambda bug fixed in Section 13.3
> - Dockerfile added (was missing entirely)
> - `PASS_FAVORABLE` status bug in M5 rules fixed — changed to `PASS`
> - Celery chain `.s()` replaced with `.si()` — eliminates `_` passthrough problem
> - `model_validator` implementations added for all computed fields in `CaseFactSchema`
> - 7 new high-priority rules added: M1_C5/C6/C7, M3_C3/C4, M4_C3, M5_C4, M6_C4, M8_C4
> - New schema fields added to support new rules
> - Pre-intake filter F4 (IBC moratorium flag) added
> - Section 23 added: Test Fixture Acquisition Guide

> This document is written to be consumed directly by an AI coding assistant (Cursor, Copilot,
> Claude Code, etc.). Every section is specified to the level where the AI produces correct code
> on the first attempt. Ambiguities that caused wrong code in v3.0 are resolved here explicitly.

---

## TABLE OF CONTENTS

1. [Governing Principles](#1-governing-principles)
2. [Project Folder Structure](#2-project-folder-structure)
3. [Dependency Versions — Pinned](#3-dependency-versions--pinned)
4. [Environment Variables](#4-environment-variables)
5. [V1 Scope — 9 Modules](#5-v1-scope--9-modules)
6. [Pre-Intake Filters](#6-pre-intake-filters)
7. [Master Case Fact Schema](#7-master-case-fact-schema)
8. [Database Schema — Complete](#8-database-schema--complete)
9. [Authentication & RBAC](#9-authentication--rbac)
10. [End-to-End Pipeline — Two-Chain Architecture](#10-end-to-end-pipeline--two-chain-architecture)
11. [OCR & Document Intelligence](#11-ocr--document-intelligence)
12. [NLP Extraction Architecture](#12-nlp-extraction-architecture)
13. [YAML Rule Engine — Interpreter Contract](#13-yaml-rule-engine--interpreter-contract)
14. [Statute Compliance Engine — All 9 Modules](#14-statute-compliance-engine--all-9-modules)
15. [Judgment Intelligence Engine](#15-judgment-intelligence-engine)
16. [Ground Strength & Scoring Engine](#16-ground-strength--scoring-engine)
17. [API Design — Full Request & Response Schemas](#17-api-design--full-request--response-schemas)
18. [Error Handling Contracts](#18-error-handling-contracts)
19. [Implementation Roadmap — 22 Weeks](#19-implementation-roadmap--22-weeks)
20. [Risk Register](#20-risk-register)
21. [Definition of Pitch-Ready](#21-definition-of-pitch-ready)
22. [Appendix: Silence Check Protocol](#22-appendix-silence-check-protocol)
23. [Appendix: Test Fixture Acquisition Guide](#23-appendix-test-fixture-acquisition-guide)

24. [Appendix: Reference Implementation — app/services/storage.py](#24-appendix-reference-implementation--appservicesstoragepy)
25. [Appendix: Reference Implementation — app/models/db.py](#25-appendix-reference-implementation--appmodelsdbpy)
26. [Appendix: API Endpoints Tracker](#26-appendix-api-endpoints-tracker)
27. [Appendix: Streamlit API Dashboard (dashboard.py)](#27-appendix-streamlit-api-dashboard-dashboardpy)

---

## 1. Governing Principles

### The Three Laws

Every technical decision is evaluated against these three laws.
A proposed solution that violates any one of them is rejected — no exceptions.

| Law | Statement | Implication |
|-----|-----------|-------------|
| Law 1 | **FACTS OVERRIDE VECTORS** | A judgment is never applied on text similarity alone. Factual conditions must be explicitly matched. |
| Law 2 | **LAW OVERRIDES MODELS** | No AI model makes a legal conclusion. Models extract structured data. Rules decide everything else. |
| Law 3 | **SYSTEM OVERRIDES AI** | If the rule engine and the AI disagree, the rule engine wins. Always. |

### Core Design Constraint

> The system operates **exclusively on documents the bank already holds** — SAs filed against
> them, their own enforcement records, their credit files. No dependency on DRT systems,
> external APIs, or third-party data in V1.

### What the System Is

- A **procedural compliance validator** for SARFAESI enforcement steps
- A **ground strength analyser** for borrower allegations in SAs
- A **judgment applicability engine** that matches facts to precedents
- A **litigation exposure quantifier** for auction purchasers

### What the System Is Not

- Not a legal advice engine
- Not a court outcome predictor
- Not a replacement for a SARFAESI lawyer
- Not a chatbot

---

## 2. Project Folder Structure

**AI IDE instruction:** Scaffold this exact structure before writing any code.
Do not deviate from this layout. Import paths depend on it.

```
slrai/
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 0001_initial_schema.py       # generated from Section 8 schema
│
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI app entry point — lifespan pattern
│   ├── config.py                        # pydantic-settings — reads from .env
│   ├── dependencies.py                  # get_db, get_current_user, require_role
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py                      # POST /auth/login, POST /auth/refresh
│   │   ├── cases.py                     # case CRUD
│   │   ├── documents.py                 # document upload
│   │   ├── pipeline.py                  # trigger analysis, get pipeline status
│   │   ├── workbench.py                 # fact review and confirmation
│   │   └── reports.py                   # report generation and download
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── db.py                        # SQLAlchemy ORM models — all tables
│   │   └── schemas.py                   # Pydantic v2 request/response schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── storage.py                   # S3 upload/download/hash
│   │   │
│   │   ├── ocr/
│   │   │   ├── __init__.py
│   │   │   ├── azure_ocr.py             # Azure Document Intelligence client
│   │   │   └── layout_parser.py         # paragraph extraction + bbox mapping
│   │   │
│   │   ├── translation/
│   │   │   ├── __init__.py
│   │   │   └── indictrans.py            # IndicTrans2 model wrapper
│   │   │
│   │   ├── extraction/
│   │   │   ├── __init__.py
│   │   │   ├── regex_layer.py           # Layer A — deterministic regex
│   │   │   ├── nlp_layer.py             # Layer B — Claude API structured extraction
│   │   │   ├── doc_classifier.py        # keyword-rule DocType classifier
│   │   │   ├── confidence_router.py     # routes fields to workbench or auto-accept
│   │   │   └── fact_persistence.py      # upsert helper — idempotent Chain A
│   │   │
│   │   ├── compliance/
│   │   │   ├── __init__.py
│   │   │   ├── engine.py                # YAML rule interpreter — uses simpleeval
│   │   │   ├── pre_intake.py            # F1–F4 filters
│   │   │   └── rules/
│   │   │       ├── m1_demand.yaml
│   │   │       ├── m2_reply.yaml
│   │   │       ├── m3_auction.yaml
│   │   │       ├── m4_limitation.yaml
│   │   │       ├── m5_tenancy.yaml
│   │   │       ├── m6_valuation.yaml
│   │   │       ├── m7_multiparty.yaml
│   │   │       ├── m8_npa.yaml
│   │   │       ├── m9_msme.yaml
│   │   │       └── m10_third_party.yaml
│   │   │
│   │   ├── judgments/
│   │   │   ├── __init__.py
│   │   │   ├── retrieval.py             # Qdrant vector search with metadata filters
│   │   │   ├── applicability.py         # fact-graph condition matching
│   │   │   └── precedence.py            # conflict resolver
│   │   │
│   │   └── scoring/
│   │       ├── __init__.py
│   │       ├── ground_strength.py       # per-ground borrower score
│   │       ├── compliance_score.py      # bank procedural score
│   │       └── recommendation.py        # final matrix lookup
│   │
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── celery_app.py                # Celery config — broker, backend, routing
│   │   ├── chain_a.py                   # Chain A: upload → workbench (auto)
│   │   └── chain_b.py                   # Chain B: workbench → report (officer-triggered)
│   │
│   ├── scripts/
│   │   ├── load_judgments.py            # ingests docs/judgments/*.json → Qdrant + DB
│   │   ├── build_law_wiki.py            # builds sarfaesi_law_wiki.md for Chain A
│   │   ├── compile_class_a_wiki.py      # compiles 75 .md files → class_a_judgments_wiki.md
│   │   ├── fetch_from_ik.py             # Indian Kanoon API fetcher + Class B summary generator
│   │   └── seed_db.py              
│   │
│   ├── docs/
│   │   ├── judgments/                   # one JSON per judgment (Harasis maintains)
│   │   └── statutes/                    # statutory text files
│   │
│   └── reports/
│       ├── __init__.py
│       ├── generator.py                 # WeasyPrint PDF generation
│       └── templates/
│           └── report.html.j2           # Jinja2 HTML template
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                      # pytest fixtures, test DB, test client
│   ├── test_rules/
│   │   ├── test_m1.py
│   │   ├── test_m2.py
│   │   └── ...                          # one test file per module
│   ├── test_extraction/
│   │   ├── test_regex.py
│   │   └── test_nlp.py
│   ├── test_scoring/
│   │   └── test_ground_strength.py
│   └── fixtures/
│       ├── sa_typed_english_01.pdf      # test SA — clean typed English
│       ├── sa_typed_english_02.pdf
│       ├── sa_hindi_mixed_01.pdf        # test SA — Hindi/English mixed
│       ├── sa_hindi_mixed_02.pdf
│       └── sa_complex_01.pdf            # test SA — multiple grounds, complex facts
│
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── .env.example                         # see Section 4
├── .env                                 # gitignored
├── requirements.txt                     # see Section 3 — pinned versions
├── pyproject.toml
└── README.md
```

### main.py — Entry Point Pattern

Use the **lifespan** pattern (FastAPI 0.109+). Do NOT use deprecated `@app.on_event`.

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import auth, cases, documents, pipeline, workbench, reports
from app.tasks.celery_app import celery_app  # noqa — initialises Celery on import

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown

app = FastAPI(title="SLRAI", version="1.0.0", lifespan=lifespan)

app.include_router(auth.router,       prefix="/api/v1/auth",      tags=["auth"])
app.include_router(cases.router,      prefix="/api/v1/cases",     tags=["cases"])
app.include_router(documents.router,  prefix="/api/v1/cases",     tags=["documents"])
app.include_router(pipeline.router,   prefix="/api/v1/cases",     tags=["pipeline"])
app.include_router(workbench.router,  prefix="/api/v1/cases",     tags=["workbench"])
app.include_router(reports.router,    prefix="/api/v1/cases",     tags=["reports"])
```

### config.py — Settings Pattern

```python
# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str

    # Redis
    redis_url: str
    celery_broker_url: str
    celery_result_backend: str

    # S3
    s3_endpoint_url: str = ""       # empty string = use AWS S3
    s3_access_key: str
    s3_secret_key: str
    s3_bucket_name: str

    # Azure OCR
    azure_ocr_endpoint: str
    azure_ocr_key: str

    # Claude API
    anthropic_api_key: str
    claude_model: str = "claude-sonnet-4-6"  # FIXED v5.0: was claude-sonnet-4-5-20251001 (does not exist)
    llm_max_tokens: int = 1000
    llm_temperature: float = 0.0    # always 0 — deterministic extraction

    # Qdrant
    qdrant_url: str
    qdrant_judgments_collection: str = "sarfaesi_judgments"   # 7,500 judgment vectors

    ik_api_token: str = ""   # empty = IK API not configured; set before running scripts

    # Auth
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 480   # 8 hours

    # Translation
    # IndicTrans2 — Gala et al., TMLR 2023 (arXiv:2305.16307). Supports all 22 Indian languages.
    # For legal-domain fine-tune: "Adapting IndicTrans2 for Legal Domain MT via QLoRA" ACL JUST-NLP 2025.
    translation_model: str = "ai4bharat/indictrans2-hi-en-dist-200M"
    translation_device: str = "cpu"  # "cpu" or "cuda"

    # Embeddings for Qdrant judgment retrieval
    # FIXED v5.0: law-ai/SyntheticLegalBench-v1 does NOT exist on HuggingFace — causes startup crash.
    # Use law-ai/InLegalBERT — same IIT Kharagpur lab, verified, 768 dims, Indian legal text trained.
    # Reference: Paul et al., "Pre-trained LMs for Indian Law", ICAIL 2023, arXiv:2209.06049.
    embedding_model: str = "law-ai/InLegalBERT"

    # Reports
    report_template_dir: str = "app/reports/templates"

settings = Settings()
```

---

## 3. Dependency Versions — Pinned

**AI IDE instruction:** Use exactly these versions in `requirements.txt`.
Do not upgrade without testing. Version mismatches listed in comments are known breaking changes.

```
# requirements.txt

# Web framework
fastapi==0.111.0
uvicorn[standard]==0.29.0
pydantic==2.7.1                  # v2 — do NOT use v1 syntax anywhere
pydantic-settings==2.2.1

# Database
sqlalchemy==2.0.30               # async SQLAlchemy 2.x — not 1.x
asyncpg==0.29.0                  # async PostgreSQL driver for SQLAlchemy
alembic==1.13.1

# Task queue
celery==5.3.6                    # NOT 5.4.x — breaking task routing changes
redis==5.0.4
kombu==5.3.4                     # Celery dependency — pin to avoid conflicts

# Azure OCR — CRITICAL: use azure-ai-documentintelligence, NOT azure-cognitiveservices
azure-ai-documentintelligence==1.0.0

# Claude API
anthropic==0.56.0  # FIXED v5.0: was 0.28.0 (severely outdated; RateLimitError paths changed in 0.50+)

# Translation — IndicTrans2 via HuggingFace
transformers==4.41.0
sentencepiece==0.2.0
sacremoses==0.1.1
torch==2.3.0                     # CPU-only install: pip install torch==2.3.0+cpu

# Vector DB
qdrant-client==1.9.1

# Embeddings
sentence-transformers==3.0.1

# Rule engine expression evaluation
simpleeval==0.9.13               # safe expression evaluator — NOT eval()

# Object storage
boto3==1.34.0
botocore==1.34.0

# Report generation
weasyprint==62.3
jinja2==3.1.4
markupsafe==2.1.5

# Auth
python-jose[cryptography]==3.3.0  # JWT
passlib[bcrypt]==1.7.4            # password hashing

# Language detection
langdetect==1.0.9

# YAML parsing (rule files)
pyyaml==6.0.1

# Utilities
python-multipart==0.0.9          # required for FastAPI file uploads
httpx==0.27.0                    # async HTTP client
python-dotenv==1.0.1

# Dev / test
pytest==8.2.0
pytest-asyncio==0.23.6
httpx==0.27.0                    # also used as async test client
factory-boy==3.3.0
```

### docker-compose.yml

```yaml
# docker-compose.yml
version: "3.9"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - postgres
      - redis
      - qdrant
      - minio
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  worker:
    build: .
    env_file: .env
    depends_on:
      - postgres
      - redis
    command: celery -A app.tasks.celery_app worker --loglevel=info --concurrency=4

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: slrai
      POSTGRES_USER: slrai
      POSTGRES_PASSWORD: slrai_dev
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  qdrant:
    image: qdrant/qdrant:v1.9.1
    ports:
      - "6333:6333"
    volumes:
      - qdrantdata:/qdrant/storage

  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data --console-address ":9001"
    volumes:
      - miniodata:/data

volumes:
  pgdata:
  qdrantdata:
  miniodata:
```

### Dockerfile

**ADDED v5.0 — was missing entirely. The docker-compose.yml references `build: .` which
requires this file. IndicTrans2 (~400MB) and InLegalBERT (~440MB) are pre-downloaded here
to avoid cold-start timeout when the worker first processes a case.**

```dockerfile
# Dockerfile
FROM python:3.11-slim

# System deps for WeasyPrint (PDF rendering) and build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libcairo2 \
    fonts-liberation \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies (layer cached separately from app code)
# Hindi script (Devanagari) support for WeasyPrint PDF rendering
# Not primary requirement but kept in pipeline for mixed-language documents
RUN apt-get install -y --no-install-recommends \
    fonts-noto-core \
    fonts-noto-extra \
    && fc-cache -fv \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download IndicTrans2 model (~400MB) — prevents cold-start timeout in worker
# Reference: Gala et al., "IndicTrans2", TMLR 2023 (arXiv:2305.16307)
RUN python -c "\
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer; \
name = 'ai4bharat/indictrans2-hi-en-dist-200M'; \
AutoTokenizer.from_pretrained(name, trust_remote_code=True); \
AutoModelForSeq2SeqLM.from_pretrained(name, trust_remote_code=True); \
print('IndicTrans2 pre-downloaded OK')"

# Pre-download InLegalBERT embedding model (~440MB) — prevents cold-start in Chain B
# Reference: Paul et al., "Pre-trained LMs for Indian Law", ICAIL 2023 (arXiv:2209.06049)
RUN python -c "\
from sentence_transformers import SentenceTransformer; \
SentenceTransformer('law-ai/InLegalBERT'); \
print('InLegalBERT pre-downloaded OK')"

# Copy application code
COPY . .

# Run as non-root for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000
```

---

## 4. Environment Variables

**AI IDE instruction:** Generate a `.env` file from `.env.example` below.
Every variable in this file is required. The system will not start if any are missing.
`pydantic-settings` validates all vars on startup — missing vars raise `ValidationError`.

```bash
# .env.example

# ── Database ──────────────────────────────────────────────────────────────────
DATABASE_URL=postgresql+asyncpg://slrai:slrai_dev@localhost:5432/slrai

# ── Redis / Celery ────────────────────────────────────────────────────────────
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# ── S3 / MinIO ────────────────────────────────────────────────────────────────
S3_ENDPOINT_URL=http://localhost:9000    # leave blank for AWS S3 in production
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET_NAME=slrai-documents

# ── Azure Document Intelligence ───────────────────────────────────────────────
# Get from Azure Portal → Cognitive Services → Keys and Endpoint
AZURE_OCR_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_OCR_KEY=your_32_char_key_here

# ── Claude API (LLM Extraction) ───────────────────────────────────────────────
ANTHROPIC_API_KEY=sk-ant-api03-your_key_here
CLAUDE_MODEL=claude-sonnet-4-6  # FIXED v5.0: was claude-sonnet-4-5-20251001 (causes APIBadRequestError)
LLM_MAX_TOKENS=1000
LLM_TEMPERATURE=0

# ── Qdrant ────────────────────────────────────────────────────────────────────
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=sarfaesi_judgments

# ── Indian Kanoon API ─────────────────────────────────────────────────────────
# Register at api.indiankanoon.org. Free Rs 500 on signup.
# Apply for non-commercial Rs 10,000/month free tier (use-case verification needed).
IK_API_TOKEN=your_ik_token_here

# ── Auth / JWT ────────────────────────────────────────────────────────────────
# Generate with: openssl rand -hex 32
JWT_SECRET_KEY=your_64_char_hex_secret_here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=480

# ── Translation (IndicTrans2) ─────────────────────────────────────────────────
TRANSLATION_MODEL=ai4bharat/indictrans2-hi-en-dist-200M
TRANSLATION_DEVICE=cpu    # use "cuda" if GPU available

# ── Embeddings (judgment retrieval) ──────────────────────────────────────────
# FIXED v5.0: was law-ai/SyntheticLegalBench-v1 (does not exist)
EMBEDDING_MODEL=law-ai/InLegalBERT

# ── Reports ───────────────────────────────────────────────────────────────────
REPORT_TEMPLATE_DIR=app/reports/templates
```

---

## 5. V1 Scope — 9 Modules

### Module Registry

| # | Module | Statutory Basis | What It Validates | Severity Class |
|---|--------|----------------|-------------------|----------------|
| M1 | Demand Notice Compliance | Section 13(2) SARFAESI | 60-day period, debt amount accuracy, service proof, all parties served | Fatal if period or service defective |
| M2 | Reply Compliance | Section 13(3A) SARFAESI | 15-day window for bank to reply to borrower objection | Fatal — no cure possible |
| M3 | Auction Notice Gap | Rule 8 & 9, Security Interest (Enforcement) Rules 2002 | 30-day gap between Sale Notice and Auction Date | Fatal if gap insufficient |
| M4 | Limitation Shield | Section 17 SARFAESI | SA filed within 45 days of the challenged measure | Absolute bar if exceeded |
| M5 | Tenancy Shield | Transfer of Property Act + Section 17(1) SARFAESI | Lease date vs mortgage date; registration status | Dispositive if proved |
| M6 | Valuation Process Check | Rule 8(6) Security Interest Rules + RBI guidelines | Valuer empanelment, valuation age, reserve price | Fatal if valuer not empanelled |
| M7 | Multiple Borrower/Guarantor Notice | Section 13(2) read with loan agreement | Notice served on every co-borrower and guarantor | Fatal — each omission separate defect |
| M8 | NPA Classification Check | RBI Master Circular + Section 2(o) SARFAESI | 90-day default window, no active restructuring at classification | Fatal if premature |
| M9 | MSME Procedural Check | RBI MSME Circulars + MSMED Act 2006 | Udyam cert in file, restructuring offered pre-NPA | Conditional — human confirmation required |

### Out of Scope — V1

| Ground | Why Excluded |
|--------|-------------|
| Fraud allegations | Requires FIR, ED proceedings, SFIO reports — all external |
| IBC Section 29A disqualification | Requires NCLT records |
| IBC moratorium | Requires NCLT order — separate proceeding |
| ED attachment proceedings | Requires ED order — external |
| Consortium lending authority | Requires inter-creditor agreement between multiple banks |

---

## 6. Pre-Intake Filters

Run synchronously on case creation, before any Celery task fires.
If any filter terminates, set `cases.status = 'INTAKE_REJECTED'` and return result to caller.

```python
# app/services/compliance/pre_intake.py



def run_pre_intake_filters(case_facts: dict) -> IntakeFilterResult:

    # F1 — Agricultural Land
    if case_facts.get("property_classification") == "agricultural":
        return IntakeFilterResult(
            passed=False,
            filter_id="F1",
            result_label="SARFAESI_NOT_APPLICABLE",
            reason="Section 31(i) SARFAESI Act — agricultural land is exempt.",
            action="Pipeline terminated. Do not proceed."
        )

    # F2 — Loan Amount Threshold
    principal = case_facts.get("principal_loan_amount")
    if principal is not None and principal < 100_000:
        return IntakeFilterResult(
            passed=False,
            filter_id="F2",
            result_label="SARFAESI_NOT_APPLICABLE",
            reason="Loans below Rs. 1 lakh are excluded. Section 31(d).",
            action="Pipeline terminated."
        )

    # F3 — Repayment Threshold (does not terminate — flags)
    amount_repaid = case_facts.get("amount_repaid")
    if principal and amount_repaid and (amount_repaid / principal) > 0.80:
        return IntakeFilterResult(
            passed=False,
            filter_id="F3",
            result_label="APPLICABILITY_QUESTIONABLE",
            reason="More than 80% of principal repaid. SARFAESI may not apply.",
            action="Flag for human legal review. Do not auto-proceed."
        )

    # F4 — IBC Moratorium (ADDED v5.0 — does not terminate pipeline, flags for legal review)
    # IBC Section 14 moratorium automatically stays all SARFAESI proceedings.
    # Cannot be auto-verified (requires NCLT records) — must be human-confirmed.
    # The ibc_moratorium_active field is in ALWAYS_HUMAN_CONFIRM in confidence_router.py.
    if case_facts.get("ibc_moratorium_active") is True:
        return IntakeFilterResult(
            passed=False,
            filter_id="F4",
            result_label="IBC_MORATORIUM_POSSIBLE",
            reason="Borrower may be subject to IBC Section 14 moratorium. "
                   "SARFAESI proceedings are automatically stayed under IBC 2016.",
            action="Do not proceed. Verify NCLT records before any enforcement action. "
                   "Human legal confirmation required — cannot be auto-verified in V1."
        )

    # F5 — Third Party Applicant (non-borrower / non-guarantor) — v5.4
    # Does not terminate pipeline. Routes to M10 module.
    route_flags = []
    applicant_type = case_facts.get("sa_applicant_type")
    if applicant_type not in (None, "BORROWER", "GUARANTOR"):
        route_flags.append({
            "filter_id": "F5",
            "result_label": "ROUTE_TO_M10",
            "reason": f"SA applicant is {applicant_type} — not the borrower or guarantor. "
                      f"Module M10 (Third Party Rights) will be the primary analysis "
                      f"framework. M1-M9 still run for procedural compliance. DRT may "
                      f"raise preliminary maintainability objection.",
        })

    # F6 — Auction Already Completed (sale certificate issued) — v5.4
    # Does not terminate. Activates Celir LLP threshold analysis in M10.
    if case_facts.get("sale_certificate_issued") is True:
        route_flags.append({
            "filter_id": "F6",
            "result_label": "HIGH_THRESHOLD_CHALLENGE",
            "reason": f"Sale certificate issued on "
                      f"{case_facts.get('sale_certificate_date', 'unknown date')}. "
                      f"The auction has been completed and sale confirmed. Setting aside "
                      f"the sale now requires fundamental procedural error or fraud per "
                      f"Celir LLP v. Bafna Motors (2023) 13 SCC 561. M3 rules will assess "
                      f"whether M3_C6/M3_C7/M3_C8 apply — these are the grounds that can "
                      f"clear the Celir LLP threshold.",
        })

    return IntakeFilterResult(passed=True, route_flags=route_flags)
```

**Note (v5.4):** `IntakeFilterResult` gains a `route_flags: list[dict] = []` field to carry
F5/F6 — unlike F1-F4, these are non-terminating routing signals, not pass/fail gates, so
they cannot use the early-`return passed=False` pattern without stopping the pipeline.

---

## 7. Master Case Fact Schema

**AI IDE instruction:** This schema is the contract between every module.
Implement as Pydantic v2 models. Use `model_validator` for computed fields.
Every field is a `FactEntry[T]` — never a raw `T`. The rule engine reads `FactEntry.value`.

### 7.1 FactEntry — Core Structure

```python
# app/models/schemas.py  (relevant section)
from pydantic import BaseModel, field_validator
from typing import Any, Generic, Literal, TypeVar
from datetime import date, datetime
from uuid import UUID

T = TypeVar("T")

ExtractionMethod = Literal[
    "regex",            # deterministic regex — confidence always 1.0
    "nlp_explicit",     # LLM extracted, stated explicitly in text
    "nlp_implied",      # LLM inferred by implication — capped at 0.75
    "human_confirmed"   # officer confirmed in workbench — confidence always 1.0
]

class FactEntry(BaseModel, Generic[T]):
    value:               T | None = None
    confidence:          float = 0.0          # 0.0 - 1.0
    source_document_id:  UUID | None = None
    source_page:         int | None = None
    source_paragraph_id: UUID | None = None
    extraction_method:   ExtractionMethod | None = None
    human_confirmed:     bool = False
    confirmed_by:        UUID | None = None
    confirmed_at:        datetime | None = None

    @field_validator("confidence")
    @classmethod
    def cap_implied_confidence(cls, v, info):
        # nlp_implied is always capped at 0.75 regardless of model output
        if info.data.get("extraction_method") == "nlp_implied":
            return min(v, 0.75)
        return v

# Confidence routing constants — used by confidence_router.py
CONFIDENCE_THRESHOLD_AUTO_ACCEPT = 0.80  # below this → workbench required
CONFIDENCE_THRESHOLD_BLOCK_RULES = 0.0   # null / unconfirmed → UNKNOWN in rule engine
```

### 7.2 Full Fact Schema by Module

```python
# All fields below are attributes of class CaseFactSchema(BaseModel)
# Located at app/models/schemas.py

from decimal import Decimal

class CaseFactSchema(BaseModel):

    # ── M1: Section 13(2) Demand Notice ──────────────────────────────────────
    demand_notice_date:              FactEntry[date] = FactEntry()
    demand_notice_amount:            FactEntry[Decimal] = FactEntry()
    actual_outstanding_amount:       FactEntry[Decimal] = FactEntry()
    notice_service_mode:             FactEntry[Literal[
                                       "registered_post_ad",
                                       "personal_service",
                                       "substituted_service",
                                       "email_if_agreed",
                                       "unknown"
                                     ]] = FactEntry()
    notice_service_date:             FactEntry[date] = FactEntry()
    notice_service_acknowledged:     FactEntry[bool] = FactEntry()
    notice_dispatch_proof_present:   FactEntry[bool] = FactEntry()
    sixty_day_period_elapsed:        FactEntry[bool] = FactEntry()   # computed

    # ── M2: Section 13(3A) Reply ──────────────────────────────────────────────
    objection_filed:                 FactEntry[bool] = FactEntry()
    objection_date:                  FactEntry[date] = FactEntry()
    objection_content_summary:       FactEntry[str] = FactEntry()
    bank_reply_given:                FactEntry[bool] = FactEntry()
    bank_reply_date:                 FactEntry[date] = FactEntry()
    reply_days_elapsed:              FactEntry[int] = FactEntry()    # computed

    # ── M3: Rule 8 & 9 Auction ────────────────────────────────────────────────
    possession_notice_date:          FactEntry[date] = FactEntry()
    possession_taken_date:           FactEntry[date] = FactEntry()
    possession_mode:                 FactEntry[Literal["symbolic","physical"]] = FactEntry()
    sale_notice_date:                FactEntry[date] = FactEntry()
    sale_notice_service_date:        FactEntry[date] = FactEntry()
    auction_date:                    FactEntry[date] = FactEntry()
    auction_gap_days:                FactEntry[int] = FactEntry()    # computed
    asset_type:                      FactEntry[Literal["immovable","movable","perishable"]] = FactEntry()
    newspaper_publication_done:      FactEntry[bool] = FactEntry()

    # ── M4: Section 17 Limitation ─────────────────────────────────────────────
    measure_date:                    FactEntry[date] = FactEntry()
    measure_type:                    FactEntry[Literal[
                                       "possession_notice",
                                       "physical_possession",
                                       "sale_notice",
                                       "auction"
                                     ]] = FactEntry()
    sa_filing_date:                  FactEntry[date] = FactEntry()
    days_from_measure_to_sa:         FactEntry[int] = FactEntry()    # computed

    # ── M5: Tenancy ───────────────────────────────────────────────────────────
    tenancy_claimed:                 FactEntry[bool] = FactEntry()
    lease_date:                      FactEntry[date] = FactEntry()
    lease_registered:                FactEntry[bool] = FactEntry()
    lease_type:                      FactEntry[Literal[
                                       "monthly_tenancy",
                                       "fixed_term_lease",
                                       "leave_and_licence",
                                       "unknown"
                                     ]] = FactEntry()
    lease_duration_months:           FactEntry[int] = FactEntry()
    mortgage_date:                   FactEntry[date] = FactEntry()
    lease_predates_mortgage:         FactEntry[bool] = FactEntry()   # computed
    lease_post_default_notice:       FactEntry[bool] = FactEntry()   # computed

    # ── M6: Rule 8(6) Valuation ───────────────────────────────────────────────
    valuation_report_present:        FactEntry[bool] = FactEntry()
    valuer_name:                     FactEntry[str] = FactEntry()
    valuer_rbi_empanelled:           FactEntry[bool] = FactEntry()   # human confirmed always
    valuer_registered_under_rvact:   FactEntry[bool] = FactEntry()   # Registered Valuers Act 2017
    valuation_date:                  FactEntry[date] = FactEntry()
    valuation_amount:                FactEntry[Decimal] = FactEntry()
    reserve_price:                   FactEntry[Decimal] = FactEntry()
    reserve_price_vs_valuation_pct:  FactEntry[float] = FactEntry()  # computed
    valuation_age_at_auction_days:   FactEntry[int] = FactEntry()    # computed
    second_valuation_done:           FactEntry[bool] = FactEntry()

    # ── M7: Multiple Borrower/Guarantor ───────────────────────────────────────
    total_borrowers_in_loan:         FactEntry[int] = FactEntry()
    total_guarantors_in_loan:        FactEntry[int] = FactEntry()
    borrowers_served_notice:         FactEntry[int] = FactEntry()
    guarantors_served_notice:        FactEntry[int] = FactEntry()
    all_borrowers_served:            FactEntry[bool] = FactEntry()   # computed
    all_guarantors_served:           FactEntry[bool] = FactEntry()   # computed
    unserved_parties:                FactEntry[list[str]] = FactEntry()

    # ── M8: NPA Classification ────────────────────────────────────────────────
    loan_account_number:             FactEntry[str] = FactEntry()
    date_of_last_payment:            FactEntry[date] = FactEntry()
    npa_classification_date:         FactEntry[date] = FactEntry()
    days_from_last_payment_to_npa:   FactEntry[int] = FactEntry()    # computed
    restructuring_proposal_pending:  FactEntry[bool] = FactEntry()
    restructuring_approval_date:     FactEntry[date] = FactEntry()
    classification_notice_given:     FactEntry[bool] = FactEntry()
    interest_application_correct:    FactEntry[bool] = FactEntry()

    # ── M9: MSME ──────────────────────────────────────────────────────────────
    msme_claimed_by_borrower:        FactEntry[bool] = FactEntry()
    udyam_cert_in_bank_file:         FactEntry[bool] = FactEntry()   # human confirmed always
    udyam_registration_number:       FactEntry[str] = FactEntry()
    udyam_registration_date:         FactEntry[date] = FactEntry()
    enterprise_category:             FactEntry[Literal["micro","small","medium"]] = FactEntry()
    restructuring_offered_pre_npa:   FactEntry[bool] = FactEntry()
    applicable_rbi_circular:         FactEntry[str] = FactEntry()

    # ── NEW v5.0 fields — required for new rules ──────────────────────────────
    # M1 additions
    notice_content_complete:         FactEntry[bool] = FactEntry()   # M1_C6 — all 4 elements present
    transfer_post_notice:            FactEntry[bool] = FactEntry()   # S.13(13) transfer bar
    # M3 additions
    emd_stated_in_notice:            FactEntry[bool] = FactEntry()   # EMD in sale notice
    # Cross-cutting
    ibc_moratorium_active:           FactEntry[bool] = FactEntry()   # human confirmed always — F4 filter
    civil_court_stay_granted:        FactEntry[bool] = FactEntry()

    # ── NEW v5.1 fields (Audit Additions) ─────────────────────────────────────
    # M1/M3 (AO Authorization)
    authorized_officer_name:         FactEntry[str] = FactEntry()
    authorized_officer_designation:  FactEntry[str] = FactEntry()
    ao_has_written_authorization:    FactEntry[bool] = FactEntry()  # human confirmed

    # M2 (Bank Reply)
    bank_reply_gives_reasons:        FactEntry[bool] = FactEntry()
    bank_reply_addresses_objection:  FactEntry[bool] = FactEntry()

    # Property (F1 filter)
    property_classification:         FactEntry[Literal[
        "residential", "commercial", "industrial",
        "agricultural", "mixed_use", "unknown"
    ]] = FactEntry()

    # DRT Stay (Pre-Report Gate)
    drt_interim_stay_granted:        FactEntry[bool] = FactEntry()  # Section 17(4) stay by DRT
    drt_stay_order_date:             FactEntry[date] = FactEntry()

    # ── APPLICANT IDENTITY (Critical routing field — v5.4) ────────────────────
    # Determines which modules run and how conclusions are framed.
    # BORROWER / GUARANTOR → standard M1-M9 analysis applies
    # THIRD_PARTY_ATS      → M10 applies; M1-M9 apply for procedural grounds only
    # THIRD_PARTY_TENANT   → M5 applies primarily
    # AUCTION_PURCHASER    → M10-B applies; challenges SA trying to set aside sale
    # THIRD_PARTY_HEIR     → limited standing analysis
    sa_applicant_type:               FactEntry[Literal[
        "BORROWER",
        "GUARANTOR",
        "THIRD_PARTY_ATS",
        "THIRD_PARTY_TENANT",
        "AUCTION_PURCHASER",
        "THIRD_PARTY_HEIR",
        "OTHER"
    ]] = FactEntry()

    # Auction Type (M3)
    auction_type:                    FactEntry[Literal["public_auction", "e_auction"]] = FactEntry()
    e_auction_platform:              FactEntry[str] = FactEntry()  # e.g. "Bank's own portal", "MSTC", "IBAPI"

    # ── M3 AUCTION NOTICE COMPLIANCE — Missing Fields (v5.4) ──────────────────
    # Rule 8(6)(7) of SI Enforcement Rules 2002 requires the sale notice to be
    # affixed at the conspicuous part of the immovable property.
    # Non-compliance = sale null and void per Mathew Varghese (2014) 5 SCC 610.
    auction_notice_affixed_on_property: FactEntry[bool] = FactEntry()
    auction_notice_affixing_date:       FactEntry[date] = FactEntry()  # date notice was affixed

    # If a DRT or HC stay was in operation when the bank conducted the auction —
    # conducting auction in defiance of a court order is ABSOLUTE_BAR (Celir LLP).
    auction_conducted_despite_stay:       FactEntry[bool] = FactEntry()
    stay_was_operational_on_auction_date: FactEntry[bool] = FactEntry()  # computed

    # Rule 8(6)(7)(a): bank must disclose all encumbrances KNOWN to it in the
    # auction notice, including pending litigation. Non-disclosure = concealment.
    auction_notice_discloses_pending_sa:  FactEntry[bool] = FactEntry()
    pending_sa_existed_at_auction_date:   FactEntry[bool] = FactEntry()

    # ── M10 THIRD PARTY ATS HOLDER FIELDS (v5.4) ─────────────────────────────
    # For cases where the SA applicant is not the borrower but holds an
    # Agreement to Sell (ATS) over the mortgaged property.
    ats_date:                         FactEntry[date]  = FactEntry()
    ats_total_consideration:          FactEntry[float] = FactEntry()   # full sale price agreed
    ats_advance_paid:                 FactEntry[float] = FactEntry()   # amount actually paid
    ats_registered:                   FactEntry[bool]  = FactEntry()   # registered u/s 17 RA 1908?
    ats_stamp_duty_paid:              FactEntry[bool]  = FactEntry()
    ats_possession_given:              FactEntry[bool]  = FactEntry()   # physical possession handed over?
    ats_predates_mortgage:            FactEntry[bool]  = FactEntry()   # computed
    ats_simultaneous_mortgage:        FactEntry[bool]  = FactEntry()   # same date = high fraud risk
    ats_payments_made_to_loan_account: FactEntry[bool] = FactEntry()  # did ATS holder pay bank EMIs?
    ats_payments_total:               FactEntry[float] = FactEntry()   # total paid to bank account

    # ── M10 AUCTION PURCHASER + RIGHT OF REDEMPTION FIELDS (v5.4) ────────────
    # For challenges to a completed auction — either by the original applicant
    # seeking to set aside, or by auction purchaser defending the sale.
    # Celir LLP v. Bafna Motors (2023) 13 SCC 561 governs these scenarios.
    sale_certificate_issued:              FactEntry[bool] = FactEntry()
    sale_certificate_date:                FactEntry[date] = FactEntry()
    sale_deed_executed:                   FactEntry[bool] = FactEntry()
    possession_given_to_auction_purchaser: FactEntry[bool] = FactEntry()
    right_of_redemption_extinguished:      FactEntry[bool] = FactEntry()  # computed
    # Right of redemption (TPA s.60) is extinguished upon confirmation of sale
    # per Celir LLP. Once possession given to auction purchaser, threshold to
    # set aside rises dramatically — requires fraud or fundamental procedural error.

    # ── M8 ENHANCEMENT — NPA Status at Auction Date (v5.4) ───────────────────
    payments_post_npa_total:            FactEntry[float] = FactEntry()
    # Total payments made AFTER NPA classification date.
    # RBI IRAC 4.2.5: if arrears of interest+principal paid, account becomes Standard.
    # Therefore: was the account still NPA on the auction date?
    account_standard_at_auction_date:   FactEntry[bool]  = FactEntry()   # computed
    overdue_amount_at_auction_date:     FactEntry[float]  = FactEntry()

    # Previous SA (Cross Check)
    previous_sa_filed:               FactEntry[bool] = FactEntry()
    previous_sa_number:              FactEntry[str] = FactEntry()
    previous_sa_outcome:             FactEntry[Literal["pending","dismissed","allowed","withdrawn"]] = FactEntry()

    # ── SA PRAYER CLAUSE — Structured (v5.4) ─────────────────────────────────
    # The prayer clause defines the scope of DRT adjudication.
    # A measure not prayed against cannot be set aside even if defective.
    # This structured schema replaces the raw sa_prayer_text string.
    #
    # Extraction target in BATCH_USER_TEMPLATE:
    # "prayers": [{"prayer_type": "...", "is_interim": bool, "measure_date": "...", "prayer_text_verbatim": "..."}]
    #
    # Controlled vocabulary for prayer_type:
    # SET_ASIDE_DEMAND_NOTICE       — Section 13(2) notice challenged
    # SET_ASIDE_POSSESSION_NOTICE   — Section 13(4) notice challenged
    # SET_ASIDE_SALE_NOTICE         — Sale notice / auction proclamation challenged
    # SET_ASIDE_AUCTION             — The auction itself challenged (most common post-auction)
    # SET_ASIDE_SALE_CERTIFICATE    — Sale certificate to auction purchaser challenged
    # RESTRAIN_POSSESSION           — Stop physical possession being taken
    # RESTRAIN_SALE_DEED_EXECUTION  — Stop bank from executing sale deed to purchaser
    # RESTRAIN_AUCTION              — Stop upcoming auction
    # GRANT_TIME_TO_PAY             — Give time to regularise / pay outstanding
    # CONSIDER_OTS                  — Direct bank to consider One Time Settlement
    # ADJUDICATE_AMOUNT             — DRT to calculate correct outstanding amount
    # STAY_ALL_PROCEEDINGS          — Omnibus stay of all SARFAESI measures
    # INTERIM_ONLY                  — Ad-interim relief pending main hearing
    # OTHER                         — Anything not in the above list

    sa_prayer_text:                  FactEntry[str]       = FactEntry()  # verbatim full text
    prayers:                         FactEntry[list[dict]] = FactEntry()  # structured list

    # Each dict in prayers has shape:
    # {
    #   "prayer_type":          str,         # from controlled vocabulary above
    #   "is_interim":           bool,        # True = ad-interim prayer, False = final relief
    #   "measure_date":         str | None,  # date of the specific measure challenged (DD.MM.YYYY)
    #   "prayer_text_verbatim": str,         # exact prayer language
    #   "granted":              bool | None  # None = unknown, True/False if order passed
    # }

    # Derived from prayers — computed at workbench confirmation:
    interim_stay_prayed:             FactEntry[bool] = FactEntry()  # any prayer with is_interim=True
    interim_stay_granted:            FactEntry[bool] = FactEntry()  # any prayer granted=True + is_interim=True

    # What SARFAESI measures are being challenged:
    challenges_demand_notice:        FactEntry[bool] = FactEntry()  # SET_ASIDE_DEMAND_NOTICE in prayers
    challenges_possession_notice:    FactEntry[bool] = FactEntry()  # SET_ASIDE_POSSESSION_NOTICE
    challenges_sale_notice:          FactEntry[bool] = FactEntry()  # SET_ASIDE_SALE_NOTICE
    challenges_auction:              FactEntry[bool] = FactEntry()  # SET_ASIDE_AUCTION or SET_ASIDE_SALE_CERTIFICATE
    challenges_demand_amount:        FactEntry[bool] = FactEntry()  # ADJUDICATE_AMOUNT in prayers

    # CRITICAL — prayer vs measure alignment check (rule engine computes this):
    # If auction is complete but applicant only prays SET_ASIDE_DEMAND_NOTICE → flag PRAYER_SCOPE_MISMATCH
    prayer_scope_covers_current_measure: FactEntry[bool] = FactEntry()

    # Loan Type (M8)
    loan_account_type:               FactEntry[Literal[
        "term_loan", "cash_credit", "overdraft",
        "housing_loan", "vehicle_loan", "other"
    ]] = FactEntry()

    # Citations
    borrower_cited_judgments:        FactEntry[list[str]] = FactEntry()  # citations in SA text

    # ── COMPUTED FIELDS — model_validator implementations ─────────────────────
    # FIXED v5.0: v4.0 declared these as FactEntry() but showed no computation.
    # An AI IDE would leave them empty (value=None). Implementations are now explicit.

    @model_validator(mode="after")
    def compute_derived_fields(self) -> "CaseFactSchema":

        # M1: sixty_day_period_elapsed — possession notice issued ≥ 60 days after service
        nd  = self.demand_notice_date.value
        sp  = self.notice_service_date.value
        pnd = self.possession_notice_date.value
        if nd and sp and pnd:
            service_d = sp if sp > nd else nd  # use later of issue and service dates
            self.sixty_day_period_elapsed = FactEntry(
                value=(pnd - service_d).days >= 60,
                confidence=1.0, extraction_method="regex"
            )

        # M2: reply_days_elapsed
        od  = self.objection_date.value
        brd = self.bank_reply_date.value
        if od and brd:
            self.reply_days_elapsed = FactEntry(
                value=(brd - od).days,
                confidence=1.0, extraction_method="regex"
            )

        # M3: auction_gap_days
        snd = self.sale_notice_date.value
        ad  = self.auction_date.value
        if snd and ad:
            self.auction_gap_days = FactEntry(
                value=(ad - snd).days,
                confidence=1.0, extraction_method="regex"
            )

        # M4: days_from_measure_to_sa
        md  = self.measure_date.value
        sfd = self.sa_filing_date.value
        if md and sfd:
            self.days_from_measure_to_sa = FactEntry(
                value=(sfd - md).days,
                confidence=1.0, extraction_method="regex"
            )

        # M5: lease_predates_mortgage
        ld  = self.lease_date.value
        mrd = self.mortgage_date.value
        if ld and mrd:
            self.lease_predates_mortgage = FactEntry(
                value=ld < mrd,
                confidence=1.0, extraction_method="regex"
            )

        # M5: lease_post_default_notice
        dnd = self.demand_notice_date.value
        ld2 = self.lease_date.value
        if ld2 and dnd:
            self.lease_post_default_notice = FactEntry(
                value=ld2 > dnd,
                confidence=1.0, extraction_method="regex"
            )

        # M6: reserve_price_vs_valuation_pct
        rp = self.reserve_price.value
        va = self.valuation_amount.value
        if rp is not None and va is not None and va > 0:
            self.reserve_price_vs_valuation_pct = FactEntry(
                value=float(rp / va * 100),
                confidence=1.0, extraction_method="regex"
            )

        # M6: valuation_age_at_auction_days
        vd  = self.valuation_date.value
        ad2 = self.auction_date.value
        if vd and ad2:
            self.valuation_age_at_auction_days = FactEntry(
                value=(ad2 - vd).days,
                confidence=1.0, extraction_method="regex"
            )

        # M7: all_borrowers_served
        tb = self.total_borrowers_in_loan.value
        bs = self.borrowers_served_notice.value
        if tb is not None and bs is not None:
            self.all_borrowers_served = FactEntry(
                value=bs >= tb,
                confidence=1.0, extraction_method="regex"
            )

        # M7: all_guarantors_served
        tg = self.total_guarantors_in_loan.value
        gs = self.guarantors_served_notice.value
        if tg is not None and gs is not None:
            self.all_guarantors_served = FactEntry(
                value=gs >= tg,
                confidence=1.0, extraction_method="regex"
            )

        # M8: days_from_last_payment_to_npa
        dlp = self.date_of_last_payment.value
        ncd = self.npa_classification_date.value
        if dlp and ncd:
            self.days_from_last_payment_to_npa = FactEntry(
                value=(ncd - dlp).days,
                confidence=1.0, extraction_method="regex"
            )

        # M10: right of redemption extinguished when sale confirmed
        try:
            if (self.sale_certificate_issued.value is True
                    and self.auction_date.value is not None):
                self.right_of_redemption_extinguished = FactEntry(
                    value=True, implied=True
                )
        except Exception:
            pass

        # M10: ATS predates mortgage
        try:
            if (self.ats_date.value is not None
                    and self.mortgage_date.value is not None):
                self.ats_predates_mortgage = FactEntry(
                    value=self.ats_date.value < self.mortgage_date.value,
                    implied=True
                )
                self.ats_simultaneous_mortgage = FactEntry(
                    value=self.ats_date.value == self.mortgage_date.value,
                    implied=True
                )
        except Exception:
            pass

        # M3: stay operational on auction date
        try:
            if (self.drt_interim_stay_granted.value is True
                    and self.drt_stay_order_date.value is not None
                    and self.auction_date.value is not None):
                self.stay_was_operational_on_auction_date = FactEntry(
                    value=self.drt_stay_order_date.value <= self.auction_date.value,
                    implied=True
                )
        except Exception:
            pass

        return self
```

### 7.3 SA Grounds Schema

```python
# app/models/schemas.py (continued)
from enum import Enum

class GroundCode(str, Enum):
    SERVICE_DEFECT          = "SERVICE_DEFECT"
    AMOUNT_DISPUTE          = "AMOUNT_DISPUTE"
    REPLY_NOT_GIVEN         = "REPLY_NOT_GIVEN"
    AUCTION_GAP_DEFECT      = "AUCTION_GAP_DEFECT"
    NEWSPAPER_PUB_DEFECT    = "NEWSPAPER_PUB_DEFECT"
    LIMITATION_EXPIRED      = "LIMITATION_EXPIRED"
    TENANCY_CLAIM           = "TENANCY_CLAIM"
    VALUATION_DISPUTE       = "VALUATION_DISPUTE"
    NOTICE_ALL_PARTIES      = "NOTICE_ALL_PARTIES"
    NPA_PREMATURE           = "NPA_PREMATURE"
    NPA_DURING_RESTRUC      = "NPA_DURING_RESTRUC"
    MSME_RESTRUC_SKIPPED    = "MSME_RESTRUC_SKIPPED"
    POSSESSION_DEFECT       = "POSSESSION_DEFECT"
    NOTICE_FORMAT_DEFECT    = "NOTICE_FORMAT_DEFECT"
    AO_AUTHORIZATION        = "AO_AUTHORIZATION"
    # ^ Authorized Officer not properly authorized — M1 ground
    AUCTION_NOTICE_AFFIXING = "AUCTION_NOTICE_AFFIXING"
    # ^ Auction notice not affixed at property — Rule 8(6)(7) — M3 ground
    AUCTION_DURING_STAY     = "AUCTION_DURING_STAY"
    # ^ Auction conducted while DRT/court stay was in operation — M3 ground
    PENDING_SA_CONCEALED    = "PENDING_SA_CONCEALED"
    # ^ Bank concealed pending SA from CMM/court when filing Section 14 petition
    THIRD_PARTY_ATS         = "THIRD_PARTY_ATS"
    # ^ Agreement to Sell holder challenging enforcement — M10 ground
    AUCTION_PURCHASER       = "AUCTION_PURCHASER"
    # ^ Auction purchaser's rights / challenge to sale being set aside — M10 ground
    RIGHT_OF_REDEMPTION     = "RIGHT_OF_REDEMPTION"
    # ^ Borrower's right to redeem u/s 60 TPA before sale confirmation — M10 ground
    SECOND_SA_FRESH_CAUSE   = "SECOND_SA_FRESH_CAUSE"
    # ^ Second SA filed on a different/fresh cause of action — Oasis Dealcom principle
    UNKNOWN                 = "UNKNOWN"

class SAGround(BaseModel):
    ground_code:           GroundCode
    statutory_basis:       Literal["ACT", "RULES", "BOTH", "RBI", "TPA", "OTHER"] = "ACT"
    source_paragraphs:     list[UUID]
    factual_claim:         str
    documents_cited_by_sa: list[str] = []
    confidence:            float
```

---

## 8. Database Schema — Complete

**AI IDE instruction:** This is the complete PostgreSQL schema.
Run via Alembic. Command: `alembic upgrade head`.
Do NOT use SQLAlchemy `create_all()` — migrations only.

### 8.1 Alembic Setup

```python
# alembic/env.py — critical lines
from app.models.db import Base
from app.config import settings

config.set_main_option("sqlalchemy.url", settings.database_url)
target_metadata = Base.metadata
```

### 8.2 Full SQL Schema

```sql
-- ─── BANKS ───────────────────────────────────────────────────────────────────
CREATE TABLE banks (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name         TEXT NOT NULL,
    short_code   TEXT UNIQUE NOT NULL,  -- e.g. 'SBI', 'HDFC', 'PNB'
    active       BOOLEAN DEFAULT TRUE,
    created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- ─── USERS ───────────────────────────────────────────────────────────────────
CREATE TABLE users (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bank_id       UUID NOT NULL REFERENCES banks(id),
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,        -- bcrypt via passlib
    role          TEXT NOT NULL
                  CHECK (role IN ('BANK_OFFICER','BANK_ADMIN','SYSTEM_ADMIN')),
    active        BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- ─── CASES ───────────────────────────────────────────────────────────────────
CREATE TABLE cases (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bank_id              UUID NOT NULL REFERENCES banks(id),
    created_by           UUID NOT NULL REFERENCES users(id),
    case_ref             TEXT,
    drt_case_number      TEXT,
    drt_bench            TEXT,
    borrower_name        TEXT NOT NULL,
    property_description TEXT,
    loan_account_number  TEXT,
    principal_amount     NUMERIC(18,2),
    status               TEXT NOT NULL DEFAULT 'DRAFT'
                         CHECK (status IN (
                             'DRAFT',
                             'INTAKE_REJECTED',       -- pre-intake filter fired
                             'PROCESSING',            -- Chain A running
                             'PENDING_HUMAN_REVIEW',  -- Chain A done, waiting workbench
                             'ANALYSING',             -- Chain B running
                             'PENDING_JUDGMENT_REVIEW', -- Chain B paused for precedent review
                             'COMPLETE',              -- report generated
                             'FAILED'                 -- unrecoverable error
                         )),
    pipeline_stage       TEXT,    -- current Celery task name for progress display
    intake_filter_result JSONB,   -- result from pre_intake.py if filter fired
    judgment_coverage_alerts JSONB DEFAULT NULL, -- null = no gaps; array = uncovered grounds
    created_at           TIMESTAMPTZ DEFAULT NOW(),
    updated_at           TIMESTAMPTZ DEFAULT NOW()
);

-- ─── DOCUMENTS ───────────────────────────────────────────────────────────────
CREATE TABLE documents (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id         UUID NOT NULL REFERENCES cases(id),
    uploaded_by     UUID NOT NULL REFERENCES users(id),
    doc_type        TEXT NOT NULL,  -- see DocType enum in Section 11
    file_url        TEXT NOT NULL,  -- S3 path — immutable after insert
    sha256_hash     TEXT NOT NULL,  -- integrity verification
    version         INT DEFAULT 1,
    language        TEXT DEFAULT 'en',
    page_count      INT,
    ocr_status      TEXT DEFAULT 'PENDING'
                    CHECK (ocr_status IN ('PENDING','PROCESSING','COMPLETE','FAILED')),
    uploaded_at     TIMESTAMPTZ DEFAULT NOW()
);
-- IMMUTABILITY RULE: No UPDATE on (file_url, sha256_hash) after insert.
-- Enforce via app layer — do not update these columns, ever.

-- ─── PARAGRAPHS ──────────────────────────────────────────────────────────────
CREATE TABLE paragraphs (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id         UUID NOT NULL REFERENCES documents(id),
    page_number         INT NOT NULL,
    para_sequence       INT NOT NULL,
    text_original       TEXT NOT NULL,   -- raw OCR — NEVER modified after insert
    text_translated     TEXT,            -- Hindi → English (additive only)
    language            TEXT DEFAULT 'en',
    is_heading          BOOLEAN DEFAULT FALSE,
    is_numbered         BOOLEAN DEFAULT FALSE,
    is_handwritten      BOOLEAN DEFAULT FALSE,  -- if true: skip extraction, flag in UI
    bbox                JSONB,           -- {x1, y1, x2, y2} in points
    ocr_confidence      FLOAT,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

-- ─── CASE FACTS ──────────────────────────────────────────────────────────────
CREATE TABLE case_facts (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id              UUID NOT NULL REFERENCES cases(id),
    field_name           TEXT NOT NULL,
    field_value          TEXT,           -- all values stored as text; typed at app layer
    confidence           FLOAT,
    source_document_id   UUID REFERENCES documents(id),
    source_page          INT,
    source_paragraph_id  UUID REFERENCES paragraphs(id),
    extraction_method    TEXT
                         CHECK (extraction_method IN (
                             'regex','nlp_explicit','nlp_implied','human_confirmed'
                         )),
    human_confirmed      BOOLEAN DEFAULT FALSE,
    confirmed_by         UUID REFERENCES users(id),
    confirmed_at         TIMESTAMPTZ,
    created_at           TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (case_id, field_name)         -- one authoritative value per field per case
);

-- ─── FACT CONFLICTS (WORKBENCH TYPE 3) ───────────────────────────────────────
CREATE TABLE fact_conflicts (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id             UUID NOT NULL REFERENCES cases(id),
    field_name          TEXT NOT NULL,

    -- Candidate A (first extracted value)
    candidate_a_value             TEXT,
    candidate_a_source_doc_id     UUID REFERENCES documents(id),
    candidate_a_source_page       INT,
    candidate_a_extraction_method TEXT,

    -- Candidate B (conflicting value from second document)
    candidate_b_value             TEXT,
    candidate_b_source_doc_id     UUID REFERENCES documents(id),
    candidate_b_source_page       INT,
    candidate_b_extraction_method TEXT,

    -- Resolution
    resolved            BOOLEAN DEFAULT FALSE,
    resolved_value      TEXT,               -- which candidate won, or manual entry
    resolved_by         UUID REFERENCES users(id),
    resolved_at         TIMESTAMPTZ,

    created_at          TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (case_id, field_name)            -- one active conflict per field per case
);

CREATE INDEX idx_fact_conflicts_case ON fact_conflicts(case_id, resolved);

-- ─── SA GROUNDS ──────────────────────────────────────────────────────────────
CREATE TABLE sa_grounds (
    id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id                  UUID NOT NULL REFERENCES cases(id),
    ground_code              TEXT NOT NULL,
    statutory_basis          TEXT,
    source_paragraph_id      UUID REFERENCES paragraphs(id),
    factual_claim_extracted  TEXT,
    documents_cited          TEXT[],
    confidence               FLOAT,
    created_at               TIMESTAMPTZ DEFAULT NOW()
);

-- ─── COMPLIANCE RESULTS ──────────────────────────────────────────────────────
CREATE TABLE compliance_results (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id         UUID NOT NULL REFERENCES cases(id),
    rule_id         TEXT NOT NULL,
    module          TEXT NOT NULL,
    status          TEXT NOT NULL CHECK (status IN ('PASS','FAIL','UNKNOWN')),
    severity        TEXT CHECK (severity IN (
                        'FATAL','ABSOLUTE_BAR','CURABLE','MINOR','ADVISORY',
                        'REVIEW_REQUIRED','UNKNOWN'
                    )),
    message         TEXT,
    detail_json     JSONB,      -- computed values used (dates, gaps, percentages)
    judgment_tags   TEXT[],
    evaluated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- ─── JUDGMENTS ───────────────────────────────────────────────────────────────
CREATE TABLE judgments (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    citation              TEXT UNIQUE NOT NULL,
    title                 TEXT NOT NULL,
    short_name            TEXT,
    court                 TEXT NOT NULL
                          CHECK (court IN ('SUPREME_COURT','HIGH_COURT','DRAT','DRT')),
    high_court_state      TEXT,
    bench_strength        INT DEFAULT 1,
    judgment_date         DATE,
    overruled             BOOLEAN DEFAULT FALSE,
    overruled_by          UUID REFERENCES judgments(id),
    favor                 TEXT CHECK (favor IN ('BANK','BORROWER','NEUTRAL')),
    favor_verified        BOOLEAN DEFAULT FALSE,
    ground_codes          TEXT[],
    holding_summary       TEXT,           -- written by lawyer, not AI
    has_verified_conditions BOOLEAN DEFAULT FALSE,
    source                TEXT CHECK (source IN ('SC_FULL_TEXT','IBC_LAW_SUMMARY')),
    applicable_conditions JSONB,          -- list of Condition objects
    exclusion_conditions  JSONB,          -- list of Condition objects
    added_by              UUID REFERENCES users(id),
    added_at              TIMESTAMPTZ DEFAULT NOW(),
    last_reviewed_at      TIMESTAMPTZ     -- quarterly review tracking
);

-- ─── JUDGMENT APPLICABILITY ───────────────────────────────────────────────────
CREATE TABLE judgment_applicability (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id         UUID NOT NULL REFERENCES cases(id),
    judgment_id     UUID NOT NULL REFERENCES judgments(id),
    ground_code     TEXT,
    status          TEXT CHECK (status IN (
                        'APPLICABLE','PARTIAL','NOT_APPLICABLE',
                        'SIMILARITY_RETRIEVED',
                        'LEGAL_UNCERTAINTY','UNAVAILABLE'  -- FIXED v5.0: added, used in Section 18.3 and 18.6
                    )),
    reason          TEXT,
    evaluated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- ─── GROUND SCORES ───────────────────────────────────────────────────────────
CREATE TABLE ground_scores (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id          UUID NOT NULL REFERENCES cases(id),
    ground_code      TEXT NOT NULL,
    factual_score    FLOAT,
    judicial_score   FLOAT,
    ground_strength  FLOAT,
    corpus_total          INT DEFAULT 0,
    corpus_borrower_wins  INT DEFAULT 0,
    corpus_bank_wins      INT DEFAULT 0,
    corpus_confidence     TEXT DEFAULT 'NO_DATA',
    evaluated_at     TIMESTAMPTZ DEFAULT NOW()
);

-- ─── REPORTS ─────────────────────────────────────────────────────────────────
CREATE TABLE reports (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id              UUID NOT NULL REFERENCES cases(id),
    compliance_score     INT,
    litigation_exposure  FLOAT,
    recommendation       TEXT,
    report_json          JSONB,     -- full structured report
    pdf_url              TEXT,      -- S3 path
    content_hash         TEXT,      -- SHA-256 of report_json — tamper evidence
    generated_by         UUID REFERENCES users(id),
    generated_at         TIMESTAMPTZ DEFAULT NOW()
);

-- ─── AUDIT LOG ───────────────────────────────────────────────────────────────
CREATE TABLE audit_log (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id     UUID REFERENCES cases(id),
    user_id     UUID REFERENCES users(id),
    action      TEXT NOT NULL,  -- UPLOAD/CONFIRM_FACT/OVERRIDE_FACT/GENERATE_REPORT/LOGIN
    detail      JSONB,
    ip_address  TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ─── CASE STATUTES ───────────────────────────────────────────────────────────
CREATE TABLE case_statutes (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id             UUID NOT NULL REFERENCES cases(id),
    rule_id             TEXT NOT NULL,
    section_number      TEXT NOT NULL,
    act_name            TEXT NOT NULL,
    statute_text        TEXT NOT NULL,
    retrieved_at        TIMESTAMPTZ DEFAULT NOW()
);

-- ─── INDEXES ─────────────────────────────────────────────────────────────────
CREATE INDEX idx_cases_bank_id           ON cases(bank_id);
CREATE INDEX idx_cases_status            ON cases(status);
CREATE INDEX idx_documents_case_id       ON documents(case_id);
CREATE INDEX idx_paragraphs_document_id  ON paragraphs(document_id);
CREATE INDEX idx_case_facts_case_id      ON case_facts(case_id);
CREATE INDEX idx_case_facts_field        ON case_facts(case_id, field_name);
CREATE INDEX idx_sa_grounds_case_id      ON sa_grounds(case_id);
CREATE INDEX idx_compliance_case_id      ON compliance_results(case_id);
CREATE INDEX idx_ground_scores_case_id   ON ground_scores(case_id);
CREATE INDEX idx_audit_case_id           ON audit_log(case_id);
CREATE INDEX idx_audit_user_id           ON audit_log(user_id);
```

### 8.3 Object Storage Structure (S3)

```
s3://slrai-documents/
    cases/{case_id}/
        documents/{doc_id}.pdf          # original — immutable
        documents/{doc_id}_v2.pdf       # re-upload (new doc_id, not overwrite)
        reports/{report_id}.pdf
        reports/{report_id}.json
    judgments/
        {judgment_id}.pdf               # source judgment document
```


### 8.4 Qdrant Collection Setup

The system uses TWO Qdrant collections. Never merge them. Never query one when
you need the other. Their retrieval patterns are fundamentally different.

```python
# app/services/judgments/retrieval.py — run on first deploy via app/main.py lifespan

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PayloadSchemaType

def setup_qdrant_collections(client: QdrantClient):
    """
    Called from app/main.py lifespan startup.
    Idempotent — skips collection creation if already exists.
    """
    _create_judgments_collection(client)
    _create_statutes_collection(client)


def _create_judgments_collection(client: QdrantClient):
    """
    sarfaesi_judgments — ~7,500 vectors.
    One vector per judgment (half-page IBC Law summary or SC full-text chunk).
    Retrieved by ground_code filter + vector similarity.
    top_k = 20 per retrieval call.
    """
    if client.collection_exists("sarfaesi_judgments"):
        return

    client.create_collection(
        collection_name="sarfaesi_judgments",
        vectors_config=VectorParams(
            size=768,               # InLegalBERT output dimension
            distance=Distance.COSINE
        )
    )

    # Payload indexes — all filter fields must be indexed for performance at 7,500 scale
    client.create_payload_index(
        "sarfaesi_judgments", "ground_codes",           PayloadSchemaType.KEYWORD
    )
    client.create_payload_index(
        "sarfaesi_judgments", "court",                  PayloadSchemaType.KEYWORD
    )
    client.create_payload_index(
        "sarfaesi_judgments", "favor",                  PayloadSchemaType.KEYWORD
    )
    client.create_payload_index(
        "sarfaesi_judgments", "overruled",              PayloadSchemaType.BOOL
    )
    client.create_payload_index(
        "sarfaesi_judgments", "has_verified_conditions", PayloadSchemaType.BOOL
    )
    client.create_payload_index(
        "sarfaesi_judgments", "source",                 PayloadSchemaType.KEYWORD
    )


### Judgment Payload Schema

Each document in `sarfaesi_judgments` has this payload:

```python
JudgmentPayload = {
    # Identity
    "id":                      str,    # UUID (matches judgments PostgreSQL table)
    "citation":                str,    # "(2011) 2 SCC 782" or "(2026) ibclaw.in 47 DRAT"
    "title":                   str,
    "short_name":              str,

    # Court metadata
    "court":                   str,    # "SUPREME_COURT" | "HIGH_COURT" | "DRAT" | "DRT"
    "high_court_state":        str | None,
    "bench_strength":          int,    # default 1 for IBC Law summaries (unknown)
    "judgment_date":           str | None,  # ISO date or None for IBC summaries without date

    # Legal classification
    "favor":                   str,    # "BANK" | "BORROWER" | "NEUTRAL"
    "ground_codes":            list[str],  # GroundCode enum values
    "overruled":               bool,

    # Content
    "holding_summary":         str,    # half-page IBC Law summary OR manually written (SC)

    # Class A vs Class B
    "has_verified_conditions": bool,   # True = Class A, False = Class B
    "source":                  str,    # "SC_FULL_TEXT" | "IBC_LAW_SUMMARY"

    # For SC full-text chunks only
    "chunk_type":              str | None,  # "facts" | "arguments" | "held" | None
}
```
## 9. Authentication & RBAC

### 9.1 JWT Token Structure

```python
# JWT payload — exactly these fields, nothing else
JWTPayload = {
    "sub":      str,    # user UUID
    "bank_id":  str,    # bank UUID — used for ALL data isolation queries
    "role":     str,    # "BANK_OFFICER" | "BANK_ADMIN" | "SYSTEM_ADMIN"
    "exp":      int     # Unix timestamp
}

# bank_id MUST come from JWT — NEVER from request body
# This is the data isolation mechanism — a bank officer cannot see another bank's cases
```

### 9.2 Role Permissions

| Action | BANK_OFFICER | BANK_ADMIN | SYSTEM_ADMIN |
|--------|:---:|:---:|:---:|
| Create case | ✓ | ✓ | ✓ |
| Upload documents | ✓ | ✓ | ✓ |
| Confirm facts in workbench | ✓ | ✓ | ✓ |
| Generate report | ✓ | ✓ | ✓ |
| View all cases in own bank | ✗ | ✓ | ✓ |
| Create/manage users | ✗ | ✓ | ✓ |
| Add/edit judgments | ✗ | ✗ | ✓ |
| View all banks' cases | ✗ | ✗ | ✓ |

### 9.3 Data Isolation Rule

**AI IDE instruction:** Every database query that touches case data MUST filter by `bank_id`.
This is enforced at the repository/service layer, not at the route layer.

```python
# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.config import settings

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        return {
            "user_id": payload["sub"],
            "bank_id": payload["bank_id"],
            "role":    payload["role"]
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

def require_role(*roles: str):
    async def checker(user: dict = Depends(get_current_user)) -> dict:
        if user["role"] not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return user
    return checker

# Example usage in a route:
# @router.get("/{case_id}")
# async def get_case(case_id: UUID, user: dict = Depends(get_current_user)):
#     # Always pass user["bank_id"] to the service — NEVER trust case_id alone
#     return await case_service.get_case(case_id, bank_id=user["bank_id"])
```

---

## 10. End-to-End Pipeline — Two-Chain Architecture

**AI IDE instruction:** This is the most critical section. Read carefully.
The pipeline is split into TWO separate Celery chains, not one.
They are never combined. Chain A ends with a DB status update.
Chain B is triggered explicitly by an API call after human confirmation.
**Do NOT connect Chain A and Chain B with `|` operator or `chord`.**

### 10.1 Case `status` and `pipeline_stage` Flow

```
DRAFT
  → (pre-intake filters pass) → PROCESSING  [Chain A fires]
  → INTAKE_REJECTED           [pre-intake filter terminated]
  → PENDING_HUMAN_REVIEW      [Chain A complete — awaiting workbench]
  → ANALYSING                 [Chain B fires on POST /workbench/confirm-all]
  → COMPLETE                  [Chain B complete — report available]
  → FAILED                    [unrecoverable error in either chain]
```

### 10.2 Chain A — Automatic (fires on document upload)

**FIXED v5.0:** All tasks now use `.si()` (immutable signature) instead of `.s()`.
`.si()` ignores the previous task's return value, eliminating the `_` passthrough problem.
Each task receives its arguments directly — `case_id` is never passed through the chain as
a positional return value. Tasks no longer have `_` as first argument.

```python
# app/tasks/chain_a.py
from celery import chain
from app.tasks.celery_app import celery_app

@celery_app.task(bind=True, name="tasks.chain_a.run", max_retries=2)
def run_chain_a(self, case_id: str, doc_id: str):
    """
    Fired automatically after first document upload for a case.
    Ends by setting case status = PENDING_HUMAN_REVIEW.
    Does NOT proceed to compliance engine — that is Chain B.
    """
    pipeline = chain(
        task_update_pipeline_stage.si(case_id, "OCR"),           # .si() = immutable — ignores prev return
        task_ocr_document.si(case_id, doc_id),
        task_update_pipeline_stage.si(case_id, "LANGUAGE_DETECTION"),
        task_detect_language.si(case_id),
        task_update_pipeline_stage.si(case_id, "TRANSLATION"),
        task_translate_hindi_paragraphs.si(case_id),
        task_update_pipeline_stage.si(case_id, "REGEX_EXTRACTION"),
        task_regex_extract_all.si(case_id),
        task_update_pipeline_stage.si(case_id, "NLP_CLASSIFICATION"),
        task_nlp_classify_issues.si(case_id),
        task_update_pipeline_stage.si(case_id, "NLP_EXTRACTION"),
        task_nlp_extract_facts.si(case_id),
        task_update_pipeline_stage.si(case_id, "POPULATING_WORKBENCH"),
        task_populate_workbench.si(case_id),
        task_set_case_status.si(case_id, "PENDING_HUMAN_REVIEW"),  # ← CHAIN A ENDS HERE
    )
    pipeline.delay()

@celery_app.task(name="tasks.chain_a.set_status")
def task_set_case_status(case_id: str, status: str) -> None:
    """Updates cases.status in DB.
    FIXED v5.0: removed _ first arg — use .si() in chains, not .s().
    """
    from app.models.db import get_sync_session, Case
    with get_sync_session() as db:
        case = db.query(Case).filter_by(id=case_id).first()
        case.status = status
        case.pipeline_stage = None
        db.commit()

@celery_app.task(name="tasks.chain_a.update_stage")
def task_update_pipeline_stage(case_id: str, stage: str) -> None:
    """FIXED v5.0: removed _ first arg — use .si() in chains."""
    from app.models.db import get_sync_session, Case
    with get_sync_session() as db:
        case = db.query(Case).filter_by(id=case_id).first()
        case.pipeline_stage = stage
        db.commit()
```

### 10.3 Chain B — Officer-Triggered (fires on workbench confirmation)

```python
# app/tasks/chain_b.py

@celery_app.task(bind=True, name="tasks.chain_b.run", max_retries=1)
def run_chain_b(self, case_id: str):
    """
    Fired by POST /api/v1/cases/{case_id}/workbench/confirm-all
    PRECONDITION: All required fields in workbench are human_confirmed = True.
    This is validated at the API layer before this task is fired.
    If precondition fails, raise HTTP 422 at the route — do NOT fire this task.
    """
    pipeline = chain(
        task_set_case_status.si(case_id, "ANALYSING"),   # .si() — imported from chain_a
        task_run_compliance_engine.si(case_id),
        task_retrieve_judgments.si(case_id),
        task_evaluate_applicability.si(case_id),
        task_compute_ground_statistics.si(case_id),      # NEW: corpus win rates
        task_check_judgment_coverage.si(case_id),
        task_resolve_precedence.si(case_id),
        task_score_grounds.si(case_id),
        task_compute_compliance_score.si(case_id),
        task_generate_recommendation.si(case_id),
        task_generate_report.si(case_id),
        task_set_case_status.si(case_id, "COMPLETE"),
    )
    pipeline.delay()

@celery_app.task(name="tasks.chain_b.run_compliance_engine")
def task_run_compliance_engine(case_id: str):
    """
    v5.4: M10 now activates for non-borrower/non-guarantor applicants.
    For standard borrower SAs: run M1-M9 only.
    For third party SAs: run M1-M9 (procedural grounds apply to bank)
    AND M10 (third party claim framework).
    For auction purchaser challenges: M3, M6, M10 are primary.
    """
    with get_sync_db() as db:
        facts = _load_confirmed_facts(case_id, db)
        applicant_type = facts.get("sa_applicant_type", "BORROWER")

        # Always run M1-M9 — procedural compliance applies regardless of applicant
        modules_to_run = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9"]

        # M10 activates for non-standard applicants
        if applicant_type not in ["BORROWER", "GUARANTOR", None]:
            modules_to_run.append("M10")

        results = run_all_modules(facts, modules_to_run=modules_to_run)

        for result in results:
            db.add(ComplianceResult(
                case_id=case_id,
                rule_id=result.rule_id,
                module=result.module,
                status=result.status,
                severity=result.severity,
                message=result.message,
            ))
        db.commit()

@celery_app.task(name="tasks.chain_b.check_judgment_coverage")
def task_check_judgment_coverage(case_id: str):
    """
    Checks whether every SA ground has at least one APPLICABLE Class A judgment.
    Stores alerts on cases when gaps exist. This task never blocks Chain B.
    Frontend shows a modal before report rendering if alerts are present.
    If officer chooses Pause, case status becomes PENDING_JUDGMENT_REVIEW and
    the resume endpoint re-fires Chain B from task_retrieve_judgments only.
    """
    from app.models.db import get_sync_session, Case, SAGround, JudgmentApplicability

    with get_sync_session() as db:
        sa_grounds = db.query(SAGround).filter_by(case_id=case_id).all()
        alerts = []

        for ground in sa_grounds:
            applicable = db.query(JudgmentApplicability).filter_by(
                case_id=case_id,
                ground_code=ground.ground_code,
                status="APPLICABLE"
            ).count()

            similarity = db.query(JudgmentApplicability).filter_by(
                case_id=case_id,
                ground_code=ground.ground_code,
                status="SIMILARITY_RETRIEVED"
            ).count()

            if applicable == 0:
                alerts.append({
                    "ground_code":      ground.ground_code,
                    "severity":         "WARNING" if similarity > 0 else "NO_PRECEDENT",
                    "similarity_count": similarity,
                    "message": (
                        f"No verified precedent for '{ground.ground_code}'. "
                        f"{similarity} potentially relevant judgment(s) found "
                        f"but factual conditions not verified. Review manually."
                        if similarity > 0 else
                        f"No precedent of any kind found for '{ground.ground_code}'. "
                        f"Neutral judicial score (0.40) applied. "
                        f"Manual legal research required."
                    ),
                    "action_required": similarity == 0
                })

        if alerts:
            case = db.query(Case).filter_by(id=case_id).first()
            case.judgment_coverage_alerts = alerts
            db.commit()
```

### 10.4 Celery Configuration

```python
# app/tasks/celery_app.py
from celery import Celery
from app.config import settings

celery_app = Celery(
    "slrai",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,           # re-queue on worker crash
    worker_prefetch_multiplier=1,  # one task at a time per worker (for heavy OCR/NLP tasks)
    task_routes={
        "tasks.chain_a.*": {"queue": "pipeline"},
        "tasks.chain_b.*": {"queue": "pipeline"},
    }
)
```

---

## 11.1. OCR & Document Intelligence

# app/services/ocr/azure_ocr.py
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from app.config import settings

# Cache at module level — never instantiate per call.
# New client per call = ~200ms HTTPS reconnect overhead every time.
_ocr_client: DocumentIntelligenceClient | None = None

def get_ocr_client() -> DocumentIntelligenceClient:
    global _ocr_client
    if _ocr_client is None:
        _ocr_client = DocumentIntelligenceClient(
            endpoint=settings.azure_ocr_endpoint,
            credential=AzureKeyCredential(settings.azure_ocr_key)
        )
    return _ocr_client


async def extract_layout(file_bytes: bytes) -> dict:
    """
    Layout extraction using Azure Document Intelligence prebuilt-layout model.

    CRITICAL — two fixes from v5.0:
    1. Use model_id="prebuilt-layout" not "prebuilt-read" (read loses structure)
    2. Use result.paragraphs not page.lines.
       page.lines = visual line breaks. A numbered clause across 3 lines becomes 3 items.
       result.paragraphs = semantic groupings. The clause stays one unit.
    """
    client = get_ocr_client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        analyze_request={"bytes_source": file_bytes},
        content_type="application/json"
    )
    result = poller.result()

    paragraphs = []
    for seq, para in enumerate(result.paragraphs or []):
        page_num = (
            para.bounding_regions[0].page_number
            if para.bounding_regions else 1
        )
        bbox = None
        if para.bounding_regions and para.bounding_regions[0].polygon:
            poly = para.bounding_regions[0].polygon
            bbox = {
                "x1": poly[0].x, "y1": poly[0].y,
                "x2": poly[4].x if len(poly) > 4 else poly[2].x,
                "y2": poly[4].y if len(poly) > 4 else poly[2].y,
            }
        paragraphs.append({
            "page_number":    page_num,
            "para_sequence":  seq,
            "text":           para.content,
            "bbox":           bbox,
            "ocr_confidence": getattr(para, "confidence", None),
            "role":           getattr(para, "role", None),
        })

    return {
        "paragraphs": paragraphs,
        "page_count": len(result.pages) if result.pages else 0
    }

### 11.2 IndicTrans2 — Translation Integration

**AI IDE instruction:** This is NOT on PyPI as `pip install IndicTrans2`.
It is loaded as a HuggingFace model. Use exactly the model name and loading code below.
On CPU, expect 2–5 seconds per paragraph. Cache model in memory at worker startup.

```python
# app/services/translation/indictrans.py
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
from app.config import settings

# Module-level cache — loaded once per worker process, not per request
_tokenizer = None
_model = None

def _load_model():
    global _tokenizer, _model
    if _tokenizer is None:
        model_name = settings.translation_model
        # model_name = "ai4bharat/indictrans2-hi-en-dist-200M"
        _tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True   # required for IndicTrans2
        )
        _model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        device = settings.translation_device  # "cpu" or "cuda"
        _model = _model.to(device)
        _model.eval()

def translate_hi_to_en(text: str) -> str:
    """
    Translates Hindi text to English.
    Input text should be a single paragraph — do not batch entire documents.
    Returns English translation. Original is preserved separately.
    """
    _load_model()
    device = settings.translation_device

    inputs = _tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512
    ).to(device)

    with torch.no_grad():
        outputs = _model.generate(
            **inputs,
            max_length=512,
            num_beams=4,
            early_stopping=True
        )

    return _tokenizer.decode(outputs[0], skip_special_tokens=True)
```

### 11.3 Language Detection

```python
# app/services/ocr/layout_parser.py (excerpt)
from langdetect import detect, LangDetectException

def detect_paragraph_language(text: str) -> str:
    """Returns 'en', 'hi', or 'mixed'."""
    try:
        lang = detect(text)
        if lang == "hi":
            return "hi"
        # Check for mixed: if Hindi script characters present alongside Latin
        hindi_chars = sum(1 for c in text if "\u0900" <= c <= "\u097F")
        if hindi_chars > 5:
            return "mixed"
        return "en"
    except LangDetectException:
        return "en"   # default to English on detection failure
```

### 11.4 Document Type Classifier

```python
# app/services/extraction/doc_classifier.py
# Keyword-rule classifier. NO AI. Deterministic.

DOC_TYPE_KEYWORDS = {
    "SA":               ["securitisation application", "section 17", "drt", "applicant"],
    "DEMAND_NOTICE":    ["section 13(2)", "13(2)", "demand notice", "60 days", "discharge"],
    "OBJECTION":        ["representation", "objection", "reply", "aggrieved"],
    "BANK_REPLY":       ["13(3a)", "section 13(3a)", "considered your objection"],
    "POSSESSION_NOTICE":["section 13(4)", "symbolic possession", "possession notice"],
    "SALE_NOTICE":      ["rule 8", "sale notice", "auction", "reserve price", "e-auction"],
    "VALUATION_REPORT": ["valuation", "valuer", "fair market value", "distress value"],
    "LOAN_AGREEMENT":   ["loan agreement", "sanction letter", "terms and conditions"],
    "GUARANTEE":        ["guarantee", "guarantor", "personal guarantee"],
    "ACCOUNT_STATEMENT":["account statement", "outstanding", "principal", "interest"],
    "UDYAM_CERT":       ["udyam", "msme", "ministry of micro"],
    "LEASE_DEED":       ["lease deed", "rent agreement", "tenancy agreement", "lessee"],
    "MORTGAGE_DEED":    ["mortgage deed", "mortgagor", "mortgagee", "equitable mortgage"],
    "DRT_ORDER":        ["drt order", "interim order", "tribunal order", "stay order"],
}

def classify_document(first_500_chars: str) -> str:
    text_lower = first_500_chars.lower()
    scores = {}
    for doc_type, keywords in DOC_TYPE_KEYWORDS.items():
        scores[doc_type] = sum(1 for kw in keywords if kw in text_lower)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "OTHER"
```

---

## 12. NLP Extraction Architecture

### 12.1 Regex Layer — Layer A (runs first, always)

```python
# app/services/extraction/regex_layer.py
import re
from datetime import date
from decimal import Decimal

REGEX_PATTERNS = {
    "date_dmy_dot":    re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b"),
    "date_dmy_slash":  re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b"),
    "date_written":    re.compile(
        r"\b(\d{1,2})(?:st|nd|rd|th)?\s+"
        r"(January|February|March|April|May|June|July|August|September|October|November|December)"
        r"\s+(\d{4})\b",
        re.IGNORECASE
    ),
    "amount_inr":      re.compile(
        r"(?:Rs\.?|INR|Rupees?)\s*"
        r"([\d,]+(?:\.\d{2})?)"
        r"(?:\s*(?:lakhs?|lacs?|crores?|thousands?|/-))?"
    ),
    "section_ref":     re.compile(
        r"(?:[Ss]ection|[Ss]ec\.?|[Ss]\.)\s*"
        r"(\d+(?:\([A-Za-z0-9]+\))*)",
        re.IGNORECASE
    ),
    "rule_ref":        re.compile(r"[Rr]ule\s+(\d+[A-Za-z]?(?:\([A-Za-z0-9]+\))*)"),
}

MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12
}

def extract_dates(text: str) -> list[dict]:
    """Returns list of {date, raw_text, confidence: 1.0}"""
    results = []
    for pattern_name, pattern in {
        k: v for k, v in REGEX_PATTERNS.items() if k.startswith("date_")
    }.items():
        for match in pattern.finditer(text):
            try:
                if pattern_name == "date_written":
                    d = date(
                        int(match.group(3)),
                        MONTH_MAP[match.group(2).lower()],
                        int(match.group(1))
                    )
                else:
                    d = date(
                        int(match.group(3)),
                        int(match.group(2)),
                        int(match.group(1))
                    )
                results.append({
                    "date": d.isoformat(),
                    "raw_text": match.group(0),
                    "confidence": 1.0,
                    "extraction_method": "regex"
                })
            except ValueError:
                continue   # invalid date (e.g. 31/02/2023) — skip
    return results

def extract_amounts(text: str) -> list[dict]:
    """Returns list of {amount: Decimal, raw_text, confidence: 1.0}"""
    results = []
    for match in REGEX_PATTERNS["amount_inr"].finditer(text):
        amount_str = match.group(1).replace(",", "")
        try:
            results.append({
                "amount": str(Decimal(amount_str)),
                "raw_text": match.group(0),
                "confidence": 1.0,
                "extraction_method": "regex"
            })
        except Exception:
            continue
    return results
```

### 12.2a LLM Layer — Layer B (Batched Claude API — never per-paragraph)

**Why batched:** A 30-page SA has ~150 paragraphs. After regex, ~70 need Claude.
Sequential calls: 70 × 1.8s = 126s. Batched at 7/call: 10 calls × 2.5s = 25s.
That is a 5× speedup on the most expensive step in Chain A.

**AI IDE instruction:** Never call Claude once per paragraph. Always batch.
`process_paragraphs_for_extraction()` is the only entry point for NLP extraction.

```python
# app/services/extraction/nlp_layer.py
import json
import time
import anthropic
from app.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

BATCH_SIZE = 7   # paragraphs per Claude call — never exceed 8

BATCH_SYSTEM_PROMPT = """You are a legal document parser for Indian SARFAESI Act proceedings.
You will receive multiple paragraphs from the same legal document.
Extract structured facts from each paragraph.
Return ONLY a valid JSON array — one extraction object per paragraph, same order.
No preamble. No markdown. No explanation. First character must be [
Do not infer beyond what is stated. For implied facts set implied: true.
Missing facts: null. Never fabricate a value.

CRITICAL DISTINCTION: ACT vs RULES
When classifying ground_codes, you must identify if the borrower is challenging the ACT (the bank's fundamental right or interpretation of law) or the RULES (specific procedural or timing defects).
- ACT challenges route to the judgment corpus (Class A/B precedent matching).
- RULES challenges route to the deterministic YAML Rule Engine.
Assign statutory_basis correctly.

THIRD PARTY AND POST-AUCTION GROUND DETECTION (v5.4):

When extracting ground_codes, also check for:

1. THIRD_PARTY_ATS — present when applicant:
   - States they are "neither borrower nor guarantor"
   - Mentions an "Agreement to Sell" or "Agreement for Sale" or "ATS"
   - Claims they are in physical possession under a private sale agreement
   - Has paid substantial consideration directly to the borrower
   -> Set sa_applicant_type: "THIRD_PARTY_ATS"

2. AUCTION_DURING_STAY — present when applicant:
   - Mentions a DRT order / High Court order restraining possession or auction
   - States the bank conducted the auction DESPITE a pending court order
   - References any interim stay, injunction, or "court receiver" restraint
   -> Set auction_conducted_despite_stay: true

3. AUCTION_NOTICE_AFFIXING — present when applicant:
   - States the auction notice was never put up / affixed / pasted on the property
   - Mentions they were in possession and no notice was given at the property
   - Cites Rule 8(6)(7) or Mathew Varghese or Vasu Shetty
   -> Set auction_notice_affixed_on_property: false

4. RIGHT_OF_REDEMPTION — present when applicant:
   - Argues they have paid all outstanding dues
   - Claims the account is no longer NPA
   - Cites RBI IRAC clause 4.2.5 (NPA upgradation)
   - States they tendered payment before auction / after auction but before possession
   -> Extract payments_post_npa_total from stated payment amounts

5. SECOND_SA_FRESH_CAUSE — present when:
   - Applicant mentions they previously filed an SA
   - Present SA challenges a different SARFAESI measure (e.g. previous challenged
     demand notice, present challenges the auction)
   - Applicant cites "Oasis Dealcom" or "fresh cause of action"
   -> Set previous_sa_filed: true, challenges_auction: true

PRAYER DETECTION RULES:
- Look for paragraph headings: "PRAYER", "PRAYER CLAUSE", "RELIEF SOUGHT",
  "IT IS THEREFORE PRAYED", "PRAYERS", "IT IS RESPECTFULLY PRAYED"
- After finding the prayer paragraph, extract EACH sub-prayer as a separate item
- Mark prayers with "(ad-interim)" or "(interim)" or "(ex-parte)" as is_interim: true
- Mark prayers asking to "set aside" the auction/certificate as
  prayer_type: "SET_ASIDE_AUCTION" or "SET_ASIDE_SALE_CERTIFICATE"
- Mark prayers asking to "restrain" the bank as prayer_type: "RESTRAIN_*"
- The prayer clause is the most important paragraph in any SA — extract it completely"""

BATCH_USER_TEMPLATE = """Document type: {doc_type}

Extract from these {count} paragraphs. Return array of exactly {count} objects.

{paragraphs_json}

Each object must have this exact structure:
{{
  "metadata": {{
    "drt_jurisdiction": "DRT bench city/name if mentioned, else null",
    "sa_number":        "SA/application number if mentioned, else null",
    "primary_borrower": "borrower name if mentioned, else null"
  }},
  "dates": [
    {{"date": "DD.MM.YYYY", "context": "what event this date refers to", "implied": false}}
  ],
  "amounts": [
    {{"amount": 0.00, "currency": "INR", "context": "what this amount refers to"}}
  ],
  "dispatch_proof_methods": [],
  "ground_codes": [
    {{"code": "CODE_NAME", "statutory_basis": "ACT | RULES | BOTH | RBI | OTHER"}}
  ],
  "prayers": [
    {{
      "prayer_type": "SET_ASIDE_DEMAND_NOTICE|SET_ASIDE_POSSESSION_NOTICE|SET_ASIDE_SALE_NOTICE|SET_ASIDE_AUCTION|SET_ASIDE_SALE_CERTIFICATE|RESTRAIN_POSSESSION|RESTRAIN_SALE_DEED_EXECUTION|RESTRAIN_AUCTION|GRANT_TIME_TO_PAY|CONSIDER_OTS|ADJUDICATE_AMOUNT|STAY_ALL_PROCEEDINGS|OTHER",
      "is_interim": true,
      "measure_date": "DD.MM.YYYY or null",
      "prayer_text_verbatim": "exact prayer language from this paragraph",
      "granted": null
    }}
  ],
  "sa_prayer_text": "full verbatim prayer clause if this paragraph contains it",
  "boolean_facts": {{
    "notice_served":                    null,
    "objection_filed":                  null,
    "bank_reply_given":                 null,
    "lease_claimed":                    null,
    "lease_registered":                 null,
    "valuation_disputed":               null,
    "valuation_challenged_by_borrower": null,
    "valuer_section_247_registered":    null,
    "valuer_rbi_empanelled":            null,
    "all_parties_served":               null,
    "npa_premature_alleged":            null,
    "msme_status_claimed":              null
  }},
  "confidence":              0.0,
  "implied_facts_present":   false,
  "ambiguous_elements":      []
}}

Valid dispatch_proof_methods: "registered_post_ad", "personal_service",
"substituted_service", "courier", "email", "affidavit_of_service", "unknown"

Valid ground_codes: SERVICE_DEFECT, AMOUNT_DISPUTE, REPLY_NOT_GIVEN,
AUCTION_GAP_DEFECT, NEWSPAPER_PUB_DEFECT, LIMITATION_EXPIRED, TENANCY_CLAIM,
VALUATION_DISPUTE, NOTICE_ALL_PARTIES, NPA_PREMATURE, NPA_DURING_RESTRUC,
MSME_RESTRUC_SKIPPED, POSSESSION_DEFECT, NOTICE_FORMAT_DEFECT, AO_AUTHORIZATION,
AUCTION_NOTICE_AFFIXING, AUCTION_DURING_STAY, PENDING_SA_CONCEALED,
THIRD_PARTY_ATS, AUCTION_PURCHASER, RIGHT_OF_REDEMPTION, SECOND_SA_FRESH_CAUSE,
UNKNOWN"""


def extract_facts_batch(
    paragraphs: list[dict],   # each: {para_id, text_for_extraction, doc_type}
    max_retries: int = 2
) -> list[dict | None]:
    """
    Single Claude API call extracting facts from up to BATCH_SIZE paragraphs.
    Returns list of extraction dicts, same order as input.
    Returns None for a paragraph slot if extraction failed.
    Never raises — failure returns None entries, caller handles gracefully.
    """
    if not paragraphs:
        return []

    doc_type = paragraphs[0].get("doc_type", "UNKNOWN")
    count     = len(paragraphs)

    paragraphs_prompt = json.dumps([
        {"index": i, "text": p["text_for_extraction"]}
        for i, p in enumerate(paragraphs)
    ], ensure_ascii=False, indent=2)

    prompt = BATCH_USER_TEMPLATE.format(
        doc_type=doc_type,
        count=count,
        paragraphs_json=paragraphs_prompt
    )

    for attempt in range(max_retries + 1):
        try:
            response = client.messages.create(
                model=settings.claude_model,       # "claude-sonnet-4-6"
                max_tokens=4000,                   # increased for batch responses
                temperature=settings.llm_temperature,  # always 0.0
                system=BATCH_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
            raw = response.content[0].text.strip()
            raw = raw.replace("```json", "").replace("```", "").strip()
            result = json.loads(raw)

            if not isinstance(result, list) or len(result) != count:
                raise ValueError(
                    f"Expected list of {count}, got {type(result).__name__} "
                    f"len={len(result) if isinstance(result, list) else 'N/A'}"
                )
            return result

        except (json.JSONDecodeError, ValueError):
            if attempt == max_retries:
                return [None] * count
            time.sleep(1)

        except anthropic.APITimeoutError:
            if attempt == max_retries:
                return [None] * count
            time.sleep(5)

        except anthropic.RateLimitError:
            raise   # re-raise to Celery for exponential backoff retry

        except anthropic.AuthenticationError:
            raise   # fatal — wrong key, Celery sets case FAILED

        except Exception:
            return [None] * count


def process_paragraphs_for_extraction(
    all_paragraphs: list[dict],
    batch_size: int = BATCH_SIZE
) -> list[dict | None]:
    """
    Entry point for NLP extraction in Chain A.
    Groups paragraphs by doc_type, handles oversized paragraphs solo,
    batches the rest. Returns results in same order as input.

    Oversized = text_for_extraction > 2,400 chars (estimate >600 tokens).
    Oversized paragraphs are sent alone to avoid max_tokens overflow.
    """
    results: list[dict | None] = [None] * len(all_paragraphs)

    from itertools import groupby
    indexed = list(enumerate(all_paragraphs))
    indexed_sorted = sorted(indexed, key=lambda x: x[1].get("doc_type", ""))

    for _, group_iter in groupby(indexed_sorted, key=lambda x: x[1].get("doc_type", "")):
        group = list(group_iter)
        solos   = [(i, p) for i, p in group if len(p["text_for_extraction"]) > 2400]
        batched = [(i, p) for i, p in group if len(p["text_for_extraction"]) <= 2400]

        for orig_idx, para in solos:
            r = extract_facts_batch([para], max_retries=2)
            results[orig_idx] = r[0] if r else None

        for start in range(0, len(batched), batch_size):
            slice_ = batched[start:start + batch_size]
            orig_indices = [i for i, _ in slice_]
            paras = [p for _, p in slice_]
            batch_result = extract_facts_batch(paras, max_retries=2)
            for orig_idx, extraction in zip(orig_indices, batch_result):
                results[orig_idx] = extraction

    return results
```

### Schema Additions Explained

**`metadata` block:** DRT jurisdiction, SA number, primary borrower — extracted from
header paragraphs, aggregated at case level (first non-null value wins).
DRT jurisdiction matters for HC precedence (Bombay HC binds Maharashtra DRTs).

**`dispatch_proof_methods: list[str]`:** Replaces `notice_dispatch_proof_present: bool`.
Now captures which modes are claimed: `["registered_post_ad", "affidavit_of_service"]`.
Multiple modes can coexist. Used by M1_C3 (mode validity) and M1_C4 (proof present).

**`valuation_challenged_by_borrower: bool`:** Borrowers allege stale/understated valuation
without triggering a date-based rule. This flag captures the allegation itself for M6.

**`valuer_section_247_registered: bool`:** Companies Act 2013 Section 247 + Registered
Valuers and Appraisers Rules 2017 requires IBBI registration. Distinct from RBI empanelment.
Both fields are captured. Both are ALWAYS_HUMAN_CONFIRM — never auto-accepted.

### 12.2b IndicTrans2 — Batched Translation with Script Filter

**Translation vs Transliteration:** SLRAI performs meaning-based translation
(Hindi → English meaning), not transliteration (Hindi script → Roman script).
Transliterated text ("Maang Notice") is meaningless to Claude's extraction prompts.
Full translation ("Demand Notice issued on...") is what the extraction layer needs.

**Translation scope:** SAs are formal court documents — predominantly English.
Realistically 10-20% of paragraphs in a typical SA contain significant Hindi.
A 30-page SA has ~30 paragraphs needing translation, not 75-100.
With batching, this takes 9-12 seconds on CPU — not a bottleneck.

**Script filter:** Use Devanagari character ratio, not langdetect alone.
langdetect misclassifies short English legal clauses as Hindi frequently.
The 5% threshold is conservative — catches mixed paragraphs too.

```python
# app/services/translation/indictrans.py
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from app.config import settings

_tokenizer = None
_model     = None
TRANSLATION_BATCH_SIZE = 10  # per forward pass — max 10 CPU, 20 GPU
HINDI_SCRIPT_RANGE = ('\u0900', '\u097F')  # Devanagari Unicode block


def _load_model():
    global _tokenizer, _model
    if _tokenizer is None:
        name = settings.translation_model
        # "ai4bharat/indictrans2-hi-en-dist-200M" — requires trust_remote_code=True
        _tokenizer = AutoTokenizer.from_pretrained(name, trust_remote_code=True)
        _model = AutoModelForSeq2SeqLM.from_pretrained(name, trust_remote_code=True)
        _model = _model.to(settings.translation_device).eval()


def needs_translation(text: str, threshold: float = 0.05) -> bool:
    """
    True if Devanagari characters exceed threshold fraction of text.
    More reliable than langdetect for short legal clauses.
    threshold=0.05: at least 5% of chars must be Hindi script.
    """
    if not text or len(text) < 5:
        return False
    hindi = sum(1 for c in text if HINDI_SCRIPT_RANGE[0] <= c <= HINDI_SCRIPT_RANGE[1])
    return (hindi / len(text)) > threshold


def translate_batch(texts: list[str]) -> list[str]:
    """
    Single batched forward pass through IndicTrans2.
    10 paragraphs in one pass ≈ 1.5× cost of one paragraph.
    vs 10 sequential calls = 10× cost. Never call one-at-a-time.
    """
    _load_model()
    inputs = _tokenizer(
        texts,
        return_tensors="pt",
        padding=True,      # pads to longest in batch
        truncation=True,
        max_length=512
    ).to(settings.translation_device)

    with torch.no_grad():
        outputs = _model.generate(**inputs, max_length=512,
                                  num_beams=4, early_stopping=True)
    return [_tokenizer.decode(o, skip_special_tokens=True) for o in outputs]


def translate_paragraphs(paragraphs: list[dict]) -> list[dict]:
    """
    Entry point for task_translate_hindi_paragraphs in Chain A.
    paragraphs: list of {para_id, text_original, language}
    Returns same list with text_translated populated for Hindi paragraphs.
    text_original is NEVER modified — translation is additive only.
    English paragraphs: text_translated = None.
    """
    to_translate = [
        (i, p) for i, p in enumerate(paragraphs)
        if needs_translation(p["text_original"])
    ]
    if not to_translate:
        return paragraphs

    preprocessed_texts = [preprocess_hindi(p["text_original"]) for _, p in to_translate]

    translations = []
    for start in range(0, len(preprocessed_texts), TRANSLATION_BATCH_SIZE):
        batch = preprocessed_texts[start:start + TRANSLATION_BATCH_SIZE]
        translations.extend(translate_batch(batch))

    for (orig_idx, _), translation in zip(to_translate, translations):
        paragraphs[orig_idx]["text_translated"] = translation

    return paragraphs


def preprocess_hindi(text: str) -> str:
    for hindi, english in HINDI_LEGAL_MAP.items():
        text = text.replace(hindi, english)
    return text


HINDI_LEGAL_MAP = {
    "जबरन कब्जा":    "forcible possession",
    "कब्जा नोटिस":   "possession notice",
    "नीलामी":        "auction",
    "माँग नोटिस":    "demand notice",
    "बकाया राशि":    "outstanding amount",
    "बंधक":          "mortgage",
    "गारंटर":        "guarantor",
    "पुनर्गठन":      "restructuring",
    "आपत्ति":        "objection",
    "किरायेदार":     "tenant",
    "अप्रचलित आस्ति": "non-performing asset",
    "प्रतिभूति":     "security interest",
    "देनदार":        "debtor",
    "वसूली":         "recovery",
    "प्रतिनिधित्व":  "representation",
    "नीलाम":         "auction sale",
}
```

### 12.2c Fact Persistence — Upsert Helper and Metadata Aggregation

```python
# app/services/extraction/fact_persistence.py
"""
Upsert helper for case_facts table.
Replaces plain INSERT everywhere in extraction pipeline.
Makes Chain A idempotent — safe to retry after crash.
Plain INSERT on chain_id+field_name UNIQUE constraint = IntegrityError on retry.
"""
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.models.db import CaseFact

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy import select
from app.models.db import CaseFact, FactConflict
from app.services.compliance.engine import COMPUTED_FIELD_RESOLVERS

def upsert_case_fact(db, case_id: str, field_name: str, fact_data: dict):
    """
    Upsert with conflict detection.

    If a value already exists for this field AND the new value is different
    AND the existing value is not human_confirmed:
        → Create a fact_conflict record
        → Do NOT overwrite the existing value
        → The conflict appears in workbench for officer to resolve

    If existing value IS human_confirmed:
        → Never overwrite. Log and move on.

    If no existing value:
        → Insert normally.
    """
    if field_name in COMPUTED_FIELD_RESOLVERS:
        raise ValueError(
            f"Attempted to store computed field '{field_name}' in case_facts. "
            f"Computed fields must never be persisted — they are derived at rule engine time."
        )

    # Check what's already stored
    existing = db.execute(
        select(CaseFact).where(
            CaseFact.case_id == case_id,
            CaseFact.field_name == field_name
        )
    ).scalar_one_or_none()

    if existing is None:
        # No existing value — simple insert
        db.add(CaseFact(case_id=case_id, field_name=field_name, **fact_data))
        return

    if existing.human_confirmed:
        # Officer already confirmed this — never touch it
        return

    new_value = fact_data.get("field_value")
    if existing.field_value == new_value or new_value is None:
        # Same value or new extraction found nothing — no conflict
        return

    # Different value from different source — create conflict for officer to resolve
    conflict_exists = db.execute(
        select(FactConflict).where(
            FactConflict.case_id == case_id,
            FactConflict.field_name == field_name,
            FactConflict.resolved == False
        )
    ).scalar_one_or_none()

    if conflict_exists:
        return  # Conflict already registered, don't add more

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
    # Existing case_fact row stays untouched — officer resolves the conflict

def aggregate_metadata(case_id: str, extraction_results: list[dict], db):
    """
    Aggregate metadata fields across all extraction results.
    Takes first non-null value for each field (SA header is usually paragraph 0-3).
    Saves to case_facts as meta_drt_jurisdiction, meta_sa_number, meta_primary_borrower.
    """
    fields = {
        "meta_drt_jurisdiction": None,
        "meta_sa_number":        None,
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
                "field_value":      value,
                "confidence":       0.85,
                "extraction_method": "nlp_explicit",
                "human_confirmed":  False,
            })
```

### 12.3 Implied Fact Handling

```python
# app/services/extraction/confidence_router.py

CONFIDENCE_THRESHOLD = 0.80

def route_fact(field_name: str, extraction_result: dict) -> dict:
    """
    Determines if a fact goes to workbench or is auto-accepted.
    Returns enriched fact dict with routing decision.
    """
    is_implied = extraction_result.get("implied", False)
    confidence = extraction_result.get("confidence", 0.0)

    # Implied facts are ALWAYS capped and routed to workbench
    if is_implied:
        confidence = min(confidence, 0.75)
        return {**extraction_result, "confidence": confidence,
                "extraction_method": "nlp_implied",
                "requires_workbench": True}

    # These specific fields always require human confirmation — no exceptions
    ALWAYS_HUMAN_CONFIRM = {
        "valuer_rbi_empanelled",
        "udyam_cert_in_bank_file",
        "total_borrowers_in_loan",
        "total_guarantors_in_loan",
        "ibc_moratorium_active",        # NEW v5.0 — cannot be auto-verified; requires NCLT records
    }
    if field_name in ALWAYS_HUMAN_CONFIRM:
        return {**extraction_result,
                "extraction_method": "nlp_explicit",
                "requires_workbench": True}

    if confidence < CONFIDENCE_THRESHOLD:
        return {**extraction_result, "requires_workbench": True,
                "extraction_method": "nlp_explicit"}

    return {**extraction_result, "requires_workbench": False,
            "extraction_method": "nlp_explicit"}
```

### 12.4 Hindi Legal Term Dictionary

```python
# app/services/translation/indictrans.py (excerpt)
# Applied BEFORE translation — deterministic dictionary substitution

HINDI_LEGAL_MAP = {
    "जबरन कब्जा":    "forcible possession",
    "कब्जा नोटिस":   "possession notice",
    "नीलामी":        "auction",
    "माँग नोटिस":    "demand notice",
    "बकाया राशि":    "outstanding amount",
    "बंधक":          "mortgage",
    "गारंटर":        "guarantor",
    "पुनर्गठन":      "restructuring",
    "आपत्ति":        "objection",
    "किरायेदार":     "tenant",
    "अप्रचलित आस्ति":"non-performing asset",
    "प्रतिभूति":     "security interest",
    "देनदार":        "debtor / borrower",
    "वसूली":         "recovery",
}

def preprocess_hindi(text: str) -> str:
    """Apply dictionary substitution before passing to IndicTrans2."""
    for hindi, english in HINDI_LEGAL_MAP.items():
        text = text.replace(hindi, english)
    return text
```

---

## 13. YAML Rule Engine — Interpreter Contract

**AI IDE instruction:** This is the complete specification for the rule engine interpreter.
Implement exactly as specified. Do not use Python's `eval()`. Use `simpleeval`.

### 13.1 Rule File Format

```yaml
# Every rule YAML file follows this exact structure.
# File: app/services/compliance/rules/m2_reply.yaml

rules:
  - rule_id: M2_C1
    module: M2_REPLY_COMPLIANCE
    statutory_basis: "Section 13(3A) SARFAESI Act 2002"
    description: "Bank must reply to borrower objection within 15 days"

    preconditions:
      - field: objection_filed
        operator: eq
        value: true
        # If precondition field is null → rule status = UNKNOWN, not FAIL

    checks:
      - check_id: M2_C1_a
        description: "Bank reply not given at all"
        expression: "bank_reply_given == False"
        # expression is evaluated by simpleeval with fact values as names
        result_if_true: FAIL
        severity: FATAL
        message_template: "Borrower filed objection on {objection_date}. Bank has not replied. Section 13(3A) is a fatal defect."
        judgment_tags:
          - s13_3a_reply
          - borrower_rights

    pass_message_template: "Bank replied on {bank_reply_date}, {reply_days_elapsed} days after objection. Within 15-day limit."
```

### 13.2 Interpreter Implementation

```python
# app/services/compliance/engine.py
import yaml
import os
from pathlib import Path
from simpleeval import simple_eval, EvalWithCompoundTypes
from app.models.schemas import RuleResult

RULES_DIR = Path("app/services/compliance/rules")

def load_all_rules() -> list[dict]:
    """Load all YAML rule files. Called once at startup."""
    rules = []
    for yaml_file in sorted(RULES_DIR.glob("*.yaml")):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
            rules.extend(data.get("rules", []))
    return rules

# Fields that are NEVER stored in case_facts — always computed from raw fields
COMPUTED_FIELD_RESOLVERS = {
    "sixty_day_period_elapsed": lambda f: (
        ((f.get("possession_notice_date") or f.get("sale_notice_date")) - 
         max(f.get("demand_notice_date"), f.get("notice_service_date") or f.get("demand_notice_date"))).days >= 60
        if all(v for v in [
            f.get("demand_notice_date"),
            f.get("possession_notice_date") or f.get("sale_notice_date")
        ]) else None
    ),
    "reply_days_elapsed": lambda f: (
        (f["bank_reply_date"] - f["objection_date"]).days
        if f.get("bank_reply_date") and f.get("objection_date") else None
    ),
    "auction_gap_days": lambda f: (
        (f["auction_date"] - f["sale_notice_date"]).days
        if f.get("auction_date") and f.get("sale_notice_date") else None
    ),
    "days_from_measure_to_sa": lambda f: (
        (f["sa_filing_date"] - f["measure_date"]).days
        if f.get("sa_filing_date") and f.get("measure_date") else None
    ),
    "lease_predates_mortgage": lambda f: (
        f["lease_date"] < f["mortgage_date"]
        if f.get("lease_date") and f.get("mortgage_date") else None
    ),
    "lease_post_default_notice": lambda f: (
        f["lease_date"] > f["demand_notice_date"]
        if f.get("lease_date") and f.get("demand_notice_date") else None
    ),
    "reserve_price_vs_valuation_pct": lambda f: (
        float(f["reserve_price"] / f["valuation_amount"] * 100)
        if f.get("reserve_price") and f.get("valuation_amount") else None
    ),
    "valuation_age_at_auction_days": lambda f: (
        (f["auction_date"] - f["valuation_date"]).days
        if f.get("auction_date") and f.get("valuation_date") else None
    ),
    "all_borrowers_served": lambda f: (
        f["borrowers_served_notice"] >= f["total_borrowers_in_loan"]
        if f.get("borrowers_served_notice") is not None and f.get("total_borrowers_in_loan") else None
    ),
    "all_guarantors_served": lambda f: (
        f["guarantors_served_notice"] >= f["total_guarantors_in_loan"]
        if f.get("guarantors_served_notice") is not None and f.get("total_guarantors_in_loan") else None
    ),
    "days_from_last_payment_to_npa": lambda f: (
        (f["npa_classification_date"] - f["date_of_last_payment"]).days
        if f.get("npa_classification_date") and f.get("date_of_last_payment") else None
    ),
    # v5.4 additions
    "stay_was_operational_on_auction_date": lambda f: (
        (f.get("drt_interim_stay_granted") is True
         and f.get("drt_stay_order_date") is not None
         and f.get("auction_date") is not None
         and f["drt_stay_order_date"] <= f["auction_date"])
        if f.get("drt_stay_order_date") and f.get("auction_date") else None
    ),
    "right_of_redemption_extinguished": lambda f: (
        True if f.get("sale_certificate_issued") is True else None
    ),
    "ats_predates_mortgage": lambda f: (
        f["ats_date"] < f["mortgage_date"]
        if f.get("ats_date") and f.get("mortgage_date") else None
    ),
    "account_standard_at_auction_date": lambda f: (
        (f.get("payments_post_npa_total", 0) >= f.get("overdue_amount_at_auction_date", float("inf")))
        if f.get("payments_post_npa_total") and f.get("overdue_amount_at_auction_date") else None
    ),
}

def _get_fact_value(field_name: str, confirmed_facts: dict):
    """
    Returns confirmed value for a field, or None.
    For computed fields: calculates from raw confirmed facts inline.
    Raw facts are never overridden by stale computed values in DB.
    """
    # If this is a computed field, derive it now from raw facts
    if field_name in COMPUTED_FIELD_RESOLVERS:
        try:
            return COMPUTED_FIELD_RESOLVERS[field_name](confirmed_facts)
        except Exception:
            return None

    # Otherwise read from confirmed DB facts
    fact = confirmed_facts.get(field_name)
    if fact is None or not fact.get("human_confirmed", False):
        return None
    return fact.get("value")

def evaluate_rule(rule: dict, confirmed_facts: dict) -> RuleResult:
    """
    Evaluates a single rule against confirmed facts.
    Returns RuleResult with status PASS / FAIL / UNKNOWN.
    """
    rule_id = rule["rule_id"]
    module  = rule["module"]

    # Step 1: Check preconditions
    for pre in rule.get("preconditions", []):
        field_val = _get_fact_value(pre["field"], confirmed_facts)
        if field_val is None:
            return RuleResult(
                rule_id=rule_id, module=module,
                status="UNKNOWN", severity="UNKNOWN",
                message=f"Precondition field '{pre['field']}' not confirmed. "
                        f"Cannot evaluate {rule_id}.",
                detail={},
                judgment_tags=[]
            )
        # evaluate precondition itself
        expected = pre.get("value")
        op = pre.get("operator", "eq")
        if op == "eq" and field_val != expected:
            # Precondition not met — rule does not apply to this case
            return RuleResult(
                rule_id=rule_id, module=module,
                status="PASS",  # Not applicable = not a problem
                severity=None,
                message=f"Rule {rule_id} not applicable: precondition '{pre['field']}' is {field_val}.",
                detail={}, judgment_tags=[]
            )

    # Step 2: Build names dict for simpleeval
    # Only include facts that are confirmed — unconfirmed fields are absent
    names = {}
    for field_name in confirmed_facts:
        val = _get_fact_value(field_name, confirmed_facts)
        if val is not None:
            names[field_name] = val

    # Step 3: Evaluate each check
    for check in rule.get("checks", []):
        expression = check["expression"]

        # Check if all variables in expression are available
        # simpleeval raises NameNotDefined if a variable is missing
        try:
            evaluator = EvalWithCompoundTypes(names=names)
            result = evaluator.eval(expression)
        except Exception as e:
            # Variable missing from confirmed facts → UNKNOWN
            return RuleResult(
                rule_id=rule_id, module=module,
                status="UNKNOWN", severity="UNKNOWN",
                message=f"Cannot evaluate {rule_id}: required fact not confirmed. ({e})",
                detail={"expression": expression},
                judgment_tags=check.get("judgment_tags", [])
            )

        if result:  # expression evaluated to True → condition triggered
            # Resolve message template — use .format_map() with fact values
            try:
                message = check["message_template"].format_map(names)
            except KeyError as e:
                message = check["message_template"]  # use raw if template var missing

            return RuleResult(
                rule_id=rule_id, module=module,
                status=check["result_if_true"],   # "FAIL" in most cases
                severity=check["severity"],
                message=message,
                detail={"expression": expression, "evaluated_names": {
                    k: str(v) for k, v in names.items()
                }},
                judgment_tags=check.get("judgment_tags", [])
            )

    # Step 4: All checks passed
    try:
        pass_message = rule.get("pass_message_template", "Rule passed.").format_map(names)
    except KeyError:
        pass_message = "Rule passed."

    return RuleResult(
        rule_id=rule_id, module=module,
        status="PASS", severity=None,
        message=pass_message,
        detail={}, judgment_tags=[]
    )

def run_all_modules(
    confirmed_facts: dict,
    modules_to_run: list[str] | None = None
) -> list[RuleResult]:
    """
    Run specified compliance modules against confirmed case facts.
    If modules_to_run is None, runs M1-M9 (default — no M10).
    Pass modules_to_run=["M1"..."M9","M10"] for third party cases.
    """
    if modules_to_run is None:
        modules_to_run = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9"]

    all_rules = load_all_rules()
    results = []
    for rule in all_rules:
        if rule["module"] not in modules_to_run:
            continue
        result = evaluate_rule(rule, confirmed_facts)
        if result:
            results.append(result)
    return results
```

### 13.3 Message Template Resolution

**AI IDE instruction:** Message templates use Python's `.format_map()` with the confirmed
fact values dict as the map. Variable names in templates match exactly the field names in
the Case Fact Schema (Section 7). If a template variable is missing from confirmed facts,
the raw template string is used without raising an exception — use `format_map()` with a
`defaultdict` that returns the placeholder name itself.

```python
from collections import defaultdict

def safe_format(template: str, names: dict) -> str:
    """Format template, replacing missing vars with [UNKNOWN].
    FIXED v5.0: was defaultdict(lambda k=None: ...) — factory must take zero args.
    """
    safe_names = defaultdict(lambda: "[UNKNOWN]", names)
    try:
        return template.format_map(safe_names)
    except Exception:
        return template
```

---

## 14. Statute Compliance Engine — All 9 Modules

> v5.4: A 10th module, M10 (Third Party Rights), was added — see `m10_third_party.yaml`
> below. Kept the section heading as "9 Modules" to preserve the TOC anchor link.

Full YAML rules for each module. These files go in
`app/services/compliance/rules/`.

### m1_demand.yaml

```yaml
rules:
  - rule_id: M1_C1
    module: M1_DEMAND_NOTICE
    statutory_basis: "Section 13(2) SARFAESI Act 2002"
    description: "60 days must elapse between demand notice and enforcement action"
    preconditions:
      - field: demand_notice_date
        operator: is_not_null
    checks:
      - check_id: M1_C1_a
        description: "60-day period not elapsed"
        expression: "sixty_day_period_elapsed == False"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Enforcement action taken before 60-day period elapsed from demand notice dated {demand_notice_date}."
        judgment_tags: [s13_2_notice_period, procedural_compliance]
    pass_message_template: "60-day period from demand notice ({demand_notice_date}) satisfied."

  - rule_id: M1_C2
    module: M1_DEMAND_NOTICE
    description: "Amount in demand notice must match account records within 5% tolerance"
    preconditions:
      - field: demand_notice_amount
        operator: is_not_null
      - field: actual_outstanding_amount
        operator: is_not_null
    checks:
      - check_id: M1_C2_a
        description: "Amount discrepancy exceeds 5%"
        expression: "abs(demand_notice_amount - actual_outstanding_amount) / actual_outstanding_amount * 100 > 5"
        result_if_true: FAIL
        severity: CURABLE
        message_template: "Demand notice amount ({demand_notice_amount}) differs from records ({actual_outstanding_amount}) by more than 5%."
        judgment_tags: [amount_dispute, s13_2_accuracy]

  - rule_id: M1_C3
    module: M1_DEMAND_NOTICE
    description: "Service mode must be valid under SARFAESI Rules"
    checks:
      - check_id: M1_C3_a
        expression: "notice_service_mode not in ['registered_post_ad','personal_service','substituted_service','email_if_agreed']"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Notice service mode '{notice_service_mode}' is not a valid mode under SARFAESI Rules."
        judgment_tags: [service_defect, s13_2_service]

  - rule_id: M1_C4
    module: M1_DEMAND_NOTICE
    description: "Proof of service must be present in bank file"
    checks:
      - check_id: M1_C4_a
        expression: "notice_dispatch_proof_present == False"
        result_if_true: FAIL
        severity: FATAL
        message_template: "No proof of service (POD/acknowledgment/affidavit) found. Cannot verify notice was served."
        judgment_tags: [service_defect, proof_of_service]

  # NEW v5.0 — M1_C5: Service date must be on or after notice issue date (data consistency)
  - rule_id: M1_C5
    module: M1_DEMAND_NOTICE
    statutory_basis: "Section 13(2) SARFAESI Act 2002 — 60-day period runs from service, not issue"
    description: "Service date must not predate notice issue date — catches data entry errors"
    preconditions:
      - field: demand_notice_date
        operator: is_not_null
      - field: notice_service_date
        operator: is_not_null
    checks:
      - check_id: M1_C5_a
        description: "Service date before notice issue date — data entry error"
        expression: "notice_service_date < demand_notice_date"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Service date ({notice_service_date}) recorded before notice issue date ({demand_notice_date}). Data entry error — 60-day period computation will be wrong."
        judgment_tags: [s13_2_notice_period, service_date_computation]
    pass_message_template: "Service date ({notice_service_date}) on or after notice issue date ({demand_notice_date}). Correct date used for 60-day computation."

  # NEW v5.0 — M1_C6: Demand notice must contain all prescribed content elements
  - rule_id: M1_C6
    module: M1_DEMAND_NOTICE
    statutory_basis: "Section 13(2) SARFAESI Act 2002 — prescribed content of demand notice"
    description: "Demand notice must state: (1) outstanding amount, (2) secured asset details, (3) 60-day demand, (4) consequences of non-payment"
    preconditions:
      - field: demand_notice_date
        operator: is_not_null
    checks:
      - check_id: M1_C6_a
        description: "Notice content not confirmed as complete"
        expression: "notice_content_complete == False"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Demand notice does not appear to contain all 4 prescribed content elements required under Section 13(2). Notice may be defective on format. Ground: NOTICE_FORMAT_DEFECT."
        judgment_tags: [s13_2_notice_format, notice_format_defect]
    pass_message_template: "Demand notice content confirmed complete — all prescribed elements present."

  # NEW v5.0 — M1_C7: Enforcement action must not predate 60-day moratorium expiry
  - rule_id: M1_C7
    module: M1_DEMAND_NOTICE
    statutory_basis: "Section 13(2) SARFAESI Act 2002 — 60-day moratorium before Section 13(4)"
    description: "Possession notice must not be issued before 60 days from service date"
    preconditions:
      - field: notice_service_date
        operator: is_not_null
      - field: possession_notice_date
        operator: is_not_null
    checks:
      - check_id: M1_C7_a
        description: "Possession notice issued before 60-day moratorium expired"
        expression: "(possession_notice_date - notice_service_date).days < 60"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Possession notice dated {possession_notice_date} issued before 60-day moratorium expired from service on {notice_service_date}. Premature enforcement under Section 13(4) is a fatal defect."
        judgment_tags: [s13_2_notice_period, premature_enforcement]
    pass_message_template: "Possession notice issued after 60-day moratorium from service date ({notice_service_date})."

  # NEW v5.1 — M1_C8: Authorized Officer authorization
  - rule_id: M1_C8
    module: M1_DEMAND_NOTICE
    statutory_basis: "Authorized Officer Authorization"
    description: "AO must have written authorization from principal officer"
    preconditions:
      - field: authorized_officer_name
        operator: is_not_null
    checks:
      - check_id: M1_C8_a
        description: "AO does not have written authorization"
        expression: "ao_has_written_authorization == False"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Authorized Officer {authorized_officer_name} ({authorized_officer_designation}) lacks written authorization from the principal officer. Enforcement action is void."
        judgment_tags: [ao_authorization_missing]
    pass_message_template: "Authorized Officer {authorized_officer_name} has verified written authorization."
```

### m2_reply.yaml

```yaml
rules:
  - rule_id: M2_C1
    module: M2_REPLY_COMPLIANCE
    statutory_basis: "Section 13(3A) SARFAESI Act 2002"
    description: "Bank must reply to objection — reply not given"
    preconditions:
      - field: objection_filed
        operator: eq
        value: true
    checks:
      - check_id: M2_C1_a
        expression: "bank_reply_given == False"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Borrower filed objection on {objection_date}. Bank has not replied. Fatal under Kanaiyalal (2011) 2 SCC 782."
        judgment_tags: [s13_3a_reply, borrower_rights, fatal_defect]
    pass_message_template: "Bank replied on {bank_reply_date}."

  - rule_id: M2_C2
    module: M2_REPLY_COMPLIANCE
    description: "Bank reply must be within 15 days"
    preconditions:
      - field: objection_filed
        operator: eq
        value: true
      - field: bank_reply_given
        operator: eq
        value: true
    checks:
      - check_id: M2_C2_a
        expression: "reply_days_elapsed > 15"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Bank replied {reply_days_elapsed} days after objection. Exceeds 15-day limit by {reply_days_elapsed - 15} days."
        judgment_tags: [s13_3a_reply, late_reply]

  # NEW v5.1 — M2_C3: Bank Reply Reasoned
  - rule_id: M2_C3
    module: M2_REPLY_COMPLIANCE
    statutory_basis: "Reasoned Reply Requirement"
    description: "Bank reply must give reasons for rejecting the objection"
    preconditions:
      - field: bank_reply_given
        operator: eq
        value: true
    checks:
      - check_id: M2_C3_a
        description: "Bank reply does not give reasons"
        expression: "bank_reply_gives_reasons == False"
        result_if_true: FAIL
        severity: CURABLE
        message_template: "Bank reply is not reasoned. DRT may set aside notice or require proper reply depending on forum."
        judgment_tags: [s13_3a_reply_unreasoned]
    pass_message_template: "Bank provided a reasoned reply."
```

### m3_auction.yaml

```yaml
rules:
  - rule_id: M3_C1
    module: M3_AUCTION_GAP
    statutory_basis: "Rule 8(6) Security Interest (Enforcement) Rules 2002"
    description: "30-day gap required between sale notice and auction (immovable)"
    preconditions:
      - field: asset_type
        operator: eq
        value: immovable
    checks:
      - check_id: M3_C1_a
        expression: "auction_gap_days < 30"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Auction held {auction_gap_days} days after sale notice. Minimum required: 30 days."
        judgment_tags: [auction_gap, rule_8_6, sale_notice]

  - rule_id: M3_C2
    module: M3_AUCTION_GAP
    description: "Newspaper publication of sale notice required"
    checks:
      - check_id: M3_C2_a
        expression: "newspaper_publication_done == False"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Newspaper publication of sale notice not confirmed in bank records."
        judgment_tags: [auction_gap, newspaper_publication]

  # NEW v5.0 — M3_C3: Reserve price must be stated in sale notice
  - rule_id: M3_C3
    module: M3_AUCTION_GAP
    statutory_basis: "Rule 8(5) and 8(6) Security Interest (Enforcement) Rules 2002"
    description: "Sale notice must state the reserve price — which must be set from an approved valuer's report"
    preconditions:
      - field: sale_notice_date
        operator: is_not_null
    checks:
      - check_id: M3_C3_a
        description: "Reserve price absent from sale notice"
        expression: "reserve_price == None"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Sale notice does not state a reserve price. Rule 8(5) requires the authorised officer to fix reserve price from an approved valuer's report before issuing the sale notice. Auction is procedurally defective."
        judgment_tags: [auction_gap, rule_8_5, reserve_price_missing]
    pass_message_template: "Reserve price ({reserve_price}) stated in sale notice as required by Rule 8(5)."

  # NEW v5.0 — M3_C4: Possession must precede sale notice
  - rule_id: M3_C4
    module: M3_AUCTION_GAP
    statutory_basis: "Rule 8 Security Interest (Enforcement) Rules 2002 — possession before sale"
    description: "Sale notice must not be issued before possession notice — bank cannot auction before taking possession"
    preconditions:
      - field: possession_notice_date
        operator: is_not_null
      - field: sale_notice_date
        operator: is_not_null
    checks:
      - check_id: M3_C4_a
        description: "Sale notice predates possession notice"
        expression: "sale_notice_date < possession_notice_date"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Sale notice dated {sale_notice_date} predates possession notice dated {possession_notice_date}. Bank cannot issue a sale notice before taking possession of the secured asset. Fatal procedural defect under Rule 8."
        judgment_tags: [auction_gap, possession_before_sale, rule_8]
    pass_message_template: "Sale notice ({sale_notice_date}) correctly issued after possession notice ({possession_notice_date})."

  # NEW v5.4 — M3_C6: Auction notice not affixed at property
  # Authority: Rule 8(6)(7), SI Enforcement Rules 2002
  # SC: Mathew Varghese v. M. Amritha Kumar (2014) 5 SCC 610
  # SC: Vasu P. Shetty v. Hotel Vandana Palace (2014) 6 SCC 660
  - rule_id: M3_C6
    module: M3_AUCTION_GAP
    statutory_basis: "Rule 8(6)(7) Security Interest (Enforcement) Rules 2002"
    description: "Auction/sale notice must be affixed at a conspicuous part of the secured property"
    preconditions:
      - field: auction_date
        operator: is_not_null
      - field: auction_notice_affixed_on_property
        operator: is_not_null
    checks:
      - check_id: M3_C6_a
        description: "Auction notice not affixed at property"
        expression: "auction_notice_affixed_on_property == False"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Rule 8(6)(7) of Security Interest (Enforcement) Rules 2002 violated. The bank did not affix the auction/sale notice at a conspicuous part of the secured property before conducting the auction on {auction_date}. The Supreme Court in Mathew Varghese v. M. Amritha Kumar (2014) 5 SCC 610 held that non-compliance with mandatory affixing requirement renders the sale null and void."
        judgment_tags: [mathew_varghese, vasu_shetty, rule_8_6_7, notice_affixing]
        ground_codes: [AUCTION_NOTICE_AFFIXING]
    pass_message_template: "Auction notice was affixed at the secured property prior to auction on {auction_date}, as required by Rule 8(6)(7)."

  # NEW v5.4 — M3_C7: Auction conducted during court/DRT stay — ABSOLUTE_BAR
  # Authority: Section 17(4) SARFAESI Act — DRT power to grant stay
  # SC: Celir LLP v. Bafna Motors (2023) 13 SCC 561
  - rule_id: M3_C7
    module: M3_AUCTION_GAP
    statutory_basis: "Section 17(4) SARFAESI Act 2002"
    description: "Auction must not be conducted while a DRT/court interim stay is operational"
    preconditions:
      - field: auction_conducted_despite_stay
        operator: is_not_null
      - field: stay_was_operational_on_auction_date
        operator: is_not_null
    checks:
      - check_id: M3_C7_a
        description: "Auction conducted in defiance of an operational stay"
        expression: "auction_conducted_despite_stay == True and stay_was_operational_on_auction_date == True"
        result_if_true: FAIL
        severity: ABSOLUTE_BAR
        message_template: "Auction was conducted on {auction_date} in express defiance of a DRT/court interim stay order passed on {drt_stay_order_date} under Section 17(4) of the SARFAESI Act. Conducting an auction in contempt of a court order is not a procedural defect — it is a jurisdictional violation that cannot be cured. The sale certificate dated {sale_certificate_date} is prima facie void. Celir LLP v. Bafna Motors (2023) 13 SCC 561 affirms that fundamental procedural errors and fraud ground setting aside of a confirmed sale."
        judgment_tags: [celir_llp_bafna_motors, auction_during_stay, section_17_4]
        ground_codes: [AUCTION_DURING_STAY]
    pass_message_template: "No evidence that the auction on {auction_date} was conducted during an operational stay."

  # NEW v5.4 — M3_C8: Pending litigation concealed from auction notice
  # Authority: Rule 8(6)(7)(a), SI Enforcement Rules 2002
  # HC: Rakesh Kumar Kaushal v. State of UP (Allahabad HC)
  # HC: M. Rajendran v. Corporation Bank, Villupuram (Madras HC)
  - rule_id: M3_C8
    module: M3_AUCTION_GAP
    statutory_basis: "Rule 8(6)(7)(a) Security Interest (Enforcement) Rules 2002"
    description: "Bank must disclose pending litigation known to it in the auction notice"
    preconditions:
      - field: pending_sa_existed_at_auction_date
        operator: is_not_null
      - field: auction_notice_discloses_pending_sa
        operator: is_not_null
    checks:
      - check_id: M3_C8_a
        description: "Pending SA existed but was not disclosed in auction notice"
        expression: "pending_sa_existed_at_auction_date == True and auction_notice_discloses_pending_sa == False"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Securitisation Application {previous_sa_number} was pending before DRT-I on the date of auction ({auction_date}). Rule 8(6)(7)(a) requires the bank to disclose all encumbrances KNOWN to it in the auction notice, which includes pending litigation. The bank failed to disclose the pending SA and any interim orders — material concealment that vitiates the auction process."
        judgment_tags: [rakesh_kumar_kaushal, pending_litigation_concealed, rule_8_6_7_a]
        ground_codes: [PENDING_SA_CONCEALED, AUCTION_NOTICE_AFFIXING]
    pass_message_template: "Auction notice disclosed pending litigation ({previous_sa_number}) as required by Rule 8(6)(7)(a)."
```

### m4_limitation.yaml

```yaml
rules:
  - rule_id: M4_C1
    module: M4_LIMITATION
    statutory_basis: "Section 17(1) SARFAESI Act 2002"
    description: "SA must be filed within 45 days of challenged measure"
    checks:
      - check_id: M4_C1_a
        expression: "days_from_measure_to_sa > 45"
        result_if_true: FAIL
        severity: ABSOLUTE_BAR
        message_template: "SA filed {days_from_measure_to_sa} days after measure dated {measure_date}. 45-day limit exceeded. Application is time-barred."
        judgment_tags: [limitation, s17_time_bar]

  - rule_id: M4_C2
    module: M4_LIMITATION
    description: "Measure type must be identified to calculate limitation"
    checks:
      - check_id: M4_C2_a
        expression: "measure_type == None"
        result_if_true: UNKNOWN
        severity: REVIEW_REQUIRED
        message_template: "The specific measure challenged by the SA cannot be determined. Review SA paragraph 1."
        judgment_tags: [limitation]

  # NEW v5.0 — M4_C3: Limitation for auction challenge runs from auction date independently
  - rule_id: M4_C3
    module: M4_LIMITATION
    statutory_basis: "Section 17(1) SARFAESI Act 2002 — each measure has independent 45-day window"
    description: "Where the SA challenges the auction itself, 45-day limitation runs from auction date independently of challenge to earlier measures"
    preconditions:
      - field: auction_date
        operator: is_not_null
      - field: sa_filing_date
        operator: is_not_null
    checks:
      - check_id: M4_C3_a
        description: "SA filed more than 45 days after auction"
        expression: "(sa_filing_date - auction_date).days > 45"
        result_if_true: FAIL
        severity: ABSOLUTE_BAR
        message_template: "SA filed {days_from_measure_to_sa} days after auction on {auction_date}. Any challenge specifically to the auction is time-barred even if challenge to earlier measures (possession) is within time."
        judgment_tags: [limitation, s17_time_bar, auction_challenge]
    pass_message_template: "SA filed within 45 days of auction date ({auction_date}). Challenge to auction is within time."

  # NEW v5.4 — M4_C5: Prayer scope mismatch (Oasis Dealcom)
  - rule_id: M4_C5
    module: M4_LIMITATION
    statutory_basis: "ACT"
    description: "DRT cannot set aside a measure not prayed against — auction completed but prayer does not cover it"
    preconditions:
      - field: auction_date
        operator: is_not_null
      - field: challenges_auction
        operator: is_not_null
    checks:
      - check_id: M4_C5_a
        expression: "challenges_auction == False and challenges_demand_notice == True"
        result_if_true: FAIL
        severity: ADVISORY
        message_template: "Prayer scope mismatch: auction already conducted on {auction_date} but SA prayer does not include SET_ASIDE_AUCTION or SET_ASIDE_SALE_CERTIFICATE. DRT cannot set aside a measure not prayed against. Applicant may need to amend prayer or file fresh SA under Oasis Dealcom principle (2016 SC)."
        judgment_tags: [oasis_dealcom, prayer_scope_mismatch]
        ground_codes: [SECOND_SA_FRESH_CAUSE]
    pass_message_template: "Prayer scope covers the current enforcement measure ({auction_date})."
```

### m5_tenancy.yaml

```yaml
rules:
  - rule_id: M5_C1
    module: M5_TENANCY
    statutory_basis: "Section 17(1)(d) SARFAESI + Transfer of Property Act"
    description: "Lease after mortgage cannot defeat enforcement"
    preconditions:
      - field: tenancy_claimed
        operator: eq
        value: true
    checks:
      - check_id: M5_C1_a
        expression: "lease_predates_mortgage == False"
        result_if_true: PASS  # FIXED v5.0: PASS_FAVORABLE not in DB check constraint
        severity: ADVISORY
        message_template: "Lease ({lease_date}) is after mortgage ({mortgage_date}). Cannot defeat bank under ITC v. Blue Coast (2018) 15 SCC 99."
        judgment_tags: [tenancy, post_mortgage_lease]

  - rule_id: M5_C2
    module: M5_TENANCY
    description: "Lease after demand notice is expressly excluded"
    preconditions:
      - field: tenancy_claimed
        operator: eq
        value: true
    checks:
      - check_id: M5_C2_a
        expression: "lease_post_default_notice == True"
        result_if_true: PASS  # FIXED v5.0: PASS_FAVORABLE not in DB check constraint
        severity: ADVISORY
        message_template: "Lease ({lease_date}) was created after demand notice ({demand_notice_date}). Section 17(1)(d) expressly excludes such leases."
        judgment_tags: [tenancy, post_notice_lease]

  - rule_id: M5_C3
    module: M5_TENANCY
    description: "Unregistered lease > 1 year is invalid"
    preconditions:
      - field: tenancy_claimed
        operator: eq
        value: true
    checks:
      - check_id: M5_C3_a
        expression: "lease_registered == False and lease_duration_months > 12"
        result_if_true: PASS  # FIXED v5.0: PASS_FAVORABLE not in DB check constraint
        severity: ADVISORY
        message_template: "BANK FAVORABLE: Claimed lease of {lease_duration_months} months is unregistered. Unregistered leases > 1 year have no validity under Section 107 Transfer of Property Act."
        judgment_tags: [tenancy, lease_registration, bank_favorable]

  # NEW v5.0 — M5_C4: Registered pre-mortgage lease — strongest tenancy defence
  - rule_id: M5_C4
    module: M5_TENANCY
    statutory_basis: "Transfer of Property Act Sections 105–111 + Section 17(1) SARFAESI"
    description: "Registered lease predating mortgage — this is the strongest tenancy defence; requires full legal review before proceeding"
    preconditions:
      - field: tenancy_claimed
        operator: eq
        value: true
    checks:
      - check_id: M5_C4_a
        description: "Registered pre-mortgage lease — borrower strong ground"
        expression: "lease_predates_mortgage == True and lease_registered == True"
        result_if_true: FAIL
        severity: REVIEW_REQUIRED
        message_template: "BORROWER STRONG GROUND: Registered lease dated {lease_date} predates mortgage dated {mortgage_date}. This is the strongest tenancy defence available under TPA. DRT will likely scrutinise enforcement. Do not proceed without full legal review."
        judgment_tags: [tenancy, pre_mortgage_registered_lease, borrower_strong_ground]
    pass_message_template: "No registered pre-mortgage lease detected. Tenancy claim assessed."
```

### m6_valuation.yaml

```yaml
rules:
  - rule_id: M6_C1
    module: M6_VALUATION
    statutory_basis: "Rule 8(6) Security Interest (Enforcement) Rules 2002"
    description: "Valuer must be RBI-empanelled and registered under Registered Valuers Act 2017"
    preconditions:
      - field: valuation_report_present
        operator: eq
        value: true
    checks:
      - check_id: M6_C1_a
        expression: "valuer_rbi_empanelled == False or valuer_registered_under_rvact == False"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Valuer '{valuer_name}' does not appear to be RBI-empanelled or registered under RVA 2017. Valuation legally defective."
        judgment_tags: [valuation_defect, rule_8_6]

  - rule_id: M6_C2
    module: M6_VALUATION
    description: "Valuation report must not be more than 6 months old at auction"
    checks:
      - check_id: M6_C2_a
        expression: "valuation_age_at_auction_days > 180"
        result_if_true: FAIL
        severity: CURABLE
        message_template: "Valuation report ({valuation_date}) is {valuation_age_at_auction_days} days old at auction. Exceeds 180-day guideline."
        judgment_tags: [valuation_defect, stale_valuation]

  - rule_id: M6_C3
    module: M6_VALUATION
    description: "Reserve price not to fall below 75% of valuation without second valuation"
    checks:
      - check_id: M6_C3_a
        expression: "reserve_price_vs_valuation_pct < 75"
        result_if_true: FAIL
        severity: CURABLE
        message_template: "Reserve price is {reserve_price_vs_valuation_pct:.1f}% of valuation. Significantly below valuation. Borrower may allege undervaluation."
        judgment_tags: [valuation_dispute, undervaluation]

  # NEW v5.0 — M6_C4: Valuation report must predate sale notice
  - rule_id: M6_C4
    module: M6_VALUATION
    statutory_basis: "Rule 8(5) Security Interest (Enforcement) Rules 2002 — reserve price set from pre-existing valuation"
    description: "Valuation must be obtained before the sale notice is issued — reserve price derives from valuation"
    preconditions:
      - field: valuation_date
        operator: is_not_null
      - field: sale_notice_date
        operator: is_not_null
    checks:
      - check_id: M6_C4_a
        description: "Sale notice issued before or on same date as valuation report"
        expression: "sale_notice_date <= valuation_date"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Sale notice dated {sale_notice_date} issued on or before valuation report dated {valuation_date}. Reserve price cannot be derived from a valuation that did not yet exist. Sequence of steps under Rule 8(5) violated."
        judgment_tags: [valuation_defect, rule_8_5, valuation_sequence]
    pass_message_template: "Valuation report ({valuation_date}) correctly obtained before sale notice ({sale_notice_date})."
```

### m7_multiparty.yaml

```yaml
rules:
  - rule_id: M7_C1
    module: M7_MULTIPARTY_NOTICE
    statutory_basis: "Section 13(2) SARFAESI — notice to all borrowers"
    description: "All co-borrowers must be individually served"
    checks:
      - check_id: M7_C1_a
        expression: "borrowers_served_notice < total_borrowers_in_loan"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Loan has {total_borrowers_in_loan} borrowers. Notice served on only {borrowers_served_notice}. Each unserved borrower is a separate fatal defect."
        judgment_tags: [service_defect, co_borrower_notice]

  - rule_id: M7_C2
    module: M7_MULTIPARTY_NOTICE
    description: "All guarantors/mortgagors must be individually served"
    checks:
      - check_id: M7_C2_a
        expression: "guarantors_served_notice < total_guarantors_in_loan"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Loan has {total_guarantors_in_loan} guarantors. Notice served on only {guarantors_served_notice}."
        judgment_tags: [service_defect, guarantor_notice]
```

### m8_npa.yaml

```yaml
rules:
  - rule_id: M8_C1
    module: M8_NPA_CLASSIFICATION
    statutory_basis: "RBI Master Circular on Prudential Norms — Income Recognition, Asset Classification"
    description: "Account can only be NPA after 90 days of default"
    checks:
      - check_id: M8_C1_a
        expression: "days_from_last_payment_to_npa < 90"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Account classified NPA on {npa_classification_date}, only {days_from_last_payment_to_npa} days after last payment. RBI requires 90-day window."
        judgment_tags: [npa_classification, premature_npa]

  - rule_id: M8_C2
    module: M8_NPA_CLASSIFICATION
    description: "Cannot classify NPA when approved restructuring is active"
    preconditions:
      - field: restructuring_proposal_pending
        operator: eq
        value: true
    checks:
      - check_id: M8_C2_a
        expression: "restructuring_approval_date == None or npa_classification_date <= restructuring_approval_date"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Account classified NPA while restructuring proposal was pending/active. Impermissible."
        judgment_tags: [npa_classification, restructuring_active]

  - rule_id: M8_C3
    module: M8_NPA_CLASSIFICATION
    description: "Borrower should be notified of NPA classification"
    checks:
      - check_id: M8_C3_a
        expression: "classification_notice_given == False"
        result_if_true: FAIL
        severity: ADVISORY
        message_template: "No record of NPA classification notice to borrower. Advisory — not statutory, but some HCs have held it as fair procedure."
        judgment_tags: [npa_classification, natural_justice]

  # NEW v5.0 — M8_C4: No compound interest permitted on NPA accounts
  - rule_id: M8_C4
    module: M8_NPA_CLASSIFICATION
    statutory_basis: "RBI IRAC Master Circular 2025-26 — income recognition on NPA accounts"
    description: "Interest charged post-NPA must be simple interest only — compound interest (interest on interest) is not permitted and inflates the demand notice amount"
    checks:
      - check_id: M8_C4_a
        description: "Interest application on NPA account flagged as incorrect"
        expression: "interest_application_correct == False"
        result_if_true: FAIL
        severity: CURABLE
        message_template: "Interest application post-NPA classification appears incorrect. RBI IRAC norms prohibit compound interest on NPA accounts. If compound interest was charged, demand notice amount is overstated — notice may be defective on amount. Ground: AMOUNT_DISPUTE."
        judgment_tags: [npa_classification, compound_interest, amount_dispute]
    pass_message_template: "Interest application on NPA account confirmed correct (simple interest only)."

  # NEW v5.4 — M8_C6: Account upgraded to Standard before auction
  # Authority: RBI IRAC Master Circular, Clause 4.2.5 (2014-15)
  # HC: Sravan Dall Mill P. Ltd. v. Central Bank (Allahabad HC)
  # HC: Oswal Spinning & Weaving Mills v. RBI (Punjab & Haryana HC)
  # Principle: Once NPA is not always NPA.
  - rule_id: M8_C6
    module: M8_NPA_CLASSIFICATION
    statutory_basis: "RBI IRAC Master Circular Clause 4.2.5"
    description: "Account no longer NPA at auction date — jurisdictional fact under Section 13(2) not satisfied"
    preconditions:
      - field: account_standard_at_auction_date
        operator: is_not_null
      - field: auction_date
        operator: is_not_null
    checks:
      - check_id: M8_C6_a
        expression: "account_standard_at_auction_date == True"
        result_if_true: FAIL
        severity: FATAL
        message_template: "Payments made after NPA classification (total Rs. {payments_post_npa_total}) were sufficient to cover the overdue amount of Rs. {overdue_amount_at_auction_date} as of the auction date {auction_date}. Under RBI IRAC Master Circular clause 4.2.5, when arrears of interest and principal are paid, the account should be reclassified as Standard. A bank cannot auction a property when the loan account is no longer NPA — the jurisdictional fact under Section 13(2) (the account being NPA) is no longer satisfied at the time of the sale."
        judgment_tags: [sravan_dall_mill, oswal_spinning, npa_upgradation]
        ground_codes: [NPA_PREMATURE]
    pass_message_template: "Account remained NPA as of the auction date ({auction_date})."
```

### m9_msme.yaml

```yaml
rules:
  - rule_id: M9_C1
    module: M9_MSME
    statutory_basis: "RBI MSME Restructuring Circular (Feb 2018 + Aug 2020)"
    description: "MSME status must be confirmed from bank file before M9 runs"
    preconditions:
      - field: msme_claimed_by_borrower
        operator: eq
        value: true
    checks:
      - check_id: M9_C1_a
        expression: "udyam_cert_in_bank_file == False"
        result_if_true: UNKNOWN
        severity: REVIEW_REQUIRED
        message_template: "Borrower claims MSME status. No Udyam Certificate in bank file. Human confirmation required: check original credit file."
        judgment_tags: [msme_restructuring]

  - rule_id: M9_C2
    module: M9_MSME
    description: "Restructuring must have been offered to MSME before NPA classification"
    preconditions:
      - field: udyam_cert_in_bank_file
        operator: eq
        value: true
    checks:
      - check_id: M9_C2_a
        expression: "restructuring_offered_pre_npa == False"
        result_if_true: FAIL
        severity: CURABLE
        message_template: "Borrower is MSME (Udyam: {udyam_registration_number}). Restructuring not offered before NPA classification. Applicable circular: {applicable_rbi_circular}."
        judgment_tags: [msme_restructuring, rbi_circular_msme]
```

### m10_third_party.yaml (NEW v5.4 — Third Party Rights Module)

> This module activates when `sa_applicant_type` is not BORROWER/GUARANTOR.
> It analyses the third party's standing and the strength of their claim
> against the bank's enforcement. M1-M9 still run for procedural grounds
> but M10 provides the primary legal framework for the third party claim.
>
> KEY CASE: Celir LLP v. Bafna Motors (2023) 13 SCC 561
> KEY CASE: Harshad Govardhan Sondagar (2014) 6 SCC 1 (pre-mortgage ATS)
> KEY CASE: ITC v. Blue Coast Hotels (2018) 15 SCC 99 (post-mortgage lease)
> KEY CASE: Oasis Dealcom v. Khazana Dealcomm (2016) 10 SCC 214 (second SA)
> KEY LAW:  TPA 1882 Sections 52, 54, 58, 60

```yaml
rules:
  # M10_C1 — ATS Holder Standing Under Section 17
  # Threshold question: can a non-borrower file an SA at all?
  # Courts are split — some allow, some deny — flag as ADVISORY.
  - rule_id: M10_C1
    module: M10_THIRD_PARTY
    statutory_basis: "ACT"
    description: "SA applicant is a third party ATS holder — standing under Section 17 is contested"
    preconditions:
      - field: sa_applicant_type
        operator: eq
        value: "THIRD_PARTY_ATS"
    checks:
      - check_id: M10_C1_a
        expression: "sa_applicant_type == 'THIRD_PARTY_ATS'"
        result_if_true: REVIEW
        severity: ADVISORY
        message_template: "SA applicant is a third party holding an Agreement to Sell — not the borrower or guarantor. Standing under Section 17 of the SARFAESI Act is contested for ATS holders. Some High Courts have allowed such SAs (Delhi HC, Madras HC) on the basis that the applicant is a person aggrieved by the measures. Other benches have denied standing. DRT will determine standing as a preliminary issue. Bank should prepare to contest maintainability."
        judgment_tags: [celir_llp_bafna_motors, ats_standing]
        ground_codes: [THIRD_PARTY_ATS]

  # M10_C2 — ATS Simultaneous With Mortgage (Fraud Risk)
  - rule_id: M10_C2
    module: M10_THIRD_PARTY
    statutory_basis: "BOTH"
    description: "ATS and mortgage executed same date — strong bank fraud defense"
    preconditions:
      - field: sa_applicant_type
        operator: eq
        value: "THIRD_PARTY_ATS"
      - field: ats_simultaneous_mortgage
        operator: eq
        value: true
    checks:
      - check_id: M10_C2_a
        expression: "ats_simultaneous_mortgage == True"
        result_if_true: FAIL
        severity: HIGH
        message_template: "Agreement to Sell (ATS) and mortgage deed executed on the same date ({ats_date} = {mortgage_date}). Bank will allege that the ATS was executed with knowledge of the mortgage and in collusion with the borrower to defeat the bank's security interest. The ATS holder cannot claim ignorance of the mortgage when both were executed simultaneously. This significantly weakens the third party's claim."
        judgment_tags: [ats_mortgage_collusion]
        ground_codes: [THIRD_PARTY_ATS]

  # M10_C3 — ATS Holder Paid Substantial Consideration (mitigating factor)
  - rule_id: M10_C3
    module: M10_THIRD_PARTY
    statutory_basis: "BOTH"
    description: "ATS holder paid substantial consideration directly to loan account — mitigates fraud allegation"
    preconditions:
      - field: sa_applicant_type
        operator: eq
        value: "THIRD_PARTY_ATS"
      - field: ats_payments_made_to_loan_account
        operator: eq
        value: true
    checks:
      - check_id: M10_C3_a
        expression: "ats_payments_made_to_loan_account == True"
        result_if_true: PASS
        severity: ADVISORY
        message_template: "ATS holder has made payments of Rs. {ats_payments_total} directly to the bank's loan account (total paid: Rs. {ats_advance_paid}). This demonstrates bona fide conduct and good faith. Courts have treated payment by the ATS holder into the loan account as evidence that the bank had knowledge of the arrangement and implicitly accepted the ATS holder as a de facto party to the loan servicing. This substantially mitigates the bank's fraud allegation under M10_C2."
        judgment_tags: [celir_llp_bafna_motors, ats_bona_fide_payment]
        ground_codes: [THIRD_PARTY_ATS]

  # M10_C4 — Auction Purchaser: Sale Certificate Already Issued + Possession Given
  - rule_id: M10_C4
    module: M10_THIRD_PARTY
    statutory_basis: "BOTH"
    description: "Sale confirmed and possession given — Celir LLP high threshold to set aside applies"
    preconditions:
      - field: sale_certificate_issued
        operator: eq
        value: true
      - field: possession_given_to_auction_purchaser
        operator: eq
        value: true
    checks:
      - check_id: M10_C4_a
        expression: "sale_certificate_issued == True and possession_given_to_auction_purchaser == True"
        result_if_true: REVIEW
        severity: HIGH
        message_template: "Sale certificate issued on {sale_certificate_date} and physical possession given to auction purchaser. The Supreme Court in Celir LLP v. Bafna Motors (2023) 13 SCC 561 held that once a sale is confirmed and possession given, the borrower's right of redemption under TPA Section 60 is extinguished. To set aside the sale at this stage requires: (1) fundamental procedural error in the auction itself, OR (2) the sale was obtained by fraud or misrepresentation. The standard for setting aside rises significantly after physical possession. Check rules M3_C6 (notice affixing), M3_C7 (auction during stay), and M3_C8 (concealment) — if any of these fire, the fundamental procedural error threshold may be met."
        judgment_tags: [celir_llp_bafna_motors, confirmed_sale_high_threshold]
        ground_codes: [AUCTION_PURCHASER, RIGHT_OF_REDEMPTION]

  # M10_C5 — Sale Confirmed But Pre-Possession (lower threshold)
  - rule_id: M10_C5
    module: M10_THIRD_PARTY
    statutory_basis: "BOTH"
    description: "Sale certificate issued but possession not yet given — right of redemption window may remain open"
    preconditions:
      - field: sale_certificate_issued
        operator: eq
        value: true
      - field: possession_given_to_auction_purchaser
        operator: eq
        value: false
    checks:
      - check_id: M10_C5_a
        expression: "sale_certificate_issued == True and possession_given_to_auction_purchaser == False"
        result_if_true: REVIEW
        severity: CURABLE
        message_template: "Sale certificate issued but physical possession not yet given to auction purchaser. The right of redemption under TPA Section 60 may not yet be fully extinguished at this stage. The borrower/applicant has a window to challenge the sale through DRT before possession is handed over. Procedural defects (M3_C6, M3_C7, M3_C8) if present are more readily actionable at this stage than post-possession."
        judgment_tags: [celir_llp_bafna_motors, pre_possession_redemption_window]
        ground_codes: [RIGHT_OF_REDEMPTION, AUCTION_PURCHASER]

  # M10_C6 — Second SA: Different Cause of Action (Oasis Dealcom)
  - rule_id: M10_C6
    module: M10_THIRD_PARTY
    statutory_basis: "ACT"
    description: "Second SA maintainable where cause of action differs from first SA"
    preconditions:
      - field: previous_sa_filed
        operator: eq
        value: true
      - field: challenges_auction
        operator: eq
        value: true
    checks:
      - check_id: M10_C6_a
        expression: "previous_sa_filed == True and challenges_auction == True and challenges_demand_notice == False"
        result_if_true: PASS
        severity: ADVISORY
        message_template: "A previous SA ({previous_sa_number}) was filed by the same applicant. The present SA challenges the auction and/or sale certificate — a distinct cause of action from the original SA's challenge. The Supreme Court in Oasis Dealcom Pvt. Ltd. v. Khazana Dealcomm (2016) 10 SCC 214 held that a second SA is maintainable under Section 17 where the cause of action is different. The fresh auction constitutes a fresh cause of action. Bank may contest maintainability but the Oasis Dealcom principle should be cited in rebuttal."
        judgment_tags: [oasis_dealcom, second_sa_fresh_cause]
        ground_codes: [SECOND_SA_FRESH_CAUSE]
```

### m_cross.yaml (Cross-Module Rules)

```yaml
rules:
  # NEW v5.1 — M_CROSS_1: Logically Contradictory Grounds
  - rule_id: M_CROSS_1
    module: CROSS_MODULE
    statutory_basis: "Logical Consistency Check"
    description: "Detect contradictory SA grounds"
    preconditions: []
    checks:
      - check_id: M_CROSS_1_a
        description: "Contradictory grounds raised"
        expression: "SERVICE_DEFECT_raised and LIMITATION_EXPIRED_not_flagged and measure_type == 'demand_notice'"
        result_if_true: FAIL
        severity: ADVISORY
        message_template: "INTERNAL CONTRADICTION: Borrower alleges non-service of demand notice while basing limitation argument on that notice's date."
        judgment_tags: [contradictory_pleadings]
```
---

## 15. Judgment Intelligence Engine

### 15.0 Knowledge Base — Hybrid Wiki + Qdrant Architecture (v5.3)

#### What Goes Where

| Content | Where | Why |
|---|---|---|
| SARFAESI Act key sections | `sarfaesi_law_wiki.md` | Loaded into Chain A context always — never retrieved |
| Security Interest Rules | `sarfaesi_law_wiki.md` | Same — extraction needs full framework present |
| RBI IRAC + MSME circulars | `sarfaesi_law_wiki.md` | Same |
| 75 Class A judgment summaries | `class_a_judgments_wiki.md` | Loaded into Chain B context always |
| 7,500 Class B judgment summaries | Qdrant `sarfaesi_judgments` | Too large for context — statistics + retrieval only |

#### Two Build Scripts (run offline)
```bash
python scripts/build_law_wiki.py        # builds sarfaesi_law_wiki.md
python scripts/compile_class_a_wiki.py  # compiles 75 .md files → class_a_judgments_wiki.md
```
- Rebuild class_a wiki whenever a judgment .md file is updated.
- Rebuild law wiki whenever RBI issues a new relevant circular.

#### `STATUTE_ORDER` — build_law_wiki.py (v5.4 addition: TPA sections)

`scripts/build_law_wiki.py` concatenates statute source files in this order:

```python
STATUTE_ORDER = [
    ("SARFAESI_ACT",    "SARFAESI Act 2002 — Full Relevant Sections",
     "sarfaesi_act.txt"),
    ("SI_RULES",        "Security Interest (Enforcement) Rules 2002 — Complete",
     "si_enforcement_rules.txt"),
    ("RDDBFI_ACT",      "RDDBFI Act 1993 — DRT and DRAT Jurisdiction",
     "rddbfi_drt_sections.txt"),
    ("RBI_IRAC",        "RBI IRAC Master Circular 2025-26 — NPA Classification",
     "rbi_irac_circular.txt"),
    ("RBI_MSME",        "RBI MSME Restructuring Circulars",
     "rbi_msme_circular.txt"),
    ("TPA_SARFAESI",    "Transfer of Property Act 1882 — SARFAESI-Relevant Sections",
     "tpa_sarfaesi_sections.txt"),   # NEW v5.4
]
```

`docs/statutes/tpa_sarfaesi_sections.txt` (new file, to be sourced verbatim from
indiacode.nic.in — see Post-Completion Steps) must cover TPA Sections 52 (lis pendens),
54 (sale/agreement to sell), 58 (mortgage types), 60 (right of redemption), 65-A
(mortgage by deposit of title deeds), and 107 (leases how made) — each annotated with
its SARFAESI significance for M10 and M3 rule interpretation.

> IMPORTANT: Section 14 of the SARFAESI Act (in `sarfaesi_act.txt`) must include the
> full text of the CMM's duty to verify that the secured creditor has disclosed:
> (a) the amount due, (b) security description, (c) that there is no other pending
> litigation regarding the security. This duty underlies rule M3_C8 (pending litigation
> concealment).

### 15.0.1 Judgment Summary Architecture

#### What a Good Summary Contains

The `holding_summary` field drives the Qdrant embedding for each judgment.
Its quality directly determines retrieval quality. A bad summary means a bad embedding,
which can surface the wrong judgment and distort ground strength scoring.

**Target length:** 120-200 words. 4-6 sentences.
**Target structure:**

Sentence 1: What procedural ground was raised and by which party
Sentence 2: The specific facts relevant to that ground
Sentence 3-4: What the court held and the exact statutory basis
Sentence 5: The specific factual condition required for this holding to apply
Sentence 6 (optional): What this means for bank vs borrower

**Example of a correct summary (IDBI v. Rajiv Ranjan Rao, DRAT 2026):**
"Bank appealed DRAT order setting aside SARFAESI possession and sale actions.
The demand notice under Section 13(2) did not mention the NPA date, but the
tribunal found this omission did not cause prejudice to the borrower. However,
the bank failed to serve the possession notice under Rule 8(1) and (2) on all
borrowers — no evidence of service existed in the record, and the notice was
not filed before the tribunal. Additionally, the bank did not comply with
Rule 4(2) and 4(2-A) regarding post-possession intimation. The tribunal held
these procedural lapses justified setting aside the possession and physical
possession actions. Applies when: possession notice was not served on all
borrowers and the bank cannot produce service evidence."

### 15.0.2 Class A Judgment Priority List — v5.4 Additions

The following 7 judgments must be added as Class A `.md` files in `docs/judgments/`
before Phase H7. Each unlocks critical module functionality.

**Priority 1 (M3 — Auction Defects — Blocks M3_C6 and M3_C7)**

1. **Celir LLP v. Bafna Motors (2023) 13 SCC 561** — `docs/judgments/celir_llp_bafna_motors.md`
   Court: SUPREME_COURT | Bench: 2 | Favor: BANK
   Ground codes: AUCTION_PURCHASER, RIGHT_OF_REDEMPTION, AUCTION_DURING_STAY
   Key holding: Once sale confirmed + possession given → right of redemption
   extinguished. Setting aside requires fundamental procedural error or fraud.
   Auction during court stay = fundamental error. Affirms Mathew Varghese.
   Applicable conditions: `sale_certificate_issued=True`, `challenges_auction=True`

2. **Mathew Varghese v. M. Amritha Kumar (2014) 5 SCC 610** — `docs/judgments/mathew_varghese.md`
   Court: SUPREME_COURT | Bench: 3 | Favor: BORROWER
   Ground codes: AUCTION_NOTICE_AFFIXING, AUCTION_GAP_DEFECT
   Key holding: Rule 8 is mandatory. Clear 30-day notice to borrower is
   non-negotiable. Once auction fails on the scheduled date and the failure is
   not solely attributable to the borrower, a fresh notice is required.
   Applicable conditions: `auction_notice_affixed_on_property=False`

3. **Vasu P. Shetty v. Hotel Vandana Palace Ors (2014) 6 SCC 660** — `docs/judgments/vasu_shetty.md`
   Court: SUPREME_COURT | Bench: 2 | Favor: BORROWER
   Ground codes: AUCTION_NOTICE_AFFIXING, AUCTION_GAP_DEFECT
   Key holding: Follows and affirms Mathew Varghese. Rule 8(5) and (6) are
   mandatory — breach renders sale null and void. Sub-rule (7) on affixing
   notice at property is part of the mandatory framework.
   Applicable conditions: `auction_notice_affixed_on_property=False`

**Priority 2 (M10 — Third Party Rights)**

4. **Harshad Govardhan Sondagar v. International Assets (2014) 6 SCC 1** — `docs/judgments/harshad_sondagar.md`
   Court: SUPREME_COURT | Bench: 3 | Favor: BORROWER/TENANT
   Ground codes: TENANCY_CLAIM, THIRD_PARTY_ATS
   Key holding: Lessee under a pre-mortgage lease for more than one year that is
   registered has protected rights even against SARFAESI enforcement.
   Distinguishes ITC v. Blue Coast Hotels.
   Applicable conditions: `tenancy_claimed=True`, `lease_predates_mortgage=True`,
   `lease_registered=True`, `lease_duration_months>11`

5. **Oasis Dealcom Pvt. Ltd. v. Khazana Dealcomm (2016) 10 SCC 214** — `docs/judgments/oasis_dealcom.md`
   Court: SUPREME_COURT | Bench: 2 | Favor: NEUTRAL
   Ground codes: SECOND_SA_FRESH_CAUSE, AUCTION_PURCHASER
   Key holding: A second SA under Section 17 is maintainable if filed on a
   different cause of action. Auction purchaser's rights must be balanced —
   cannot be dispossessed without return of purchase money + interest if sale
   set aside.
   Applicable conditions: `previous_sa_filed=True`, `challenges_auction=True`

**Priority 3 (M8 + M2)**

6. **United Bank of India v. Satyawati Tondon (2010) 8 SCC 110** — `docs/judgments/satyawati_tondon.md`
   Court: SUPREME_COURT | Bench: 3 | Favor: BANK
   Ground codes: REPLY_NOT_GIVEN, NPA_PREMATURE
   Key holding: High Courts should not interfere with SARFAESI proceedings
   unless there is a clear statutory violation; DRT is the appropriate forum.
   Confirms Kanaiyalal on 13(3A) compliance as mandatory.
   Applicable conditions: `reply_not_given=False` (bank-favorable judgment)

7. **Transcore v. Union of India (2008) 1 SCC 125** — `docs/judgments/transcore.md`
   Court: SUPREME_COURT | Bench: 3 | Favor: BANK
   Ground codes: AMOUNT_DISPUTE, AUCTION_GAP_DEFECT
   Key holding: Bank can simultaneously proceed under SARFAESI and file an OA
   under RDDBFI Act. Pursuing one remedy does not bar the other. Also addresses
   Rule 8(5) interest calculation method.
   Applicable conditions: `challenges_demand_notice=True`, `challenges_demand_amount=True`

#### Human-AI Hybrid Approach by Tier

**Class A SC judgments (12 total) — Harasis writes manually, no AI:**
Read full text on Indian Kanoon. Write 4-6 sentences covering the ratio only.
Advocate reviews before loading. No shortcuts. These 12 drive the entire
judicial scoring for the most frequently raised grounds.

**Class A HC/DRAT judgments (~32 total) — AI drafts, Harasis corrects:**
Claude produces a first-pass summary. Harasis reads the judgment's Conclusion
paragraphs on Indian Kanoon (structural analysis) and corrects Claude's draft.
Time per judgment: 15-25 minutes. 32 judgments = 8-13 hours across Phase S1.

**Class B judgments (~7,400 total) — AI generates with safety gate:**
Claude generates summaries automatically during `scripts/fetch_from_ik.py` run.
Safety gate: if Claude returns `SUMMARY_UNCERTAIN: [reason]`, judgment is skipped
entirely. Better to have a smaller honest corpus than a larger uncertain one.
Class B summaries serve only retrieval — never directly produce legal conclusions.

#### Claude Summary Generation Prompt (Class B)

```python
SUMMARY_DRAFT_PROMPT = """You are summarising an Indian court judgment for a legal database.
Write a 120-180 word summary with this exact structure:
Sentence 1: What procedural ground was raised and by which party
Sentence 2: Specific facts relevant to that ground
Sentence 3-4: What the court held and the statutory basis cited
Sentence 5: The specific condition required for this holding to apply

Rules:
- Write only what the COURT decided — not what was argued
- Include the exact SARFAESI section or Rule number mentioned
- State explicitly whether the outcome favoured the bank or the borrower
- If the ratio is unclear or the judgment is purely procedural with no holding,
  write exactly: SUMMARY_UNCERTAIN: [one-sentence reason]
- Return only the summary text — nothing else"""

def generate_class_b_summary(judgment_text: str, max_retries: int = 2) -> str | None:
    """
    Generates holding summary for Class B judgments.
    Returns None if uncertain or generation failed.
    None = judgment is skipped from corpus (not loaded with wrong summary).
    """
    for attempt in range(max_retries + 1):
        try:
            response = client.messages.create(
                model=settings.claude_model,
                max_tokens=400,
                temperature=0.0,
                system=SUMMARY_DRAFT_PROMPT,
                messages=[{"role": "user",
                           "content": judgment_text[:8000]}]
            )
            summary = response.content[0].text.strip()

            if "SUMMARY_UNCERTAIN" in summary:
                return None

            if len(summary.split()) < 80:
                return None

            words = summary.split()
            if len(words) > 250:
                summary = " ".join(words[:200])

            return summary
        except Exception:
            if attempt == max_retries:
                return None
            time.sleep(2)
    return None
```

### 15.1 Judgment Data Structure

```python
# app/models/schemas.py (continued)

class JudgmentCondition(BaseModel):
    field:       str      # must match a field name in CaseFactSchema
    operator:    Literal["eq","neq","gt","lt","gte","lte","is_null","is_not_null","in"]
    value:       Any
    description: str

class JudgmentRecord(BaseModel):
    id:                    UUID
    citation:              str
    title:                 str
    short_name:            str
    court:                 Literal["SUPREME_COURT","HIGH_COURT","DRAT","DRT"]
    high_court_state:      str | None
    bench_strength:        int = 1          # default 1 for IBC Law summaries (bench unknown)
    judgment_date:         date | None      # None for IBC summaries without date
    overruled:             bool
    overruled_by:          UUID | None
    favor:                 Literal["BANK","BORROWER","NEUTRAL"]
    ground_codes:          list[GroundCode]
    holding_summary:       str
    applicable_conditions: list[JudgmentCondition] = []   # empty for Class B
    exclusion_conditions:  list[JudgmentCondition] = []
    has_verified_conditions: bool = False   # True = Class A, False = Class B
    source:                Literal["SC_FULL_TEXT","IBC_LAW_SUMMARY"]
    chunk_type:            str | None = None  # "facts"|"arguments"|"held" for SC chunks
```

### 15.2 Retrieval — Lazy, Ground-Code-Filtered, Class A/B Split

**Lazy retrieval rule:** Chain B retrieves judgments ONLY for ground codes raised in
THIS case (from sa_grounds table) OR failed in THIS case's compliance results.
Never retrieve for all 15 ground codes on every case.

```python
# app/services/judgments/retrieval.py

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, MatchAny
from sentence_transformers import SentenceTransformer
from app.config import settings

_embedder = None

def _get_embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(settings.embedding_model)
        # settings.embedding_model = "law-ai/InLegalBERT" (768-dim, pre-downloaded in Docker)
    return _embedder


def get_relevant_ground_codes(case_id: str, db) -> set[str]:
    """
    Returns the set of ground codes to retrieve judgments for.
    Only ground codes raised in THIS SA or failed in THIS case's compliance.
    Never all 15 — lazy retrieval.
    """
    # Ground codes the borrower raised in the SA
    sa_grounds = db.query(SAGround.ground_code).filter_by(case_id=case_id).all()
    sa_codes = {row.ground_code for row in sa_grounds}

    # Ground codes where compliance engine returned FAIL
    failed = db.query(ComplianceResult.rule_id).filter_by(
        case_id=case_id, status="FAIL"
    ).all()
    # Map rule_ids back to ground codes via RULE_TO_GROUND_MAP
    failed_codes = {RULE_TO_GROUND_MAP.get(row.rule_id) for row in failed} - {None}

    return sa_codes | failed_codes


# Maps each rule_id to its primary ground code for lazy retrieval
RULE_TO_GROUND_MAP = {
    "M1_C1": "SERVICE_DEFECT",    "M1_C2": "AMOUNT_DISPUTE",
    "M1_C3": "SERVICE_DEFECT",    "M1_C4": "SERVICE_DEFECT",
    "M1_C5": "SERVICE_DEFECT",    "M1_C6": "NOTICE_FORMAT_DEFECT",
    "M1_C7": "SERVICE_DEFECT",
    "M2_C1": "REPLY_NOT_GIVEN",   "M2_C2": "REPLY_NOT_GIVEN",
    "M3_C1": "AUCTION_GAP_DEFECT","M3_C2": "NEWSPAPER_PUB_DEFECT",
    "M3_C3": "AUCTION_GAP_DEFECT","M3_C4": "POSSESSION_DEFECT",
    "M3_C6": "AUCTION_NOTICE_AFFIXING", "M3_C7": "AUCTION_DURING_STAY",
    "M3_C8": "PENDING_SA_CONCEALED",
    "M4_C1": "LIMITATION_EXPIRED","M4_C2": "LIMITATION_EXPIRED",
    "M4_C3": "LIMITATION_EXPIRED","M4_C5": "SECOND_SA_FRESH_CAUSE",
    "M5_C1": "TENANCY_CLAIM",     "M5_C2": "TENANCY_CLAIM",
    "M5_C3": "TENANCY_CLAIM",     "M5_C4": "TENANCY_CLAIM",
    "M6_C1": "VALUATION_DISPUTE", "M6_C2": "VALUATION_DISPUTE",
    "M6_C3": "VALUATION_DISPUTE", "M6_C4": "VALUATION_DISPUTE",
    "M7_C1": "NOTICE_ALL_PARTIES","M7_C2": "NOTICE_ALL_PARTIES",
    "M8_C1": "NPA_PREMATURE",     "M8_C2": "NPA_DURING_RESTRUC",
    "M8_C3": "NPA_PREMATURE",     "M8_C4": "AMOUNT_DISPUTE",
    "M8_C6": "NPA_PREMATURE",
    "M9_C1": "MSME_RESTRUC_SKIPPED","M9_C2": "MSME_RESTRUC_SKIPPED",
    "M10_C1": "THIRD_PARTY_ATS",   "M10_C2": "THIRD_PARTY_ATS",
    "M10_C3": "THIRD_PARTY_ATS",   "M10_C4": "AUCTION_PURCHASER",
    "M10_C5": "RIGHT_OF_REDEMPTION","M10_C6": "SECOND_SA_FRESH_CAUSE",
}


def retrieve_candidate_judgments(
    ground_code: str,
    top_k: int = 20       # increased from 10 — corpus is 7,500, filter leaves ~200-600
) -> tuple[list[dict], list[dict]]:
    """
    Returns (class_a_candidates, class_b_candidates) for a single ground code.
    Filters: ground_code match + overruled=False.
    Then splits by has_verified_conditions.

    IMPORTANT: Always metadata-filtered first, then vector similarity.
    NEVER pure vector search — violates Law 1 (FACTS OVERRIDE VECTORS).
    """
    client = QdrantClient(url=settings.qdrant_url)
    embedder = _get_embedder()
    query_vector = embedder.encode(ground_code).tolist()

    results = client.search(
        collection_name=settings.qdrant_judgments_collection,
        query_vector=query_vector,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="ground_codes",
                    match=MatchAny(any=[ground_code])
                ),
                FieldCondition(
                    key="overruled",
                    match=MatchValue(value=False)
                )
            ]
        ),
        limit=top_k,
        with_payload=True
    )

    all_hits = [hit.payload for hit in results]

    class_a = [j for j in all_hits if j.get("has_verified_conditions") is True]
    class_b = [j for j in all_hits if j.get("has_verified_conditions") is False]

    return class_a, class_b



import re

def _load_statutory_wiki() -> str:
    """Loads the entire sarfaesi_law_wiki.md file into memory."""
    with open("docs/wiki/sarfaesi_law_wiki.md", "r", encoding="utf-8") as f:
        return f.read()

def retrieve_statute_text(act_name: str, section_number: str) -> str:
    """
    Retrieves the exact statutory text from the wiki using regex.
    wiki format expects headers like: "## Section 13(2)" or "## Rule 8"
    """
    wiki_text = _load_statutory_wiki()
    pattern = rf"## (Section|Rule)\s+{re.escape(section_number)}\b(.*?)(?=\n## |\Z)"
    match = re.search(pattern, wiki_text, flags=re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0).strip()
    return f"Statute text for {act_name} Sec/Rule {section_number} not found."
```

### IBC Category → GroundCode Mapping (ingestion use)

```python
# scripts/load_judgments.py — IBC_CATEGORY_TO_GROUND_CODE dict
# Maps lowercased keywords from IBC Law bold heading + summary to GroundCode values.
# Used during ingestion to auto-tag ground_codes[] for each judgment.
# Harasis extends this table as new categories are encountered.

IBC_CATEGORY_TO_GROUND_CODE = {
    "demand notice":               ["SERVICE_DEFECT", "NOTICE_FORMAT_DEFECT"],
    "section 13(2)":               ["SERVICE_DEFECT"],
    "date of npa":                 ["AMOUNT_DISPUTE"],
    "npa date":                    ["AMOUNT_DISPUTE"],
    "service on all borrowers":    ["NOTICE_ALL_PARTIES"],
    "service on guarantor":        ["NOTICE_ALL_PARTIES"],
    "guarantor":                   ["NOTICE_ALL_PARTIES"],
    "co-borrower":                 ["NOTICE_ALL_PARTIES"],
    "section 13(3a)":              ["REPLY_NOT_GIVEN"],
    "13(3a)":                      ["REPLY_NOT_GIVEN"],
    "reply to objection":          ["REPLY_NOT_GIVEN"],
    "limitation":                  ["LIMITATION_EXPIRED"],
    "45 days":                     ["LIMITATION_EXPIRED"],
    "section 17":                  ["LIMITATION_EXPIRED"],
    "time-barred":                 ["LIMITATION_EXPIRED"],
    "auction notice":              ["AUCTION_GAP_DEFECT"],
    "30 days":                     ["AUCTION_GAP_DEFECT"],
    "rule 8":                      ["AUCTION_GAP_DEFECT", "POSSESSION_DEFECT"],
    "rule 9":                      ["AUCTION_GAP_DEFECT"],
    "newspaper publication":       ["NEWSPAPER_PUB_DEFECT"],
    "sale notice":                 ["AUCTION_GAP_DEFECT"],
    "valuation":                   ["VALUATION_DISPUTE"],
    "reserve price":               ["VALUATION_DISPUTE"],
    "registered valuer":           ["VALUATION_DISPUTE"],
    "tenancy":                     ["TENANCY_CLAIM"],
    "lease":                       ["TENANCY_CLAIM"],
    "tenant":                      ["TENANCY_CLAIM"],
    "npa classification":          ["NPA_PREMATURE"],
    "90 days":                     ["NPA_PREMATURE"],
    "asset classification":        ["NPA_PREMATURE"],
    "restructuring":               ["NPA_DURING_RESTRUC", "MSME_RESTRUC_SKIPPED"],
    "msme":                        ["MSME_RESTRUC_SKIPPED"],
    "udyam":                       ["MSME_RESTRUC_SKIPPED"],
    "possession notice":           ["POSSESSION_DEFECT"],
    "physical possession":         ["POSSESSION_DEFECT"],
}

def infer_ground_codes(bold_heading: str, summary_text: str) -> list[str]:
    """
    Auto-tags a judgment with GroundCode values based on IBC Law heading + summary.
    Used during ingestion — Harasis can manually override tags in the JSON file.
    """
    combined = (bold_heading + " " + summary_text).lower()
    codes = set()
    for keyword, ground_codes in IBC_CATEGORY_TO_GROUND_CODE.items():
        if keyword in combined:
            codes.update(ground_codes)
    return sorted(codes) if codes else ["UNKNOWN"]
```

### 15.3a Applicability Engine

```python
# app/services/judgments/applicability.py
from simpleeval import simple_eval

def evaluate_condition(condition: dict, fact_value) -> bool:
    op = condition["operator"]
    expected = condition.get("value")
    if op == "eq":          return fact_value == expected
    if op == "neq":         return fact_value != expected
    if op == "gt":          return fact_value > expected
    if op == "lt":          return fact_value < expected
    if op == "gte":         return fact_value >= expected
    if op == "lte":         return fact_value <= expected
    if op == "is_null":     return fact_value is None
    if op == "is_not_null": return fact_value is not None
    if op == "in":          return fact_value in expected
    return False

def check_applicability(judgment: dict, confirmed_facts: dict) -> dict:
    # Check exclusions first
    for cond in judgment.get("exclusion_conditions", []):
        fact_val = confirmed_facts.get(cond["field"])
        if fact_val is not None and evaluate_condition(cond, fact_val):
            return {"status": "NOT_APPLICABLE",
                    "reason": f"Exclusion: {cond['description']}"}

    met, not_met, unknown = [], [], []
    for cond in judgment.get("applicable_conditions", []):
        fact_val = confirmed_facts.get(cond["field"])
        if fact_val is None:
            unknown.append(cond)
        elif evaluate_condition(cond, fact_val):
            met.append(cond)
        else:
            not_met.append(cond)

    if not_met:
        return {"status": "NOT_APPLICABLE",
                "reason": f"Condition not met: {not_met[0]['description']}"}
    if unknown:
        return {"status": "PARTIAL",
                "reason": f"{len(unknown)} conditions unverifiable"}
    return {"status": "APPLICABLE", "conditions_met": len(met)}
```
### 15.3b Class A and Class B Processing

```python
# app/services/judgments/applicability.py (continued)

def process_judgment_candidates(
    ground_code: str,
    class_a_candidates: list[dict],
    class_b_candidates: list[dict],
    confirmed_facts: dict
) -> dict:
    """
    Processes Class A through full applicability check.
    Class B is stored as-is with status SIMILARITY_RETRIEVED.

    Returns:
    {
        "verified":   list of {judgment, status, reason} where status=APPLICABLE|PARTIAL
        "rejected":   list of {judgment, status, reason} where status=NOT_APPLICABLE
        "similarity": list of {judgment, status=SIMILARITY_RETRIEVED} — Class B
    }
    """
    verified, rejected, similarity = [], [], []

    # Class A — run full fact-graph check
    for judgment in class_a_candidates:
        result = check_applicability(judgment, confirmed_facts)
        entry = {"judgment": judgment, "status": result["status"],
                 "reason": result.get("reason", "")}
        if result["status"] in ("APPLICABLE", "PARTIAL"):
            verified.append(entry)
        else:
            rejected.append(entry)

    # Class B — no fact-graph check, flag as similarity-retrieved
    for judgment in class_b_candidates:
        similarity.append({
            "judgment": judgment,
            "status": "SIMILARITY_RETRIEVED",
            "reason": "No verified conditions. Included as potentially relevant."
        })

    return {"verified": verified, "rejected": rejected, "similarity": similarity}
```

### Report Judgment Sections

The report generator (app/reports/generator.py) receives both result sets and
renders two distinct sections:

**Section A — Verified Applicable Precedents**
Shows only judgments where status=APPLICABLE or PARTIAL.
Full applicability reasoning shown. Citation carries verified weight.
Header: "The following precedents have been matched against the facts of this case."

**Section B — Additional Relevant Judgments**
Shows all SIMILARITY_RETRIEVED judgments.
No applicability reasoning — only citation and holding_summary.
Header: "The following judgments were retrieved as potentially relevant to the
grounds raised. Applicability to the specific facts of this case should be
verified by legal counsel before reliance."

This distinction is legally honest. Banks understand the difference between
"this precedent applies to your facts" and "this precedent exists and may be relevant."

### 15.4 Precedence Resolver

```python
# app/services/judgments/precedence.py

COURT_RANK = {
    "SUPREME_COURT": 4,
    "HIGH_COURT":    3,
    "DRAT":          2,
    "DRT":           1
}

class LegalUncertaintyException(Exception):
    pass

def resolve_conflict(j1: dict, j2: dict) -> dict:
    """Returns the judgment that takes precedence. Raises on genuine ambiguity."""
    r1, r2 = COURT_RANK[j1["court"]], COURT_RANK[j2["court"]]
    if r1 != r2:
        return j1 if r1 > r2 else j2
    if j1["bench_strength"] != j2["bench_strength"]:
        return j1 if j1["bench_strength"] > j2["bench_strength"] else j2
    if j1["judgment_date"] != j2["judgment_date"]:
        return j1 if j1["judgment_date"] > j2["judgment_date"] else j2
    raise LegalUncertaintyException(
        f"Unresolvable conflict between {j1['citation']} and {j2['citation']}. "
        f"Flag as LEGAL_UNCERTAINTY. Human lawyer review required."
    )
```
### 15.5 Judgment Statistics Generation

```python
# app/services/judgments/statistics.py

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, MatchAny
from app.config import settings
from app.models.db import get_sync_db, SAGround, GroundScore

def get_ground_statistics(ground_code: str) -> dict:
    """
    Counts judgments in the corpus by outcome for a specific ground code.
    Uses Qdrant payload filtering — no vector search needed, just counting.
    Returns both verified (Class A) and full (Class A + B) counts.
    """
    client = QdrantClient(url=settings.qdrant_url)

    def count_favor(favor_value: str, verified_only: bool = False) -> int:
        must_conditions = [
            FieldCondition(key="ground_codes", match=MatchAny(any=[ground_code])),
            FieldCondition(key="favor", match=MatchValue(value=favor_value)),
            FieldCondition(key="overruled", match=MatchValue(value=False))
        ]
        
        if verified_only:
            must_conditions.append(
                FieldCondition(key="favor_verified", match=MatchValue(value=True))
            )
            
        result = client.count(
            collection_name=settings.qdrant_judgments_collection,
            count_filter=Filter(must=must_conditions)
        )
        return result.count

    v_borrower = count_favor("BORROWER", verified_only=True)
    v_bank     = count_favor("BANK", verified_only=True)
    v_neutral  = count_favor("NEUTRAL", verified_only=True)
    v_total    = v_borrower + v_bank + v_neutral

    f_borrower = count_favor("BORROWER", verified_only=False)
    f_bank     = count_favor("BANK", verified_only=False)
    f_neutral  = count_favor("NEUTRAL", verified_only=False)
    f_total    = f_borrower + f_bank + f_neutral

    return {
        "verified": {
            "total":            v_total,
            "borrower_wins":    v_borrower,
            "bank_wins":        v_bank,
            "neutral":          v_neutral,
            "borrower_win_pct": round(v_borrower / v_total * 100, 1) if v_total > 0 else None,
            "bank_win_pct":     round(v_bank / v_total * 100, 1) if v_total > 0 else None,
        },
        "full": {
            "total":            f_total,
            "borrower_wins":    f_borrower,
            "bank_wins":        f_bank,
            "neutral":          f_neutral,
            "borrower_win_pct": round(f_borrower / f_total * 100, 1) if f_total > 0 else None,
            "bank_win_pct":     round(f_bank / f_total * 100, 1) if f_total > 0 else None,
        },
        "data_confidence":  "HIGH" if v_total >= 10 else ("MEDIUM" if v_total >= 5 else ("LOW" if f_total > 0 else "NO_DATA"))
    }

@celery_app.task(name="tasks.chain_b.compute_ground_statistics")
def task_compute_ground_statistics(case_id: str):
    """
    For each ground raised in this SA, fetch win-rate statistics
    from the Qdrant corpus. Stores in ground_scores table.
    """
    with get_sync_db() as db:
        grounds = db.query(SAGround).filter_by(case_id=case_id).all()
        for ground in grounds:
            stats = get_ground_statistics(ground.ground_code)
            score_row = db.query(GroundScore).filter_by(case_id=case_id, ground_code=ground.ground_code).first()
            if score_row:
                # Store verified as primary; report can access both if we added columns, but here we show primary
                score_row.corpus_total         = stats["verified"]["total"]
                score_row.corpus_borrower_wins = stats["verified"]["borrower_wins"]
                score_row.corpus_bank_wins     = stats["verified"]["bank_wins"]
                score_row.corpus_confidence    = stats["data_confidence"]
            db.commit()
```

---

## 16. Ground Strength & Scoring Engine

```python
# app/services/scoring/ground_strength.py

COURT_RANK = {"SUPREME_COURT": 4, "HIGH_COURT": 3, "DRAT": 2, "DRT": 1}

def compute_judicial_score(
    ground_code: str,
    applicable_judgments: list[dict],
    corpus_stats: dict
) -> float:
    # Base: use verified corpus win rate as the foundation
    if corpus_stats["data_confidence"] in ("HIGH", "MEDIUM"):
        borrower_win_pct = corpus_stats.get("verified", {}).get("borrower_win_pct")
        if borrower_win_pct is None:
            borrower_win_pct = corpus_stats.get("full", {}).get("borrower_win_pct") or 0
        base_score = borrower_win_pct / 100   # 80% win rate → base 0.80
    else:
        base_score = 0.40   # no data — neutral

    # Modifier: SC judgment in this specific case adjusts up/down
    sc_borrower = [j for j in applicable_judgments if j["court"] == "SUPREME_COURT" and j["favor"] == "BORROWER"]
    sc_bank     = [j for j in applicable_judgments if j["court"] == "SUPREME_COURT" and j["favor"] == "BANK"]

    if sc_borrower:
        return max(base_score, 0.85)
    elif sc_bank:
        return min(base_score, 0.20)
    else:
        hc_borrower = [j for j in applicable_judgments if j["favor"] == "BORROWER"]
        if hc_borrower:
            return min(base_score + 0.10, 1.0)
        return base_score

def compute_ground_strength(
    ground_code: str,
    compliance_result_status: str,  # 'PASS' | 'FAIL' | 'UNKNOWN'
    applicable_judgments: list[dict],
    corpus_stats: dict
) -> dict:

    # Component 1: Factual score
    if compliance_result_status == "FAIL":
        factual_score = 1.0   # bank's record confirms borrower's allegation
    elif compliance_result_status == "UNKNOWN":
        factual_score = 0.4   # conservative: unverified = some risk
    else:
        factual_score = 0.0   # bank's record contradicts allegation

    # Component 2: Judicial score
    judicial_score = compute_judicial_score(ground_code, applicable_judgments, corpus_stats)

    ground_strength = (factual_score * 0.55) + (judicial_score * 0.45)

    return {
        "ground_code":      ground_code,
        "factual_score":    round(factual_score, 4),
        "judicial_score":   round(judicial_score, 4),
        "ground_strength":  round(ground_strength, 4),
        "strength_label":   _strength_label(ground_strength)
    }

def _strength_label(score: float) -> str:
    if score < 0.25:  return "WEAK"
    if score < 0.50:  return "ARGUABLE"
    if score < 0.70:  return "STRONG"
    return "VERY_STRONG"

def compute_litigation_exposure(ground_scores: list[dict]) -> float:
    if not ground_scores:
        return 0.0
    scores = [g["ground_strength"] for g in ground_scores]
    return round((max(scores) * 0.65) + (sum(scores) / len(scores) * 0.35), 4)

def compute_compliance_score(compliance_results: list) -> int:
    DEDUCTIONS = {
        "FATAL":        40,
        "ABSOLUTE_BAR": 50,
        "CURABLE":      15,
        "MINOR":         5,
        "ADVISORY":      3,
        "UNKNOWN":      10,
    }
    total_deductions = sum(
        DEDUCTIONS.get(r.severity, 0)
        for r in compliance_results
        if r.status == "FAIL"
    )
    return max(0, 100 - total_deductions)
```

### 16.1 Recommendation Matrix

```python
# app/services/scoring/recommendation.py

def get_recommendation(compliance_score: int, litigation_exposure: float,
                        absolute_bar_triggered: bool) -> dict:

    # Special case: SA is time-barred — this overrides everything
    if absolute_bar_triggered and litigation_exposure < 0.30:
        return {
            "label": "PROCEED_FAVOURABLE",
            "text": "SA appears to be time-barred under Section 17. Dismissal likely."
        }

    matrix = [
        # (compliance_min, compliance_max, exposure_max, label, text)
        (90, 100, 0.25, "PROCEED",
         "Bank followed procedure correctly. Borrower's case is weak."),
        (90, 100, 0.45, "PROCEED_WITH_AWARENESS",
         "Procedure clean. Some arguable grounds. Monitor DRT hearings."),
        (90, 100, 1.00, "HIGH_RISK",
         "Procedure clean but borrower has strong legal grounds."),
        (70,  89, 0.25, "PROCEED_WITH_CONDITIONS",
         "Minor procedural gaps. Borrower case weak. Get legal affidavit on curable defects."),
        (70,  89, 0.45, "ELEVATED_RISK",
         "Both sides have exposure. Detailed legal review recommended."),
        (70,  89, 1.00, "HIGH_RISK",
         "Do not proceed without detailed legal review."),
        ( 0,  69, 1.00, "DO_NOT_PROCEED",
         "Significant procedural defects. Auction highly vulnerable."),
    ]

    for comp_min, comp_max, exp_max, label, text in matrix:
        if comp_min <= compliance_score <= comp_max and litigation_exposure <= exp_max:
            return {"label": label, "text": text}

    # Critical — litigation exposure > 0.65 regardless of compliance
    if litigation_exposure >= 0.65:
        return {
            "label": "DO_NOT_PROCEED_CRITICAL",
            "text": "Borrower has very strong grounds regardless of bank procedure."
        }

    return {"label": "MANUAL_REVIEW_REQUIRED",
            "text": "Score combination not in matrix. Legal review required."}
```

---

## 17. API Design — Full Request & Response Schemas

**AI IDE instruction:** `bank_id` is NEVER in a request body. It always comes from JWT.
`user_id` / `confirmed_by` always come from JWT. Never from request body.

### 17.1 Pydantic Request Schemas

```python
# app/models/schemas.py (request schemas section)


class ConfirmFactRequest(BaseModel):
    corrected_value:  str | None = None  # None = accept extracted value as-is
    human_confirmed:  bool = True
    # confirmed_by → from JWT, confirmed_at → server timestamp

class WorkbenchCompleteRequest(BaseModel):
    trigger_analysis: bool = True
    # If True, fires Chain B immediately after confirmation gate passes.
    # If False, only marks workbench complete — Chain B must be triggered separately.

class TriggerAnalysisRequest(BaseModel):
    # Used when trigger_analysis=False in WorkbenchCompleteRequest
    # or for re-running analysis after manual fact correction
    pass  # no body needed — case_id from path param

class GenerateReportRequest(BaseModel):
    # Report is auto-generated at end of Chain B.
    # This endpoint re-generates on demand if report is stale.
    pass
```

### 17.2 Route Definitions

```python
# All routes — exact signatures for AI IDE to implement

# ── Auth ──────────────────────────────────────────────────────────────────────
POST   /api/v1/auth/login
       body: {email: str, password: str}
       returns: {access_token: str, token_type: "bearer"}

POST   /api/v1/auth/refresh
       header: Authorization: Bearer <token>
       returns: {access_token: str, token_type: "bearer"}

# ── Cases ─────────────────────────────────────────────────────────────────────
POST   /api/v1/cases
       body: CreateCaseRequest
       returns: CaseResponse
       auth: BANK_OFFICER | BANK_ADMIN

GET    /api/v1/cases
       returns: list[CaseSummaryResponse]
       auth: BANK_OFFICER (own cases) | BANK_ADMIN (all bank cases)

GET    /api/v1/cases/{case_id}
       returns: CaseResponse
       auth: any — scoped to bank_id from JWT

# ── Documents ────────────────────────────────────────────────────────────────
POST   /api/v1/cases/{case_id}/documents
       body: multipart/form-data {file: UploadFile, doc_type: str}
       returns: DocumentResponse
       side_effect: triggers Chain A if first document for this case
       auth: BANK_OFFICER | BANK_ADMIN

GET    /api/v1/cases/{case_id}/documents
       returns: list[DocumentResponse]

# ── Pipeline ─────────────────────────────────────────────────────────────────
GET    /api/v1/cases/{case_id}/pipeline-status
       returns: {status: str, pipeline_stage: str | None, progress_pct: int}

# ── Workbench ────────────────────────────────────────────────────────────────
GET    /api/v1/cases/{case_id}/workbench
       returns: {pending_count: int, items: list[WorkbenchItemResponse]}
       # Returns only items requiring human review (low confidence + implied facts)

GET    /api/v1/cases/{case_id}/facts
       returns: list[FactResponse]
       # Returns ALL extracted facts with confidence and extraction_method

PATCH  /api/v1/cases/{case_id}/facts/{fact_id}
       body: ConfirmFactRequest
       returns: FactResponse
       side_effect: writes audit_log entry

POST   /api/v1/cases/{case_id}/workbench/confirm-all
       body: WorkbenchCompleteRequest
       returns: {case_id: str, trigger_analysis: bool, chain_b_task_id: str | None}
       precondition: all required fields must be human_confirmed. Returns HTTP 422 if not.
       side_effect: fires Chain B if trigger_analysis=True

# ── Results ───────────────────────────────────────────────────────────────────
GET    /api/v1/cases/{case_id}/compliance
       returns: ComplianceResultsResponse

GET    /api/v1/cases/{case_id}/grounds
       returns: GroundScoresResponse

GET    /api/v1/cases/{case_id}/judgments
       returns: JudgmentApplicabilityResponse

# ── Reports ───────────────────────────────────────────────────────────────────
POST   /api/v1/cases/{case_id}/report
       body: GenerateReportRequest
       returns: ReportMetaResponse
       note: report is auto-generated in Chain B. This endpoint re-generates on demand.

GET    /api/v1/cases/{case_id}/report
       returns: ReportJsonResponse

GET    /api/v1/cases/{case_id}/report/pdf
       returns: StreamingResponse (application/pdf)
```

### 17.3 Response Schemas

```python

class FactResponse(BaseModel):
    id:                  UUID
    field_name:          str
    field_value:         str | None
    confidence:          float
    extraction_method:   str | None
    human_confirmed:     bool
    source_page:         int | None
    requires_workbench:  bool

class ComplianceResultsResponse(BaseModel):
    case_id:          UUID
    compliance_score: int
    modules:          dict[str, list[dict]]  # module_name → list of rule results

class GroundScoresResponse(BaseModel):
    case_id:             UUID
    grounds_raised:      list[dict]
    litigation_exposure: float
    exposure_label:      str
    recommendation:      dict
```

### 17.4 Workbench API Updates (Conflicts and Missing Fields)

```python
import uuid
from pydantic import BaseModel
from typing import Literal

class WorkbenchFactItem(BaseModel):
    fact_id:           uuid.UUID
    field_name:        str
    field_label:       str          # human-readable label
    extracted_value:   str | None
    confidence:        float
    source_page:       int | None
    source_text:       str | None   # the paragraph it was extracted from
    extraction_method: str
    module:            str          # which compliance module needs this
    why_flagged:       str          # plain English: "Confidence below 80%"

class WorkbenchNotFoundItem(BaseModel):
    field_name:   str
    field_label:  str
    module:       str
    why_needed:   str       # "Required for Section 13(2) 60-day period calculation"
    input_type:   str       # "date" | "amount" | "boolean" | "text"
    hint:         str       # "Check the demand notice document. Format: DD.MM.YYYY"

class WorkbenchConflictItem(BaseModel):
    conflict_id:         uuid.UUID
    field_name:          str
    field_label:         str
    candidate_a_value:   str
    candidate_a_source:  str    # "Page 3 of Securitisation Application"
    candidate_a_excerpt: str    # the sentence containing this value
    candidate_b_value:   str
    candidate_b_source:  str    # "Page 1 of Demand Notice"
    candidate_b_excerpt: str
    module:              str

class WorkbenchResponse(BaseModel):
    # Fields extracted but uncertain — officer confirms or corrects
    low_confidence_items: list[WorkbenchFactItem]

    # Fields required for compliance that could not be found anywhere
    not_found_items: list[WorkbenchNotFoundItem]

    # Fields where two documents disagree — officer chooses
    conflict_items: list[WorkbenchConflictItem]

    total_pending: int
    all_resolved:  bool   # True only when all three lists are empty

class ConflictResolutionRequest(BaseModel):
    resolution: Literal["candidate_a", "candidate_b", "custom"]
    custom_value: str | None = None   # required if resolution == "custom"

# @router.patch("/cases/{case_id}/workbench/conflicts/{conflict_id}")
# async def resolve_conflict(...) 
# -> Officer resolves fact conflict by choosing candidate A/B or custom value.
# Updates case_facts row, sets human_confirmed = True, marks conflict resolved.
```

---

## 18. Error Handling Contracts

**AI IDE instruction:** These are the required error handling behaviors per service.
Do not invent alternative behaviors. Do not swallow exceptions silently.

### 18.1 Azure OCR Failures

```python
# app/services/ocr/azure_ocr.py error handling

# WHEN: Azure API returns non-200, quota exceeded, or timeout
# ACTION:
#   1. Set documents.ocr_status = 'FAILED'
#   2. Set cases.pipeline_stage = 'OCR_FAILED'
#   3. Insert workbench item: {
#        field_name: f"ocr_failed_{doc_id}",
#        message: f"OCR failed for document {doc_id}. Manual text entry required.",
#        action: "Enter document text manually in the workbench."
#      }
#   4. Do NOT retry automatically (OCR failures are usually quota/key issues)
#   5. Do NOT raise to Celery — handle within the OCR task

# WHEN: ocr_confidence < 0.70 for a paragraph
# ACTION:
#   Set paragraphs.ocr_confidence = <value>
#   Flag paragraph with is_handwritten check
#   Add workbench item for that paragraph: "Low OCR confidence. Review manually."
```

### 18.2 Claude API Failures

```python
# app/services/extraction/nlp_layer.py error handling

# WHEN: Claude API returns malformed JSON (after strip of backticks)
# RETRY: up to 2 times with identical prompt
# AFTER 2 RETRIES:
#   Return None for that paragraph's extraction
#   Set all fields from that paragraph to confidence = 0.0, extraction_method = None
#   Add workbench item: "NLP extraction failed for paragraph {para_id}. Manual review required."
#   Do NOT raise exception — partial extraction better than blocking pipeline

# WHEN: anthropic.APITimeoutError (> 30 seconds)
# RETRY: once after 5-second sleep
# AFTER RETRY: same as malformed JSON handling above

# WHEN: anthropic.RateLimitError
# ACTION: Celery task raises exception → Celery retries with exponential backoff
#   max_retries=3, countdown=60 (1 minute between retries)

# WHEN: anthropic.AuthenticationError
# ACTION: Set cases.status = 'FAILED'
#         Log error with case_id and "ANTHROPIC_AUTH_FAILED"
#         Do NOT retry — this requires human intervention (key issue)
```

### 18.3 Qdrant Failures

```python
# app/services/judgments/retrieval.py error handling

# WHEN: Qdrant is unreachable (connection refused, timeout)
# ACTION:
#   Log error: "Qdrant unavailable for case {case_id}"
#   Set judgment_applicability entries for all grounds to:
#     {status: 'UNAVAILABLE', reason: 'Judgment database temporarily unavailable'}
#   Continue Chain B — compliance engine still runs
#   Report generation proceeds with section: "Judgment analysis unavailable at this time."
#   Do NOT set case status to FAILED — report is still generated without judgment section
```

### 18.4 Workbench Precondition Check

```python
# app/api/workbench.py — POST /workbench/confirm-all

# BEFORE firing Chain B, validate:
REQUIRED_CONFIRMED_FIELDS_BY_MODULE = {
    "M1": ["demand_notice_date", "notice_service_mode", "notice_dispatch_proof_present"],
    "M2": ["objection_filed"],  # if objection_filed = True, also: bank_reply_given
    "M3": ["sale_notice_date", "auction_date", "asset_type"],
    "M4": ["measure_date", "sa_filing_date"],
    "M5": [],  # M5 only runs if tenancy_claimed = True
    "M6": ["valuation_report_present"],
    "M7": ["total_borrowers_in_loan", "total_guarantors_in_loan"],
    "M8": ["date_of_last_payment", "npa_classification_date"],
    "M9": [],  # M9 only runs if msme_claimed_by_borrower = True
}

# If any required field is not human_confirmed:
# Return HTTP 422 with body:
# {
#   "detail": "Cannot trigger analysis. Required fields not confirmed.",
#   "unconfirmed_fields": ["demand_notice_date", "notice_service_mode"]
# }
```

### 18.5 Report Generation Failures

```python
# app/reports/generator.py error handling

# WHEN: WeasyPrint fails (CSS error, missing font, template syntax error)
# ACTION:
#   Log error with traceback and case_id
#   Save report_json to DB (reports table) even if PDF fails
#   Set reports.pdf_url = None
#   Return JSON report to caller with header: X-Report-Format: json-only
#   Do NOT set case status to FAILED — JSON report is still usable
```

### 18.6 LegalUncertaintyException

```python
# app/services/judgments/precedence.py error handling

# WHEN: LegalUncertaintyException raised during precedence resolution
# ACTION:
#   Do NOT raise to Celery — catch within the precedence resolver task
#   Store in judgment_applicability:
#     {status: 'LEGAL_UNCERTAINTY',
#      reason: 'Conflicting judgments cannot be auto-resolved. Human lawyer review required.'}
#   Continue Chain B
#   Include in report: "Legal Uncertainty Flagged: [conflict details]. Expert review required."
```

---

## 19. Implementation Roadmap — 22 Weeks

### PHASE 0: Legal Foundation (Weeks 1–2)
**Zero code. All legal work. Nothing in Phase 1 starts until Phase 0 gate passes.**

| Deliverable | Owner | Done When |
|---|---|---|
| Case Fact Schema reviewed and approved | SARFAESI Lawyer | Every field confirmed, no omissions |
| All 9 module YAML rules written and paper-tested | Lawyer + Engineer | Rule engine gives correct verdict on 5 paper test cases |
| 15 starter judgments structured with conditions | Legal Researcher | applicable_conditions + exclusion_conditions populated for each |
| 5 anonymised test SAs provided | Bank Advisor | Mix: 2 typed English, 2 Hindi/mixed, 1 complex multi-ground |
| Tech infrastructure up | Engineer | docker-compose up runs all services, alembic upgrade head passes, InLegalBERT downloads successfully |

**Gate:** Rule engine (manually entered facts, no OCR) produces correct verdict on all 5 test SAs, agreed by lawyer. 100% — not 4/5. InLegalBERT verification command (`python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('law-ai/InLegalBERT')"`) must execute without downloading.

---

### PHASE 1: Document Intelligence (Weeks 3–6)

| Week | Deliverable | Test |
|---|---|---|
| 3 | Document upload API, SHA-256, S3, DocType classifier | Upload all 5 test SAs, verify hashes match |
| 4 | Azure OCR integration, paragraph extraction, bbox storage | Lawyer reviews paragraph output vs source PDF |
| 5 | Language detection, IndicTrans2 integration | Verify Hindi paragraphs translated correctly |
| 6 | Regex layer — all date/amount/section patterns | Run on all 5 test SAs, measure date extraction accuracy |

**Gate:** System ingests one typed English SA and one Hindi/mixed SA. Paragraphs table populated. Target: >95% text fidelity. Lawyer confirms.

---

### PHASE 2: NLP Extraction (Weeks 7–10)

| Week | Deliverable | Test |
|---|---|---|
| 7 | Issue classifier — ground_code tags per paragraph | Classification accuracy vs lawyer's manual tagging |
| 8 | LLM fact extraction service, confidence scoring | Field extraction accuracy on all 5 test SAs |
| 9 | Implied fact detection, confidence routing | All implied facts correctly flagged for workbench |
| 10 | case_facts table population, sa_grounds table | Lawyer reviews full extraction output field by field |

**Gate:** >85% field accuracy on typed English, >75% on Hindi/mixed. Every error documented and fixed.

---

### PHASE 3: Workbench + Engines (Weeks 11–14)

| Week | Deliverable | Test |
|---|---|---|
| 11 | Verification Workbench UI — split screen, confirm/correct flow | Officer can confirm all 5 test SAs without confusion |
| 12 | Rule engine interpreter, all 9 YAML modules wired, silence check | 100% verdict agreement with lawyer on all 5 test SAs |
| 13 | Qdrant setup, Class A judgment JSONs loaded (Harasis must deliver before this week), applicability engine, precedence resolver | Applicability engine correctly rejects fact-mismatched judgments on all 5 fixtures |
| 14 | Ground strength, litigation exposure, compliance score, recommendation | Scores reviewed by lawyer — 80% directional agreement |

**Gate:** End-to-end pipeline on all 5 test SAs. 100% compliance verdict agreement. Chain B triggers correctly from workbench.

**Hard dependency for Week 13:** Harasis must deliver all Class A judgment JSONs
(44 total — see Section 15.0) with has_verified_conditions=true and
applicable_conditions populated BEFORE Haragam starts Week 13.
If delayed, Week 13 shifts to basic Qdrant setup with Class B only.
Class A gate deferred to Phase 4 Week 16.

---

### PHASE 4: Report + Security (Weeks 15–18)

| Week | Deliverable | Test |
|---|---|---|
| 15 | PDF report generator, all sections, tamper-evident hash | Lawyer reviews complete report |
| 16 | Legal disclaimer block drafted by advocate | Advocate confirms no legal advice statement |
| 17 | JWT + RBAC, bank data isolation, audit logging | Cross-bank data leakage test (cannot see another bank's cases) |
| 18 | Case dashboard, full end-to-end test | Complete pipeline run without manual intervention |

**Gate:** PDF report for one test SA reviewed by SARFAESI lawyer. Confirmed accurate and safe to show bank audience.

---

### PHASE 5: Hardening + Pitch Prep (Weeks 19–22)

| Week | Deliverable | Test |
|---|---|---|
| 19 | Calibration Phase: Run on 20 historical cases (not training set) | Document every error, validate recommendation accuracy |
| 20 | Fix all errors from accuracy test | Re-run 20 historical cases, measure improvement |
| 21 | Demo environment with 3 pre-loaded cases | Full live demo rehearsal |
| 22 | Final lawyer review, brief bank contact | System is pitch-ready |

**Gate:** All 6 Definition of Pitch-Ready criteria met.

---

## 20. Risk Register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| OCR accuracy < 80% on poor scans | Medium | High | Manual text entry fallback in workbench. OCR failure flags paragraph, never blocks pipeline. |
| LLM extracts wrong date for critical field | Medium | Fatal | All date fields: `requires_workbench = True` regardless of confidence. No date auto-confirmed. |
| YAML rule interpreter evaluates expression incorrectly | Medium | Fatal | `simpleeval` only — never `eval()`. Unit test every rule against 3 known cases before deployment. |
| Judgment conditions wrong | Medium | High | Lawyer signs off per judgment before loading into Qdrant. Tested against 3 known cases. |
| IndicTrans2 model cold-start timeout | Low | Medium | **FIXED v5.0:** Pre-downloaded in Dockerfile. Cold-start risk eliminated. Risk now LOW. |
| InLegalBERT cold-start timeout | Low | Medium | **FIXED v5.0:** Pre-downloaded in Dockerfile. Cold-start risk eliminated. Risk now LOW. |
| Chain A and Chain B accidentally connected | High | Fatal | Use `.si()` not `.s()` in all chains. Code review: `chain_b.py` must have no auto-trigger. |
| `bank_id` trusted from request body | High | Fatal | Code review gate: grep codebase for `bank_id` in any Pydantic request model — must not exist there. |
| `simpleeval` missing a variable in expression | Medium | Medium | Wrap all `evaluator.eval()` calls in try/except. Missing variable → UNKNOWN result, not crash. |
| Legal team unavailable during Phase 3 | Medium | Fatal | Phase 3 cannot start without Phase 0 complete. Legal availability is a hard project dependency. |
| New SC judgment overrules key precedent post-launch | Low | High | `last_reviewed_at` on each judgment record. Alert when > 6 months. Quarterly legal review. |
| IndicTrans2 base model insufficient for legal Hindi text | Medium | Medium | QLoRA fine-tuned variant available — "Adapting IndicTrans2 for Legal Domain MT" (ACL JUST-NLP 2025). Use if base model accuracy < 75% on SARFAESI documents. |
| IBC moratorium not flagged — bank proceeds against frozen asset | Low | Fatal | F4 pre-intake filter added in v5.0. `ibc_moratorium_active` is always-human-confirm. |

---

## 21. Definition of Pitch-Ready

All six criteria must be true. Not five of six.

1. **Extraction accuracy** — ≥ 90% on typed English, ≥ 80% on Hindi/mixed. Verified by lawyer on 20 test cases.
2. **Compliance verdict accuracy** — 100% match with lawyer's manual assessment on 20 test cases. A wrong FATAL verdict is unacceptable.
3. **Ground strength accuracy** — Directionally correct on ≥ 16/20 test cases (80%), agreed by lawyer.
4. **Legal safety** — Advocate confirms no statement in report can be construed as legal advice.
5. **Performance** — Full pipeline (upload to PDF report) completes in < 5 minutes for a 30-page SA.
6. **Demo stability** — 3 pre-loaded cases run live without failure in front of bank audience.

---

## 22. Appendix: Silence Check Protocol

```python
# The system NEVER assumes a null field means the action did or did not happen.
# It surfaces the unknown explicitly and blocks the report.

class SilenceCheckFlag(Exception):
    def __init__(self, field: str, module: str, description: str = ""):
        self.field = field
        self.module = module
        self.description = description
        super().__init__(
            f"Field '{field}' required for {module} is null and not confirmed. "
            f"Check bank records: {description}"
        )

# In the rule engine:
def _get_confirmed_value(field: str, facts: dict, module: str):
    fact = facts.get(field)
    if fact is None or not fact.get("human_confirmed"):
        # Do NOT raise — return None, which causes UNKNOWN in rule evaluation
        return None
    return fact["value"]

# NEVER DO THIS:
if notice_service_date is None:
    assume_not_served = True      # WRONG — silence ≠ absence of the action

# ALWAYS DO THIS:
val = _get_confirmed_value("notice_service_date", facts, "M1")
if val is None:
    return RuleResult(status="UNKNOWN", severity="UNKNOWN",
                      message="notice_service_date not confirmed. Check dispatch records.")
```

### Fields That Block Report Generation When UNKNOWN

The following fields, if UNKNOWN at report generation time, prevent the report from
being finalized. The workbench must resolve them first:

| Field | Module | Why Blocking |
|---|---|---|
| `demand_notice_date` | M1 | Cannot calculate 60-day period |
| `notice_service_mode` | M1 | Cannot assess service validity |
| `notice_dispatch_proof_present` | M1 | Cannot confirm service occurred |
| `sale_notice_date` + `auction_date` | M3 | Cannot calculate auction gap |
| `measure_date` + `sa_filing_date` | M4 | Cannot calculate limitation |
| `total_borrowers_in_loan` | M7 | Cannot verify all parties served |

All other UNKNOWN fields produce UNKNOWN rule results but do not block report generation.
They are surfaced in the report with explicit "could not be verified" language.

---

## 23. Appendix: Test Fixture Acquisition Guide

**Context:** Phase 0 requires 5 anonymised SARFAESI Application (SA) PDFs before any
code is written. The rule engine Phase 3 gate (100% verdict agreement) cannot pass without
them. These cannot be generated programmatically — they must be acquired from real or
legally-realistic sources, then reviewed by a SARFAESI lawyer.

### What the 5 fixtures must cover

| Filename | Language | Grounds to cover | Complexity |
|---|---|---|---|
| `sa_typed_english_01.pdf` | English | M1 or M4 (single ground) | Simple |
| `sa_typed_english_02.pdf` | English | M1 + M3 or M1 + M7 (multi-ground) | Medium |
| `sa_hindi_mixed_01.pdf` | Hindi/English | M8 or M9 | Simple |
| `sa_hindi_mixed_02.pdf` | Hindi/English | M5 + M6 | Medium |
| `sa_complex_01.pdf` | Mixed | 3+ grounds across modules | Complex |

### Source options (in order of preference)

**Option 1 — Bank partner (preferred)**
Ask your bank contact for SAs filed against them in the past 2 years, redacted.
Redact: borrower name → `[BORROWER]`, account number → `[ACCOUNT_XXXX]`,
property address → `[PROPERTY]`, guarantor names → `[GUARANTOR_N]`.
Retain all dates, amounts, section references — those are what the system tests.

**Option 2 — SARFAESI practising advocate**
Any advocate who has appeared on both sides in SARFAESI cases will have past file copies.
Request anonymised copies. Both bank-side and borrower-side SAs are needed.

**Option 3 — Reconstruct from DRT orders on Indian Kanoon**
DRT orders are public. The factual narrative section of a DRT order quotes the SA grounds
verbatim. Procedure:
1. Go to `indiankanoon.org` → search `SARFAESI section 17 DRT [state name]`
2. Open a DRT order that quotes SA grounds in detail
3. Extract the factual narrative into a synthetic SA PDF following the template below
4. Have lawyer confirm the synthetic SA is legally realistic before using

**Option 4 — Synthetic SA (last resort)**
If Phases 1–2 must start before real SAs are acquired, use this template.
**The Phase 3 gate still requires real or lawyer-confirmed SAs.**

```
Synthetic SA paragraph structure:
¶1  Identity: Applicant (borrower) and Respondent (bank + branch)
¶2  Loan details: account number, sanction date, sanction amount, purpose
¶3  NPA classification: date, notice if any
¶4  Section 13(2) demand notice: date of issue, date of service, mode, amount demanded
¶5  Borrower's objection under Section 13(3A): date, content (if filed)
¶6  Bank's reply or non-reply (if applicable)
¶7  Section 13(4) possession notice: date, symbolic or physical
¶8  Sale notice: date, reserve price, auction date (if applicable)
¶9  Grounds of challenge: numbered list with factual basis for each
¶10 Relief sought: specific prayer(s) to the DRT
```

### Anonymisation checklist before committing files

Before placing any fixture in `tests/fixtures/`, verify each item:

- [ ] Borrower full name removed
- [ ] Bank branch genericised (e.g. "State Bank of India, [City] Branch")
- [ ] Property address replaced with `[PROPERTY_ADDRESS]`
- [ ] Loan account number replaced with `[LOAN_ACCOUNT_XXXX]`
- [ ] All guarantor and co-borrower names replaced
- [ ] Advocate names replaced
- [ ] DRT case number **retained** (used in M4 limitation calculation)
- [ ] All dates **retained** (critical for rule engine)
- [ ] All rupee amounts **retained** (critical for M1_C2, M6)

**Storage:** Fixture PDFs are gitignored — store in shared secure drive accessible to the team.
The expected-verdict JSON files (see below) are version-controlled.

### Ground truth JSON format for each fixture

Create one JSON file per fixture, confirmed and signed off by your SARFAESI lawyer.
These live at `tests/fixtures/<fixture_name>_expected.json`.

```json
{
  "fixture_file": "sa_typed_english_01.pdf",
  "confirmed_by_lawyer": "Advocate [Name], Bar No. [N]",
  "confirmed_date": "YYYY-MM-DD",
  "expected_verdicts": {
    "M1_C1": {"status": "PASS",    "severity": null},
    "M1_C2": {"status": "FAIL",    "severity": "CURABLE"},
    "M1_C3": {"status": "PASS",    "severity": null},
    "M1_C4": {"status": "FAIL",    "severity": "FATAL"},
    "M1_C5": {"status": "PASS",    "severity": null},
    "M1_C6": {"status": "UNKNOWN", "severity": "UNKNOWN"},
    "M1_C7": {"status": "PASS",    "severity": null},
    "M2_C1": {"status": "UNKNOWN", "severity": "UNKNOWN"},
    "M4_C1": {"status": "FAIL",    "severity": "ABSOLUTE_BAR"}
  },
  "notes": "Demand notice amount overstated by 8%. Service by courier — invalid mode."
}
```

The Phase 3 gate (100% verdict agreement) is measured by comparing rule engine output
against these JSON files using `pytest tests/test_rules/test_end_to_end.py`.

---

> **FACTS OVERRIDE VECTORS — LAW OVERRIDES MODELS — SYSTEM OVERRIDES AI**

*Document Version 5.0 | AI-IDE Complete — All v4.0 Bugs Fixed | June 2026*

---

## 24. Appendix: Reference Implementation — app/services/storage.py

```python
# app/services/storage.py
"""
S3-compatible object storage service.

Works with both:
  - AWS S3 (production): set S3_ENDPOINT_URL="" in .env
  - MinIO (local dev):   set S3_ENDPOINT_URL="http://localhost:9000"

SECURITY RULES:
  - All S3 paths are constructed from UUIDs only (never user input in path)
  - Files are never publicly accessible — always served through FastAPI endpoint
  - SHA-256 hash computed before upload for integrity verification
  - Duplicate detection: same hash + same case = reject with 409

PATH STRUCTURE (immutable after design):
  cases/{case_id}/documents/{doc_id}.pdf
  cases/{case_id}/reports/{report_id}.pdf
  cases/{case_id}/reports/{report_id}.json
"""

import hashlib
import io
import logging
import uuid
from typing import BinaryIO

import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, status

from app.config import settings

logger = logging.getLogger(__name__)

# ─── CLIENT ──────────────────────────────────────────────────────────────────

_s3_client = None


def get_s3_client():
    """
    Return cached boto3 S3 client.
    Cached at module level — boto3 client is thread-safe for reads.
    endpoint_url is only set for MinIO. AWS S3 uses default endpoint.
    """
    global _s3_client
    if _s3_client is None:
        kwargs = {
            "aws_access_key_id":     settings.s3_access_key,
            "aws_secret_access_key": settings.s3_secret_key,
            "region_name":           "ap-south-1",   # Mumbai — closest to Indian banks
        }
        if settings.s3_endpoint_url:
            # MinIO or other S3-compatible: set endpoint_url
            kwargs["endpoint_url"] = settings.s3_endpoint_url
        _s3_client = boto3.client("s3", **kwargs)
    return _s3_client


# ─── PATH CONSTRUCTORS ────────────────────────────────────────────────────────

def document_s3_key(case_id: uuid.UUID, doc_id: uuid.UUID) -> str:
    """S3 key for uploaded legal documents. Always UUID-based — never user input."""
    return f"cases/{case_id}/documents/{doc_id}.pdf"


def report_pdf_s3_key(case_id: uuid.UUID, report_id: uuid.UUID) -> str:
    """S3 key for generated PDF reports."""
    return f"cases/{case_id}/reports/{report_id}.pdf"


def report_json_s3_key(case_id: uuid.UUID, report_id: uuid.UUID) -> str:
    """S3 key for report JSON (stored alongside PDF for programmatic access)."""
    return f"cases/{case_id}/reports/{report_id}.json"


# ─── HASH ─────────────────────────────────────────────────────────────────────

def compute_sha256(file_bytes: bytes) -> str:
    """
    Compute SHA-256 hash of file bytes.
    Used for:
      1. Duplicate detection before upload (same hash + same case_id = 409)
      2. Document integrity verification after download
      3. Report tamper-evidence (hash stored in reports.content_hash)
    """
    return hashlib.sha256(file_bytes).hexdigest()


def compute_sha256_stream(file_obj: BinaryIO, chunk_size: int = 65536) -> str:
    """
    Compute SHA-256 from a file-like object without loading into memory.
    Use for large files (>10MB).
    """
    h = hashlib.sha256()
    while True:
        chunk = file_obj.read(chunk_size)
        if not chunk:
            break
        h.update(chunk)
    return h.hexdigest()


# ─── UPLOAD ──────────────────────────────────────────────────────────────────

async def upload_document(
    file_bytes: bytes,
    case_id:    uuid.UUID,
    doc_id:     uuid.UUID,
    content_type: str = "application/pdf",
) -> tuple[str, str]:
    """
    Upload a legal document to S3.
    Returns (s3_key, sha256_hash).

    Raises:
      HTTPException 413: file exceeds MAX_UPLOAD_SIZE_BYTES
      HTTPException 500: S3 upload failed

    SECURITY: S3 key is built from UUIDs only. No user input touches the path.
    SECURITY: File stored with ServerSideEncryption=AES256.
    SECURITY: No public ACL — bucket must be private.
    """
    if len(file_bytes) > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum size of {MAX_UPLOAD_SIZE_MB}MB."
        )

    file_hash = compute_sha256(file_bytes)
    s3_key    = document_s3_key(case_id, doc_id)

    try:
        get_s3_client().put_object(
            Bucket=settings.s3_bucket_name,
            Key=s3_key,
            Body=file_bytes,
            ContentType=content_type,
            ServerSideEncryption="AES256",   # always encrypt at rest
            Metadata={
                "case-id":     str(case_id),
                "doc-id":      str(doc_id),
                "sha256":      file_hash,
                "uploaded-at": _utc_now_str(),
            }
        )
        logger.info(f"Uploaded document {doc_id} for case {case_id} ({len(file_bytes)} bytes)")
        return s3_key, file_hash

    except ClientError as e:
        logger.error(f"S3 upload failed for doc {doc_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document storage failed. Please try again."
        )


async def upload_report_pdf(
    pdf_bytes:   bytes,
    case_id:     uuid.UUID,
    report_id:   uuid.UUID,
) -> str:
    """
    Upload a generated PDF report. Returns s3_key.
    Called from app/reports/generator.py after WeasyPrint generation.
    """
    s3_key = report_pdf_s3_key(case_id, report_id)
    try:
        get_s3_client().put_object(
            Bucket=settings.s3_bucket_name,
            Key=s3_key,
            Body=pdf_bytes,
            ContentType="application/pdf",
            ServerSideEncryption="AES256",
        )
        return s3_key
    except ClientError as e:
        logger.error(f"S3 upload failed for report PDF {report_id}: {e}")
        return None   # caller handles None gracefully — JSON-only fallback


async def upload_report_json(
    json_str:  str,
    case_id:   uuid.UUID,
    report_id: uuid.UUID,
) -> str:
    """Upload report JSON alongside PDF for programmatic access."""
    s3_key = report_json_s3_key(case_id, report_id)
    try:
        get_s3_client().put_object(
            Bucket=settings.s3_bucket_name,
            Key=s3_key,
            Body=json_str.encode("utf-8"),
            ContentType="application/json",
            ServerSideEncryption="AES256",
        )
        return s3_key
    except ClientError as e:
        logger.error(f"S3 JSON upload failed for report {report_id}: {e}")
        return None


# ─── DOWNLOAD ─────────────────────────────────────────────────────────────────

async def download_document(s3_key: str) -> bytes:
    """
    Download a document from S3 by its key.
    Used by: OCR service (passes bytes to Azure), report streamer.

    Raises:
      HTTPException 404: file not found in S3
      HTTPException 500: S3 download failed
    """
    try:
        response = get_s3_client().get_object(
            Bucket=settings.s3_bucket_name,
            Key=s3_key
        )
        return response["Body"].read()
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code in ("NoSuchKey", "404"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document not found in storage."
            )
        logger.error(f"S3 download failed for {s3_key}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document retrieval failed."
        )


async def stream_document(s3_key: str):
    """
    Stream document from S3 as a generator.
    More memory-efficient for large PDFs.
    Used by FastAPI StreamingResponse for report downloads.
    """
    try:
        response = get_s3_client().get_object(
            Bucket=settings.s3_bucket_name,
            Key=s3_key
        )
        body = response["Body"]
        while True:
            chunk = body.read(65536)  # 64KB chunks
            if not chunk:
                break
            yield chunk
    except ClientError as e:
        logger.error(f"S3 stream failed for {s3_key}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document streaming failed."
        )


# ─── INTEGRITY VERIFICATION ───────────────────────────────────────────────────

def verify_document_integrity(file_bytes: bytes, stored_hash: str) -> bool:
    """
    Verify downloaded bytes match the stored SHA-256 hash.
    Call this after download_document() before passing to OCR.
    Returns False if file has been tampered with — log and raise.
    """
    computed = compute_sha256(file_bytes)
    if computed != stored_hash:
        logger.critical(
            f"INTEGRITY VIOLATION: stored_hash={stored_hash!r}, "
            f"computed_hash={computed!r}. File may have been tampered."
        )
        return False
    return True


# ─── EXISTENCE CHECK ─────────────────────────────────────────────────────────

def document_exists(s3_key: str) -> bool:
    """
    Check if a document exists in S3 without downloading it.
    Used for duplicate detection by hash comparison at DB level (preferred),
    but this is the S3-level fallback.
    """
    try:
        get_s3_client().head_object(
            Bucket=settings.s3_bucket_name,
            Key=s3_key
        )
        return True
    except ClientError:
        return False


# ─── BUCKET SETUP ────────────────────────────────────────────────────────────

def ensure_bucket_exists() -> None:
    """
    Ensure the S3 bucket exists. Creates it if not.
    Called from app/main.py lifespan startup for MinIO dev environments.
    For AWS S3 production: bucket must exist before deploy — do not create programmatically.
    """
    if not settings.s3_endpoint_url:
        # AWS S3 production — bucket must be pre-created with correct IAM policies
        return

    # MinIO local dev — create bucket if it doesn't exist
    client = get_s3_client()
    try:
        client.head_bucket(Bucket=settings.s3_bucket_name)
    except ClientError:
        client.create_bucket(Bucket=settings.s3_bucket_name)
        logger.info(f"Created MinIO bucket: {settings.s3_bucket_name}")


# ─── CONSTANTS ───────────────────────────────────────────────────────────────

MAX_UPLOAD_SIZE_MB    = 25                          # covers exhibit-heavy SAs
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/tiff",   # some DRT documents are TIFF scans
}


def validate_file_type(content_type: str, filename: str) -> None:
    """
    Validate uploaded file is a permitted type.
    Checks Content-Type header AND file extension.
    Never trust Content-Type alone — clients can spoof it.

    Raises HTTPException 415 if not permitted.
    """
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type '{content_type}' not permitted. "
                   f"Allowed: PDF, JPEG, PNG, TIFF."
        )
    # Extension check as secondary validation
    allowed_ext = {".pdf", ".jpg", ".jpeg", ".png", ".tif", ".tiff"}
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in allowed_ext:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File extension '{ext}' not permitted."
        )


# ─── INTERNAL HELPERS ────────────────────────────────────────────────────────

def _utc_now_str() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()
```

## 25. Appendix: Reference Implementation — app/models/db.py

```python
# app/models/db.py
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

import hashlib
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

# Async engine — used by FastAPI route handlers via get_async_db()
async_engine = create_async_engine(
    settings.database_url,   # must be postgresql+asyncpg://...
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,   # recycle connections every 30 min
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,   # don't expire after commit — avoids lazy-load errors
    autoflush=False,
    autocommit=False,
)

# Sync engine — used by Celery workers via get_sync_db()
# Build sync URL from async URL: replace asyncpg driver with psycopg2
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
    """
    Base class for all ORM models.
    AsyncAttrs enables awaitable relationship access on async sessions.
    """
    pass


# ─── SESSION DEPENDENCIES ─────────────────────────────────────────────────────

@asynccontextmanager
async def get_async_db() -> AsyncSession:
    """
    Async session for FastAPI route handlers.
    Use as: async with get_async_db() as db:
    Or inject via Depends(get_async_db) in route signature.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@contextmanager
def get_sync_db() -> Session:
    """
    Sync session for Celery tasks.
    Celery workers are synchronous — never use async session in tasks.
    Use as: with get_sync_db() as db:
    """
    session = SyncSessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ─── MODELS ──────────────────────────────────────────────────────────────────

class Bank(Base):
    __tablename__ = "banks"

    id:         Mapped[uuid.UUID] = mapped_column(
                    UUID(as_uuid=True), primary_key=True,
                    default=uuid.uuid4
                )
    name:       Mapped[str]       = mapped_column(Text, nullable=False)
    short_code: Mapped[str]       = mapped_column(
                    String(20), nullable=False, unique=True
                )   # e.g. 'SBI', 'HDFC', 'PNB'
    active:     Mapped[bool]      = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime]  = mapped_column(
                    DateTime(timezone=True), server_default=func.now()
                )

    # Relationships
    users: Mapped[list[User]]     = relationship(
                    "User", back_populates="bank", lazy="selectin"
                )
    cases: Mapped[list[Case]]     = relationship(
                    "Case", back_populates="bank", lazy="selectin"
                )

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

    id:            Mapped[uuid.UUID] = mapped_column(
                       UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
                   )
    bank_id:       Mapped[uuid.UUID] = mapped_column(
                       UUID(as_uuid=True),
                       ForeignKey("banks.id", ondelete="RESTRICT"),
                       nullable=False
                   )
    email:         Mapped[str]       = mapped_column(
                       Text, nullable=False, unique=True
                   )
    password_hash: Mapped[str]       = mapped_column(Text, nullable=False)
    role:          Mapped[str]       = mapped_column(
                       String(20), nullable=False
                   )
    active:        Mapped[bool]      = mapped_column(Boolean, default=True)
    created_at:    Mapped[datetime]  = mapped_column(
                       DateTime(timezone=True), server_default=func.now()
                   )

    # Relationships
    bank:   Mapped[Bank]         = relationship("Bank", back_populates="users")
    cases:  Mapped[list[Case]]   = relationship(
                "Case", back_populates="created_by_user", lazy="selectin",
                foreign_keys="Case.created_by"
            )

    def __repr__(self) -> str:
        return f"<User {self.email} [{self.role}]>"


class Case(Base):
    __tablename__ = "cases"
    __table_args__ = (
        CheckConstraint(
            """status IN (
                'DRAFT','INTAKE_REJECTED','PROCESSING',
                'PENDING_HUMAN_REVIEW','ANALYSING',
                'PENDING_JUDGMENT_REVIEW','COMPLETE','FAILED'
            )""",
            name="cases_status_check"
        ),
        Index("idx_cases_bank_id", "bank_id"),
        Index("idx_cases_status", "status"),
    )

    id:                      Mapped[uuid.UUID]       = mapped_column(
                                 UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
                             )
    bank_id:                 Mapped[uuid.UUID]       = mapped_column(
                                 UUID(as_uuid=True),
                                 ForeignKey("banks.id", ondelete="RESTRICT"),
                                 nullable=False
                             )
    created_by:              Mapped[uuid.UUID]       = mapped_column(
                                 UUID(as_uuid=True),
                                 ForeignKey("users.id", ondelete="RESTRICT"),
                                 nullable=False
                             )
    case_ref:                Mapped[Optional[str]]   = mapped_column(Text)
    drt_case_number:         Mapped[Optional[str]]   = mapped_column(Text)
    drt_bench:               Mapped[Optional[str]]   = mapped_column(Text)
    borrower_name:           Mapped[str]             = mapped_column(Text, nullable=False)
    property_description:    Mapped[Optional[str]]   = mapped_column(Text)
    loan_account_number:     Mapped[Optional[str]]   = mapped_column(Text)
    principal_amount:        Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2))
    status:                  Mapped[str]             = mapped_column(
                                 String(30), nullable=False, default="DRAFT"
                             )
    pipeline_stage:          Mapped[Optional[str]]   = mapped_column(Text)
    intake_filter_result:    Mapped[Optional[dict]]  = mapped_column(JSONB)
    judgment_coverage_alerts: Mapped[Optional[list]] = mapped_column(JSONB)
    created_at:              Mapped[datetime]        = mapped_column(
                                 DateTime(timezone=True), server_default=func.now()
                             )
    updated_at:              Mapped[datetime]        = mapped_column(
                                 DateTime(timezone=True),
                                 server_default=func.now(),
                                 onupdate=func.now()
                             )

    # Relationships
    bank:             Mapped[Bank]                  = relationship("Bank", back_populates="cases")
    created_by_user:  Mapped[User]                  = relationship(
                          "User", back_populates="cases",
                          foreign_keys=[created_by]
                      )
    documents:        Mapped[list[Document]]        = relationship(
                          "Document", back_populates="case", lazy="selectin"
                      )
    case_facts:       Mapped[list[CaseFact]]        = relationship(
                          "CaseFact", back_populates="case", lazy="selectin"
                      )
    sa_grounds:       Mapped[list[SAGround]]        = relationship(
                          "SAGround", back_populates="case", lazy="selectin"
                      )
    compliance_results: Mapped[list[ComplianceResult]] = relationship(
                          "ComplianceResult", back_populates="case", lazy="selectin"
                      )
    ground_scores:    Mapped[list[GroundScore]]     = relationship(
                          "GroundScore", back_populates="case", lazy="selectin"
                      )
    reports:          Mapped[list[Report]]          = relationship(
                          "Report", back_populates="case", lazy="selectin"
                      )
    audit_logs:       Mapped[list[AuditLog]]        = relationship(
                          "AuditLog", back_populates="case", lazy="selectin"
                      )

    def __repr__(self) -> str:
        return f"<Case {self.id} [{self.status}] borrower={self.borrower_name}>"


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = (
        CheckConstraint(
            "ocr_status IN ('PENDING','PROCESSING','COMPLETE','FAILED')",
            name="documents_ocr_status_check"
        ),
        Index("idx_documents_case_id", "case_id"),
    )

    id:          Mapped[uuid.UUID]      = mapped_column(
                     UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
                 )
    case_id:     Mapped[uuid.UUID]      = mapped_column(
                     UUID(as_uuid=True),
                     ForeignKey("cases.id", ondelete="CASCADE"),
                     nullable=False
                 )
    uploaded_by: Mapped[uuid.UUID]      = mapped_column(
                     UUID(as_uuid=True),
                     ForeignKey("users.id", ondelete="RESTRICT"),
                     nullable=False
                 )
    doc_type:    Mapped[str]            = mapped_column(Text, nullable=False)
    file_url:    Mapped[str]            = mapped_column(Text, nullable=False)
    # IMMUTABLE: never UPDATE file_url or sha256_hash after insert
    sha256_hash: Mapped[str]            = mapped_column(Text, nullable=False)
    version:     Mapped[int]            = mapped_column(Integer, default=1)
    language:    Mapped[str]            = mapped_column(String(10), default="en")
    page_count:  Mapped[Optional[int]]  = mapped_column(Integer)
    ocr_status:  Mapped[str]            = mapped_column(
                     String(20), default="PENDING"
                 )
    uploaded_at: Mapped[datetime]       = mapped_column(
                     DateTime(timezone=True), server_default=func.now()
                 )

    # Relationships
    case:        Mapped[Case]             = relationship("Case", back_populates="documents")
    uploader:    Mapped[User]             = relationship("User")
    paragraphs:  Mapped[list[Paragraph]]  = relationship(
                     "Paragraph", back_populates="document", lazy="selectin"
                 )
    case_facts:  Mapped[list[CaseFact]]   = relationship(
                     "CaseFact", back_populates="source_document", lazy="selectin"
                 )

    def __repr__(self) -> str:
        return f"<Document {self.doc_type} [{self.ocr_status}]>"


class Paragraph(Base):
    __tablename__ = "paragraphs"
    __table_args__ = (
        Index("idx_paragraphs_document_id", "document_id"),
    )

    id:              Mapped[uuid.UUID]      = mapped_column(
                         UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
                     )
    document_id:     Mapped[uuid.UUID]      = mapped_column(
                         UUID(as_uuid=True),
                         ForeignKey("documents.id", ondelete="CASCADE"),
                         nullable=False
                     )
    page_number:     Mapped[int]            = mapped_column(Integer, nullable=False)
    para_sequence:   Mapped[int]            = mapped_column(Integer, nullable=False)
    # IMMUTABLE: text_original is raw OCR output — never modified after insert
    text_original:   Mapped[str]            = mapped_column(Text, nullable=False)
    # Additive only: text_translated is written once after IndicTrans2
    text_translated: Mapped[Optional[str]]  = mapped_column(Text)
    language:        Mapped[str]            = mapped_column(String(10), default="en")
    is_heading:      Mapped[bool]           = mapped_column(Boolean, default=False)
    is_numbered:     Mapped[bool]           = mapped_column(Boolean, default=False)
    is_handwritten:  Mapped[bool]           = mapped_column(Boolean, default=False)
    bbox:            Mapped[Optional[dict]] = mapped_column(JSONB)
    ocr_confidence:  Mapped[Optional[float]] = mapped_column(Float)
    created_at:      Mapped[datetime]       = mapped_column(
                         DateTime(timezone=True), server_default=func.now()
                     )

    # Relationships
    document: Mapped[Document] = relationship("Document", back_populates="paragraphs")

    def get_text(self) -> str:
        """Return translated text if available, else original."""
        return self.text_translated or self.text_original

    def __repr__(self) -> str:
        return f"<Paragraph page={self.page_number} seq={self.para_sequence}>"


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

    id:                  Mapped[uuid.UUID]       = mapped_column(
                             UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
                         )
    case_id:             Mapped[uuid.UUID]       = mapped_column(
                             UUID(as_uuid=True),
                             ForeignKey("cases.id", ondelete="CASCADE"),
                             nullable=False
                         )
    field_name:          Mapped[str]             = mapped_column(Text, nullable=False)
    field_value:         Mapped[Optional[str]]   = mapped_column(Text)
    # All values stored as TEXT. Typed at application layer by CaseFactSchema.
    confidence:          Mapped[Optional[float]] = mapped_column(Float)
    source_document_id:  Mapped[Optional[uuid.UUID]] = mapped_column(
                             UUID(as_uuid=True),
                             ForeignKey("documents.id", ondelete="SET NULL")
                         )
    source_page:         Mapped[Optional[int]]   = mapped_column(Integer)
    source_paragraph_id: Mapped[Optional[uuid.UUID]] = mapped_column(
                             UUID(as_uuid=True),
                             ForeignKey("paragraphs.id", ondelete="SET NULL")
                         )
    extraction_method:   Mapped[Optional[str]]   = mapped_column(String(20))
    human_confirmed:     Mapped[bool]            = mapped_column(Boolean, default=False)
    confirmed_by:        Mapped[Optional[uuid.UUID]] = mapped_column(
                             UUID(as_uuid=True),
                             ForeignKey("users.id", ondelete="SET NULL")
                         )
    confirmed_at:        Mapped[Optional[datetime]] = mapped_column(
                             DateTime(timezone=True)
                         )
    created_at:          Mapped[datetime]        = mapped_column(
                             DateTime(timezone=True), server_default=func.now()
                         )

    # Relationships
    case:             Mapped[Case]                  = relationship("Case", back_populates="case_facts")
    source_document:  Mapped[Optional[Document]]    = relationship("Document", back_populates="case_facts")
    source_paragraph: Mapped[Optional[Paragraph]]   = relationship("Paragraph")
    confirming_user:  Mapped[Optional[User]]        = relationship("User")

    @property
    def requires_workbench(self) -> bool:
        """True if this fact needs human review before pipeline can proceed."""
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


# Fields that always require human confirmation regardless of confidence
ALWAYS_HUMAN_CONFIRM_FIELDS = {
    "valuer_rbi_empanelled",
    "valuer_section_247_registered",
    "udyam_cert_in_bank_file",
    "total_borrowers_in_loan",
    "total_guarantors_in_loan",
}

class FactConflict(Base):
    __tablename__ = "fact_conflicts"
    __table_args__ = (
        UniqueConstraint("case_id", "field_name", name="fact_conflicts_case_id_field_name_key"),
        Index("idx_fact_conflicts_case", "case_id", "resolved"),
    )

    id:                            Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id:                       Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    field_name:                    Mapped[str]             = mapped_column(Text, nullable=False)
    candidate_a_value:             Mapped[Optional[str]]   = mapped_column(Text)
    candidate_a_source_doc_id:     Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"))
    candidate_a_source_page:       Mapped[Optional[int]]   = mapped_column(Integer)
    candidate_a_extraction_method: Mapped[Optional[str]]   = mapped_column(Text)
    candidate_b_value:             Mapped[Optional[str]]   = mapped_column(Text)
    candidate_b_source_doc_id:     Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"))
    candidate_b_source_page:       Mapped[Optional[int]]   = mapped_column(Integer)
    candidate_b_extraction_method: Mapped[Optional[str]]   = mapped_column(Text)
    resolved:                      Mapped[bool]            = mapped_column(Boolean, default=False)
    resolved_value:                Mapped[Optional[str]]   = mapped_column(Text)
    resolved_by:                   Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    resolved_at:                   Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at:                    Mapped[datetime]        = mapped_column(DateTime(timezone=True), server_default=func.now())

ALWAYS_HUMAN_CONFIRM_FIELDS = {
    "valuer_rbi_empanelled",
    "valuer_section_247_registered",
    "udyam_cert_in_bank_file",
    "total_borrowers_in_loan",
    "total_guarantors_in_loan",
}


class SAGround(Base):
    __tablename__ = "sa_grounds"
    __table_args__ = (
        Index("idx_sa_grounds_case_id", "case_id"),
    )

    id:                     Mapped[uuid.UUID]       = mapped_column(
                                UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
                            )
    case_id:                Mapped[uuid.UUID]       = mapped_column(
                                UUID(as_uuid=True),
                                ForeignKey("cases.id", ondelete="CASCADE"),
                                nullable=False
                            )
    ground_code:            Mapped[str]             = mapped_column(Text, nullable=False)
    statutory_basis:        Mapped[Optional[str]]   = mapped_column(Text)
    source_paragraph_id:    Mapped[Optional[uuid.UUID]] = mapped_column(
                                UUID(as_uuid=True),
                                ForeignKey("paragraphs.id", ondelete="SET NULL")
                            )
    factual_claim_extracted: Mapped[Optional[str]]  = mapped_column(Text)
    documents_cited:        Mapped[Optional[list]]  = mapped_column(ARRAY(Text))
    confidence:             Mapped[Optional[float]] = mapped_column(Float)
    created_at:             Mapped[datetime]        = mapped_column(
                                DateTime(timezone=True), server_default=func.now()
                            )

    # Relationships
    case:             Mapped[Case]                = relationship("Case", back_populates="sa_grounds")
    source_paragraph: Mapped[Optional[Paragraph]] = relationship("Paragraph")

    def __repr__(self) -> str:
        return f"<SAGround {self.ground_code} [{self.confidence:.2f}]>"


class ComplianceResult(Base):
    __tablename__ = "compliance_results"
    __table_args__ = (
        CheckConstraint(
            "status IN ('PASS','FAIL','UNKNOWN')",
            name="compliance_results_status_check"
        ),
        CheckConstraint(
            """severity IN (
                'FATAL','ABSOLUTE_BAR','CURABLE','MINOR',
                'ADVISORY','REVIEW_REQUIRED','UNKNOWN'
            )""",
            name="compliance_results_severity_check"
        ),
        Index("idx_compliance_case_id", "case_id"),
    )

    id:           Mapped[uuid.UUID]       = mapped_column(
                      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
                  )
    case_id:      Mapped[uuid.UUID]       = mapped_column(
                      UUID(as_uuid=True),
                      ForeignKey("cases.id", ondelete="CASCADE"),
                      nullable=False
                  )
    rule_id:      Mapped[str]             = mapped_column(Text, nullable=False)
    module:       Mapped[str]             = mapped_column(Text, nullable=False)
    status:       Mapped[str]             = mapped_column(String(10), nullable=False)
    severity:     Mapped[Optional[str]]   = mapped_column(String(20))
    message:      Mapped[Optional[str]]   = mapped_column(Text)
    detail_json:  Mapped[Optional[dict]]  = mapped_column(JSONB)
    judgment_tags: Mapped[Optional[list]] = mapped_column(ARRAY(Text))
    evaluated_at: Mapped[datetime]        = mapped_column(
                      DateTime(timezone=True), server_default=func.now()
                  )

    # Relationships
    case: Mapped[Case] = relationship("Case", back_populates="compliance_results")

    def __repr__(self) -> str:
        return f"<ComplianceResult {self.rule_id} [{self.status}/{self.severity}]>"


class Judgment(Base):
    __tablename__ = "judgments"
    __table_args__ = (
        CheckConstraint(
            "court IN ('SUPREME_COURT','HIGH_COURT','DRAT','DRT')",
            name="judgments_court_check"
        ),
        CheckConstraint(
            "favor IN ('BANK','BORROWER','NEUTRAL')",
            name="judgments_favor_check"
        ),
    )

    id:                    Mapped[uuid.UUID]       = mapped_column(
                               UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
                           )
    citation:              Mapped[str]             = mapped_column(
                               Text, nullable=False, unique=True
                           )
    title:                 Mapped[str]             = mapped_column(Text, nullable=False)
    short_name:            Mapped[Optional[str]]   = mapped_column(Text)
    court:                 Mapped[str]             = mapped_column(String(20), nullable=False)
    high_court_state:      Mapped[Optional[str]]   = mapped_column(Text)
    bench_strength:        Mapped[int]             = mapped_column(Integer, default=1)
    judgment_date:         Mapped[Optional[date]]  = mapped_column(Date)
    overruled:             Mapped[bool]            = mapped_column(Boolean, default=False)
    overruled_by:          Mapped[Optional[uuid.UUID]] = mapped_column(
                               UUID(as_uuid=True),
                               ForeignKey("judgments.id", ondelete="SET NULL")
                           )
    favor:                 Mapped[Optional[str]]   = mapped_column(String(10))
    favor_verified:        Mapped[bool]            = mapped_column(Boolean, default=False)
    ground_codes:          Mapped[Optional[list]]  = mapped_column(ARRAY(Text))
    holding_summary:       Mapped[Optional[str]]   = mapped_column(Text)
    applicable_conditions: Mapped[Optional[list]]  = mapped_column(JSONB)
    exclusion_conditions:  Mapped[Optional[list]]  = mapped_column(JSONB)
    added_by:              Mapped[Optional[uuid.UUID]] = mapped_column(
                               UUID(as_uuid=True),
                               ForeignKey("users.id", ondelete="SET NULL")
                           )
    added_at:              Mapped[datetime]        = mapped_column(
                               DateTime(timezone=True), server_default=func.now()
                           )
    last_reviewed_at:      Mapped[Optional[datetime]] = mapped_column(
                               DateTime(timezone=True)
                           )

    def __repr__(self) -> str:
        return f"<Judgment {self.citation}>"


class JudgmentApplicability(Base):
    __tablename__ = "judgment_applicability"
    __table_args__ = (
        CheckConstraint(
            """status IN (
                'APPLICABLE','PARTIAL','NOT_APPLICABLE',
                'SIMILARITY_RETRIEVED','LEGAL_UNCERTAINTY','UNAVAILABLE'
            )""",
            name="judgment_applicability_status_check"
        ),
    )

    id:           Mapped[uuid.UUID]       = mapped_column(
                      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
                  )
    case_id:      Mapped[uuid.UUID]       = mapped_column(
                      UUID(as_uuid=True),
                      ForeignKey("cases.id", ondelete="CASCADE"),
                      nullable=False
                  )
    judgment_id:  Mapped[uuid.UUID]       = mapped_column(
                      UUID(as_uuid=True),
                      ForeignKey("judgments.id", ondelete="CASCADE"),
                      nullable=False
                  )
    ground_code:  Mapped[Optional[str]]   = mapped_column(Text)
    status:       Mapped[Optional[str]]   = mapped_column(String(25))
    reason:       Mapped[Optional[str]]   = mapped_column(Text)
    evaluated_at: Mapped[datetime]        = mapped_column(
                      DateTime(timezone=True), server_default=func.now()
                  )

    # Relationships
    judgment: Mapped[Judgment] = relationship("Judgment")


class GroundScore(Base):
    __tablename__ = "ground_scores"
    __table_args__ = (
        Index("idx_ground_scores_case_id", "case_id"),
    )

    id:              Mapped[uuid.UUID]       = mapped_column(
                         UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
                     )
    case_id:         Mapped[uuid.UUID]       = mapped_column(
                         UUID(as_uuid=True),
                         ForeignKey("cases.id", ondelete="CASCADE"),
                         nullable=False
                     )
    ground_code:     Mapped[str]             = mapped_column(Text, nullable=False)
    factual_score:   Mapped[Optional[float]] = mapped_column(Float)
    judicial_score:  Mapped[Optional[float]] = mapped_column(Float)
    ground_strength: Mapped[Optional[float]] = mapped_column(Float)
    corpus_total:          Mapped[int]       = mapped_column(Integer, default=0)
    corpus_borrower_wins:  Mapped[int]       = mapped_column(Integer, default=0)
    corpus_bank_wins:      Mapped[int]       = mapped_column(Integer, default=0)
    corpus_confidence:     Mapped[str]       = mapped_column(Text, default="NO_DATA")
    evaluated_at:    Mapped[datetime]        = mapped_column(
                         DateTime(timezone=True), server_default=func.now()
                     )

    # Relationships
    case: Mapped[Case] = relationship("Case", back_populates="ground_scores")

    def __repr__(self) -> str:
        return f"<GroundScore {self.ground_code}={self.ground_strength:.3f}>"


class Report(Base):
    __tablename__ = "reports"

    id:                  Mapped[uuid.UUID]       = mapped_column(
                             UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
                         )
    case_id:             Mapped[uuid.UUID]       = mapped_column(
                             UUID(as_uuid=True),
                             ForeignKey("cases.id", ondelete="CASCADE"),
                             nullable=False
                         )
    compliance_score:    Mapped[Optional[int]]   = mapped_column(Integer)
    litigation_exposure: Mapped[Optional[float]] = mapped_column(Float)
    recommendation:      Mapped[Optional[str]]   = mapped_column(Text)
    report_json:         Mapped[Optional[dict]]  = mapped_column(JSONB)
    pdf_url:             Mapped[Optional[str]]   = mapped_column(Text)
    content_hash:        Mapped[Optional[str]]   = mapped_column(Text)
    generated_by:        Mapped[Optional[uuid.UUID]] = mapped_column(
                             UUID(as_uuid=True),
                             ForeignKey("users.id", ondelete="SET NULL")
                         )
    generated_at:        Mapped[datetime]        = mapped_column(
                             DateTime(timezone=True), server_default=func.now()
                         )

    # Relationships
    case:          Mapped[Case]          = relationship("Case", back_populates="reports")
    generated_user: Mapped[Optional[User]] = relationship("User")

    def __repr__(self) -> str:
        return f"<Report {self.id} score={self.compliance_score}>"


class AuditLog(Base):
    __tablename__ = "audit_log"
    __table_args__ = (
        Index("idx_audit_case_id", "case_id"),
        Index("idx_audit_user_id", "user_id"),
    )

    id:         Mapped[uuid.UUID]       = mapped_column(
                    UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
                )
    case_id:    Mapped[Optional[uuid.UUID]] = mapped_column(
                    UUID(as_uuid=True),
                    ForeignKey("cases.id", ondelete="SET NULL")
                )
    user_id:    Mapped[Optional[uuid.UUID]] = mapped_column(
                    UUID(as_uuid=True),
                    ForeignKey("users.id", ondelete="SET NULL")
                )
    action:     Mapped[str]             = mapped_column(Text, nullable=False)
    # Valid actions: LOGIN, CREATE_CASE, UPLOAD_DOCUMENT, CONFIRM_FACT,
    #                OVERRIDE_FACT, TRIGGER_ANALYSIS, GENERATE_REPORT,
    #                DOWNLOAD_REPORT, RESUME_ANALYSIS
    detail:     Mapped[Optional[dict]]  = mapped_column(JSONB)
    ip_address: Mapped[Optional[str]]   = mapped_column(String(45))  # IPv6 max length
    created_at: Mapped[datetime]        = mapped_column(
                    DateTime(timezone=True), server_default=func.now()
                )

    # Relationships
    case: Mapped[Optional[Case]] = relationship("Case", back_populates="audit_logs")
    user: Mapped[Optional[User]] = relationship("User")

    def __repr__(self) -> str:
        return f"<AuditLog {self.action} user={self.user_id}>"


class CaseStatute(Base):
    __tablename__ = "case_statutes"
    __table_args__ = (
        Index("idx_case_statutes_case_id", "case_id"),
    )

    id:             Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id:        Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    rule_id:        Mapped[str]             = mapped_column(Text, nullable=False)
    section_number: Mapped[str]             = mapped_column(Text, nullable=False)
    act_name:       Mapped[str]             = mapped_column(Text, nullable=False)
    statute_text:   Mapped[str]             = mapped_column(Text, nullable=False)
    retrieved_at:   Mapped[datetime]        = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    case: Mapped[Case] = relationship("Case")

    def __repr__(self) -> str:
        return f"<CaseStatute {self.rule_id} -> {self.act_name} Sec {self.section_number}>"


# ─── AUDIT LOG HELPER ─────────────────────────────────────────────────────────

async def write_audit_log(
    db: AsyncSession,
    action: str,
    user_id: uuid.UUID | None = None,
    case_id: uuid.UUID | None = None,
    detail:  dict | None = None,
    ip_address: str | None = None,
) -> None:
    """
    Write an audit log entry. Call this from every state-changing route handler.
    Use async version for FastAPI routes, sync version below for Celery tasks.
    """
    log = AuditLog(
        action=action,
        user_id=user_id,
        case_id=case_id,
        detail=detail or {},
        ip_address=ip_address,
    )
    db.add(log)
    # Do not commit — caller commits as part of the same transaction


def write_audit_log_sync(
    db: Session,
    action: str,
    user_id: uuid.UUID | None = None,
    case_id: uuid.UUID | None = None,
    detail:  dict | None = None,
) -> None:
    """Sync version for Celery task audit logging."""
    log = AuditLog(
        action=action,
        user_id=user_id,
        case_id=case_id,
        detail=detail or {},
    )
    db.add(log)
```


## 26. Appendix: Reference Implementation — app/dependencies.py

```python
# app/dependencies.py
"""
FastAPI dependencies — injected via Depends() in route handlers.

THREE RULES that must never be broken:
  1. bank_id always comes from JWT — never from request body or path params
  2. Every DB query on case data includes bank_id filter
  3. require_role() is declared on the route, not checked inside the service
"""

from __future__ import annotations

import uuid
import logging
from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.db import AsyncSessionLocal, User

logger = logging.getLogger(__name__)

# ─── HTTP BEARER ──────────────────────────────────────────────────────────────

# auto_error=False — we return our own 401 with a clear message
_bearer = HTTPBearer(auto_error=False)


# ─── DATABASE ─────────────────────────────────────────────────────────────────

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Async DB session dependency for FastAPI route handlers.
    Injects as: db: AsyncSession = Depends(get_db)

    Commits on successful response, rolls back on exception.
    expire_on_commit=False is set on the sessionmaker so accessing
    ORM attributes after commit works without re-querying.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# ─── CURRENT USER ─────────────────────────────────────────────────────────────

class CurrentUser:
    """
    Typed container for the authenticated user context.
    Extracted from JWT — no DB query needed for auth on every request.
    """
    def __init__(self, payload: dict):
        self.user_id: uuid.UUID = uuid.UUID(payload["sub"])
        self.bank_id: uuid.UUID = uuid.UUID(payload["bank_id"])
        self.role:    str       = payload["role"]
        self.email:   str       = payload.get("email", "")

    def __repr__(self) -> str:
        return f"<CurrentUser {self.email} [{self.role}] bank={self.bank_id}>"


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)]
) -> CurrentUser:
    """
    Decode JWT and return CurrentUser.
    Raises 401 for missing, expired, or invalid tokens.

    NEVER call this with an expired token expecting a refresh —
    use POST /auth/refresh while the token is still valid.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Provide a Bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        # Validate required claims are present
        for claim in ("sub", "bank_id", "role"):
            if claim not in payload:
                raise JWTError(f"Missing claim: {claim}")

        return CurrentUser(payload)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        logger.warning(f"JWT validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ─── ROLE ENFORCEMENT ────────────────────────────────────────────────────────

def require_role(*allowed_roles: str):
    """
    Role-based access control dependency factory.
    Declare on the route — not checked inside service functions.

    Usage:
        @router.post("/admin/users")
        async def create_user(
            user: CurrentUser = Depends(require_role("BANK_ADMIN", "SYSTEM_ADMIN"))
        ):

    Role hierarchy (highest to lowest):
        SYSTEM_ADMIN  — full access across all banks
        BANK_ADMIN    — full access within their bank
        BANK_OFFICER  — read/write within their bank, no admin actions
    """
    async def _check(
        current_user: CurrentUser = Depends(get_current_user)
    ) -> CurrentUser:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires role: {' or '.join(allowed_roles)}. "
                       f"Your role: {current_user.role}."
            )
        return current_user
    return _check


# ─── BANK-SCOPED CASE GUARD ──────────────────────────────────────────────────

async def verify_case_bank_access(
    case_id: uuid.UUID,
    current_user: CurrentUser,
    db: AsyncSession,
):
    """
    Verify that a case belongs to the current user's bank.
    Call this inside every route handler that operates on a specific case.

    Returns the Case ORM object if access is permitted.
    Raises 404 (not 403) — we do not reveal that a case exists in another bank.

    Usage in route handler:
        case = await verify_case_bank_access(case_id, current_user, db)
    """
    from app.models.db import Case
    from sqlalchemy import select

    result = await db.execute(
        select(Case).where(
            Case.id == case_id,
            Case.bank_id == current_user.bank_id  # ← THE CRITICAL FILTER
        )
    )
    case = result.scalar_one_or_none()
    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case {case_id} not found."
            # Intentionally vague — do not say "access denied"
        )
    return case


# ─── CLIENT IP ────────────────────────────────────────────────────────────────

def get_client_ip(request: Request) -> str:
    """
    Extract client IP from request for audit logging.
    Handles X-Forwarded-For header when behind nginx/proxy.
    """
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # X-Forwarded-For: client, proxy1, proxy2
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


# ─── TYPE ALIASES (for cleaner route signatures) ──────────────────────────────

DbDep          = Annotated[AsyncSession, Depends(get_db)]
CurrentUserDep = Annotated[CurrentUser,  Depends(get_current_user)]
AdminDep       = Annotated[CurrentUser,  Depends(require_role("BANK_ADMIN", "SYSTEM_ADMIN"))]
OfficerDep     = Annotated[CurrentUser,  Depends(require_role("BANK_OFFICER", "BANK_ADMIN", "SYSTEM_ADMIN"))]


```

## 27. Appendix: Reference Implementation — app/api/auth.py

```python

# app/api/auth.py
"""
Authentication endpoints.

POST /api/v1/auth/register  — create bank + first BANK_ADMIN user (seed equivalent via API)
POST /api/v1/auth/login     — email + password → JWT
POST /api/v1/auth/refresh   — re-issue 8-hour token while current token is valid
POST /api/v1/auth/users     — BANK_ADMIN creates additional users in their bank

SECURITY DECISIONS:
  - Passwords hashed with bcrypt (passlib), rounds=12
  - JWT is stateless — no server-side session storage
  - Refresh only works on VALID (non-expired) tokens — expired = must re-login
  - Failed login attempts are audit-logged with IP address
  - bank_id on new users ALWAYS comes from JWT of creating admin, never from body
  - Register endpoint is open (no auth) — intended for onboarding new banks.
    When scaling to production, protect this endpoint behind an IP allowlist
    or add a SYSTEM_ADMIN pre-approval step.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.dependencies import (
    AdminDep, CurrentUserDep, DbDep, get_client_ip, get_current_user, get_db
)
from app.models.db import AuditLog, Bank, User, write_audit_log

logger = logging.getLogger(__name__)
router = APIRouter()

# ─── PASSWORD HASHING ────────────────────────────────────────────────────────

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,   # 12 rounds: ~250ms on modern hardware — balances security/speed
)


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ─── JWT ──────────────────────────────────────────────────────────────────────

def create_access_token(user: User) -> tuple[str, datetime]:
    """
    Create an 8-hour JWT access token.
    Payload: sub (user_id), bank_id, role, email, exp, iat.
    Returns (token_string, expiry_datetime).
    """
    now    = datetime.now(timezone.utc)
    expiry = now + timedelta(minutes=settings.jwt_expire_minutes)   # 480 min = 8 hours

    payload = {
        "sub":      str(user.id),
        "bank_id":  str(user.bank_id),
        "role":     user.role,
        "email":    user.email,
        "iat":      int(now.timestamp()),
        "exp":      int(expiry.timestamp()),
    }
    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return token, expiry


# ─── REQUEST / RESPONSE SCHEMAS ──────────────────────────────────────────────

class RegisterRequest(BaseModel):
    """
    Create a new bank + its first BANK_ADMIN user in one transaction.
    This is the entry point for onboarding a new bank to SLRAI.
    """
    bank_name:       str       = Field(..., min_length=2, max_length=200)
    bank_short_code: str       = Field(..., min_length=2, max_length=10,
                                       pattern=r'^[A-Z0-9]+$')
    # short_code must be uppercase alphanumeric: SBI, HDFC, PNB
    admin_email:     EmailStr
    admin_password:  str       = Field(..., min_length=8)

    @field_validator("admin_password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit.")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter.")
        return v


class LoginRequest(BaseModel):
    email:    EmailStr
    password: str


class CreateUserRequest(BaseModel):
    """
    BANK_ADMIN creates additional users within their bank.
    bank_id is NOT in this schema — it comes from the admin's JWT.
    """
    email:    EmailStr
    password: str       = Field(..., min_length=8)
    role:     str       = Field(..., pattern=r'^(BANK_OFFICER|BANK_ADMIN)$')
    # SYSTEM_ADMIN cannot be created via API — only via seed script

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit.")
        return v


class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    expires_at:   datetime
    user_id:      str
    bank_id:      str
    role:         str
    email:        str


class UserResponse(BaseModel):
    id:         uuid.UUID
    email:      str
    role:       str
    bank_id:    uuid.UUID
    active:     bool
    created_at: datetime


# ─── ENDPOINTS ────────────────────────────────────────────────────────────────

@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new bank + admin user",
    description=(
        "Creates a new bank and its first BANK_ADMIN user in a single transaction. "
        "Returns a JWT token — the admin is automatically logged in. "
        "NOTE: Protect this endpoint with IP allowlist in production."
    ),
)
async def register(
    body:    RegisterRequest,
    request: Request,
    db:      DbDep,
) -> TokenResponse:
    # Check bank short_code not already taken
    existing_bank = await db.execute(
        select(Bank).where(Bank.short_code == body.bank_short_code.upper())
    )
    if existing_bank.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Bank with code '{body.bank_short_code}' already exists."
        )

    # Check email not already taken
    existing_user = await db.execute(
        select(User).where(User.email == body.admin_email.lower())
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists."
        )

    # Create bank + admin user in one transaction
    bank = Bank(
        name=body.bank_name,
        short_code=body.bank_short_code.upper(),
        active=True,
    )
    db.add(bank)
    await db.flush()   # flush to get bank.id before creating user

    admin = User(
        bank_id=bank.id,
        email=body.admin_email.lower(),
        password_hash=hash_password(body.admin_password),
        role="BANK_ADMIN",
        active=True,
    )
    db.add(admin)
    await db.flush()   # flush to get admin.id before audit log

    # Audit log
    await write_audit_log(
        db,
        action="REGISTER",
        user_id=admin.id,
        detail={"bank_name": body.bank_name, "bank_short_code": body.bank_short_code},
        ip_address=get_client_ip(request),
    )

    # commit happens via get_db() dependency on response

    token, expiry = create_access_token(admin)

    logger.info(f"New bank registered: {bank.short_code} | admin: {admin.email}")

    return TokenResponse(
        access_token=token,
        expires_at=expiry,
        user_id=str(admin.id),
        bank_id=str(admin.bank_id),
        role=admin.role,
        email=admin.email,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login with email and password",
)
async def login(
    body:    LoginRequest,
    request: Request,
    db:      DbDep,
) -> TokenResponse:
    client_ip = get_client_ip(request)

    # Fetch user — always look up by lowercase email
    result = await db.execute(
        select(User).where(User.email == body.email.lower())
    )
    user = result.scalar_one_or_none()

    # SECURITY: Use constant-time comparison regardless of whether user exists.
    # If user doesn't exist, we still call verify_password with a dummy hash
    # to prevent timing attacks that reveal valid email addresses.
    _dummy_hash = "$2b$12$invalidhashfortimingequalisation"
    password_ok = verify_password(
        body.password,
        user.password_hash if user else _dummy_hash
    )

    if not user or not password_ok or not user.active:
        # Log failed attempt with IP for security monitoring
        if user:
            await write_audit_log(
                db,
                action="LOGIN_FAILED",
                user_id=user.id,
                detail={"reason": "wrong_password" if not password_ok else "inactive_account"},
                ip_address=client_ip,
            )
        logger.warning(f"Failed login for email={body.email!r} from IP={client_ip}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            # Intentionally vague — do not reveal which is wrong
        )

    # Successful login
    token, expiry = create_access_token(user)

    await write_audit_log(
        db,
        action="LOGIN",
        user_id=user.id,
        detail={"bank_id": str(user.bank_id)},
        ip_address=client_ip,
    )

    logger.info(f"Login: {user.email} [{user.role}] from {client_ip}")

    return TokenResponse(
        access_token=token,
        expires_at=expiry,
        user_id=str(user.id),
        bank_id=str(user.bank_id),
        role=user.role,
        email=user.email,
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description=(
        "Re-issues a fresh 8-hour token. "
        "Token must be currently VALID (not expired) — expired tokens cannot be refreshed. "
        "Call this when the token has ≤60 minutes remaining to avoid session interruption. "
        "Can also be called at any point during a valid session to extend it."
    ),
)
async def refresh_token(
    current_user: CurrentUserDep,
    db:           DbDep,
) -> TokenResponse:
    """
    Strategy (Option C): Re-issue fresh 8-hour token whenever a valid token calls this.
    This is simple and correct — no complex refresh token rotation needed for
    an internal bank tool with 8-hour sessions.

    The dependency `CurrentUserDep` validates the token first — expired tokens
    raise 401 before reaching this handler.
    """
    # Load fresh user state from DB (role may have changed since token was issued)
    result = await db.execute(
        select(User).where(
            User.id == current_user.user_id,
            User.active == True
        )
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account not found or deactivated."
        )

    # Issue fresh 8-hour token with current DB state
    token, expiry = create_access_token(user)

    return TokenResponse(
        access_token=token,
        expires_at=expiry,
        user_id=str(user.id),
        bank_id=str(user.bank_id),
        role=user.role,
        email=user.email,
    )


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user in the admin's bank",
    description=(
        "BANK_ADMIN or SYSTEM_ADMIN only. "
        "Creates a BANK_OFFICER or BANK_ADMIN user. "
        "bank_id is always taken from the creating admin's JWT — never from request body."
    ),
)
async def create_user(
    body:  CreateUserRequest,
    admin: AdminDep,
    db:    DbDep,
) -> UserResponse:
    # Check email uniqueness
    existing = await db.execute(
        select(User).where(User.email == body.email.lower())
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists."
        )

    # SYSTEM_ADMIN can create users in any bank (bank_id would need to be
    # specified — leave this for the scaling phase where admin UI is built)
    # For now: all created users belong to the creating admin's bank
    new_user = User(
        bank_id=admin.bank_id,     # ← FROM JWT, never from body
        email=body.email.lower(),
        password_hash=hash_password(body.password),
        role=body.role,
        active=True,
    )
    db.add(new_user)
    await db.flush()

    await write_audit_log(
        db,
        action="CREATE_USER",
        user_id=admin.user_id,
        detail={
            "new_user_email": body.email,
            "new_user_role":  body.role,
            "bank_id":        str(admin.bank_id),
        },
    )

    logger.info(
        f"User created: {new_user.email} [{new_user.role}] "
        f"by admin {admin.email} in bank {admin.bank_id}"
    )

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        role=new_user.role,
        bank_id=new_user.bank_id,
        active=new_user.active,
        created_at=new_user.created_at,
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
async def get_me(
    current_user: CurrentUserDep,
    db:           DbDep,
) -> UserResponse:
    """Returns the authenticated user's profile from DB (not just JWT payload)."""
    result = await db.execute(
        select(User).where(User.id == current_user.user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        bank_id=user.bank_id,
        active=user.active,
        created_at=user.created_at,
    )
```

## 28. Appendix: Reference Implementation — app/api/case.py

```python

# app/api/cases.py
"""
Case management endpoints.

BANK ISOLATION RULE (enforced here, not in services):
  Every query includes: WHERE bank_id = current_user.bank_id
  This is the single most important security property in the system.
  A bank officer must never see another bank's cases — not even via case_id guessing.
  We return 404 (not 403) when a case exists but belongs to another bank.
  This prevents information leakage about what cases exist.

VISIBILITY: All users (BANK_OFFICER, BANK_ADMIN) see ALL cases in their bank.
            SYSTEM_ADMIN can see across banks (not implemented in V1 — placeholder noted).

PIPELINE TRIGGER: Chain A fires from documents.py on first document upload.
                  Case creation only creates the record and runs F2 pre-intake filter.
                  F1, F3, F4 filters run during Chain A after document processing.
"""

from __future__ import annotations

import logging
import math
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import (
    CurrentUserDep, DbDep, OfficerDep, AdminDep,
    get_client_ip, verify_case_bank_access,
)
from app.models.db import AuditLog, Case, write_audit_log
from app.services.compliance.pre_intake import IntakeFilterResult, run_f2_filter

logger = logging.getLogger(__name__)
router = APIRouter()


# ─── REQUEST / RESPONSE SCHEMAS ──────────────────────────────────────────────

class CreateCaseRequest(BaseModel):
    """
    bank_id is NOT here — comes from JWT always.
    Only F2 filter (principal_amount < Rs. 1 lakh) can run at creation time.
    F1 (agricultural land), F3 (>80% repaid), F4 (IBC moratorium) require documents.
    """
    borrower_name:        str           = Field(..., min_length=2, max_length=500)
    case_ref:             Optional[str] = Field(None, max_length=100)
    drt_case_number:      Optional[str] = Field(None, max_length=100)
    drt_bench:            Optional[str] = Field(None, max_length=200)
    property_description: Optional[str] = Field(None, max_length=2000)
    loan_account_number:  Optional[str] = Field(None, max_length=100)
    principal_amount:     Optional[Decimal] = Field(None, ge=0)


class UpdateCaseRequest(BaseModel):
    """Metadata-only updates. Status is never set by the client directly."""
    case_ref:             Optional[str] = Field(None, max_length=100)
    drt_case_number:      Optional[str] = Field(None, max_length=100)
    drt_bench:            Optional[str] = Field(None, max_length=200)
    property_description: Optional[str] = Field(None, max_length=2000)
    loan_account_number:  Optional[str] = Field(None, max_length=100)


class CaseResponse(BaseModel):
    id:                       uuid.UUID
    bank_id:                  uuid.UUID
    created_by:               uuid.UUID
    borrower_name:            str
    case_ref:                 Optional[str]
    drt_case_number:          Optional[str]
    drt_bench:                Optional[str]
    property_description:     Optional[str]
    loan_account_number:      Optional[str]
    principal_amount:         Optional[Decimal]
    status:                   str
    pipeline_stage:           Optional[str]
    intake_filter_result:     Optional[dict]
    judgment_coverage_alerts: Optional[list]
    created_at:               datetime
    updated_at:               datetime

    model_config = {"from_attributes": True}


class CaseSummaryResponse(BaseModel):
    """Lightweight response for list endpoint — excludes heavy JSONB fields."""
    id:             uuid.UUID
    borrower_name:  str
    case_ref:       Optional[str]
    drt_case_number: Optional[str]
    status:         str
    pipeline_stage: Optional[str]
    created_at:     datetime

    model_config = {"from_attributes": True}


class CaseListResponse(BaseModel):
    items:       list[CaseSummaryResponse]
    total:       int
    page:        int
    page_size:   int
    total_pages: int


class PipelineStatusResponse(BaseModel):
    case_id:        uuid.UUID
    status:         str
    pipeline_stage: Optional[str]
    progress_pct:   int
    message:        str


# ─── PIPELINE STAGE → PROGRESS MAP ───────────────────────────────────────────

STAGE_PROGRESS = {
    # Chain A stages
    "OCR":                  10,
    "LANGUAGE_DETECTION":   20,
    "TRANSLATION":          30,
    "REGEX_EXTRACTION":     40,
    "NLP_CLASSIFICATION":   55,
    "NLP_EXTRACTION":       65,
    "POPULATING_WORKBENCH": 80,
    # Status-based (not stage-based)
    "PENDING_HUMAN_REVIEW": 85,   # Chain A done, waiting for officer
    # Chain B stages
    "COMPLIANCE":           90,
    "JUDGMENT_RETRIEVAL":   93,
    "APPLICABILITY":        95,
    "PRECEDENCE":           96,
    "SCORING":              97,
    "RECOMMENDATION":       98,
    "GENERATING_REPORT":    99,
    # Terminal
    "COMPLETE":             100,
}

STAGE_MESSAGES = {
    "DRAFT":                  "Case created. Upload documents to begin analysis.",
    "INTAKE_REJECTED":        "Case rejected at intake. See intake_filter_result for details.",
    "PROCESSING":             "Documents are being processed. This takes 2-5 minutes.",
    "PENDING_HUMAN_REVIEW":   "Document processing complete. Please review and confirm extracted facts.",
    "ANALYSING":              "Compliance analysis and judgment retrieval in progress.",
    "PENDING_JUDGMENT_REVIEW":"Analysis paused — no precedent found for one or more grounds.",
    "COMPLETE":               "Analysis complete. Report is ready.",
    "FAILED":                 "Processing failed. Contact support with the case ID.",
}


# ─── ENDPOINTS ────────────────────────────────────────────────────────────────

@router.post(
    "",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new case",
)
async def create_case(
    body:         CreateCaseRequest,
    current_user: OfficerDep,
    request:      Request,
    db:           DbDep,
) -> CaseResponse:
    """
    Create a case record. Runs F2 pre-intake filter (loan amount check).
    F1/F3/F4 filters run later during Chain A after document upload.
    Chain A is NOT triggered here — it fires when first document is uploaded.
    """
    # F2: Only filter we can apply without documents — loan amount threshold
    f2_result = run_f2_filter(body.principal_amount)

    # Determine initial status based on F2 result
    if f2_result and not f2_result.passed and f2_result.filter_id == "F2":
        initial_status = "INTAKE_REJECTED"
        intake_result  = f2_result.model_dump()
        logger.info(
            f"Case creation: F2 filter fired for bank={current_user.bank_id} "
            f"amount={body.principal_amount}"
        )
    else:
        initial_status = "DRAFT"
        intake_result  = None

    case = Case(
        bank_id=current_user.bank_id,           # ← FROM JWT — never from body
        created_by=current_user.user_id,        # ← FROM JWT
        borrower_name=body.borrower_name,
        case_ref=body.case_ref,
        drt_case_number=body.drt_case_number,
        drt_bench=body.drt_bench,
        property_description=body.property_description,
        loan_account_number=body.loan_account_number,
        principal_amount=body.principal_amount,
        status=initial_status,
        intake_filter_result=intake_result,
    )
    db.add(case)
    await db.flush()   # get case.id before audit log

    await write_audit_log(
        db,
        action="CREATE_CASE",
        user_id=current_user.user_id,
        case_id=case.id,
        detail={
            "borrower_name":  body.borrower_name,
            "initial_status": initial_status,
            "f2_fired":       initial_status == "INTAKE_REJECTED",
        },
        ip_address=get_client_ip(request),
    )

    logger.info(
        f"Case created: {case.id} [{initial_status}] "
        f"bank={current_user.bank_id} borrower={body.borrower_name!r}"
    )
    return CaseResponse.model_validate(case)


@router.get(
    "",
    response_model=CaseListResponse,
    summary="List all cases for the current bank",
)
async def list_cases(
    current_user: OfficerDep,
    db:           DbDep,
    page:         int = Query(default=1, ge=1),
    page_size:    int = Query(default=20, ge=1, le=100),
    status_filter: Optional[str] = Query(default=None, alias="status"),
    search:       Optional[str] = Query(default=None, description="Search by borrower name or case_ref"),
) -> CaseListResponse:
    """
    Returns all cases for the authenticated user's bank.
    BANK_OFFICER and BANK_ADMIN see all cases in their bank equally.
    Supports: pagination, status filtering, borrower name search.
    """
    # Base query — bank_id filter is ALWAYS present
    base_query = select(Case).where(Case.bank_id == current_user.bank_id)

    # Optional filters
    if status_filter:
        valid_statuses = {
            "DRAFT","INTAKE_REJECTED","PROCESSING","PENDING_HUMAN_REVIEW",
            "ANALYSING","PENDING_JUDGMENT_REVIEW","COMPLETE","FAILED"
        }
        if status_filter not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid status filter. Valid values: {sorted(valid_statuses)}"
            )
        base_query = base_query.where(Case.status == status_filter)

    if search:
        # Case-insensitive search on borrower_name OR case_ref
        search_term = f"%{search.strip()}%"
        from sqlalchemy import or_, cast, String
        base_query = base_query.where(
            or_(
                Case.borrower_name.ilike(search_term),
                Case.case_ref.ilike(search_term),
                Case.drt_case_number.ilike(search_term),
            )
        )

    # Count total matching records
    count_query = select(func.count()).select_from(base_query.subquery())
    total       = (await db.execute(count_query)).scalar_one()

    # Fetch paginated results — newest first
    offset   = (page - 1) * page_size
    paginated = base_query.order_by(Case.created_at.desc()).offset(offset).limit(page_size)
    result    = await db.execute(paginated)
    cases     = result.scalars().all()

    return CaseListResponse(
        items=[CaseSummaryResponse.model_validate(c) for c in cases],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total > 0 else 0,
    )


@router.get(
    "/{case_id}",
    response_model=CaseResponse,
    summary="Get case details",
)
async def get_case(
    case_id:      uuid.UUID,
    current_user: OfficerDep,
    db:           DbDep,
) -> CaseResponse:
    """
    Returns full case details. Returns 404 if case not found OR if it belongs
    to a different bank — intentionally indistinguishable.
    """
    case = await verify_case_bank_access(case_id, current_user, db)
    return CaseResponse.model_validate(case)


@router.patch(
    "/{case_id}",
    response_model=CaseResponse,
    summary="Update case metadata",
    description=(
        "Updates metadata fields only — borrower_name, case_ref, drt_case_number, "
        "drt_bench, property_description, loan_account_number. "
        "Status is never updated by clients — only by the pipeline."
    ),
)
async def update_case(
    case_id:      uuid.UUID,
    body:         UpdateCaseRequest,
    current_user: OfficerDep,
    db:           DbDep,
) -> CaseResponse:
    case = await verify_case_bank_access(case_id, current_user, db)

    # Only update fields that were explicitly provided in the request
    update_data = body.model_dump(exclude_none=True)
    if not update_data:
        return CaseResponse.model_validate(case)   # nothing to update

    for field, value in update_data.items():
        setattr(case, field, value)

    await write_audit_log(
        db,
        action="UPDATE_CASE",
        user_id=current_user.user_id,
        case_id=case.id,
        detail={"updated_fields": list(update_data.keys())},
    )

    return CaseResponse.model_validate(case)


@router.get(
    "/{case_id}/pipeline-status",
    response_model=PipelineStatusResponse,
    summary="Get pipeline processing status",
)
async def get_pipeline_status(
    case_id:      uuid.UUID,
    current_user: OfficerDep,
    db:           DbDep,
) -> PipelineStatusResponse:
    """
    Returns current status and progress percentage.
    Frontend polls this endpoint every 3 seconds while status is PROCESSING or ANALYSING.
    """
    case = await verify_case_bank_access(case_id, current_user, db)

    # Determine progress percentage
    if case.status == "COMPLETE":
        progress = 100
    elif case.status in ("DRAFT", "INTAKE_REJECTED", "FAILED"):
        progress = 0
    elif case.pipeline_stage and case.pipeline_stage in STAGE_PROGRESS:
        progress = STAGE_PROGRESS[case.pipeline_stage]
    elif case.status in STAGE_PROGRESS:
        progress = STAGE_PROGRESS[case.status]
    else:
        progress = 5   # processing started but stage not yet set

    return PipelineStatusResponse(
        case_id=case.id,
        status=case.status,
        pipeline_stage=case.pipeline_stage,
        progress_pct=progress,
        message=STAGE_MESSAGES.get(case.status, "Processing..."),
    )


@router.post(
    "/{case_id}/resume",
    response_model=PipelineStatusResponse,
    summary="Resume analysis after judgment gap review",
    description=(
        "Resumes Chain B from judgment retrieval when case is in "
        "PENDING_JUDGMENT_REVIEW status. Called after Harasis manually "
        "adds new judgment JSONs and they are loaded into Qdrant."
    ),
)
async def resume_analysis(
    case_id:      uuid.UUID,
    current_user: OfficerDep,
    db:           DbDep,
) -> PipelineStatusResponse:
    case = await verify_case_bank_access(case_id, current_user, db)

    if case.status != "PENDING_JUDGMENT_REVIEW":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Cannot resume analysis from status '{case.status}'. "
                   f"Only PENDING_JUDGMENT_REVIEW cases can be resumed."
        )

    # Reset status and re-fire Chain B from judgment retrieval
    case.status        = "ANALYSING"
    case.pipeline_stage = "JUDGMENT_RETRIEVAL"

    await write_audit_log(
        db,
        action="RESUME_ANALYSIS",
        user_id=current_user.user_id,
        case_id=case.id,
        detail={"resumed_from": "PENDING_JUDGMENT_REVIEW"},
    )

    # Fire Chain B from judgment retrieval task only
    from app.tasks.chain_b import run_chain_b_from_judgments
    run_chain_b_from_judgments.delay(str(case_id))

    logger.info(f"Analysis resumed for case {case_id} by {current_user.email}")

    return PipelineStatusResponse(
        case_id=case.id,
        status=case.status,
        pipeline_stage=case.pipeline_stage,
        progress_pct=STAGE_PROGRESS.get("JUDGMENT_RETRIEVAL", 90),
        message="Analysis resumed. Retrieving precedents...",
    )


@router.delete(
    "/{case_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a case (BANK_ADMIN only)",
    description=(
        "Soft-delete only — sets status to DRAFT and removes all pipeline data. "
        "Documents in S3 are NOT deleted (retained for audit purposes). "
        "Only BANK_ADMIN can delete cases."
    ),
)
async def delete_case(
    case_id:      uuid.UUID,
    admin:        AdminDep,
    db:           DbDep,
) -> None:
    """
    This is a HARD design decision: we do not physically delete cases or documents
    from banks. Legal documents have retention requirements. Physical deletion is
    a separate offline process requiring explicit bank IT sign-off.

    What this endpoint does:
      - Marks the case as DRAFT (hides it from normal views)
      - Clears pipeline_stage, intake_filter_result, judgment_coverage_alerts
      - Audit logs the deletion with the admin's identity
    """
    case = await verify_case_bank_access(case_id, admin, db)

    # Clear pipeline state but keep the case record and documents
    case.status                   = "DRAFT"
    case.pipeline_stage           = None
    case.intake_filter_result     = None
    case.judgment_coverage_alerts = None

    await write_audit_log(
        db,
        action="DELETE_CASE",
        user_id=admin.user_id,
        case_id=case.id,
        detail={"note": "Soft delete by admin. S3 documents retained."},
    )

    logger.info(f"Case {case_id} soft-deleted by admin {admin.email}")
```

## 29. Appendix: Reference Implementation — app/services/complaince/seed_intake.py

```python

# app/services/compliance/pre_intake.py
"""
Pre-intake filters — run before pipeline analysis begins.

FILTER TIMING:
  F2 runs at CASE CREATION (cases.py) — only needs principal_amount
  F1, F3, F4 run during CHAIN A — need document content

F1: Agricultural land exemption (Section 31(i) SARFAESI)
F2: Loan amount threshold (Section 31(d) SARFAESI) — < Rs. 1 lakh
F3: >80% principal repaid — SARFAESI applicability questionable
F4: IBC moratorium claimed — Section 14 NCLT protection
"""

from __future__ import annotations

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class IntakeFilterResult(BaseModel):
    passed:       bool
    filter_id:    Optional[str]   = None
    result_label: Optional[str]   = None
    reason:       Optional[str]   = None
    action:       Optional[str]   = None
    route_flags:  list[dict]      = []   # v5.4 — non-terminating routing signals (F5, F6)


# ─── F2 — runs at case creation ──────────────────────────────────────────────

SARFAESI_MIN_LOAN_AMOUNT = Decimal("100000")   # Rs. 1,00,000

def run_f2_filter(principal_amount: Optional[Decimal]) -> Optional[IntakeFilterResult]:
    """
    F2: Loan amount threshold check.
    Returns IntakeFilterResult if filter fires, None if it does not apply.
    None (not fired) is different from IntakeFilterResult(passed=True).
    """
    if principal_amount is None:
        return None   # amount not provided — can't run filter, proceed

    if principal_amount < SARFAESI_MIN_LOAN_AMOUNT:
        return IntakeFilterResult(
            passed=False,
            filter_id="F2",
            result_label="SARFAESI_NOT_APPLICABLE",
            reason=(
                f"Loan amount Rs. {principal_amount:,.2f} is below the Rs. 1,00,000 "
                f"minimum threshold under Section 31(d) of the SARFAESI Act 2002. "
                f"SARFAESI enforcement is not available for this loan."
            ),
            action="Case rejected at intake. Proceed via DRT or civil court."
        )

    return None   # filter did not fire — case can proceed


# ─── F1, F3, F4 — run during Chain A after document processing ───────────────

def run_pre_intake_filters_chain_a(case_facts: dict) -> Optional[IntakeFilterResult]:
    """
    Runs F1, F3, F4 during Chain A after facts are extracted from documents.
    Called by task_regex_extract_all after the initial fact extraction.

    Returns the first filter that fires, or None if all pass.
    If a filter fires, Chain A sets case status = INTAKE_REJECTED and stops.
    """
    f1 = _run_f1(case_facts)
    if f1:
        return f1

    f3 = _run_f3(case_facts)
    if f3:
        return f3

    f4 = _run_f4(case_facts)
    if f4:
        return f4

    return None


def _run_f1(facts: dict) -> Optional[IntakeFilterResult]:
    """F1: Agricultural land — Section 31(i) SARFAESI."""
    secured_asset_type = facts.get("secured_asset_type", {}).get("field_value")
    if secured_asset_type == "agricultural_land":
        return IntakeFilterResult(
            passed=False,
            filter_id="F1",
            result_label="SARFAESI_NOT_APPLICABLE",
            reason=(
                "The secured asset is agricultural land. "
                "Section 31(i) of the SARFAESI Act 2002 explicitly excludes "
                "agricultural land from SARFAESI enforcement."
            ),
            action="Pipeline terminated. SARFAESI remedy is not available for agricultural land."
        )
    return None


def _run_f3(facts: dict) -> Optional[IntakeFilterResult]:
    """F3: >80% principal repaid — questionable applicability."""
    principal = facts.get("principal_loan_amount", {}).get("field_value")
    repaid    = facts.get("amount_repaid", {}).get("field_value")

    if principal and repaid:
        try:
            pct = Decimal(repaid) / Decimal(principal)
            if pct > Decimal("0.80"):
                return IntakeFilterResult(
                    passed=False,
                    filter_id="F3",
                    result_label="APPLICABILITY_QUESTIONABLE",
                    reason=(
                        f"More than 80% of the principal ({pct:.1%}) has been repaid. "
                        f"SARFAESI applicability may be contested by the borrower. "
                        f"Verify outstanding amount and consult legal counsel."
                    ),
                    action="Flag for human legal review. Do not auto-proceed."
                )
        except Exception:
            pass   # non-numeric values — silently skip filter
    return None


def _run_f4(facts: dict) -> Optional[IntakeFilterResult]:
    """F4: IBC Section 14 moratorium — all SARFAESI proceedings are stayed."""
    moratorium_claimed = facts.get("ibc_moratorium_active", {}).get("field_value")
    if moratorium_claimed == "true":
        return IntakeFilterResult(
            passed=False,
            filter_id="F4",
            result_label="IBC_MORATORIUM",
            reason=(
                "Borrower claims protection under Section 14 of the Insolvency "
                "and Bankruptcy Code 2016 (IBC moratorium). If NCLT has admitted "
                "the insolvency petition, all SARFAESI proceedings are automatically stayed."
            ),
            action=(
                "Requires human legal review. Verify NCLT order number and admission date. "
                "Cannot be verified from bank documents alone — check NCLT records."
            )
        )
    return None
```

## 30. Appendix: Reference Implementation — scripts/seed_db.py

```python

#!/usr/bin/env python3
# scripts/seed_db.py
"""
Seed script — creates the first bank and SYSTEM_ADMIN user.
Run ONCE before the first deployment. All subsequent banks/users
are created via POST /api/v1/auth/register and POST /api/v1/auth/users.

Usage:
    python scripts/seed_db.py

Environment variables required:
    DATABASE_URL (sync URL with psycopg2 driver)
    Or set in .env and load with: python -m dotenv run python scripts/seed_db.py

SECURITY: This script creates a SYSTEM_ADMIN user.
  - Run only on first deploy
  - Delete or restrict this script after use in production
  - Change the SYSTEM_ADMIN password immediately after first login
"""

import os
import sys
import uuid

# Allow running from repo root without installing the package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from passlib.context import CryptContext
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# ─── CONFIG ──────────────────────────────────────────────────────────────────

# Build sync URL from env — handles both asyncpg and psycopg2 formats
_raw_url = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://slrai:slrai_dev@localhost:5432/slrai"
)
SYNC_URL = _raw_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://")

# First bank details — edit before running
SEED_BANK_NAME       = os.environ.get("SEED_BANK_NAME",       "Demo Bank Ltd")
SEED_BANK_SHORT_CODE = os.environ.get("SEED_BANK_SHORT_CODE", "DEMO")

# System admin — CHANGE PASSWORD after first login
SEED_ADMIN_EMAIL    = os.environ.get("SEED_ADMIN_EMAIL",    "admin@slrai.internal")
SEED_ADMIN_PASSWORD = os.environ.get("SEED_ADMIN_PASSWORD", "Admin@1234!Change")

# ─── SETUP ────────────────────────────────────────────────────────────────────

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

engine       = create_engine(SYNC_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


def run_seed():
    with SessionLocal() as db:
        # Check if already seeded
        existing_bank = db.execute(
            text("SELECT id FROM banks WHERE short_code = :code"),
            {"code": SEED_BANK_SHORT_CODE}
        ).fetchone()

        if existing_bank:
            print(f"\n⚠️  Bank '{SEED_BANK_SHORT_CODE}' already exists. Skipping seed.")
            print("   If you need to re-seed, manually delete the bank and user from the DB first.\n")
            return

        # Create bank
        bank_id = uuid.uuid4()
        db.execute(
            text("""
                INSERT INTO banks (id, name, short_code, active)
                VALUES (:id, :name, :short_code, TRUE)
            """),
            {"id": bank_id, "name": SEED_BANK_NAME, "short_code": SEED_BANK_SHORT_CODE}
        )

        # Create SYSTEM_ADMIN user
        admin_id = uuid.uuid4()
        password_hash = pwd_context.hash(SEED_ADMIN_PASSWORD)
        db.execute(
            text("""
                INSERT INTO users (id, bank_id, email, password_hash, role, active)
                VALUES (:id, :bank_id, :email, :password_hash, 'SYSTEM_ADMIN', TRUE)
            """),
            {
                "id":            admin_id,
                "bank_id":       bank_id,
                "email":         SEED_ADMIN_EMAIL,
                "password_hash": password_hash,
            }
        )

        db.commit()

        print("\n✅  Seed complete!")
        print(f"   Bank:    {SEED_BANK_NAME} ({SEED_BANK_SHORT_CODE})")
        print(f"   Bank ID: {bank_id}")
        print(f"   Admin:   {SEED_ADMIN_EMAIL}")
        print(f"   Role:    SYSTEM_ADMIN")
        print(f"\n⚠️  IMPORTANT: Change the admin password immediately after first login.")
        print(f"   POST /api/v1/auth/login with email={SEED_ADMIN_EMAIL}")
        print(f"   Then use POST /api/v1/auth/users to create bank-specific users.\n")


if __name__ == "__main__":
    run_seed()
```

---

## 25. Report Generator and Templates

### 25.1 `app/reports/generator.py`

```python
"""
Report Generator — WeasyPrint PDF from Jinja2 template.

DESIGN DECISIONS (from product requirements):
  - Audience: Bank officer + auction purchaser — both non-lawyers
  - Goal: Answer "should I proceed with this asset?" — legal stand only
  - Format: Screen-optimised PDF, Claude-like clean style
  - Structure: Recommendation on page 1, Red Flags page 2, Detail pages after
  - Scoring: Visual gauge + numbers
  - Language: English (Hindi script rendered if font available)
  - Watermark: CONFIDENTIAL diagonal watermark on every page
  - Footer: Legal disclaimer on every page

WATERMARK NOTE:
  WeasyPrint renders the watermark via CSS position:fixed, which places it
  on every page. The watermark text is rendered at 45° using CSS transform.

GAUGE NOTE:
  The compliance score and litigation exposure use SVG-based circular gauges.
  WeasyPrint supports basic SVG. The gauge is a stroke-dasharray circle.

FONT NOTE:
  To render Hindi script (Devanagari) in the PDF, add to Dockerfile:
  RUN apt-get install -y fonts-noto-core fonts-noto-extra
  This bundles Noto Sans Devanagari for WeasyPrint.
"""

from __future__ import annotations

import hashlib
import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML, CSS

from app.config import settings
from app.models.db import (
    Case, CaseFact, ComplianceResult, GroundScore,
    JudgmentApplicability, Report, SAGround, get_sync_db,
    write_audit_log_sync
)
from app.services.storage import upload_report_pdf, upload_report_json

logger = logging.getLogger(__name__)

# ─── SEVERITY MAPPING ────────────────────────────────────────────────────────

SEVERITY_TO_LABEL = {
    "FATAL":          ("CRITICAL",        "#DC2626"),   # red-600
    "ABSOLUTE_BAR":   ("CRITICAL",        "#7F1D1D"),   # red-900
    "CURABLE":        ("HIGH",            "#EA580C"),   # orange-600
    "MINOR":          ("MODERATE",        "#D97706"),   # amber-600
    "ADVISORY":       ("MODERATE",        "#D97706"),
    "REVIEW_REQUIRED":("REVIEW REQUIRED", "#6B7280"),   # gray-500
    "UNKNOWN":        ("REVIEW REQUIRED", "#6B7280"),
}

GROUND_CODE_NAMES = {
    "SERVICE_DEFECT":        "Demand Notice — Service Defect",
    "AMOUNT_DISPUTE":        "Demand Notice — Amount Dispute",
    "REPLY_NOT_GIVEN":       "Bank Failed to Reply to Objection",
    "AUCTION_GAP_DEFECT":    "Auction Notice Gap Insufficient",
    "NEWSPAPER_PUB_DEFECT":  "Newspaper Publication Defect",
    "LIMITATION_EXPIRED":    "Limitation — SA Time-Barred",
    "TENANCY_CLAIM":         "Tenancy / Lease Protection Claimed",
    "VALUATION_DISPUTE":     "Valuation Challenged",
    "NOTICE_ALL_PARTIES":    "Notice Not Served on All Borrowers/Guarantors",
    "NPA_PREMATURE":         "NPA Classification — Premature",
    "NPA_DURING_RESTRUC":    "NPA During Active Restructuring",
    "MSME_RESTRUC_SKIPPED":  "MSME — Restructuring Not Offered",
    "POSSESSION_DEFECT":     "Possession Notice Defect",
    "NOTICE_FORMAT_DEFECT":  "Demand Notice — Format Defect",
    "UNKNOWN":               "Unclassified Ground",
}

MODULE_NAMES = {
    "M1_DEMAND_NOTICE":      "M1 — Demand Notice (Section 13(2))",
    "M2_REPLY_COMPLIANCE":   "M2 — Reply Compliance (Section 13(3A))",
    "M3_AUCTION_GAP":        "M3 — Auction Notice Gap (Rules 8 & 9)",
    "M4_LIMITATION":         "M4 — Limitation Period (Section 17)",
    "M5_TENANCY":            "M5 — Tenancy Shield",
    "M6_VALUATION":          "M6 — Valuation Process",
    "M7_MULTIPARTY_NOTICE":  "M7 — Multi-Party Notice",
    "M8_NPA_CLASSIFICATION": "M8 — NPA Classification",
    "M9_MSME":               "M9 — MSME Procedural Check",
}

RECOMMENDATION_DISPLAY = {
    "PROCEED":                  ("PROCEED",            "#16A34A", "Low litigation risk. Bank followed SARFAESI procedure correctly. Borrower's grounds are weak."),
    "PROCEED_WITH_AWARENESS":   ("PROCEED WITH CAUTION","#CA8A04","Procedure largely correct. Some arguable grounds exist. Monitor DRT hearing dates."),
    "PROCEED_WITH_CONDITIONS":  ("PROCEED WITH CONDITIONS","#EA580C","Minor procedural gaps. Borrower's case is weak. Obtain legal affidavit on curable defects before bidding."),
    "ELEVATED_RISK":            ("ELEVATED RISK",       "#DC2626", "Both bank and borrower have exposure. Detailed legal review strongly recommended before bidding."),
    "HIGH_RISK":                ("HIGH RISK",           "#B91C1C", "Significant risk. Do not proceed without comprehensive legal review by a SARFAESI specialist."),
    "DO_NOT_PROCEED":           ("DO NOT PROCEED",      "#7F1D1D", "Fatal procedural defects or strong borrower grounds found. Auction is highly vulnerable to challenge."),
    "DO_NOT_PROCEED_CRITICAL":  ("DO NOT PROCEED — CRITICAL","#450A0A","Borrower has very strong legal grounds. Proceeding with auction carries extreme litigation risk."),
    "PROCEED_FAVOURABLE":       ("PROCEED — FAVOURABLE","#15803D","SA appears time-barred under Section 17. Dismissal of borrower's application is likely."),
    "MANUAL_REVIEW_REQUIRED":   ("MANUAL REVIEW REQUIRED","#6B7280","Score combination requires legal review. Consult a SARFAESI specialist before proceeding."),
}


# ─── CONTEXT BUILDER ─────────────────────────────────────────────────────────

def build_report_context(case_id: str, db) -> dict:
    """
    Builds the complete context dict passed to the Jinja2 template.
    This is the single function that assembles everything the report needs.
    All data comes from PostgreSQL — never from Qdrant at this stage.

    Called from generate_report() which is called from task_generate_report.
    """
    # ── Case ──────────────────────────────────────────────────────────────────
    case = db.query(Case).filter_by(id=case_id).first()
    if not case:
        raise ValueError(f"Case {case_id} not found")

    # ── Bank name ─────────────────────────────────────────────────────────────
    bank_name = case.bank.name if case.bank else "Unknown Bank"

    # ── Case facts (confirmed only) ───────────────────────────────────────────
    facts_rows = db.query(CaseFact).filter_by(case_id=case_id).all()
    facts = {row.field_name: row.field_value for row in facts_rows}

    # ── Prayer clause + third party context (v5.4) ────────────────────────────
    prayer_context = {
        "sa_applicant_type":            facts.get("sa_applicant_type"),
        "challenges_demand_notice":     facts.get("challenges_demand_notice"),
        "challenges_possession_notice": facts.get("challenges_possession_notice"),
        "challenges_sale_notice":       facts.get("challenges_sale_notice"),
        "challenges_auction":           facts.get("challenges_auction"),
        "challenges_demand_amount":     facts.get("challenges_demand_amount"),
        "interim_stay_prayed":          facts.get("interim_stay_prayed"),
        "interim_stay_granted":         facts.get("interim_stay_granted"),
        "prayer_scope_covers_current_measure": facts.get("prayer_scope_covers_current_measure"),
        "ats_advance_paid":             facts.get("ats_advance_paid"),
        "ats_date":                     facts.get("ats_date"),
        "ats_simultaneous_mortgage":    facts.get("ats_simultaneous_mortgage"),
    }

    # Pre-generation gate — no UNKNOWN compliance results allowed in final report.
    # The workbench flow ensures all required fields are confirmed before Chain B fires.
    # If somehow unknowns remain, log a warning but proceed (do not hard-block here —
    # the workbench confirm-all endpoint is the authoritative gate).
    # We discuss the full unknown resolution policy separately.
    unresolved = [
        r for r in db.query(ComplianceResult).filter_by(case_id=case_id).all()
        if r.status == "UNKNOWN" and r.severity in ("FATAL", "ABSOLUTE_BAR")
    ]
    if unresolved:
        logger.warning(
            f"Report generated for case {case_id} with {len(unresolved)} unresolved "
            f"FATAL/ABSOLUTE_BAR rules. Workbench gate may not have caught these. "
            f"Rules: {[r.rule_id for r in unresolved]}"
        )

    # ── Asset identifier (Q1 answer: Option C — both) ─────────────────────────
    property_display = case.property_description or "Property address not recorded"
    asset_heading    = case.borrower_name
    asset_subheading = (
        f"{property_display} | "
        f"Case Ref: {case.case_ref or 'N/A'} | "
        f"DRT: {case.drt_case_number or 'N/A'}"
    )

    # ── Compliance results ────────────────────────────────────────────────────
    compliance_rows = db.query(ComplianceResult).filter_by(case_id=case_id).all()

    # Red flags — FAIL results only, sorted by severity
    severity_order = {"FATAL": 0, "ABSOLUTE_BAR": 0, "CURABLE": 1, "MINOR": 2,
                      "ADVISORY": 3, "REVIEW_REQUIRED": 4, "UNKNOWN": 5}
    failed_rules = sorted(
        [r for r in compliance_rows if r.status == "FAIL"],
        key=lambda r: severity_order.get(r.severity or "UNKNOWN", 5)
    )

    red_flags = []
    for rule in failed_rules:
        label, color = SEVERITY_TO_LABEL.get(rule.severity or "UNKNOWN", ("UNKNOWN", "#6B7280"))

        # Get statute text if available
        statute_text = _get_statute_text(case_id, rule.rule_id, db)

        # Get authority (first judgment tag that has a known citation)
        authority = _get_authority_for_rule(case_id, rule.rule_id, db)

        red_flags.append({
            "severity_label": label,
            "severity_color": color,
            "module":         MODULE_NAMES.get(rule.module, rule.module),
            "rule_id":        rule.rule_id,
            "finding":        rule.message or "",
            "statute_text":   statute_text,
            "authority":      authority,
            "detail":         rule.detail_json or {},
        })

    # Group compliance results by module for the detailed section
    module_results = {}
    for row in compliance_rows:
        mod = row.module
        if mod not in module_results:
            module_results[mod] = {
                "name":    MODULE_NAMES.get(mod, mod),
                "results": [],
                "worst_status": "PASS",
            }
        label, color = SEVERITY_TO_LABEL.get(row.severity or "", ("", ""))
        module_results[mod]["results"].append({
            "rule_id":        row.rule_id,
            "status":         row.status,
            "severity":       row.severity,
            "severity_label": label,
            "severity_color": color,
            "message":        row.message or "",
        })
        # Track worst status for module summary icon
        if row.status == "FAIL":
            module_results[mod]["worst_status"] = "FAIL"
        elif row.status == "UNKNOWN" and module_results[mod]["worst_status"] == "PASS":
            module_results[mod]["worst_status"] = "UNKNOWN"

    # ── Ground scores ─────────────────────────────────────────────────────────
    sa_grounds_rows  = db.query(SAGround).filter_by(case_id=case_id).all()
    ground_score_rows = db.query(GroundScore).filter_by(case_id=case_id).all()
    ground_score_map  = {row.ground_code: row for row in ground_score_rows}

    ground_scores = []
    for ground in sa_grounds_rows:
        score_row = ground_score_map.get(ground.ground_code)

        # Applicable judgments for this ground
        applicable_judgments = _get_applicable_judgments(case_id, ground.ground_code, db)

        strength       = score_row.ground_strength if score_row else 0.40
        strength_label = _strength_label(strength)

        ground_scores.append({
            "ground_code":          ground.ground_code,
            "ground_name":          GROUND_CODE_NAMES.get(ground.ground_code, ground.ground_code),
            "factual_claim":        ground.factual_claim_extracted or "",
            "factual_score":        score_row.factual_score if score_row else None,
            "judicial_score":       score_row.judicial_score if score_row else None,
            "ground_strength":      strength,
            "strength_label":       strength_label,
            "strength_color":       _strength_color(strength),
            "applicable_judgments": applicable_judgments,
        })

    # Sort by ground_strength descending — strongest borrower grounds first
    ground_scores.sort(key=lambda g: g["ground_strength"] or 0, reverse=True)

    # ── Scores ────────────────────────────────────────────────────────────────
    report_row = db.query(Report).filter_by(case_id=case_id).order_by(
        Report.generated_at.desc()
    ).first()

    compliance_score    = report_row.compliance_score    if report_row else _calculate_compliance(failed_rules)
    litigation_exposure = report_row.litigation_exposure if report_row else _calculate_exposure(ground_scores)
    recommendation_key  = report_row.recommendation     if report_row else "MANUAL_REVIEW_REQUIRED"

    rec_label, rec_color, rec_text = RECOMMENDATION_DISPLAY.get(
        recommendation_key,
        ("MANUAL REVIEW REQUIRED", "#6B7280", "Consult a SARFAESI specialist.")
    )

    # ── DRT Stay Gate (Audit Addition) ────────────────────────────────────────
    if facts.get("drt_interim_stay_granted"):
        recommendation_key = "DO_NOT_PROCEED_CRITICAL"
        rec_label = "DRT STAY IN EFFECT"
        rec_color = "#450A0A"  # Darkest red
        rec_text = "Auction cannot proceed until stay is vacated. Proceeding violates Section 17(4) DRT order."

    exposure_label = _exposure_label(litigation_exposure)
    compliance_band = _compliance_band(compliance_score)

    # ── SVG gauge data ────────────────────────────────────────────────────────
    # SVG circular gauge: circumference = 2 * pi * r = 2 * 3.14159 * 52 ≈ 326.7
    # stroke-dasharray = (score/100) * circumference for compliance
    circumference = 326.7
    compliance_dash    = (compliance_score / 100) * circumference
    exposure_dash      = litigation_exposure * circumference
    compliance_color   = _score_color(compliance_score)
    exposure_color     = _exposure_color(litigation_exposure)

    # ── Judgment coverage alerts ──────────────────────────────────────────────
    judgment_alerts = case.judgment_coverage_alerts or []

    # ── Report metadata ───────────────────────────────────────────────────────
    generated_at = datetime.now(timezone.utc)

    return {
        # Case info
        "case_id":              str(case_id),
        "asset_heading":        asset_heading,
        "asset_subheading":     asset_subheading,
        "borrower_name":        case.borrower_name,
        "property_description": property_display,
        "case_ref":             case.case_ref or "N/A",
        "drt_case_number":      case.drt_case_number or "N/A",
        "drt_bench":            case.drt_bench or "N/A",
        "bank_name":            bank_name,
        "loan_account_number":  case.loan_account_number or "N/A",
        "principal_amount":     facts.get("principal_loan_amount"),

        # Recommendation (page 1)
        "recommendation_key":   recommendation_key,
        "recommendation_label": rec_label,
        "recommendation_color": rec_color,
        "recommendation_text":  rec_text,

        # Scores
        "compliance_score":     compliance_score,
        "compliance_band":      compliance_band,
        "compliance_color":     compliance_color,
        "compliance_dash":      round(compliance_dash, 2),
        "circumference":        circumference,
        "litigation_exposure":  round(litigation_exposure, 3),
        "exposure_pct":         round(litigation_exposure * 100, 1),
        "exposure_label":       exposure_label,
        "exposure_color":       exposure_color,
        "exposure_dash":        round(exposure_dash, 2),

        # Red flags (page 2)
        "red_flags":            red_flags,
        "fatal_count":          sum(1 for r in failed_rules if r.severity in ("FATAL","ABSOLUTE_BAR")),
        "curable_count":        sum(1 for r in failed_rules if r.severity == "CURABLE"),

        # Module detail
        "module_results":       module_results,

        # Ground strength
        "ground_scores":        ground_scores,

        # Judgment alerts
        "judgment_alerts":      judgment_alerts,

        # Meta
        "generated_at":         generated_at.strftime("%d %B %Y, %H:%M UTC"),
        "disclaimer_text":      DISCLAIMER_TEXT,
        "report_id":            str(uuid.uuid4()),

        # Prayer clause + third party context (v5.4)
        **prayer_context,
    }


# ─── GENERATE REPORT ─────────────────────────────────────────────────────────

def generate_report(case_id: str, user_id: str) -> str:
    """
    Entry point for task_generate_report in chain_b.py.
    Builds context, renders HTML, converts to PDF, stores in S3,
    saves to reports table.
    Returns report_id.

    Error handling:
    - WeasyPrint fails → save JSON only, pdf_url = None, do NOT fail case
    - S3 upload fails → save report_json to DB only, log error
    """
    import asyncio

    with get_sync_db() as db:
        context = build_report_context(case_id, db)
        report_id = context["report_id"]

        # Render Jinja2 template → HTML string
        html_string = _render_template(context)

        # Convert HTML → PDF using WeasyPrint
        pdf_bytes = None
        pdf_url   = None
        try:
            pdf_bytes = HTML(string=html_string, base_url=str(
                Path(settings.report_template_dir).parent.absolute()
            )).write_pdf()
        except Exception as e:
            logger.error(f"WeasyPrint failed for case {case_id}: {e}")
            # Continue — JSON report still saved

        # Compute content hash for tamper evidence
        report_json     = json.dumps(context, default=str, ensure_ascii=False)
        content_hash    = hashlib.sha256(report_json.encode()).hexdigest()

        # Upload PDF to S3 (if generated)
        if pdf_bytes:
            try:
                s3_key  = f"cases/{case_id}/reports/{report_id}.pdf"
                pdf_url = asyncio.get_event_loop().run_until_complete(
                    upload_report_pdf(pdf_bytes, uuid.UUID(case_id), uuid.UUID(report_id))
                ) if pdf_bytes else None
            except Exception as e:
                logger.error(f"S3 PDF upload failed for report {report_id}: {e}")

        # Save report record to DB
        existing = db.query(Report).filter_by(
            case_id=case_id
        ).order_by(Report.generated_at.desc()).first()

        if existing:
            existing.compliance_score    = context["compliance_score"]
            existing.litigation_exposure = context["litigation_exposure"]
            existing.recommendation      = context["recommendation_key"]
            existing.report_json         = context
            existing.pdf_url             = pdf_url
            existing.content_hash        = content_hash
            existing.generated_by        = uuid.UUID(user_id) if user_id else None
            existing.generated_at        = datetime.now(timezone.utc)
        else:
            report = Report(
                id=uuid.UUID(report_id),
                case_id=uuid.UUID(case_id),
                compliance_score=context["compliance_score"],
                litigation_exposure=context["litigation_exposure"],
                recommendation=context["recommendation_key"],
                report_json=context,
                pdf_url=pdf_url,
                content_hash=content_hash,
                generated_by=uuid.UUID(user_id) if user_id else None,
            )
            db.add(report)

        write_audit_log_sync(
            db,
            action="GENERATE_REPORT",
            user_id=uuid.UUID(user_id) if user_id else None,
            case_id=uuid.UUID(case_id),
            detail={"report_id": report_id, "pdf_generated": pdf_bytes is not None},
        )

        logger.info(f"Report generated for case {case_id}: {report_id} | PDF: {pdf_url is not None}")
        return report_id


# ─── TEMPLATE RENDERING ──────────────────────────────────────────────────────

def _render_template(context: dict) -> str:
    template_dir = Path(settings.report_template_dir).absolute()
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html", "j2"]),
    )
    # Custom filters
    env.filters["currency"] = lambda v: f"Rs. {float(v):,.2f}" if v else "N/A"
    env.filters["pct"]      = lambda v: f"{float(v)*100:.1f}%"  if v else "N/A"
    env.filters["date_fmt"] = lambda v: v.strftime("%d %B %Y")  if v else "N/A"

    template = env.get_template("report.html.j2")
    return template.render(**context)


# ─── HELPER FUNCTIONS ────────────────────────────────────────────────────────

def _get_statute_text(case_id: str, rule_id: str, db) -> Optional[str]:
    """Get statutory text stored during Chain B judgment retrieval."""
    try:
        from app.models.db import CaseStatute
        row = db.query(CaseStatute).filter_by(
            case_id=case_id, rule_id=rule_id
        ).first()
        return row.statute_text if row else None
    except Exception:
        return None


def _get_authority_for_rule(case_id: str, rule_id: str, db) -> Optional[str]:
    """Get the primary applicable judgment citation for a failed rule."""
    try:
        from app.models.db import JudgmentApplicability, Judgment, ComplianceResult
        # Map rule_id → ground_code
        from app.tasks.chain_b import RULE_TO_GROUND_MAP
        ground_code = RULE_TO_GROUND_MAP.get(rule_id)
        if not ground_code:
            return None
        ja = db.query(JudgmentApplicability).filter_by(
            case_id=case_id, ground_code=ground_code, status="APPLICABLE"
        ).first()
        if not ja:
            return None
        j = db.query(Judgment).filter_by(id=ja.judgment_id).first()
        return j.citation if j else None
    except Exception:
        return None


def _get_applicable_judgments(case_id: str, ground_code: str, db) -> list[dict]:
    """Get all applicable/similarity-retrieved judgments for a ground code."""
    try:
        from app.models.db import JudgmentApplicability, Judgment
        rows = db.query(JudgmentApplicability).filter_by(
            case_id=case_id, ground_code=ground_code
        ).all()
        results = []
        for row in rows:
            j = db.query(Judgment).filter_by(id=row.judgment_id).first()
            if j:
                results.append({
                    "citation":        j.citation,
                    "short_name":      j.short_name or j.title,
                    "court":           j.court,
                    "favor":           j.favor,
                    "holding_summary": j.holding_summary or "",
                    "status":          row.status,
                    "reason":          row.reason or "",
                })
        return results
    except Exception:
        return []


def _strength_label(score: float) -> str:
    if score >= 0.70: return "VERY STRONG"
    if score >= 0.50: return "STRONG"
    if score >= 0.25: return "ARGUABLE"
    return "WEAK"

def _strength_color(score: float) -> str:
    if score >= 0.70: return "#DC2626"   # red — strong for borrower = bad for bank
    if score >= 0.50: return "#EA580C"   # orange
    if score >= 0.25: return "#CA8A04"   # amber
    return "#16A34A"                      # green — weak for borrower = good for bank

def _exposure_label(score: float) -> str:
    if score >= 0.65: return "CRITICAL"
    if score >= 0.45: return "HIGH"
    if score >= 0.25: return "MEDIUM"
    return "LOW"

def _exposure_color(score: float) -> str:
    if score >= 0.65: return "#DC2626"
    if score >= 0.45: return "#EA580C"
    if score >= 0.25: return "#D97706"
    return "#16A34A"

def _score_color(score: int) -> str:
    if score >= 90: return "#16A34A"
    if score >= 70: return "#CA8A04"
    if score >= 50: return "#EA580C"
    return "#DC2626"

def _compliance_band(score: int) -> str:
    if score >= 90: return "Procedurally Clean"
    if score >= 70: return "Minor Issues"
    if score >= 50: return "Significant Risk"
    return "Fatal Defects"

def _calculate_compliance(failed_rules: list) -> int:
    DEDUCTIONS = {"FATAL": 40, "ABSOLUTE_BAR": 50, "CURABLE": 15,
                  "MINOR": 5, "ADVISORY": 3, "UNKNOWN": 10}
    total = sum(DEDUCTIONS.get(r.severity or "", 0) for r in failed_rules)
    return max(0, 100 - total)

def _calculate_exposure(ground_scores: list) -> float:
    scores = [g["ground_strength"] for g in ground_scores if g["ground_strength"] is not None]
    if not scores: return 0.0
    return round((max(scores) * 0.65) + (sum(scores) / len(scores) * 0.35), 3)


# ─── DISCLAIMER ──────────────────────────────────────────────────────────────

DISCLAIMER_TEXT = (
    "This report is a procedural compliance analysis generated by the SLRAI Platform. "
    "It is based exclusively on documents provided by the bank and facts verified by a "
    "bank officer through the SLRAI Verification Workbench. This report does not "
    "constitute legal advice and shall not be relied upon as such. The compliance "
    "findings, risk scores, and recommendations herein are analytical outputs based on "
    "statutory rules and judicial precedents — they do not predict court outcomes. "
    "The final decision to participate in any auction or enforcement action must be "
    "taken by the relevant party's own legal counsel after independent review. "
    "SLRAI and the generating institution accept no liability for decisions made "
    "solely in reliance on this report."
)
```

### 25.3 `app/reports/templates/report.html.j2` (Truncated version)

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width">
<title>SLRAI Legal Risk Analysis — {{ borrower_name }}</title>
<style>

/* ── FONTS ──────────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Noto Sans Devanagari for Hindi script rendering (must be installed in Docker) */
@font-face {
  font-family: 'NotoDevanagari';
  src: local('Noto Sans Devanagari');
}

/* ── PAGE SETUP ─────────────────────────────────────────────────────────── */
@page {
  size: A4;
  margin: 20mm 18mm 28mm 18mm;  /* top right bottom left */

  /* Footer on every page */
  @bottom-center {
    content: element(page-footer);
    font-size: 7pt;
  }
  @bottom-right {
    content: "Page " counter(page) " of " counter(pages);
    font-size: 7pt;
    color: #9CA3AF;
    font-family: Inter, sans-serif;
  }
}

/* ── GLOBAL ─────────────────────────────────────────────────────────────── */
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: Inter, 'NotoDevanagari', sans-serif;
  font-size: 9pt;
  color: #111827;
  line-height: 1.5;
  background: #ffffff;
}

/* ── CONFIDENTIAL WATERMARK ─────────────────────────────────────────────── */
/* WeasyPrint renders position:fixed elements on every page */
.watermark {
  position: fixed;
  top: 38%;
  left: 0;
  width: 100%;
  text-align: center;
  font-size: 52pt;
  font-weight: 800;
  color: rgba(220, 38, 38, 0.05);
  transform: rotate(-45deg);
  z-index: -1;
  letter-spacing: 12px;
  font-family: Inter, sans-serif;
  pointer-events: none;
}

/* ── FOOTER (repeated via position:running) ─────────────────────────────── */
#page-footer {
  position: running(page-footer);
  font-size: 6.5pt;
  color: #9CA3AF;
  border-top: 0.5pt solid #E5E7EB;
  padding-top: 3mm;
  font-family: Inter, sans-serif;
}

/* ── HEADER ─────────────────────────────────────────────────────────────── */
.report-header {
  border-bottom: 2.5pt solid #1E3A5F;
  padding-bottom: 6mm;
  margin-bottom: 5mm;
}

/* Top bar: SLRAI brand left, bank meta right */
.header-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 5mm;
}

/* SLRAI brand block */
.brand-block {
  display: flex;
  flex-direction: column;
  gap: 1mm;
}

.brand-slrai {
  font-size: 22pt;
  font-weight: 800;
  color: #1E3A5F;
  letter-spacing: 3px;
  line-height: 1;
}

.brand-full-name {
  font-size: 7.5pt;
  color: #6B7280;
  font-weight: 400;
  letter-spacing: 0.3px;
}

.brand-tagline {
  font-size: 6.5pt;
  color: #9CA3AF;
  margin-top: 0.5mm;
}

/* Bank / meta block on the right */
.header-meta {
  text-align: right;
  font-size: 7.5pt;
  color: #6B7280;
  line-height: 1.8;
}

.header-meta strong { color: #374151; }

/* Thin rule between brand and asset title */
.header-divider {
  border: none;
  border-top: 0.5pt solid #E5E7EB;
  margin: 0 0 4mm 0;
}

/* Asset/case title section */
.asset-title { }

.asset-label {
  font-size: 6.5pt;
  font-weight: 700;
  color: #9CA3AF;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 1.5mm;
}

.asset-heading {
  font-size: 18pt;
  font-weight: 700;
  color: #111827;
  line-height: 1.2;
}

.asset-subheading {
  font-size: 8.5pt;
  color: #6B7280;
  margin-top: 2mm;
  line-height: 1.6;
}

/* ── RECOMMENDATION BANNER ───────────────────────────────────────────────── */
.recommendation-banner {
  border-radius: 4pt;
  padding: 5mm 6mm;
  margin: 5mm 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.rec-label {
  font-size: 14pt;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: 0.5px;
}

.rec-text {
  font-size: 8pt;
  color: rgba(255,255,255,0.92);
  margin-top: 1.5mm;
  max-width: 80%;
  line-height: 1.5;
}

.rec-right {
  font-size: 7.5pt;
  color: rgba(255,255,255,0.75);
  text-align: right;
  white-space: nowrap;
}

/* ── SCORE DASHBOARD ────────────────────────────────────────────────────── */
.score-dashboard {
  display: flex;
  gap: 5mm;
  margin: 5mm 0;
}

.score-card {
  flex: 1;
  background: #F9FAFB;
  border: 0.5pt solid #E5E7EB;
  border-radius: 4pt;
  padding: 4mm 5mm;
  display: flex;
  align-items: center;
  gap: 4mm;
}

.gauge-wrapper {
  flex-shrink: 0;
}

.gauge-wrapper svg {
  display: block;
}

.score-text h3 {
  font-size: 7.5pt;
  font-weight: 600;
  color: #6B7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 1mm;
}

.score-number {
  font-size: 18pt;
  font-weight: 800;
  line-height: 1;
}

.score-band {
  font-size: 7pt;
  color: #6B7280;
  margin-top: 1mm;
}

/* ── SUMMARY STATS ──────────────────────────────────────────────────────── */
.summary-stats {
  display: flex;
  gap: 3mm;
  margin: 4mm 0;
}

.stat-pill {
  flex: 1;
  border-radius: 3pt;
  padding: 3mm 4mm;
  text-align: center;
}

.stat-pill .stat-num {
  font-size: 14pt;
  font-weight: 800;
}

.stat-pill .stat-label {
  font-size: 6.5pt;
  margin-top: 0.5mm;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.stat-critical { background: #FEF2F2; color: #DC2626; }
.stat-high     { background: #FFF7ED; color: #EA580C; }
.stat-review   { background: #F3F4F6; color: #6B7280; }

/* ── SECTION HEADERS ────────────────────────────────────────────────────── */
.section-header {
  display: flex;
  align-items: center;
  gap: 2mm;
  margin: 7mm 0 4mm 0;
  padding-bottom: 2mm;
  border-bottom: 1pt solid #E5E7EB;
}

.section-number {
  background: #1E3A5F;
  color: #ffffff;
  font-size: 7pt;
  font-weight: 700;
  padding: 1.5mm 2.5mm;
  border-radius: 2pt;
  letter-spacing: 0.5px;
}

.section-title {
  font-size: 11pt;
  font-weight: 700;
  color: #111827;
}

/* ── RED FLAGS ──────────────────────────────────────────────────────────── */
.red-flag-item {
  border-left: 3pt solid;
  margin-bottom: 4mm;
  padding: 3.5mm 4mm;
  background: #FAFAFA;
  border-radius: 0 3pt 3pt 0;
  page-break-inside: avoid;
}

.red-flag-header {
  display: flex;
  align-items: center;
  gap: 2.5mm;
  margin-bottom: 2mm;
}

.severity-badge {
  font-size: 6.5pt;
  font-weight: 700;
  padding: 1mm 2.5mm;
  border-radius: 2pt;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.red-flag-module {
  font-size: 7pt;
  color: #6B7280;
  font-weight: 500;
}

.red-flag-finding {
  font-size: 8.5pt;
  font-weight: 600;
  color: #111827;
  margin-bottom: 2mm;
  line-height: 1.4;
}

.statute-box {
  background: #EFF6FF;
  border: 0.5pt solid #BFDBFE;
  border-radius: 2pt;
  padding: 2.5mm 3mm;
  margin: 2mm 0;
  font-size: 7.5pt;
  color: #1D4ED8;
  line-height: 1.5;
}

.statute-label {
  font-weight: 700;
  font-size: 6.5pt;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin-bottom: 1mm;
}

.authority-line {
  font-size: 7pt;
  color: #4B5563;
  margin-top: 1.5mm;
  font-style: italic;
}

/* ── MODULE RESULTS ─────────────────────────────────────────────────────── */
.module-block {
  margin-bottom: 4mm;
  border: 0.5pt solid #E5E7EB;
  border-radius: 3pt;
  overflow: hidden;
  page-break-inside: avoid;
}

.module-title-row {
  display: flex;
  align-items: center;
  gap: 2mm;
  padding: 2.5mm 3.5mm;
  background: #F3F4F6;
  border-bottom: 0.5pt solid #E5E7EB;
}

.module-status-dot {
  width: 7pt;
  height: 7pt;
  border-radius: 50%;
  flex-shrink: 0;
}

.module-name {
  font-size: 8pt;
  font-weight: 600;
  color: #111827;
}

.rule-row {
  display: flex;
  gap: 2.5mm;
  padding: 2mm 3.5mm;
  border-bottom: 0.5pt solid #F3F4F6;
  align-items: flex-start;
}

.rule-row:last-child { border-bottom: none; }

.rule-status-badge {
  font-size: 6pt;
  font-weight: 700;
  padding: 0.5mm 2mm;
  border-radius: 1.5pt;
  flex-shrink: 0;
  margin-top: 0.5mm;
  text-transform: uppercase;
}

.badge-pass    { background: #D1FAE5; color: #065F46; }
.badge-fail    { background: #FEE2E2; color: #991B1B; }
.badge-unknown { background: #F3F4F6; color: #4B5563; }

.rule-message {
  font-size: 8pt;
  color: #374151;
  line-height: 1.4;
}

/* ── GROUND STRENGTH TABLE ──────────────────────────────────────────────── */
.ground-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 8pt;
  margin-bottom: 3mm;
}

.ground-table th {
  background: #1E3A5F;
  color: #ffffff;
  padding: 2.5mm 3mm;
  text-align: left;
  font-size: 7pt;
  font-weight: 600;
  letter-spacing: 0.3px;
}

.ground-table td {
  padding: 2.5mm 3mm;
  border-bottom: 0.5pt solid #F3F4F6;
  vertical-align: top;
}

.ground-table tr:nth-child(even) td { background: #F9FAFB; }

.strength-bar-bg {
  background: #E5E7EB;
  border-radius: 99pt;
  height: 5pt;
  width: 60pt;
  display: inline-block;
  vertical-align: middle;
}

.strength-bar-fill {
  height: 5pt;
  border-radius: 99pt;
  display: block;
}

.strength-badge {
  font-size: 6pt;
  font-weight: 700;
  padding: 0.5mm 2mm;
  border-radius: 2pt;
  color: white;
  text-transform: uppercase;
  display: inline-block;
  margin-top: 1mm;
}

/* ── JUDGMENT BLOCK ─────────────────────────────────────────────────────── */
.judgment-block {
  border: 0.5pt solid #E5E7EB;
  border-radius: 3pt;
  padding: 3mm 3.5mm;
  margin: 2mm 0;
  background: #FAFAFA;
  page-break-inside: avoid;
}

.judgment-citation {
  font-size: 8pt;
  font-weight: 600;
  color: #1E3A5F;
}

.judgment-court {
  font-size: 7pt;
  color: #6B7280;
  margin-left: 2mm;
}

.judgment-favor {
  font-size: 6.5pt;
  font-weight: 700;
  padding: 0.5mm 2mm;
  border-radius: 2pt;
  float: right;
  text-transform: uppercase;
}

.favor-bank     { background: #D1FAE5; color: #065F46; }
.favor-borrower { background: #FEE2E2; color: #991B1B; }
.favor-neutral  { background: #F3F4F6; color: #4B5563; }

.judgment-holding {
  font-size: 7.5pt;
  color: #374151;
  margin-top: 2mm;
  line-height: 1.5;
}

.judgment-status {
  font-size: 6.5pt;
  color: #6B7280;
  margin-top: 1.5mm;
  font-style: italic;
}

/* ── ALERT BOXES ────────────────────────────────────────────────────────── */
.alert-box {
  background: #FEF3C7;
  border: 0.5pt solid #F59E0B;
  border-radius: 3pt;
  padding: 3mm 4mm;
  margin: 3mm 0;
  font-size: 8pt;
  color: #78350F;
}

/* ── THIRD PARTY / PRAYER CLAUSE (v5.4) ────────────────────────────────────── */
.third-party-notice {
  background: var(--bg-warning); border: 1.5px solid var(--border-warning);
  border-radius: 8pt; padding: 4mm 5mm; margin: 3mm 0;
}
.notice-header { font-size: 9pt; font-weight: 600; color: var(--text-warning); margin-bottom: 1.5mm; }
.notice-body { font-size: 8pt; color: var(--text-warning); line-height: 1.5; }
.prayer-summary {
  background: var(--surface-1); border: 0.5pt solid var(--border);
  border-radius: 6pt; padding: 3mm 4mm; margin: 2mm 0 3mm;
}
.prayer-header { font-size: 7.5pt; font-weight: 600; color: var(--text-secondary); margin-bottom: 2mm; }
.prayer-tags { display: flex; flex-wrap: wrap; gap: 2mm; }
.prayer-tag {
  font-size: 7pt; padding: 1.5px 6px; border-radius: 3pt;
  border: 0.5pt solid var(--border-strong); color: var(--text-secondary);
  background: var(--surface-1);
}
.prayer-tag.challenged { border-color: #D85A30; color: #D85A30; font-weight: 500; }
.prayer-tag.interim { border-color: #BA7517; color: #BA7517; }
.prayer-mismatch-alert {
  font-size: 7.5pt; color: var(--text-warning); margin-top: 2mm;
  padding: 1.5mm 3mm; border-left: 2pt solid var(--border-warning);
}

/* ── PAGE BREAK UTILITIES ───────────────────────────────────────────────── */
.page-break    { page-break-after: always; }
.no-break      { page-break-inside: avoid; }
.break-before  { page-break-before: always; }

/* ── UTILITY ────────────────────────────────────────────────────────────── */
.clearfix::after { content: ""; display: table; clear: both; }
.text-right  { text-align: right; }
.text-center { text-align: center; }
.mt-2 { margin-top: 2mm; }
.mt-4 { margin-top: 4mm; }
.mb-2 { margin-bottom: 2mm; }
.bold { font-weight: 600; }
.muted { color: #6B7280; }
.small { font-size: 7.5pt; }

</style>
</head>
<body>

{# ── WATERMARK ─────────────────────────────────────────────────────────── #}
<div class="watermark">CONFIDENTIAL</div>

{# ── FOOTER (rendered on every page by @page rule) ─────────────────────── #}
<div id="page-footer">
  <span>{{ disclaimer_text[:180] }}...</span>
  &nbsp;|&nbsp;
  <span>Report ID: {{ report_id }} | Hash: {{ report_id[:12] }}...</span>
</div>

{# ════════════════════════════════════════════════════════════════════════ #}
{# PAGE 1 — EXECUTIVE SUMMARY                                              #}
{# ════════════════════════════════════════════════════════════════════════ #}

{# ── HEADER ───────────────────────────────────────────────────────────── #}
<div class="report-header">

  {# Top row: SLRAI brand (left) + bank meta (right) #}
  <div class="header-top">
    <div class="brand-block">
      <div class="brand-slrai">SLRAI</div>
      <div class="brand-full-name">SARFAESI Legal Risk &amp; Auction Intelligence Platform</div>
      <div class="brand-tagline">Legal Risk Analysis Report</div>
    </div>
    <div class="header-meta">
      <strong>Bank:</strong> {{ bank_name }}<br>
      <strong>Generated:</strong> {{ generated_at }}<br>
      <strong>Case Ref:</strong> {{ case_ref }}<br>
      <strong>DRT Case:</strong> {{ drt_case_number }}<br>
      <strong>DRT Bench:</strong> {{ drt_bench }}
    </div>
  </div>

  <hr class="header-divider">

  {# Asset / case identity #}
  <div class="asset-title">
    <div class="asset-label">Case Subject</div>
    <div class="asset-heading">{{ asset_heading }}</div>
    <div class="asset-subheading">{{ asset_subheading }}</div>
  </div>

</div>

{# ── RECOMMENDATION BANNER ────────────────────────────────────────────── #}
<div class="recommendation-banner" style="background: {{ recommendation_color }};">
  <div>
    <div class="rec-label">{{ recommendation_label }}</div>
    <div class="rec-text">{{ recommendation_text }}</div>
  </div>
  <div class="rec-right">
    Legal Risk<br>Assessment
  </div>
</div>

{# ── SCORE DASHBOARD ──────────────────────────────────────────────────── #}
<div class="score-dashboard">

  {# Compliance Score Gauge #}
  <div class="score-card">
    <div class="gauge-wrapper">
      <svg width="68" height="68" viewBox="0 0 68 68">
        <circle cx="34" cy="34" r="30" fill="none" stroke="#E5E7EB" stroke-width="7"/>
        <circle cx="34" cy="34" r="30" fill="none"
                stroke="{{ compliance_color }}" stroke-width="7"
                stroke-dasharray="{{ compliance_dash }} {{ circumference }}"
                stroke-dashoffset="81.7"
                stroke-linecap="round"
                transform="rotate(-90 34 34)"/>
        <text x="34" y="38" text-anchor="middle"
              font-size="14" font-weight="800" fill="{{ compliance_color }}"
              font-family="Inter, sans-serif">{{ compliance_score }}</text>
      </svg>
    </div>
    <div class="score-text">
      <h3>Compliance Score</h3>
      <div class="score-number" style="color: {{ compliance_color }};">
        {{ compliance_score }}<span style="font-size:10pt;font-weight:400;color:#6B7280;">/100</span>
      </div>
      <div class="score-band">{{ compliance_band }}</div>
    </div>
  </div>

  {# Litigation Exposure Gauge #}
  <div class="score-card">
    <div class="gauge-wrapper">
      <svg width="68" height="68" viewBox="0 0 68 68">
        <circle cx="34" cy="34" r="30" fill="none" stroke="#E5E7EB" stroke-width="7"/>
        <circle cx="34" cy="34" r="30" fill="none"
                stroke="{{ exposure_color }}" stroke-width="7"
                stroke-dasharray="{{ exposure_dash }} {{ circumference }}"
                stroke-dashoffset="81.7"
                stroke-linecap="round"
                transform="rotate(-90 34 34)"/>
        <text x="34" y="38" text-anchor="middle"
              font-size="11" font-weight="800" fill="{{ exposure_color }}"
              font-family="Inter, sans-serif">{{ exposure_pct }}%</text>
      </svg>
    </div>
    <div class="score-text">
      <h3>Litigation Exposure</h3>
      <div class="score-number" style="color: {{ exposure_color }};">
        {{ exposure_label }}
      </div>
      <div class="score-band">Borrower strength: {{ "%.2f"|format(litigation_exposure) }}</div>
    </div>
  </div>

</div>

{# ── SUMMARY STATS ────────────────────────────────────────────────────── #}
<div class="summary-stats">
  <div class="stat-pill stat-critical">
    <div class="stat-num">{{ fatal_count }}</div>
    <div class="stat-label">Fatal Defect{{ "s" if fatal_count != 1 else "" }}</div>
  </div>
  <div class="stat-pill stat-high">
    <div class="stat-num">{{ curable_count }}</div>
    <div class="stat-label">Curable Issue{{ "s" if curable_count != 1 else "" }}</div>
  </div>
  <div class="stat-pill stat-review">
    <div class="stat-num">{{ ground_scores|length }}</div>
    <div class="stat-label">Ground{{ "s" if ground_scores|length != 1 else "" }} Raised</div>
  </div>
</div>

{% if judgment_alerts %}
<div class="alert-box">
  <strong>⚠ Judgment Gap:</strong>
  No verified judicial precedent found for:
  {% for alert in judgment_alerts %}
    <strong>{{ alert.ground_code }}</strong>{% if not loop.last %}, {% endif %}
  {% endfor %}.
  Neutral judicial strength (0.40) applied. Consult a SARFAESI specialist.
</div>
{% endif %}

{% if sa_applicant_type != "BORROWER" and sa_applicant_type != "GUARANTOR" %}
<!-- Third Party Applicant Notice (v5.4) -->
<div class="third-party-notice">
  <div class="notice-header">⚠ Third Party SA — {{ sa_applicant_type | replace("_", " ") }}</div>
  <div class="notice-body">
    The Securitisation Application has been filed by a party who is
    <strong>neither the borrower nor the guarantor</strong>.
    Standard M1-M9 procedural analysis has been run on behalf of the bank.
    Module M10 (Third Party Rights) provides the primary legal framework
    for this applicant's claim. DRT will likely raise maintainability
    as a preliminary issue.
    {% if sa_applicant_type == "THIRD_PARTY_ATS" %}
    <br>ATS Advance Paid: Rs. {{ ats_advance_paid | format_currency }}
    | ATS Date: {{ ats_date }}
    | Simultaneous with Mortgage: {{ ats_simultaneous_mortgage }}
    {% endif %}
  </div>
</div>
{% endif %}

<!-- Prayer Clause Summary (v5.4) -->
<div class="prayer-summary">
  <div class="prayer-header">SA Prayer Clause — Measures Challenged</div>
  <div class="prayer-tags">
    {% if challenges_demand_notice %}
    <span class="prayer-tag">Section 13(2) Demand Notice</span>
    {% endif %}
    {% if challenges_possession_notice %}
    <span class="prayer-tag">Section 13(4) Possession Notice</span>
    {% endif %}
    {% if challenges_sale_notice %}
    <span class="prayer-tag">Sale Notice / Auction Proclamation</span>
    {% endif %}
    {% if challenges_auction %}
    <span class="prayer-tag challenged">Auction / Sale Certificate</span>
    {% endif %}
    {% if challenges_demand_amount %}
    <span class="prayer-tag">Amount Disputed</span>
    {% endif %}
    {% if interim_stay_prayed %}
    <span class="prayer-tag interim">Interim Stay Prayed
      {% if interim_stay_granted %} ✓ Granted{% else %} — Pending{% endif %}
    </span>
    {% endif %}
  </div>
  {% if not prayer_scope_covers_current_measure %}
  <div class="prayer-mismatch-alert">
    ⚠ Prayer Scope Mismatch: current enforcement measure not covered
    by the SA prayer. Bank should raise this as a preliminary objection.
  </div>
  {% endif %}
</div>

<div class="page-break"></div>

{# ════════════════════════════════════════════════════════════════════════ #}
{# PAGE 2 — RED FLAGS                                                       #}
{# ════════════════════════════════════════════════════════════════════════ #}

<div class="section-header">
  <span class="section-number">01</span>
  <span class="section-title">Red Flags — Procedural Violations Found</span>
</div>

{% if red_flags %}
  {% for flag in red_flags %}
  <div class="red-flag-item no-break" style="border-color: {{ flag.severity_color }};">
    <div class="red-flag-header">
      <span class="severity-badge" style="background: {{ flag.severity_color }};">
        {{ flag.severity_label }}
      </span>
      <span class="red-flag-module">{{ flag.module }}</span>
    </div>
    <div class="red-flag-finding">{{ flag.finding }}</div>

    {% if flag.statute_text %}
    <div class="statute-box">
      <div class="statute-label">Statutory Provision</div>
      {{ flag.statute_text }}
    </div>
    {% endif %}

    {% if flag.authority %}
    <div class="authority-line">
      Authority: {{ flag.authority }}
    </div>
    {% endif %}
  </div>
  {% endfor %}
{% else %}
  <p style="color: #16A34A; font-weight: 600; font-size: 9pt; padding: 3mm 0;">
    ✓ No procedural violations identified in the reviewed documents.
  </p>
{% endif %}

<div class="page-break"></div>

{# ════════════════════════════════════════════════════════════════════════ #}
{# PAGE 3+ — GROUND STRENGTH ANALYSIS                                       #}
{# ════════════════════════════════════════════════════════════════════════ #}

<div class="section-header">
  <span class="section-number">02</span>
  <span class="section-title">Borrower's Legal Grounds — Strength Analysis</span>
</div>

<p class="small muted mb-2">
  For each ground raised by the borrower in the SA, this section shows:
  how well the facts support it (Factual Score) and whether binding judicial
  precedent supports it (Judicial Score). Higher scores = stronger borrower case = higher risk for bank/purchaser.
</p>

{% if ground_scores %}
<table class="ground-table">
  <thead>
    <tr>
      <th style="width:32%;">Ground Raised</th>
      <th style="width:14%;">Factual Score</th>
      <th style="width:14%;">Judicial Score</th>
      <th style="width:22%;">Overall Strength</th>
      <th style="width:18%;">Asses
```

*(Note: The `report.html.j2` file has been partially appended as the input provided was truncated. The remainder of the HTML should be added when available.)*

---

## 26. Appendix: API Endpoints Tracker

Single source of truth for every endpoint in the system.
Legend: ⬜ Not started | 🟨 In progress | ✅ Done + tested | 🔒 Auth required

### 1. AUTH — `app/api/auth.py`

| Method | Path | Auth | Role | Status | Notes |
|---|---|---|---|---|---|
| POST | `/api/v1/auth/register` | None | — | ✅ | Creates bank + first BANK_ADMIN. Returns JWT. |
| POST | `/api/v1/auth/login` | None | — | ✅ | email + password → JWT. Constant-time compare. |
| POST | `/api/v1/auth/refresh` | 🔒 | Any | ✅ | Re-issues fresh 8hr token. Token must be currently valid. |
| POST | `/api/v1/auth/users` | 🔒 | BANK_ADMIN, SYSTEM_ADMIN | ✅ | Creates BANK_OFFICER/BANK_ADMIN in admin's bank. |
| GET | `/api/v1/auth/me` | 🔒 | Any | ✅ | Returns current user profile from DB. |

### 2. CASES — `app/api/cases.py`

| Method | Path | Auth | Role | Status | Notes |
|---|---|---|---|---|---|
| POST | `/api/v1/cases` | 🔒 | Officer+ | ✅ | Creates case. Runs F2 pre-intake filter. bank_id from JWT. |
| GET | `/api/v1/cases` | 🔒 | Officer+ | ✅ | Lists all cases in bank. Pagination, status filter, search. |
| GET | `/api/v1/cases/{case_id}` | 🔒 | Officer+ | ✅ | Full case detail. 404 if wrong bank. |
| PATCH | `/api/v1/cases/{case_id}` | 🔒 | Officer+ | ✅ | Update metadata fields only. Status never client-set. |
| GET | `/api/v1/cases/{case_id}/pipeline-status` | 🔒 | Officer+ | ✅ | Status + pipeline_stage + progress_pct. Poll every 3s. |
| POST | `/api/v1/cases/{case_id}/resume` | 🔒 | Officer+ | ✅ | Resume from PENDING_JUDGMENT_REVIEW. Fires Chain B partial. |
| DELETE | `/api/v1/cases/{case_id}` | 🔒 | BANK_ADMIN | ✅ | Soft delete. S3 documents retained. |

### 3. DOCUMENTS — `app/api/documents.py`

| Method | Path | Auth | Role | Status | Notes |
|---|---|---|---|---|---|
| POST | `/api/v1/cases/{case_id}/documents` | 🔒 | Officer+ | ⬜ | Multipart upload. SHA-256 dedupe. Fires Chain A if first doc. |
| GET | `/api/v1/cases/{case_id}/documents` | 🔒 | Officer+ | ⬜ | List all documents for case. |
| GET | `/api/v1/cases/{case_id}/documents/{doc_id}` | 🔒 | Officer+ | ⬜ | Single document metadata. |
| GET | `/api/v1/cases/{case_id}/documents/{doc_id}/file` | 🔒 | Officer+ | ⬜ | Stream original file (never raw S3 URL). |

**Build target: Phase H2**

### 4. WORKBENCH — `app/api/workbench.py`

| Method | Path | Auth | Role | Status | Notes |
|---|---|---|---|---|---|
| GET | `/api/v1/cases/{case_id}/workbench` | 🔒 | Officer+ | ⬜ | Three sections: low_confidence, not_found, conflict. |
| GET | `/api/v1/cases/{case_id}/facts` | 🔒 | Officer+ | ⬜ | All case_facts with confidence + source. |
| PATCH | `/api/v1/cases/{case_id}/facts/{fact_id}` | 🔒 | Officer+ | ⬜ | Confirm or correct a fact. Sets human_confirmed=True. |
| PATCH | `/api/v1/cases/{case_id}/workbench/conflicts/{conflict_id}` | 🔒 | Officer+ | ⬜ | Resolve a fact conflict (candidate_a / candidate_b / custom). |
| POST | `/api/v1/cases/{case_id}/workbench/confirm-all` | 🔒 | Officer+ | ⬜ | Validates preconditions. Fires Chain B. 422 if incomplete. |

**Build target: Phase H4**
**Dependency:** Requires `fact_conflicts` table, `CaseFact.requires_workbench` property

### 5. COMPLIANCE / RESULTS — `app/api/results.py`

| Method | Path | Auth | Role | Status | Notes |
|---|---|---|---|---|---|
| GET | `/api/v1/cases/{case_id}/compliance` | 🔒 | Officer+ | ⬜ | All compliance_results grouped by module (M1-M9). |
| GET | `/api/v1/cases/{case_id}/grounds` | 🔒 | Officer+ | ⬜ | Ground strength scores + litigation exposure. |
| GET | `/api/v1/cases/{case_id}/judgments` | 🔒 | Officer+ | ⬜ | Applicable (Class A) + similarity-retrieved (Class B) judgments. |
| GET | `/api/v1/cases/{case_id}/statistics` | 🔒 | Officer+ | ⬜ | NEW: 12/15 corpus win-rate stats per ground code. |

**Build target: Phase H5–H8 (populated incrementally as engines complete)**

### 6. REPORTS — `app/api/reports.py`

| Method | Path | Auth | Role | Status | Notes |
|---|---|---|---|---|---|
| POST | `/api/v1/cases/{case_id}/report` | 🔒 | Officer+ | ⬜ | Generate/regenerate report. Requires status=COMPLETE. |
| GET | `/api/v1/cases/{case_id}/report` | 🔒 | Officer+ | ⬜ | Latest report as JSON. |
| GET | `/api/v1/cases/{case_id}/report/pdf` | 🔒 | Officer+ | ⬜ | StreamingResponse — PDF bytes via S3, never raw URL. |

**Build target: Phase H9**
**Dependency:** `generator.py` and `report.html.j2` already written — just needs wiring

### 7. SYSTEM / HEALTH

| Method | Path | Auth | Role | Status | Notes |
|---|---|---|---|---|---|
| GET | `/health` | None | — | ⬜ | Liveness check — DB + Redis + Qdrant ping. |
| GET | `/docs` | None | — | ✅ (auto) | FastAPI auto-generated Swagger UI. |
| GET | `/openapi.json` | None | — | ✅ (auto) | OpenAPI spec — Karan generates TS types from this. |

**Build target: Phase H0**

### SUMMARY COUNTS

| Module | Total Endpoints | Done | Remaining |
|---|---|---|---|
| Auth | 5 | 5 | 0 |
| Cases | 7 | 7 | 0 |
| Documents | 4 | 0 | 4 |
| Workbench | 5 | 0 | 5 |
| Compliance/Results | 4 | 0 | 4 |
| Reports | 3 | 0 | 3 |
| System | 3 | 1 | 2 |
| **TOTAL** | **31** | **13** | **18** |

### REQUEST/RESPONSE SCHEMA QUICK REFERENCE

For exact Pydantic schemas, see Blueprint Section 17. Summary of what each endpoint expects/returns — used by the Streamlit dashboard to build forms.

**Auth**
```
POST /auth/register   → {bank_name, bank_short_code, admin_email, admin_password}
POST /auth/login      → {email, password}
POST /auth/users      → {email, password, role}  [needs admin token]
```

**Cases**
```
POST /cases  → {borrower_name, case_ref?, drt_case_number?, drt_bench?, property_description?, loan_account_number?, principal_amount?}
PATCH /cases/{id} → {case_ref?, drt_case_number?, drt_bench?, property_description?, loan_account_number?}
```

**Documents**
```
POST /cases/{id}/documents → multipart: file, doc_type
```

**Workbench**
```
PATCH /facts/{fact_id} → {corrected_value?, human_confirmed}
PATCH /workbench/conflicts/{conflict_id} → {resolution: "candidate_a"|"candidate_b"|"custom", custom_value?}
POST /workbench/confirm-all → {trigger_analysis: bool}
```

**Reports**
```
POST /report → {} (empty body — case_id from path)
```

---

## 27. Appendix: Streamlit API Dashboard (`dashboard.py`)

Internal tool for testing every FastAPI endpoint without needing the real Next.js frontend. Not for production use — this is a developer/QA tool.

```python
# dashboard.py
"""
SLRAI — Streamlit API Test Dashboard

Internal tool for testing every FastAPI endpoint without needing the real
Next.js frontend. Not for production use — this is a developer/QA tool.

Run with:
    streamlit run dashboard.py

Requires:
    pip install streamlit requests pandas

Set API_BASE_URL below or via environment variable SLRAI_API_URL.
Default assumes the API is running locally via docker-compose.
"""

import os
import json
from datetime import datetime

import requests
import streamlit as st
import pandas as pd

# ─── CONFIG ──────────────────────────────────────────────────────────────────

API_BASE_URL = os.environ.get("SLRAI_API_URL", "http://localhost:8000/api/v1")

st.set_page_config(
    page_title="SLRAI API Dashboard",
    page_icon="⚖️",
    layout="wide",
)

# ─── SESSION STATE INIT ───────────────────────────────────────────────────────

if "token" not in st.session_state:
    st.session_state.token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "current_case_id" not in st.session_state:
    st.session_state.current_case_id = None
if "request_log" not in st.session_state:
    st.session_state.request_log = []


# ─── HTTP HELPER ──────────────────────────────────────────────────────────────

def api_call(method: str, path: str, **kwargs) -> tuple[int, dict | str]:
    """
    Makes a request to the API, automatically attaching the auth token.
    Logs every call to the request log shown in the sidebar.
    Returns (status_code, response_body).
    """
    url = f"{API_BASE_URL}{path}"
    headers = kwargs.pop("headers", {})
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"

    try:
        response = requests.request(method, url, headers=headers, timeout=30, **kwargs)
        try:
            body = response.json()
        except ValueError:
            body = response.text

        # Log the call
        st.session_state.request_log.insert(0, {
            "time":   datetime.now().strftime("%H:%M:%S"),
            "method": method,
            "path":   path,
            "status": response.status_code,
        })
        st.session_state.request_log = st.session_state.request_log[:30]  # keep last 30

        return response.status_code, body

    except requests.exceptions.ConnectionError:
        st.session_state.request_log.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "method": method, "path": path, "status": "CONN_ERR",
        })
        return 0, {"error": f"Cannot connect to {url}. Is the API running?"}
    except requests.exceptions.Timeout:
        return 0, {"error": "Request timed out after 30s."}


def show_response(status: int, body):
    """Standard response display block — color coded by status."""
    if status == 0:
        st.error(body.get("error", "Connection failed"))
    elif 200 <= status < 300:
        st.success(f"Status {status}")
        st.json(body)
    elif status == 401:
        st.warning(f"Status {status} — Unauthorized. Check your token below.")
        st.json(body)
    elif status == 404:
        st.warning(f"Status {status} — Not Found")
        st.json(body)
    elif status == 422:
        st.warning(f"Status {status} — Validation Error")
        st.json(body)
    else:
        st.error(f"Status {status}")
        st.json(body)


def require_auth():
    """Show a blocking warning if not authenticated. Call at top of protected tabs."""
    if not st.session_state.token:
        st.warning("⚠️ Not logged in. Go to the **Auth** tab and log in first.")
        st.stop()


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("⚖️ SLRAI Dashboard")
    st.caption(f"API: `{API_BASE_URL}`")

    st.divider()

    if st.session_state.token:
        st.success("🟢 Authenticated")
        if st.session_state.user_info:
            u = st.session_state.user_info
            st.write(f"**{u.get('email', 'unknown')}**")
            st.write(f"Role: `{u.get('role', '?')}`")
            st.write(f"Bank ID: `{str(u.get('bank_id', '?'))[:8]}...`")
        if st.button("Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.user_info = None
            st.rerun()
    else:
        st.error("🔴 Not authenticated")

    st.divider()

    if st.session_state.current_case_id:
        st.info(f"**Active case:**\n`{st.session_state.current_case_id[:13]}...`")
        if st.button("Clear active case", use_container_width=True):
            st.session_state.current_case_id = None
            st.rerun()

    st.divider()
    st.caption("API Base URL override")
    new_url = st.text_input("URL", value=API_BASE_URL, label_visibility="collapsed")
    if new_url != API_BASE_URL:
        st.info("Restart with SLRAI_API_URL env var set to persist this change.")

    st.divider()
    st.caption("**Request Log** (last 30)")
    if st.session_state.request_log:
        log_df = pd.DataFrame(st.session_state.request_log)
        st.dataframe(log_df, hide_index=True, use_container_width=True, height=300)
    else:
        st.caption("No requests yet.")


# ─── MAIN TABS ────────────────────────────────────────────────────────────────

tabs = st.tabs([
    "🔐 Auth",
    "📁 Cases",
    "📄 Documents",
    "✅ Workbench",
    "📊 Results",
    "📑 Report",
    "🩺 Health",
])

# ════════════════════════════════════════════════════════════════════════════
# TAB: AUTH
# ════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.header("Authentication")

    auth_action = st.radio(
        "Action", ["Login", "Register New Bank", "Create User", "Refresh Token", "Whoami"],
        horizontal=True
    )

    if auth_action == "Login":
        st.subheader("POST /auth/login")
        with st.form("login_form"):
            email = st.text_input("Email", value="admin@slrai.internal")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", type="primary")

        if submitted:
            status, body = api_call("POST", "/auth/login", json={
                "email": email, "password": password
            })
            if status == 200:
                st.session_state.token = body["access_token"]
                st.session_state.user_info = {
                    "email": body["email"], "role": body["role"], "bank_id": body["bank_id"]
                }
                st.success(f"Logged in as {body['email']} [{body['role']}]")
                st.rerun()
            else:
                show_response(status, body)

    elif auth_action == "Register New Bank":
        st.subheader("POST /auth/register")
        st.caption("Creates a new bank + first BANK_ADMIN user in one transaction.")
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            with col1:
                bank_name = st.text_input("Bank Name", value="Test Bank Ltd")
                bank_code = st.text_input("Bank Short Code (uppercase)", value="TESTBNK")
            with col2:
                admin_email = st.text_input("Admin Email", value="admin@testbank.com")
                admin_password = st.text_input(
                    "Admin Password", type="password",
                    help="Min 8 chars, 1 digit, 1 uppercase"
                )
            submitted = st.form_submit_button("Register", type="primary")

        if submitted:
            status, body = api_call("POST", "/auth/register", json={
                "bank_name": bank_name,
                "bank_short_code": bank_code,
                "admin_email": admin_email,
                "admin_password": admin_password,
            })
            if status == 201:
                st.session_state.token = body["access_token"]
                st.session_state.user_info = {
                    "email": body["email"], "role": body["role"], "bank_id": body["bank_id"]
                }
                st.success("Bank registered and logged in!")
                st.rerun()
            else:
                show_response(status, body)

    elif auth_action == "Create User":
        require_auth()
        st.subheader("POST /auth/users")
        st.caption("BANK_ADMIN or SYSTEM_ADMIN only. Creates a user in your bank.")
        with st.form("create_user_form"):
            new_email = st.text_input("New User Email")
            new_password = st.text_input("New User Password", type="password")
            new_role = st.selectbox("Role", ["BANK_OFFICER", "BANK_ADMIN"])
            submitted = st.form_submit_button("Create User", type="primary")

        if submitted:
            status, body = api_call("POST", "/auth/users", json={
                "email": new_email, "password": new_password, "role": new_role
            })
            show_response(status, body)

    elif auth_action == "Refresh Token":
        require_auth()
        st.subheader("POST /auth/refresh")
        if st.button("Refresh My Token", type="primary"):
            status, body = api_call("POST", "/auth/refresh")
            if status == 200:
                st.session_state.token = body["access_token"]
                st.success("Token refreshed.")
            show_response(status, body)

    elif auth_action == "Whoami":
        require_auth()
        st.subheader("GET /auth/me")
        if st.button("Fetch My Profile", type="primary"):
            status, body = api_call("GET", "/auth/me")
            show_response(status, body)

    with st.expander("🔑 Manual token entry (paste a token from elsewhere)"):
        manual_token = st.text_area("JWT Token", height=80)
        if st.button("Use this token"):
            st.session_state.token = manual_token.strip()
            st.success("Token set.")
            st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# TAB: CASES
# ════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.header("Case Management")
    require_auth()

    case_action = st.radio(
        "Action",
        ["List Cases", "Create Case", "Get Case", "Update Case",
         "Pipeline Status", "Resume Analysis", "Delete Case"],
        horizontal=True
    )

    if case_action == "List Cases":
        st.subheader("GET /cases")
        col1, col2, col3 = st.columns(3)
        with col1:
            page = st.number_input("Page", min_value=1, value=1)
        with col2:
            page_size = st.number_input("Page Size", min_value=1, max_value=100, value=20)
        with col3:
            status_filter = st.selectbox("Status filter", [
                "(any)", "DRAFT", "INTAKE_REJECTED", "PROCESSING",
                "PENDING_HUMAN_REVIEW", "ANALYSING", "PENDING_JUDGMENT_REVIEW",
                "COMPLETE", "FAILED"
            ])
        search = st.text_input("Search (borrower name / case ref)")

        if st.button("Fetch Cases", type="primary"):
            params = {"page": page, "page_size": page_size}
            if status_filter != "(any)":
                params["status"] = status_filter
            if search:
                params["search"] = search
            status, body = api_call("GET", "/cases", params=params)

            if status == 200:
                st.success(f"Total: {body['total']} cases")
                if body["items"]:
                    df = pd.DataFrame(body["items"])
                    st.dataframe(df, use_container_width=True, hide_index=True)

                    # Quick-select for other tabs
                    selected = st.selectbox(
                        "Select a case to set as active",
                        options=[item["id"] for item in body["items"]],
                        format_func=lambda x: next(
                            (f"{i['borrower_name']} ({i['status']})"
                             for i in body["items"] if i["id"] == x), x
                        )
                    )
                    if st.button("Set as Active Case"):
                        st.session_state.current_case_id = selected
                        st.rerun()
                else:
                    st.info("No cases found.")
            else:
                show_response(status, body)

    elif case_action == "Create Case":
        st.subheader("POST /cases")
        with st.form("create_case_form"):
            borrower_name = st.text_input("Borrower Name *", value="Test Borrower")
            col1, col2 = st.columns(2)
            with col1:
                case_ref = st.text_input("Case Ref")
                drt_case_number = st.text_input("DRT Case Number")
                drt_bench = st.text_input("DRT Bench")
            with col2:
                property_description = st.text_area("Property Description", height=80)
                loan_account_number = st.text_input("Loan Account Number")
                principal_amount = st.number_input(
                    "Principal Amount (Rs.)", min_value=0.0, value=4000000.0, step=10000.0
                )
            submitted = st.form_submit_button("Create Case", type="primary")

        if submitted:
            payload = {
                "borrower_name": borrower_name,
                "case_ref": case_ref or None,
                "drt_case_number": drt_case_number or None,
                "drt_bench": drt_bench or None,
                "property_description": property_description or None,
                "loan_account_number": loan_account_number or None,
                "principal_amount": principal_amount if principal_amount > 0 else None,
            }
            status, body = api_call("POST", "/cases", json=payload)
            if status == 201:
                st.session_state.current_case_id = body["id"]
                st.success(f"Case created: {body['id']} — status: {body['status']}")
            show_response(status, body)

    elif case_action == "Get Case":
        st.subheader("GET /cases/{case_id}")
        case_id = st.text_input(
            "Case ID",
            value=st.session_state.current_case_id or "",
        )
        if st.button("Fetch Case", type="primary") and case_id:
            status, body = api_call("GET", f"/cases/{case_id}")
            show_response(status, body)

    elif case_action == "Update Case":
        st.subheader("PATCH /cases/{case_id}")
        case_id = st.text_input("Case ID", value=st.session_state.current_case_id or "")
        with st.form("update_case_form"):
            case_ref = st.text_input("New Case Ref (leave blank to skip)")
            drt_bench = st.text_input("New DRT Bench (leave blank to skip)")
            submitted = st.form_submit_button("Update", type="primary")
        if submitted and case_id:
            payload = {}
            if case_ref: payload["case_ref"] = case_ref
            if drt_bench: payload["drt_bench"] = drt_bench
            status, body = api_call("PATCH", f"/cases/{case_id}", json=payload)
            show_response(status, body)

    elif case_action == "Pipeline Status":
        st.subheader("GET /cases/{case_id}/pipeline-status")
        case_id = st.text_input("Case ID", value=st.session_state.current_case_id or "")
        auto_refresh = st.checkbox("Auto-refresh every 3s (simulates frontend polling)")
        if st.button("Check Status", type="primary") and case_id:
            status, body = api_call("GET", f"/cases/{case_id}/pipeline-status")
            if status == 200:
                progress = body.get("progress_pct", 0)
                st.progress(progress / 100, text=f"{body.get('status')} — {progress}%")
                st.write(body.get("message", ""))
            show_response(status, body)
        if auto_refresh and case_id:
            import time
            time.sleep(3)
            st.rerun()

    elif case_action == "Resume Analysis":
        st.subheader("POST /cases/{case_id}/resume")
        st.caption("Only works when case status = PENDING_JUDGMENT_REVIEW")
        case_id = st.text_input("Case ID", value=st.session_state.current_case_id or "")
        if st.button("Resume Analysis", type="primary") and case_id:
            status, body = api_call("POST", f"/cases/{case_id}/resume")
            show_response(status, body)

    elif case_action == "Delete Case":
        st.subheader("DELETE /cases/{case_id}")
        st.caption("BANK_ADMIN only. Soft delete — sets status to DRAFT.")
        case_id = st.text_input("Case ID", value=st.session_state.current_case_id or "")
        confirm = st.checkbox("I understand this will reset the case")
        if st.button("Delete Case", type="primary", disabled=not confirm) and case_id:
            status, body = api_call("DELETE", f"/cases/{case_id}")
            if status == 204:
                st.success("Case soft-deleted.")
            else:
                show_response(status, body)


# ════════════════════════════════════════════════════════════════════════════
# TAB: DOCUMENTS
# ════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.header("Document Upload")
    require_auth()

    doc_action = st.radio("Action", ["Upload Document", "List Documents"], horizontal=True)

    case_id = st.text_input(
        "Case ID",
        value=st.session_state.current_case_id or "",
        key="doc_case_id"
    )

    if doc_action == "Upload Document":
        st.subheader("POST /cases/{case_id}/documents")
        uploaded_file = st.file_uploader(
            "Choose a PDF/image file", type=["pdf", "jpg", "jpeg", "png", "tiff"]
        )
        doc_type = st.selectbox("Document Type", [
            "SA", "DEMAND_NOTICE", "OBJECTION", "BANK_REPLY", "POSSESSION_NOTICE",
            "SALE_NOTICE", "VALUATION_REPORT", "LOAN_AGREEMENT", "GUARANTEE",
            "ACCOUNT_STATEMENT", "UDYAM_CERT", "LEASE_DEED", "MORTGAGE_DEED",
            "DRT_ORDER", "OTHER"
        ])

        if st.button("Upload", type="primary") and uploaded_file and case_id:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            data = {"doc_type": doc_type}
            status, body = api_call(
                "POST", f"/cases/{case_id}/documents", files=files, data=data
            )
            if status == 201:
                st.success(f"Uploaded! SHA-256: {body.get('sha256_hash', 'N/A')[:16]}...")
            elif status == 409:
                st.warning("Duplicate document — already uploaded for this case.")
            show_response(status, body)

    elif doc_action == "List Documents":
        st.subheader("GET /cases/{case_id}/documents")
        if st.button("Fetch Documents", type="primary") and case_id:
            status, body = api_call("GET", f"/cases/{case_id}/documents")
            if status == 200 and isinstance(body, list) and body:
                st.dataframe(pd.DataFrame(body), use_container_width=True, hide_index=True)
            else:
                show_response(status, body)


# ════════════════════════════════════════════════════════════════════════════
# TAB: WORKBENCH
# ════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.header("Verification Workbench")
    require_auth()

    case_id = st.text_input(
        "Case ID", value=st.session_state.current_case_id or "", key="wb_case_id"
    )

    wb_action = st.radio(
        "Action",
        ["View Workbench", "All Facts", "Confirm/Correct Fact",
         "Resolve Conflict", "Confirm All & Trigger Analysis"],
        horizontal=True
    )

    if wb_action == "View Workbench":
        st.subheader("GET /cases/{case_id}/workbench")
        if st.button("Load Workbench", type="primary") and case_id:
            status, body = api_call("GET", f"/cases/{case_id}/workbench")
            if status == 200:
                col1, col2, col3 = st.columns(3)
                col1.metric("Low Confidence", len(body.get("low_confidence_items", [])))
                col2.metric("Not Found", len(body.get("not_found_items", [])))
                col3.metric("Conflicts", len(body.get("conflict_items", [])))

                if body.get("low_confidence_items"):
                    st.write("**Low Confidence Items**")
                    st.dataframe(pd.DataFrame(body["low_confidence_items"]),
                                use_container_width=True, hide_index=True)
                if body.get("not_found_items"):
                    st.write("**Not Found Items**")
                    st.dataframe(pd.DataFrame(body["not_found_items"]),
                                use_container_width=True, hide_index=True)
                if body.get("conflict_items"):
                    st.write("**Conflict Items**")
                    st.dataframe(pd.DataFrame(body["conflict_items"]),
                                use_container_width=True, hide_index=True)
            else:
                show_response(status, body)

    elif wb_action == "All Facts":
        st.subheader("GET /cases/{case_id}/facts")
        if st.button("Load All Facts", type="primary") and case_id:
            status, body = api_call("GET", f"/cases/{case_id}/facts")
            if status == 200 and isinstance(body, list):
                st.dataframe(pd.DataFrame(body), use_container_width=True, hide_index=True, height=500)
            else:
                show_response(status, body)

    elif wb_action == "Confirm/Correct Fact":
        st.subheader("PATCH /cases/{case_id}/facts/{fact_id}")
        with st.form("confirm_fact_form"):
            fact_id = st.text_input("Fact ID")
            corrected_value = st.text_input("Corrected Value (leave blank to accept as-is)")
            human_confirmed = st.checkbox("Mark as human_confirmed", value=True)
            submitted = st.form_submit_button("Submit", type="primary")
        if submitted and case_id and fact_id:
            payload = {"human_confirmed": human_confirmed}
            if corrected_value:
                payload["corrected_value"] = corrected_value
            status, body = api_call(
                "PATCH", f"/cases/{case_id}/facts/{fact_id}", json=payload
            )
            show_response(status, body)

    elif wb_action == "Resolve Conflict":
        st.subheader("PATCH /cases/{case_id}/workbench/conflicts/{conflict_id}")
        with st.form("resolve_conflict_form"):
            conflict_id = st.text_input("Conflict ID")
            resolution = st.selectbox("Resolution", ["candidate_a", "candidate_b", "custom"])
            custom_value = st.text_input("Custom Value (only if resolution=custom)")
            submitted = st.form_submit_button("Resolve", type="primary")
        if submitted and case_id and conflict_id:
            payload = {"resolution": resolution}
            if resolution == "custom":
                payload["custom_value"] = custom_value
            status, body = api_call(
                "PATCH", f"/cases/{case_id}/workbench/conflicts/{conflict_id}", json=payload
            )
            show_response(status, body)

    elif wb_action == "Confirm All & Trigger Analysis":
        st.subheader("POST /cases/{case_id}/workbench/confirm-all")
        st.caption("Validates all required fields are confirmed, then fires Chain B.")
        trigger = st.checkbox("trigger_analysis", value=True)
        if st.button("Confirm All", type="primary") and case_id:
            status, body = api_call(
                "POST", f"/cases/{case_id}/workbench/confirm-all",
                json={"trigger_analysis": trigger}
            )
            if status == 422:
                st.warning("Cannot proceed — some required fields are unconfirmed:")
                st.json(body.get("unconfirmed_fields", body))
            else:
                show_response(status, body)


# ════════════════════════════════════════════════════════════════════════════
# TAB: RESULTS
# ════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.header("Compliance, Grounds & Judgments")
    require_auth()

    case_id = st.text_input(
        "Case ID", value=st.session_state.current_case_id or "", key="results_case_id"
    )

    result_action = st.radio(
        "View", ["Compliance Results", "Ground Scores", "Judgments", "Corpus Statistics"],
        horizontal=True
    )

    if result_action == "Compliance Results":
        st.subheader("GET /cases/{case_id}/compliance")
        if st.button("Load Compliance", type="primary") and case_id:
            status, body = api_call("GET", f"/cases/{case_id}/compliance")
            if status == 200:
                st.metric("Compliance Score", body.get("compliance_score", "N/A"))
                modules = body.get("modules", {})
                for mod_name, results in modules.items():
                    with st.expander(f"**{mod_name}** ({len(results)} rules)"):
                        st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
            else:
                show_response(status, body)

    elif result_action == "Ground Scores":
        st.subheader("GET /cases/{case_id}/grounds")
        if st.button("Load Grounds", type="primary") and case_id:
            status, body = api_call("GET", f"/cases/{case_id}/grounds")
            if status == 200:
                exposure = body.get("litigation_exposure", 0)
                st.metric("Litigation Exposure", f"{exposure:.2f}",
                          body.get("exposure_label", ""))
                grounds = body.get("grounds_raised", [])
                if grounds:
                    st.dataframe(pd.DataFrame(grounds), use_container_width=True, hide_index=True)
            else:
                show_response(status, body)

    elif result_action == "Judgments":
        st.subheader("GET /cases/{case_id}/judgments")
        if st.button("Load Judgments", type="primary") and case_id:
            status, body = api_call("GET", f"/cases/{case_id}/judgments")
            show_response(status, body)

    elif result_action == "Corpus Statistics":
        st.subheader("GET /cases/{case_id}/statistics")
        st.caption("The 12/15 win-rate feature — verified vs full corpus counts.")
        if st.button("Load Statistics", type="primary") and case_id:
            status, body = api_call("GET", f"/cases/{case_id}/statistics")
            show_response(status, body)


# ════════════════════════════════════════════════════════════════════════════
# TAB: REPORT
# ════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.header("Report Generation")
    require_auth()

    case_id = st.text_input(
        "Case ID", value=st.session_state.current_case_id or "", key="report_case_id"
    )

    report_action = st.radio(
        "Action", ["Generate Report", "Get Report JSON", "Download PDF"], horizontal=True
    )

    if report_action == "Generate Report":
        st.subheader("POST /cases/{case_id}/report")
        if st.button("Generate", type="primary") and case_id:
            status, body = api_call("POST", f"/cases/{case_id}/report")
            show_response(status, body)

    elif report_action == "Get Report JSON":
        st.subheader("GET /cases/{case_id}/report")
        if st.button("Fetch JSON", type="primary") and case_id:
            status, body = api_call("GET", f"/cases/{case_id}/report")
            if status == 200:
                col1, col2, col3 = st.columns(3)
                col1.metric("Compliance Score", body.get("compliance_score"))
                col2.metric("Litigation Exposure", body.get("litigation_exposure"))
                col3.metric("Recommendation", body.get("recommendation_label", "N/A"))
            show_response(status, body)

    elif report_action == "Download PDF":
        st.subheader("GET /cases/{case_id}/report/pdf")
        if st.button("Download PDF", type="primary") and case_id:
            url = f"{API_BASE_URL}/cases/{case_id}/report/pdf"
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            try:
                r = requests.get(url, headers=headers, timeout=30)
                if r.status_code == 200:
                    st.success(f"PDF retrieved ({len(r.content):,} bytes)")
                    st.download_button(
                        "Save PDF",
                        data=r.content,
                        file_name=f"SLRAI_Report_{case_id[:8]}.pdf",
                        mime="application/pdf",
                    )
                else:
                    st.error(f"Status {r.status_code}")
                    st.write(r.text)
            except Exception as e:
                st.error(str(e))


# ════════════════════════════════════════════════════════════════════════════
# TAB: HEALTH
# ════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.header("System Health")

    if st.button("Check /health", type="primary"):
        status, body = api_call("GET", "/health")
        show_response(status, body)

    st.divider()
    st.subheader("Quick Connectivity Test")
    if st.button("Ping API root"):
        try:
            r = requests.get(API_BASE_URL.replace("/api/v1", ""), timeout=5)
            st.success(f"API reachable — status {r.status_code}")
        except Exception as e:
            st.error(f"Cannot reach API: {e}")

    st.divider()
    st.caption(
        "This dashboard is a developer/QA tool for exercising every SLRAI "
        "endpoint manually. It is not the production frontend — see Karan's "
        "Next.js app for the real user-facing UI."
    )
```

---

## Blueprint v5.4 — Changelog

1. **Prayer clause structured extraction** — `sa_prayer_text`/`interim_stay_*` replaced
   with a full `prayers: list[dict]` schema plus derived `challenges_*` and
   `prayer_scope_covers_current_measure` fields (Section 7). New rule `M4_C5` flags
   prayer/measure scope mismatch (`m4_limitation.yaml`). `BATCH_USER_TEMPLATE` extended
   with `prayers` + `sa_prayer_text` extraction targets; `BATCH_SYSTEM_PROMPT` gained
   PRAYER DETECTION RULES guidance.
2. **GroundCode enum** — 8 new codes added (`AO_AUTHORIZATION`, `AUCTION_NOTICE_AFFIXING`,
   `AUCTION_DURING_STAY`, `PENDING_SA_CONCEALED`, `THIRD_PARTY_ATS`, `AUCTION_PURCHASER`,
   `RIGHT_OF_REDEMPTION`, `SECOND_SA_FRESH_CAUSE`). `SAGround` Pydantic model gained
   `statutory_basis` (the SQL table and ORM model already had this column).
3. **CaseFactSchema** — added `sa_applicant_type` (critical routing field), M3 auction-notice
   compliance fields, M10 ATS-holder and auction-purchaser/redemption fields, and M8
   NPA-at-auction-date fields. `compute_derived_fields` validator extended with 3 new
   computed blocks; matching lambdas added to `COMPUTED_FIELD_RESOLVERS`.
4. **M3 auction rules** — `M3_C6` (notice not affixed), `M3_C7` (auction during stay,
   ABSOLUTE_BAR), `M3_C8` (pending litigation concealed) added to `m3_auction.yaml`.
5. **M8 rule** — `M8_C6` (NPA upgraded to Standard before auction) added to `m8_npa.yaml`.
6. **M10 module (new)** — `m10_third_party.yaml` with 6 rules (`M10_C1`-`M10_C6`) covering
   ATS holder standing, fraud-risk simultaneity, bona fide payment mitigation, confirmed-sale
   thresholds, and second-SA fresh-cause. Section 14 heading text left as "9 Modules" to
   preserve its TOC anchor — a note calls out the actual 10th module.
7. **Pre-intake filters F5/F6** — added as non-terminating routing signals. Since F1-F4 use
   an early-return single-result pattern and F5/F6 must not terminate, `IntakeFilterResult`
   gained a `route_flags: list[dict]` field to carry both simultaneously.
8. **Judgment priority list** — new subsection 15.0.2 lists the 7 Class A judgments to add
   (`celir_llp_bafna_motors`, `mathew_varghese`, `vasu_shetty`, `harshad_sondagar`,
   `oasis_dealcom`, `satyawati_tondon`, `transcore`). No prior anchor existed for this list.
9. **Law wiki** — `STATUTE_ORDER` (with new `TPA_SARFAESI` entry) and the TPA sections
   content spec documented under Section 15.0 for the first time (no prior inline script
   content existed in the blueprint to replace).
10. **Report template** — third-party notice + prayer-clause-summary blocks inserted before
    the Red Flags page, with matching CSS classes and new `build_report_context()` context
    variables (prayer/ATS fields).
11. **Chain B / engine routing** — `task_run_compliance_engine` given a full body (previously
    only referenced by name in the pipeline chain), routing to M10 for non-borrower/guarantor
    applicants. `run_all_modules()` now accepts `modules_to_run`.
12. **BATCH_SYSTEM_PROMPT** — THIRD PARTY AND POST-AUCTION GROUND DETECTION instructions
    appended; `BATCH_USER_TEMPLATE`'s "Valid ground_codes" list extended with the 8 new codes.

**Known inconsistency to resolve before Phase H7:** `task_run_compliance_engine` passes
short module ids (`"M1"`..`"M9"`, `"M10"`) to `modules_to_run`, but rule YAML files use
longer `module:` values (e.g. `M3_AUCTION_GAP`, `M4_LIMITATION`, `M10_THIRD_PARTY`). Either
`run_all_modules()`'s filter or the task's `modules_to_run` list must be reconciled to match
before this routing works correctly — carried over verbatim from the v5.4 upgrade prompt.

**Not done in this pass (manual follow-up, per the v5.4 upgrade prompt's own instructions):**
- Create the 7 judgment `.md` files in `docs/judgments/`.
- Create `docs/statutes/tpa_sarfaesi_sections.txt` with verbatim TPA section text.
- Rebuild both wikis (`build_law_wiki.py`, `compile_class_a_wiki.py`).
- Add Alembic migration for `sa_grounds.statutory_basis` — **note:** this column already
  exists in the current schema (see block 2 above), so this migration step is likely
  unnecessary; verify against the live DB schema before running it.
- Add `GET /api/v1/cases/{case_id}/third-party-analysis` to `API_ENDPOINTS.md`.

**Open questions for Harasis (unresolved, carried over verbatim):**
1. Santosh Jain case — final DRT/DRAT outcome on auction-during-stay, to confirm whether
   Celir LLP or Oasis Dealcom is primary authority for `M10_C4`.
2. Any precedent of a third-party ATS holder successfully maintaining an SA — determines
   whether `M10_C1` should stay ADVISORY or become CURABLE.
3. Should prayer extraction cover only the original SA, or also every Interim Application?
4. Confirm the exact neutral citation for Celir LLP v. Bafna Motors — (2023) 13 SCC 561.


