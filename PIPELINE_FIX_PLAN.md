# SLRAI Pipeline + Report Fix Plan

Source: gemini_test_report_santosh_jain.pdf audit + worker log trace (case 622a4a93), 2026-08-05.

## Phase 0 — free wins, no code (do first)

1. **`docker compose up --build`** before next run. Worker is on a 24h-stale image running pre-fix `chain_a.py` (`.s()` mutable chain instead of `.si()`). Causes `task_update_pipeline_stage() takes 2 positional arguments but 3 were given` crash + 42min dead pipeline stall. Working tree already has the fix — just not deployed. Zero code change, kills ~40% of total runtime.

## Phase 1 — corpus restructure (Class A only, live-sourced)

Decided: no Class B. 69 curated judgments in `docs/judgments/*.md` are the entire corpus. Kill the compiled-wiki cache — it drifts stale (was 47, folder now has 69).

1. `docs/judgments/*.md` — keep as-is, this is now the single source of truth.
2. `scripts/_judgment_md.py` — move `_format_entry()` (currently in `compile_class_a_wiki.py`) here as a shared helper.
3. `app/services/judgments/applicability.py`:
   - `_load_class_a_wiki()` → stop reading `settings.class_a_judgments_wiki_path`. Instead call `load_all_judgment_files(Path("docs/judgments"))`, format each record with the shared `_format_entry()`, join in memory. Keep the module-level cache var (built once per worker process).
   - Drop the `has_verified_conditions is True` filter — all 69 files count now.
   - `judgment_count` check in `evaluate_class_a_applicability` → count `len(records)` from the loader, not regex-count `### ` headers in wiki text.
4. `scripts/compile_class_a_wiki.py` — delete.
5. `docs/wiki/class_a_judgments_wiki.md` — delete.
6. `app/config.py` — remove `class_a_judgments_wiki_path` setting.
7. **Retrieval simplification** — with only 69 judgments, decide: keep Qdrant ground_code-prefilter step, or drop Qdrant retrieval entirely and let the single Claude call see the whole 69-judgment wiki every case (same pattern already used for the wiki text itself). Recommend dropping Qdrant for this corpus — one less moving part, no retrieval-precision surface to get wrong at this size. Confirm before removing `sarfaesi_judgments` Qdrant collection usage in `retrieval.py`.

## Phase 2 — remove Class B entirely

1. `app/services/judgments/retrieval.py`:
   - `retrieve_candidate_judgments()` — drop `has_verified_conditions` split, return one list not `(class_a, class_b)` tuple.
   - `PAYLOAD_INDEXES` — drop `has_verified_conditions` entry (moot if Qdrant is dropped per Phase 1.7).
2. `app/services/judgments/applicability.py` — delete `process_class_b_candidates()`.
3. `app/tasks/chain_b.py`:
   - Remove class_b loop (~line 194-198) and `SIMILARITY_RETRIEVED` persistence (~line 281).
   - Remove class_b logging (~line 155-158).
4. `app/models/db.py` — drop `SIMILARITY_RETRIEVED` from the status CHECK constraint (~line 463). `has_verified_conditions` column: leave or migrate out, not urgent.
5. `app/reports/templates/report.html.j2` — delete the `SIMILARITY_RETRIEVED` branch (~line 601-610). Every judgment block is now a real Applicable/Not-applicable Class A verdict.
6. `app/api/results.py` (~line 133), `app/services/judgments/statistics.py` — update "Class A + Class B" wording/comments.

## Phase 3 — statutory grounding for applicability (the "doesn't make sense" fix)

`sarfaesi_law_wiki.md` (307KB, full SARFAESI Act + Enforcement Rules digest) exists, has a settings path, is loaded in `nlp_layer.py` — but never reaches `applicability.py`. This is why judgment-relevance reasoning has no statutory grounding.

