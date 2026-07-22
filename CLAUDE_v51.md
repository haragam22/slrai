# SLRAI — SARFAESI Legal Risk & Auction Intelligence Platform
# Claude Code Context File — Read this before doing anything
# Version: 5.3 — Hybrid Wiki + Qdrant Architecture Added

## Authority Note

For judgment architecture conflicts, follow this file. For all other conflicts, follow the blueprint section numbers referenced below.

## What This Project Is

A legal intelligence platform for Indian banks. When a borrower files a
Securitisation Application (SA) at the Debt Recovery Tribunal (DRT) challenging
a bank's SARFAESI enforcement action, this system:

1. Ingests the SA PDF and enforcement documents from the bank
2. Extracts structured legal facts via OCR + LLM (never free text — JSON only)
3. Routes unconfirmed facts to a human workbench for the bank officer to verify
4. Runs verified facts through a YAML-based statutory rule engine (9 modules, 35 rules)
5. Retrieves applicable SC/HC/DRAT precedents from Qdrant using lazy retrieval
6. Computes a compliance score + litigation exposure metric
7. Generates a tamper-evident PDF report with statutory citations and precedents

It is NOT a legal advice tool. It is a procedural compliance validator.
A human bank officer always confirms facts before any verdict is produced.

---

## Recent Architectural Updates (Audit Schema Additions)

Based on recent audits, several critical structured fields and logical gates have been incorporated into the project blueprint:
- **Cross-module validation:** A new rule (`M_CROSS_1`) detects logical contradictions (e.g., alleging non-service of a notice while relying on its date).
- **Pre-report Gate:** A `drt_interim_stay_granted` flag immediately halts the auction recommendation regardless of compliance scores.
- **Enhanced Schema Coverage:** Included detailed Bank Reply substance checks, Authorized Officer (AO) verification, specific SA prayer/citation extractions, and Pre-intake F1 filter updates (using `property_classification`).
- **Computed Fields at Rule Engine Time:** Computed fields (e.g., elapsed days) are now evaluated inline at runtime (`COMPUTED_FIELD_RESOLVERS`) and are strictly prevented from being persisted in the database.
- **Advanced Workbench Resolution:** The workbench now delineates items into three clear categories: `LOW_CONFIDENCE`, `NOT_FOUND` (missing required fields), and `CONFLICT` (divergent extractions), supported by a new `fact_conflicts` table for manual resolution.
- **Corpus-Informed Win Statistics:** Real-world judgment win/loss rates are queried directly from Qdrant via payload filters (`get_ground_statistics`) and stored in the `ground_scores` table.
- **Statistics-Informed Judicial Scoring:** Instead of static heuristic values, the engine uses corpus win-rate statistics as a base modifier for computing the `judicial_score`.
- **Hybrid Wiki + Qdrant Architecture (v5.3):** The `sarfaesi_statutes` Qdrant collection is completely deprecated. Statutes and Class A judgments are now managed as static markdown files (`sarfaesi_law_wiki.md` for Chain A, and `class_a_judgments_wiki.md` for Chain B) and injected directly into context.
- **ACT vs RULES Distinction:** Ground code classification now explicitly requires a `statutory_basis`. `ACT` challenges route to the Qdrant judgment corpus for precedent matching; `RULES` challenges route to the deterministic YAML Rule Engine.
- **Dual Verification Statistics:** Corpus win rates now surface both verified manual statistics (`favor_verified=True`) and total gross statistics.

---

## The Three Laws — Never Violate These

1. FACTS OVERRIDE VECTORS: Judgments are never applied on text similarity alone.
   Factual conditions in judgment.applicable_conditions MUST be verified against
   CaseFactSchema before a judgment is marked APPLICABLE (Class A).
   Similarity-retrieved judgments without verified conditions are Class B only.

2. LAW OVERRIDES MODELS: Claude API only extracts structured data (JSON).
   It never makes a compliance verdict. The YAML rule engine makes all verdicts.

3. SYSTEM OVERRIDES AI: If the rule engine and LLM disagree, rule engine wins.

---

## Tech Stack (exact versions — do not upgrade without checking)

