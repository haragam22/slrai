# SLRAI API Endpoints

Base URL: `http://localhost:8000/api/v1`

## Status Legend
- ✅ Implemented (router + handler + schema)
- ⬜ Stub / Not yet implemented
- 🔒 Requires auth token

---

## Auth — `/api/v1/auth`

| Method | Path | Status | Role Required | Phase | Notes |
|--------|------|--------|---------------|-------|-------|
| POST | `/auth/register` | ✅ | Public | H1 | Creates bank + first BANK_ADMIN |
| POST | `/auth/login` | ✅ | Public | H1 | Returns JWT |
| POST | `/auth/refresh` | ✅ | 🔒 Any | H1 | Reissues token |
| POST | `/auth/users` | ✅ | 🔒 ADMIN | H1 | Creates BANK_OFFICER or BANK_ADMIN |
| GET  | `/auth/me` | ✅ | 🔒 Any | H1 | Returns current user |

---

## Cases — `/api/v1/cases`

| Method | Path | Status | Role Required | Phase | Notes |
|--------|------|--------|---------------|-------|-------|
| POST | `/cases` | ✅ | 🔒 Officer+ | H1 | Creates case; runs F2 filter |
| GET  | `/cases` | ✅ | 🔒 Officer+ | H1 | List with pagination, status filter, search |
| GET  | `/cases/{case_id}` | ✅ | 🔒 Officer+ | H1 | Get single case |
| PATCH | `/cases/{case_id}` | ✅ | 🔒 Officer+ | H1 | Update metadata (DRAFT status only) |
| DELETE | `/cases/{case_id}` | ✅ | 🔒 ADMIN | H1 | Soft delete (status reset) |
| GET  | `/cases/{case_id}/pipeline-status` | ✅ | 🔒 Officer+ | H1 | Progress %, stage message |
| POST | `/cases/{case_id}/resume` | ✅ | 🔒 Officer+ | H1 | Triggers Chain B |

---

## Documents — `/api/v1/cases/{case_id}/documents`

| Method | Path | Status | Role Required | Phase | Notes |
|--------|------|--------|---------------|-------|-------|
| POST | `/{case_id}/documents` | ⬜ | 🔒 Officer+ | H2 | Upload PDF; triggers Chain A |
| GET  | `/{case_id}/documents` | ⬜ | 🔒 Officer+ | H2 | List documents |
| GET  | `/{case_id}/documents/{doc_id}` | ⬜ | 🔒 Officer+ | H2 | Get document metadata |
| GET  | `/{case_id}/documents/{doc_id}/download` | ⬜ | 🔒 Officer+ | H2 | Stream PDF |

---

## Workbench — `/api/v1/cases/{case_id}/workbench`

| Method | Path | Status | Role Required | Phase | Notes |
|--------|------|--------|---------------|-------|-------|
| GET  | `/{case_id}/workbench` | ⬜ | 🔒 Officer+ | H4 | Facts needing review (low_confidence/not_found/conflict) — built, pending dashboard verify |
| GET  | `/{case_id}/facts` | ⬜ | 🔒 Officer+ | H4 | All extracted facts — built, pending dashboard verify |
| PATCH | `/{case_id}/facts/{fact_id}` | ⬜ | 🔒 Officer+ | H4 | Confirm/correct single fact — built, pending dashboard verify |
| PATCH | `/{case_id}/workbench/conflicts/{conflict_id}` | ⬜ | 🔒 Officer+ | H4 | Resolve fact conflict — built, pending dashboard verify |
| POST | `/{case_id}/workbench/confirm-all` | ⬜ | 🔒 Officer+ | H4 | Confirm all; triggers Chain B — built, pending dashboard verify |

---

## Compliance & Results — `/api/v1/cases/{case_id}/results`

| Method | Path | Status | Role Required | Phase | Notes |
|--------|------|--------|---------------|-------|-------|
| GET  | `/{case_id}/results/compliance` | ✅ | 🔒 Officer+ | H5 | Compliance results by module |
| GET  | `/{case_id}/results/grounds` | ✅ | 🔒 Officer+ | H6 | Ground scores (verified + full corpus counts) |
| GET  | `/{case_id}/results/judgments` | ✅ | 🔒 Officer+ | H7 | Judgment applicability (Class A verified + Class B similarity) |
| GET  | `/{case_id}/results/corpus-stats` | ✅ | 🔒 Officer+ | H7 | Live Qdrant corpus win-rate stats, per SA ground raised |

---

## Reports — `/api/v1/cases/{case_id}/reports`

| Method | Path | Status | Role Required | Phase | Notes |
|--------|------|--------|---------------|-------|-------|
| POST | `/{case_id}/reports/generate` | ⬜ | 🔒 Officer+ | H9 | Generate PDF + JSON report |
| GET  | `/{case_id}/reports/latest` | ⬜ | 🔒 Officer+ | H9 | Get latest report JSON |
| GET  | `/{case_id}/reports/{report_id}/pdf` | ⬜ | 🔒 Officer+ | H9 | Download PDF (presigned URL or stream) |

---

## System

| Method | Path | Status | Notes |
|--------|------|--------|-------|
| GET | `/health` | ⬜ | Health check — Phase H10 |
| GET | `/docs` | ✅ | FastAPI auto Swagger UI |
| GET | `/openapi.json` | ✅ | OpenAPI schema |

---

## Total: 31 endpoints
- ✅ Implemented: 12
- ⬜ Pending: 19 (Phases H2, H4–H10)