1. `app/services/judgments/applicability.py` — add `_load_sarfaesi_law_wiki()` (mirrors `_load_third_party_wiki()`), wire into `_build_system_blocks()` unconditionally, same `cache_control: ephemeral` pattern (cached, not resent full-price per case).
2. `APPLICABILITY_SYSTEM_PROMPT` — expand `"reason"` field from one sentence to structured multi-part:
   `2-4 sentences: (a) statutory provision (Act section/Rule number) governing this ground, (b) confirmed case fact(s) that trigger/fail it, (c) judgment's ratio applied to those facts, (d) net effect on ground strength.`
3. Add a `statutory_basis` filter check — cross-reference judgment's own `statutory_basis` field (SARFAESI/IBC/RDB Act/etc.) against the case's actual measure type before treating it as a candidate, so cross-regime mismatches (e.g. IBC Section-7-admission judgment surfacing for a SARFAESI `AMOUNT_DISPUTE` ground) get filtered before reaching the LLM, not just relying on the LLM to catch it in one line.
4. Audit `docs/judgments/*.md` ground_code tags for regime mismatches like the `radha_exports_v_axis_bank_drt_mumbai.md` case (IBC judgment tagged `AMOUNT_DISPUTE` under a SARFAESI ground) — one-time pass, flag/retag or add `statutory_basis` disambiguation to any similarly broad ground_codes.

## Phase 4 — extraction speed + coverage

1. `app/services/extraction/nlp_layer.py` — `process_paragraphs_for_extraction()` is the 39.6-min bottleneck. Check for serial per-paragraph API calls; batch or run concurrently. This is the single biggest remaining time cost after Phase 0.
2. Investigate why core case fields never populate despite full extraction run: `case_ref`, `drt_bench`, `loan_account_number`, `principal`, and most M1-M9 compliance preconditions (`notice_service_mode`, `valuation_report_present`, `tenancy_claimed`, etc.). Check `fact_persistence.py` and the regex layer's field coverage — this is a coverage gap, separate from the speed problem in #1.

## Phase 5 — report generator fixes

1. `app/tasks/chain_a.py` (or wherever `SAGround` rows get created) — `GROUP BY ground_code` before persisting, so one ground code = one row, not one row per source paragraph. Fixes: repeated ground rows (RIGHT_OF_REDEMPTION x15), repeated coverage alerts (71→~18 real), repeated identical judgment citations downstream.
2. `app/reports/generator.py` — pull precedent short-citation into the Ground-by-Ground table row itself (currently only a bare count, citations live disconnected on pages 20-24).
3. `app/reports/generator.py` — scrub `⚠ — ✓ ' '` and other non-ASCII symbols to plain equivalents before templating (cheapest fix), OR add a font covering U+26A0/curly-quotes/em-dash to `report.html.j2`'s `font-family` stack (`Inter`, `NotoDevanagari` currently, neither covers these). Recommend the `.replace()` scrub — no new font asset, no glyph-coverage risk on future symbols.

## Order of execution

1. Phase 0 (docker rebuild) — do immediately, unblocks all testing below
2. Phase 4.1 (batch extraction) — biggest remaining time win
3. Phase 5.1 (SAGround dedup) — unblocks clean testing of everything downstream (Phase 1-3 outputs are unreadable while duplicated 15x)
4. Phase 1 + 2 (Class A live-load, kill Class B) — corpus/retrieval restructure
5. Phase 3 (statute wiring + expanded reasoning) — depends on Phase 1/2 being in place
6. Phase 5.2 + 5.3 (citation linking, font scrub) — cosmetic, do last
7. Phase 4.2 (core-fact coverage gap) — needs its own investigation session, not a quick fix

## Verification after all phases

- Rerun full pipeline on a fresh case, confirm: no crash, extraction time drops, one row per unique ground in report, no `SIMILARITY_RETRIEVED` anywhere, judgment reasoning cites Act/Rule sections by number, no `�` in output PDF.
