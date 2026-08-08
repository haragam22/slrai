# Session handoff — Bedrock→OpenRouter(qwen) swap + pipeline fixes

Goal: Bedrock was erroring server-side, so swap the case pipeline's LLM calls
to OpenRouter's qwen3-235b, get Docker up, and run one real case through to a
report, fixing whatever broke along the way.

## Code changes made (all done, not reverted)

1. **`app/services/llm_client.py`** (new file) — thin OpenAI-SDK wrapper
   around OpenRouter, shaped to match the Anthropic `client.messages.create()`
   interface so call sites needed minimal changes. Exposes
   `llm_client.MODEL` (= `settings.openrouter_lock_model`, currently
   `qwen/qwen3-235b-a22b-2507`) and exception aliases
   (`APITimeoutError`/`RateLimitError`/`AuthenticationError`).

2. **`app/services/extraction/nlp_layer.py`** and
   **`app/services/judgments/applicability.py`** — swapped
   `AnthropicBedrock` client → `llm_client.client`, model →
   `llm_client.MODEL`, `max_tokens` 4000→8000 (see bug #2 below), and the
   `except anthropic.*Error` clauses → `except llm_client.*Error`.

3. **`requirements.txt`** — added `openai==1.30.1`.

4. **`docker-compose.yml`** — added `MINIO_KMS_SECRET_KEY` env var to the
   `minio` service (real bug, unrelated to qwen: MinIO 501s
   `put_object(ServerSideEncryption=AES256)` without a KMS key configured —
   blocked every document upload).

5. **`app/services/ocr/docai_ocr.py`** — `extract_one_chunk()` now also
   catches `google.auth.exceptions.GoogleAuthError` (not just
   `GoogleAPICallError`) and passes `retry=None, timeout=30.0` to
   `process_document()`, so an expired/invalid GCP credential fails fast into
   the existing pypdf fallback instead of retrying under gapic's default
   retry policy for minutes.

6. **`app/tasks/celery_app.py`** — added
   `broker_transport_options={"visibility_timeout": 21600}` (6h). Real bug:
   Redis's default 3600s visibility timeout was shorter than
   `nlp_extract_facts` was taking on a large doc with qwen retries, so Redis
   assumed the worker died and redelivered the same task to run again in
   parallel — corrupting/duplicating progress on the original run. This was
   the single biggest source of the "it's been running forever" symptom.

7. **`.env`** — `GCP_ADC_HOST_PATH` updated twice as the user re-authed:
   first to `gcloud auth application-default login`'s ADC path, then to a
   downloaded service-account key
   `C:/Users/harag/Downloads/slrai-504118-347817a53268.json` for a new GCP
   project `slrai-504118`. `GCP_PROJECT_ID` / `GCP_DOCUMENT_AI_PROCESSOR_ID`
   in `.env` already point at the new project.

## Bugs found along the way (all fixed except #8)

1. MinIO SSE upload failure (`KMS not configured`) — fixed (#4 above).
2. `max_tokens=4000` too small for qwen's more verbose output → truncated
   mid-JSON on many batches, forcing retries — bumped to 8000. **Turned out
   not to be the main slowness cause** (see #3).
3. qwen intermittently emits malformed JSON (unterminated strings) well
   under the token budget — this is qwen model-quality flakiness, not a
   config bug. Costs a full retry round-trip (~10-40s) per occurrence,
   roughly 1 in 5-8 batches. Nothing to fix here — the retry-then-null-out
   logic in `nlp_layer.py`/`applicability.py` is the correct handling
   already.
4. Google Document AI OCR: expired ADC token → fixed by user re-running
   `gcloud auth application-default login`, then it turned out the
   re-authed account also lacks the `documentai.processors.processOnline`
   IAM permission on the GCP project — **still unresolved, needs the user to
   grant that role in GCP console** (or accept the pypdf fallback
   permanently, which works fine on born-digital PDFs like the test fixture).
5. `client.process_document()` had no explicit retry/timeout override →
   fixed (#5 above) so credential failures surface in ~30s not minutes.
6. Celery/Redis visibility_timeout too short → fixed (#6 above). This was
   confirmed via: `case_facts` row count staying flat while qwen calls kept
   returning 200 OK — meaning duplicate/zombie task executions were
   competing for DB writes without the original ever finishing.
7. Multiple worker container rebuilds (needed to ship code fixes) killed
   in-flight Celery tasks each time via SIGTERM without `task_acks_late`
   redelivery being clean, leaving zombie unacked messages in Redis that got
   redelivered later and ran concurrently with fresh test cases, stealing
   worker capacity. Fixed by fully flushing Redis DB0/DB1
   (`redis-cli FLUSHDB`) before the last test run rather than relying on
   `celery purge` (which only clears the queue, not in-flight/unacked
   messages).
8. **Still open / not a bug, just a fact**: `nlp_extract_facts` buffers all
   batch results in memory and writes to `case_facts` in one shot at the
   very end of the Celery task — so there is no way to observe partial
   progress from the DB mid-run. Only the qwen HTTP call log line count is a
   real progress signal. Worth knowing if debugging this again.

## State at handoff

- Docker stack is up (`docker compose ps` — postgres/redis/qdrant/minio/api/
  worker all healthy).
- Test bank + admin user already registered: email `qwentest@example.com`,
  password `ChangeMe123!` (JWT tokens used in this session are stored only
  in shell history inside the session, not saved anywhere — re-login via
  `POST /api/v1/auth/register` gives a fresh token, or reuse the same
  bank/login if a `/auth/login` endpoint exists).
- Currently a case is **still running end-to-end** as the final validation
  run:
  - case_id: `e7687380-10b9-4c68-b9a8-63187f5b1947`
  - doc uploaded: `tests/fixtures/sa_pdfs/sample sa(santosh_jain_1).pdf`
    (214 paragraphs after OCR)
  - Stuck-looking but actually just slow: NLP_EXTRACTION stage, ~1hr+ in,
    driven by qwen being both slower and less JSON-reliable than Claude was.
    Roughly 50-70+ sequential batch calls needed total (paragraphs get
    batched 7-at-a-time, oversized ones sent solo) — expect this stage alone
    to take **45-90 minutes** at current qwen latency/retry rates. This is
    the realistic throughput to plan around until Bedrock is fixed.
  - To resume checking it: poll
    `GET /api/v1/cases/e7687380-10b9-4c68-b9a8-63187f5b1947/pipeline-status`
    with the bank's bearer token, or tail `docker compose logs worker -f`.

## To resume next session

1. `docker compose ps` to confirm the stack is still up (Docker Desktop may
   have been closed/restarted — if so, `docker compose up -d` again, no
   rebuild needed unless more code changes are made).
2. Check the case above — if it finished, hit `.../workbench/confirm-all`
   to kick off Chain B (compliance engine → judgment retrieval →
   applicability → scoring → report), then
   `GET /api/v1/cases/{id}/report`.
3. If it's still stuck or failed, check `docker compose logs worker --tail=50`
   first before assuming it's broken — qwen is genuinely this slow.
4. Open item: grant the GCP service account
   `documentai.processors.processOnline` permission on project
   `slrai-504118` if real Document AI OCR (vs. pypdf fallback) is wanted.
