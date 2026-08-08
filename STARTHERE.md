# Start Here

New session, new person? Read in this order.

**Last verified against code: 2026-08-06.** Everything below was checked
against the actual running codebase, not assumed from older docs — this file
had drifted badly stale before this pass (wrong judgment count, a "fix
needed" item that was already fixed, an LLM-provider section describing code
that no longer exists). If something here contradicts the code next time
you read this, trust the code and fix this file, the same way this pass did.

## 1. Docs map

| File | What it is | When to open it |
|---|---|---|
| `CLAUDE.md` | Pointer file only — says "read `CLAUDE_v51.md`". | Never needs opening itself. |
| `CLAUDE_v51.md` | **Canonical context file.** Architecture, tech stack, judgment-corpus design (hybrid wiki + Qdrant), authority note (wins over blueprint on judgment-arch conflicts). | Every session, first. |
| `SLRAI_Blueprint_v5.md` | Original full technical blueprint — DB schema, rule engine design, Celery chains, Dockerfile. Older than `CLAUDE_v51.md`; defer to v51 where they conflict. | When you need spec depth v51 doesn't restate. |
| `API_ENDPOINTS.md` / `docs/API_ENDPOINTS.md` | Endpoint status table (✅/⬜) — what's implemented vs stub, by phase (H1–H10). | Checking if a route exists before building against it. |
| `docs/schema_gaps.md` | Log of `CaseFactSchema` gaps found while building, and how each was closed. History, not a TODO list — but check the date on an entry before trusting it, this file has had stale "still open" claims that were actually already fixed. | Debugging a missing/odd case-fact field. |
| `docs/wiki/sarfaesi_law_wiki.md`, `third_party_law_wiki.md` | Full/selective statute text (SARFAESI Act, RDB Act) — source for rule-engine YAML citations, and (as of 2026-08-06) compulsory context in every `applicability.py` judgment-relevance call, not just `nlp_layer.py` extraction. | Writing or checking a compliance rule, or judgment-relevance reasoning. |
| `docs/judgments/*.md` | The judgment corpus — 69 files as of 2026-08-06, loaded live at runtime (no compiled cache file anymore, `class_a_judgments_wiki.md` was deleted). "Class A/Class B" split was removed the same day — every judgment gets a real applicability check now. | Understanding what the judgment corpus looks like, or adding a judgment by hand. |
| `JUDGMENT_SUMMARY_PROMPT_v2.md` | Prompt spec for summarizing a judgment into the structured format the corpus expects. | Adding a judgment by hand, or fixing the auto-summarize script. |
| `here-is-a-draft-buzzing-lantern.md` | Master roadmap, phases H11–H36. Everything after "first report works." | Planning work after the pipeline is stable. |
| `README.md` | Prereqs + docker-compose setup, curl examples for every API step. | Actually running the stack. |
| `PIPELINE_FIX_PLAN.md` | 2026-08-05/06 debugging session's fix plan — pipeline timing, report-quality bugs, corpus restructure. Executed, not a live TODO. | Understanding what changed in that session and why. |

## 2. Current state (2026-08-06)

- **LLM provider: Gemini via Vertex AI** (`LLM_PROVIDER=gemini` in `.env`), not Bedrock/Claude. `app/services/llm_client.py` branches on `settings.llm_provider` — `"gemini"` uses `google.genai.Client(vertexai=True, ...)` with ADC auth; anything else falls to `AnthropicVertex`. To switch back to Claude: set `LLM_PROVIDER=claude` (or delete the line, defaults to `claude`), rebuild, restart.
- **OpenRouter/qwen support (`openrouter_api_key`/`openrouter_model`/`openrouter_lock_model` in `config.py`) is dead config**, left over from an earlier session (see `SESSION_HANDOFF_qwen_swap.md`) that was fully superseded by the Gemini rewrite in a later session (`SESSION_HANDOFF_gemini_pipeline_test.md`). `llm_client.py` has no code path that reads these settings — don't assume they do anything.
- **Judgment corpus: 69 files** in `docs/judgments/`, loaded live (not "1 verified judgment" — that count is years stale, ignore any doc that still says it).
- **Compliance-score polarity bug: already fixed**, not open. `compliance_score.py`/`ground_strength.py` gate on `outcome_favors` (BANK/BORROWER/NEUTRAL, set explicitly per YAML check) — verified against the exact two examples an older doc cited as broken (`M4_C1` time-barred SA, `M10_C2` same-date ATS/mortgage fraud): both have `outcome_favors: BANK` and the scoring code correctly treats them as bank-favorable, not worst-case.
- **Date-field extraction: already fixed**, not open. All ~16 named date fields (`auction_date`, `demand_notice_date`, etc.) are extracted and persisted, not just `balance_payment_date`.
- **Bedrock/AWS setup section from the old checklist is gone** — the pipeline runs on Gemini/Vertex now, no AWS/Bedrock dependency. If you're picking this up fresh and want Claude instead of Gemini, that's a `LLM_PROVIDER` env change + rebuild, not a Bedrock approval process.
- **F1/F3/F4/F5/F6 pre-intake filters (`app/services/compliance/pre_intake.py`) are now wired into Chain A** (`task_check_pre_intake_filters`, runs right after NLP extraction). Previously fully coded but never called anywhere — a case with an active IBC moratorium or secured against agricultural land could reach a PROCEED recommendation with neither condition ever checked. Fixed 2026-08-06.
- **Gemini exception handling was broken, now fixed.** `llm_client.py`'s Gemini branch didn't translate Google's real exceptions (`google.genai.errors.APIError`, `requests.exceptions.Timeout`) into the anthropic exception types every caller (`nlp_layer.py`, `applicability.py`) checks for — every real Gemini rate-limit/auth/timeout error fell through to a generic catch-all that silently returned empty results, no retry, no case-FAILED on auth errors. This was live in production; the report that kicked off the 2026-08-05/06 debugging session was generated while this bug was active.

## 3. Known dormant/minor items (not urgent, noted for whoever picks these up)

- Three independent fact-schema sources exist (`nlp_layer.py` extraction prompt, YAML rule preconditions, `app/api/workbench.py`'s `REQUIRED_FIELDS`/`FIELD_LABELS`) that drifted apart over time. Extraction-coverage gaps between them were closed 2026-08-06, but the three lists still aren't unified into one `CaseFactSchema` source of truth — worth doing eventually, not done as part of an additive patch.
- `app/api/pipeline.py` is an empty router stub (no endpoints) despite its docstring claiming pipeline trigger/status routes — the real `GET /pipeline-status` endpoint lives in `cases.py`. Harmless (mounting an empty router is a no-op) but misleadingly named.
- No CORS middleware configured in `main.py` — fine for curl/Postman-only testing, will need addressing before any browser-based frontend is built against this API.
- `sarfaesi_law_wiki.md` token budget was raised (65k→85k) rather than trimmed, since it's now compulsory context in every applicability call — still full_text=True by design for legal completeness.

## 4. Don't touch yet

Roadmap H11–H36 (`here-is-a-draft-buzzing-lantern.md`): red-flag scoring overhaul, bidder-sheet report, multi-branch access, RDS/S3 migration, sellable API, DPDP work, growing the corpus further. Come back after the pipeline is stable end-to-end.
