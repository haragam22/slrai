# SLRAI — SARFAESI Legal Risk & Auction Intelligence Platform

Legal intelligence platform for Indian banks: ingests a borrower's Securitisation
Application (SA), extracts structured facts (OCR + LLM), runs them through a
YAML statutory rule engine + judgment precedent matching, and produces a
compliance/litigation-risk report. See `CLAUDE_v51.md` for full architecture.

## Prerequisites

- Docker Desktop (Windows/Mac/Linux)
- A Google Cloud project with **Document AI billing enabled** and a Layout
  Parser processor created, plus Application Default Credentials on the host:
  ```
  gcloud auth application-default login
  ```
- A real Anthropic API key (`sk-ant-...`)
- (Optional) `HF_TOKEN` — HuggingFace token, needed at image build time to
  pre-download the gated IndicTrans2 translation model

## 1. Configure environment

Copy `.env.example` to `.env` and fill in:

| Variable | Notes |
|---|---|
| `ANTHROPIC_API_KEY` | Real key — NLP extraction, Class A applicability, and report generation all call Claude. A placeholder key fails at the NLP extraction stage with `401 invalid x-api-key`. |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path *inside the container* (`/app/secrets/gcp-adc.json`) — mounted from `GCP_ADC_HOST_PATH` |
| `GCP_ADC_HOST_PATH` | Host path to `application_default_credentials.json` |
| `GCP_PROJECT_ID`, `GCP_DOCUMENT_AI_LOCATION`, `GCP_DOCUMENT_AI_PROCESSOR_ID` | Your Document AI processor |
| `HF_TOKEN` | Build-time secret for IndicTrans2 (gated model) |
| `DATABASE_URL`, `QDRANT_URL`, `QDRANT_COLLECTION` | Defaults in `.env.example` match `docker-compose.yml` service names — usually no change needed |

**If Document AI billing isn't enabled** (no card/UPI on the GCP project),
OCR falls back automatically to local `pypdf` text-layer extraction — works
for born-digital PDFs, not scanned/image-only ones. It logs a loud
`DOCAI_FALLBACK_TRIGGERED` warning every time it fires so this doesn't go
unnoticed. See `app/services/ocr/docai_ocr.py`.

## 2. Bring up the stack

```bash
docker compose --env-file .env up -d --build
```

Starts: `postgres`, `redis`, `qdrant`, `minio`, `api` (port 8000), `worker`
(Celery, queues `celery`+`pipeline`).

Check everything is actually reachable:
```bash
curl http://localhost:8000/health
# {"status": "healthy", "db": true, "redis": true, "qdrant": true, "minio": true}
```
`"status": "degraded"` + one of the booleans `false` tells you exactly which
backing service is down.

## 3. Run migrations

```bash
docker compose exec api alembic upgrade head
```

## 4. Register a bank + admin user

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "bank_name": "Your Bank",
    "bank_short_code": "YB01",
    "admin_email": "you@example.com",
    "admin_password": "ChangeMe123!"
  }'
```
Save the returned `access_token` — every other endpoint needs
`Authorization: Bearer <token>`.

## 5. Run the pipeline

**Create a case:**
```bash
curl -X POST http://localhost:8000/api/v1/cases \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"borrower_name": "Test Borrower"}'
```

**Upload the SA PDF** (triggers Chain A automatically: OCR → language
detection → Hindi translation → regex extraction → NLP extraction →
workbench population → status `PENDING_HUMAN_REVIEW`). Multipart form,
field `file`, one upload per case per 30 seconds (rate limited):
```bash
curl -X POST "http://localhost:8000/api/v1/cases/$CASE_ID/documents" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@sample_sa.pdf" -F "doc_type=SA_PETITION"
```
Watch progress:
```bash
docker compose logs worker -f
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/cases/$CASE_ID/pipeline-status"
```

**Review the workbench and confirm facts** (human-in-the-loop — required
before Chain B runs; see fields required per module in Blueprint §18.4):
```bash
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/cases/$CASE_ID/workbench"
curl -X POST -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/cases/$CASE_ID/workbench/confirm-all"
```
`confirm-all` triggers Chain B: compliance engine → judgment retrieval →
applicability → scoring → recommendation → PDF report → status `COMPLETE`.

**Get the report:**
```bash
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/cases/$CASE_ID/report"
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/cases/$CASE_ID/report/pdf" -o report.pdf
```
If WeasyPrint fails, the JSON report still generates (`pdf_url: null`) — the
pipeline is never blocked by PDF rendering.

## Local dev without Docker

```bash
python -m venv .venv && .venv/Scripts/activate   # or source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
celery -A app.tasks.celery_app worker --loglevel=info --queues=celery,pipeline
```
Requires Postgres/Redis/Qdrant/MinIO reachable at the URLs in `.env` — either
run them via `docker compose up postgres redis qdrant minio` or point at your
own instances.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `GET /health` → `qdrant: false` | Qdrant container down/unreachable | `docker compose up -d qdrant`; Chain B still completes without a judgment section (contract §18.3) |
| Worker log: `403 billing to be enabled` (Document AI) | GCP billing disabled | Enable billing, or accept the automatic pypdf fallback (born-digital PDFs only) |
| Worker log: `401 invalid x-api-key` (Anthropic) | Placeholder/invalid `ANTHROPIC_API_KEY` | Put a real key in `.env`, rebuild worker |
| `429` on document upload | Rate limit — one upload per case per 30s | Wait 30s |
| Case stuck at `pipeline_stage: OCR_FAILED` | OCR failed (quota/key/corrupt file) | Check `case_facts` for `ocr_failed_<doc_id>` workbench item; manual text entry required, no auto-retry |