- Python 3.11+
- fastapi==0.111.0, pydantic==2.7.1 (v2 syntax ONLY — never v1)
- sqlalchemy==2.0.30 (async), asyncpg==0.29.0, alembic==1.13.1
- celery==5.3.6 (NOT 5.4.x — breaking task routing changes)
- google-cloud-documentai==2.29.2 (OCR — NOT Azure Document Intelligence, switched away from Azure)
- anthropic==0.56.0, claude_model="claude-sonnet-4-6"
- torch==2.3.0 (CPU: torch==2.3.0+cpu --index-url https://download.pytorch.org/whl/cpu)
- transformers==4.41.0, sentencepiece==0.2.0, sacremoses==0.1.1
- qdrant-client==1.9.1, sentence-transformers==3.0.1
- embedding model: "law-ai/InLegalBERT" (768-dim, Indian legal text)
- translation model: "ai4bharat/indictrans2-indic-en-dist-200M" (trust_remote_code=True, gated — requires HF_TOKEN)
- simpleeval==0.9.13 (rule engine expression evaluator — NEVER use eval())
- weasyprint==62.3 (PDF generation — requires fonts-noto-core & fonts-noto-extra in Dockerfile for Hindi Devanagari script)
- redis==5.0.4, kombu==5.3.4

---

## Project Structure

See blueprint Section 2 for the exact folder structure.
All code lives under app/. Tests under tests/. YAML rules under app/services/compliance/rules/.
Judgment JSONs for ingestion: docs/judgments/
Statute text files for ingestion: docs/statutes/
Ingestion scripts: scripts/load_judgments.py, scripts/load_statutes.py
Corpus scripts: scripts/fetch_from_ik.py, scripts/load_judgments.py, scripts/load_statutes.py
Docs folders: docs/judgments/, docs/statutes/
Import paths follow the Section 2 structure — do not deviate.

---

## Judgment Knowledge Base Architecture

### Two Qdrant Collections — Always

The system uses EXACTLY TWO Qdrant collections. Never merge them.

**Collection 1: `sarfaesi_judgments`** (~7,500 vectors)
- One vector per judgment (half-page IBC Law summary as holding_summary)
- Corpus: 12 SC judgments (full text chunked) + ~7,488 HC/DRAT summaries from ibclaw.in
- Retrieved by ground_code metadata filter + vector similarity
- top_k = 20 per ground code
- Has Class A / Class B distinction (see below)

**Collection 2: `sarfaesi_statutes`** (~150-200 vectors)
- One vector per statutory section/rule
- Content: SARFAESI Act 2002, Security Interest (Enforcement) Rules 2002,
  RDDBFI Act 1993 (DRT sections only), RBI IRAC Master Circular key paragraphs
- Retrieved by EXACT section_number payload match — NOT vector similarity
- Used to pull statutory text into every rule violation finding in the report
- Source: indiacode.nic.in (authoritative, free)

### Class A vs Class B Judgments

Every judgment in `sarfaesi_judgments` is either Class A or Class B.
This is stored as `has_verified_conditions: bool` in the Qdrant payload.

**Class A (has_verified_conditions = True):**
- Has manually tagged `applicable_conditions` JSON (Harasis + advocate sign-off)
- Applicability engine runs full fact-graph check
- If conditions met → status = APPLICABLE
- Report section: "Verified Applicable Precedents"
- Priority: 12 SC judgments first, then ~32 high-frequency HC/DRAT judgments (44 Class A total)

**Class B (has_verified_conditions = False):**
- Has holding_summary and ground_codes only — no conditions JSON
- Applicability engine skips fact-graph check
- Status = SIMILARITY_RETRIEVED (not APPLICABLE or NOT_APPLICABLE)
- Report section: "Additional Relevant Judgments — applicability to specific
  facts of this case not verified. Review with legal counsel."
- The majority of the 7,500 HC/DRAT corpus is Class B at launch

**This distinction is honest and legally defensible.**
Class A citations carry verified weight. Class B citations flag further precedent exists.

### Lazy Retrieval — Only Retrieve What This SA Raised

Chain B retrieves judgments ONLY for ground codes that are:
(a) raised by the borrower in this SA (from sa_grounds table), OR
(b) failed in the compliance engine for this case

Do NOT retrieve judgments for all 15 ground codes on every case.
If this SA raises SERVICE_DEFECT + REPLY_NOT_GIVEN only,
retrieve only from those two ground code buckets.

This means: from 7,500 total judgments, the ground_code filter leaves
~200-600 candidates per ground code. top_k=20 from ~400 is precise.

### IBC Law Category → GroundCode Mapping

IBC category → ground code mapping: see `IBC_CATEGORY_TO_GROUND_CODE` in `scripts/load_judgments.py`.

### Judgment Source Field

Every judgment has a `source` field in its Qdrant payload:
- "SC_FULL_TEXT" — Supreme Court, ingested from full text (Indian Kanoon)
- "IBC_LAW_SUMMARY" — HC/DRAT, ingested from ibclaw.in half-page summary

SC judgments are chunked differently — 3 chunks per judgment:
  chunk 1: case name + facts + procedural history
  chunk 2: issues + arguments
  chunk 3: held + ratio decidendi (most important — this chunk is the primary retrieval target)
  All 3 chunks share the same judgment metadata.
  chunk_type payload values: "facts", "arguments", "held" — retrieval should prioritize chunk_type="held".

HC/DRAT summaries: 1 vector per judgment. The entire half-page summary is the content.

### Null judgment_date Handling

IBC Law summaries often have no judgment date (only ibclaw.in citation like "(2026) ibclaw.in 47 DRAT").
Store judgment_date = None for these entries.
The precedence resolver handles null dates:
  - null date judgment loses tiebreak to any dated judgment at the same court tier
  - Two null-date same-court judgments → flag LEGAL_UNCERTAINTY

### Statutory Text in Reports

For every rule that fires FAIL, Chain B retrieves the exact statutory text:
  → query sarfaesi_statutes where section_number = "13(3A)"
  → exact text returned and inserted into the report finding

This makes reports self-contained — the bank officer reads the exact law violated
without looking it up. No vector search on statutes — always exact section_number match.

### Statutory Wiki Build — Full-Act Ingestion (H4)

`scripts/build_law_wiki.py` builds `docs/wiki/sarfaesi_law_wiki.md` from full-text
source files in `docs/statutes/`, NOT a cherry-picked subset of sections.

Source files (full Act text, bare-act numbering, one file per Act):
  - `sarfaesi_act.txt` — SARFAESI Act, 2002
  - `sarfaesi_rules.txt` — Security Interest (Enforcement) Rules, 2002
  - `transfer_of_property_act.txt` — Transfer of Property Act, 1882
  - `rdb_act.txt` — Recovery of Debts and Bankruptcy Act, 1993 (RDB Act — renamed
    from RDDBFI Act by the 2016 amendment; same Act)

The script auto-splits each source on the Act's own numbering (e.g. "13. Enforcement
of security interest.—") and produces TWO wiki entries per section: the whole
section ("## Section 13") and every sub-clause individually ("## Section 13(2)",
"## Section 13(3A)") — exact sub-clause citation is what the rule engine and
retrieve_statute_text() actually query on. Every section/rule in the source
gets ingested; nothing is hand-selected.

Still outstanding (not yet in bare-act numbered form, need separate handling):
RBI Master Circular on IRAC/NPA classification (M8), RBI MSME Restructuring
Circulars Feb 2018 + Aug 2020 (M9), MSMED Act 2006 (M9).

Re-run after any change to `docs/statutes/`:
    python scripts/build_law_wiki.py

---

## Critical Architecture Rules

### Two-Chain Celery Pipeline — NEVER Connect Chain A and Chain B

Chain A fires automatically on document upload. Ends at PENDING_HUMAN_REVIEW.
Chain B fires only when bank officer calls POST /workbench/confirm-all.

DO NOT use | operator or chord to connect them.
DO NOT use .s() in Celery tasks — use .si() to prevent result passthrough.

Chain A steps (chain_a.py):
OCR → language detect → Hindi translation → doc classify → regex extract →
Claude extract → confidence routing → workbench population → status=PENDING_HUMAN_REVIEW

Chain B steps (chain_b.py):
compliance engine → lazy judgment retrieval (ground codes from THIS SA only) →
Class A applicability check → Class B similarity flag → statute text retrieval →
precedence resolve → ground scoring → compliance score → recommendation →
PDF report (with verified precedents + additional judgments + statutory citations) →
status=COMPLETE

### Data Isolation — bank_id from JWT Always

bank_id MUST come from the JWT payload, never from the request body.
Every DB query on cases/documents/facts MUST include bank_id filter.
This is enforced at the service layer, not the route layer.

### Object Storage Contracts (app/services/storage.py)

- S3 client entrypoint: `get_s3_client()` (module-level cached client)
- Path constructors (UUID-only paths, never user input):
  - `document_s3_key(case_id, doc_id)`
  - `report_pdf_s3_key(case_id, report_id)`
  - `report_json_s3_key(case_id, report_id)`
- Upload APIs:
  - `upload_document()` → returns `(s3_key, sha256_hash)`
  - `upload_report_pdf()` / `upload_report_json()`
- Download/stream APIs:
  - `download_document()`
  - `stream_document()`
- Integrity and validation:
  - `compute_sha256()` / `compute_sha256_stream()`
  - `verify_document_integrity()`
  - `validate_file_type()`
  - `document_exists()`
- Bucket bootstrap:
  - `ensure_bucket_exists()` (MinIO — self-hosted in dev and prod, no AWS S3)
- Storage constants:
  - `MAX_UPLOAD_SIZE_MB = 25`
  - `ALLOWED_CONTENT_TYPES = {application/pdf, image/jpeg, image/png, image/tiff}`
- Security rules:
  - AES-256 server-side encryption on put
  - No public ACL
  - Duplicate detection uses `sha256_hash` + `case_id`

### Confidence Routing Rules

- extraction_method="regex" → confidence=1.0 automatically, never goes to workbench
- extraction_method="nlp_implied" → cap confidence at 0.75, ALWAYS goes to workbench
- ALWAYS_HUMAN_CONFIRM fields regardless of confidence:
  valuer_rbi_empanelled, udyam_cert_in_bank_file,
  total_borrowers_in_loan, total_guarantors_in_loan,
  ibc_moratorium_active
- Fields with confidence < 0.80 → workbench required

### Silence Check — Never Assume Null

If a required fact field is None (not extracted, not confirmed):
- Do NOT assume the action happened
- Do NOT assume the action did not happen
- Return RuleResult(status="UNKNOWN", severity="UNKNOWN")
- The rule engine raises UNKNOWN, never fails silently

### YAML Rule Engine — simpleeval Only

Rule expressions are evaluated using EvalWithCompoundTypes from simpleeval.
NEVER use Python eval() on rule expressions.
Message templates use safe_format() with defaultdict, not .format().
Missing template variables produce "[UNKNOWN]", never raise KeyError.

### Claude API — Structured Output Contract

temperature MUST be 0.0 (deterministic extraction).
Response is always parsed as JSON after stripping markdown fences.
If JSON parse fails: retry up to 2 times with identical prompt.
After 2 retries: return None (caller handles gracefully, does NOT crash pipeline).
Claude API NEVER generates free text for legal output — JSON schema always provided.

### Error Handling Summary

Full contracts in blueprint Section 18 — this is a summary only.

Google Document AI OCR fails → set doc ocr_status=FAILED, add workbench flag, do NOT retry
Claude API bad JSON → retry max 2x, then None, add workbench flag
Claude API timeout → retry once after 5s, then None
Claude API rate limit → Celery retries with exponential backoff (max 3, countdown=60)
Claude API auth error → set case status=FAILED, do NOT retry
Qdrant unavailable → continue pipeline without judgment section, note in report
WeasyPrint fails → save JSON report, set pdf_url=None, do NOT fail the case
LegalUncertaintyException → store as LEGAL_UNCERTAINTY in judgment_applicability, continue

Storage layer specifics:
- `upload_document()` oversize file → HTTP 413
- S3 missing key on download → HTTP 404
- Other S3 failures (upload/download/stream) → HTTP 500

---

## Database Quick Reference

Tables: banks, users, cases, documents, paragraphs, case_facts,
sa_grounds, compliance_results, judgments, judgment_applicability,
ground_scores, reports, audit_log

case_facts has UNIQUE(case_id, field_name) — one value per field per case.
documents: file_url and sha256_hash are immutable after insert.
paragraphs: text_original is immutable after insert (OCR output, never modified).
cases.status enum: DRAFT → PROCESSING → PENDING_HUMAN_REVIEW → ANALYSING → PENDING_JUDGMENT_REVIEW → COMPLETE | FAILED | INTAKE_REJECTED

ORM/session contract in `app/models/db.py`:
- Two engines only:
  - `async_engine` + `AsyncSessionLocal` for FastAPI handlers
  - `sync_engine` + `SyncSessionLocal` for Celery workers
- Session entrypoints:
  - `get_async_db()` for route handlers
  - `get_sync_db()` for Celery tasks
- Relationship default loading strategy: `lazy="selectin"`
- App-layer immutability:
  - `documents.file_url`, `documents.sha256_hash` immutable after insert
  - `paragraphs.text_original` immutable after insert

judgments table key fields:
  has_verified_conditions BOOLEAN DEFAULT FALSE  — Class A vs Class B
  source TEXT CHECK (source IN ('SC_FULL_TEXT','IBC_LAW_SUMMARY'))
  chunk_type TEXT CHECK (chunk_type IN ('facts','arguments','held'))  — SC chunking payload field
  judgment_date DATE (NULLABLE — IBC Law summaries may have no date)

judgment_applicability.status CHECK includes: APPLICABLE, PARTIAL, NOT_APPLICABLE,
  SIMILARITY_RETRIEVED, LEGAL_UNCERTAINTY, UNAVAILABLE

---

## Running the Stack

Register at api.indiankanoon.org before running fetch_from_ik.py. Put the token in `.env` as `IK_API_TOKEN`.

docker-compose up  # starts PostgreSQL, Redis, Qdrant, MinIO
alembic upgrade head  # run migrations
uvicorn app.main:app --reload  # API server
celery -A app.tasks.celery_app worker --loglevel=info  # worker

# Seed judgment corpus (run once, then incrementally as Harasis adds JSONs)
python scripts/load_judgments.py --dir docs/judgments/

# Seed statutory text (run once)
python scripts/load_statutes.py --dir docs/statutes/

---

## Key Files and What They Do

app/main.py — FastAPI lifespan pattern (NOT @app.on_event — deprecated)
app/config.py — pydantic-settings, reads .env, all vars validated on startup
app/dependencies.py — get_current_user, require_role, get_db
app/models/db.py — SQLAlchemy ORM, dual-engine session helpers (get_async_db/get_sync_db)
app/models/schemas.py — Pydantic v2 (all request/response schemas + CaseFactSchema)
app/tasks/chain_a.py — Chain A tasks (.si() pattern)
app/tasks/chain_b.py — Chain B tasks (.si() pattern)
app/services/compliance/engine.py — YAML rule interpreter (simpleeval)
app/services/compliance/rules/*.yaml — 9 YAML rule files (M1–M9)
app/services/extraction/regex_layer.py — Layer A, deterministic
app/services/extraction/nlp_layer.py — Layer B, Claude API, JSON only
app/services/extraction/fact_persistence.py — idempotent upsert helper for case_facts
app/services/storage.py — S3/MinIO upload-download-stream service + SHA-256 integrity
app/services/judgments/retrieval.py — Qdrant lazy retrieval, both collections
app/services/judgments/applicability.py — Class A fact-graph check, Class B flag
app/services/scoring/ — ground_strength.py, compliance_score.py, recommendation.py
app/reports/generator.py — WeasyPrint PDF (two judgment sections + statutory citations)
scripts/load_judgments.py — ingests docs/judgments/*.json into sarfaesi_judgments
scripts/load_statutes.py — ingests docs/statutes/*.txt into sarfaesi_statutes
scripts/fetch_from_ik.py — fetches Indian Kanoon judgments and generates Class B summaries
docs/judgments/ — judgment JSON files (one per judgment, Harasis maintains)
docs/statutes/ — statutory text files (SARFAESI Act, Rules, RDDBFI Act sections)

---

## Blueprint Reference

The full technical specification is in SLRAI_Blueprint_v5.md (~8,600 lines).
This file (CLAUDE.md) reflects all decisions including v5.1 judgment architecture.
For everything else: blueprint Section numbers are referenced in phase prompts.
