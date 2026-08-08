# CaseFactSchema Gaps

## From E. Muthurathinasabathy (2026 INSC 303)

**Status: CLOSED.** These were originally flagged as v5.5-pending gaps by
`JUDGMENT_SUMMARY_PROMPT_v2.md`'s worked example, but were implemented directly
during H7 (ahead of a formal blueprint patch) because the judgment engine's
gate required them to be testable. Documenting what was actually done, not a
future TODO.

- `balance_payment_date` — informal `FactEntry[date]`. No fixed `CaseFactSchema`
  Pydantic class exists in this codebase (case facts are dynamic
  `field_name`/`field_value` rows in `case_facts`, extracted via Claude/regex
  and confirmed via the workbench) — so there is nothing to "add to a schema
  class." The field just needs to appear as a confirmed fact; extraction
  prompt coverage for it is not yet wired into `nlp_layer.py`'s
  `BATCH_USER_TEMPLATE` (still open, see below).
  = Date when auction purchaser deposited balance 75% sale consideration
  = Module: M10

- `balance_consideration_paid_within_90_days` — COMPUTED field.
  = `app/services/compliance/engine.py::COMPUTED_FIELD_RESOLVERS`
  = `(balance_payment_date - auction_date).days <= 90`
  = Module: M10
  = Rule: `M10_C7` fires FATAL when this is False AND `sale_certificate_issued` is True
  = `app/services/compliance/rules/m10_third_party.yaml`

## Still genuinely open

1. **Extraction coverage — date_facts is CLOSED, not open.** (Stale as of
   2026-08-06 — this item previously said all ~16 named date fields were
   unextracted. They are not: `nlp_layer.py`'s `BATCH_USER_TEMPLATE`
   `date_facts` object has all 16 fields, and `chain_a.py::task_nlp_extract_facts`
   persists every key generically, not just `balance_payment_date`. Anyone
   reading this file before 2026-08-06 would have wasted time re-fixing an
   already-fixed gap — checked the actual code before acting on this doc.)

2. **`boolean_facts` field names didn't match ~94% of YAML rule
   preconditions — found and closed 2026-08-06 (full audit, not a partial
   pass).** Built the complete set of every raw (non-computed) field name
   referenced across `app/services/compliance/rules/*.yaml` — both `field:`
   preconditions and bare identifiers inside `expression:` strings, minus
   `COMPUTED_FIELD_RESOLVERS` entries (those derive from other confirmed
   dates/facts at rule-engine time, not from extraction) — 52 fields total.
   Diffed against every key `nlp_layer.py`'s `BATCH_USER_TEMPLATE` actually
   extracts. First pass matched only 2 of 32 checked; the full 52-field diff
   found 12 more misses the first pass didn't catch, including two
   deceptively named ones that read like dates but are booleans
   (`pending_sa_existed_at_auction_date`, `account_standard_at_auction_date`
   — both compared with `== True`/`== False` in expressions, not date math)
   and one genuinely distinct date the first pass conflated with an existing
   field (`notice_service_date` ≠ `demand_notice_date` — service date can
   trail issue date by the postal delay, and `M1_C5`/`M1_C7` compare them
   directly). All 52 now have a matching schema slot — `boolean_facts`,
   `date_facts`, a new `numeric_facts` dict, and four new flat enum/string
   fields (`sa_applicant_type`, `notice_service_mode`, `asset_type`,
   `measure_type`), all persisted generically in `chain_a.py`.
   `authorized_officer_name` persists under its own exact name via
   `aggregate_metadata()` (it's a direct YAML field, M1_C8 — different
   handling from `drt_jurisdiction`/`sa_number`, which sync to `Case`
   columns instead, see item 3 below).

   Did NOT rename or remove the old mismatched keys that were already
   there (`notice_served`, `valuation_disputed`, `msme_status_claimed`,
   etc.) — found a **third** independent schema in `app/api/workbench.py`'s
   `REQUIRED_FIELDS`/`FIELD_LABELS` that references some of those old names
   for workbench UI display, and renaming without auditing that call site
   risked breaking it silently. Net result: three fact-schema sources
   (`nlp_layer.py` prompt, YAML preconditions, workbench UI labels) still
   exist independently and still aren't unified — this patch closes the
   extraction-coverage gap, it does not eliminate the architectural drift
   risk of having three lists. A real `CaseFactSchema` single source of
   truth is the actual fix; not done here, out of scope for an additive
   patch.

   **Not done**: full semantic verification of all 52 fields' meaning
   against the actual SARFAESI Act/Rules text (only Rule 8/9-tied fields —
   auction notice, valuation, reserve price — were spot-checked against
   `docs/statutes/sarfaesi_rules.txt` and confirmed correct). Coverage
   (does a schema slot exist) and semantic correctness (does the slot mean
   what the statute means) are two different checks — this closed the
   first, not the second.

3. **Case identity fields (`case_ref`, `drt_bench`, `loan_account_number`,
   `principal_amount`) showing blank in reports — two distinct causes found
   2026-08-06.**
   - `case_ref`/`drt_bench`: NLP *does* extract this data (`meta_sa_number`,
     `meta_drt_jurisdiction` via `aggregate_metadata()`) but it was persisted
     only to `case_facts` under `meta_*` names and never copied to the
     `Case.case_ref`/`Case.drt_bench` columns the report template reads
     directly (`report.html.j2` uses `case.case_ref`, not a `case_facts`
     lookup). Fixed: `aggregate_metadata()` now backfills those two Case
     columns when they're empty, without overwriting officer-entered values.
   - `loan_account_number`/`principal_amount`: genuinely never extracted —
     no field for either anywhere in `nlp_layer.py`'s schema. These remain
     manual-entry-only (`CreateCaseRequest`) unless/until extraction
     coverage is added for them — not done here, needs its own scope
     decision same as item 2.

4. **`load_confirmed_facts()` only reads `human_confirmed=True` rows** —
   confirmed by design, not a bug: no NLP-extracted fact (regardless of
   correct field name) reaches the compliance rule engine until a human
   confirms it in the workbench. This means a case that goes through
   extraction but skips workbench review will show "Unknown" for every
   precondition even with a fully-fixed field schema — that's the
   human-in-the-loop safety gate working as intended for a legal-risk
   platform, not something to route around. Noting it here because it
   explains report symptoms that look identical to the field-name bug above
   but have a different, non-bug cause.

5. **New ground code — decided NOT needed.** The source doc's Scenario A
   suggested `BALANCE_PAYMENT_DELAY` as a possible new ground code. Resolved
   without one: `M10_C7`'s `ground_codes` reuses `AUCTION_PURCHASER` and
   `RIGHT_OF_REDEMPTION` (matches the source doc's own stated resolution
   "expand `AUCTION_PURCHASER` and `RIGHT_OF_REDEMPTION` to cover it").

6. **`celir_llp_bafna_motors.md` — CLOSED, file exists now** (as
   `celir_llp_v_bafna_motors_supreme_court_2023.md`, part of the 69-file
   corpus). The `Distinguished by:` cross-reference line item from the
   original note still hasn't been verified as added — worth a quick check
   next time either file is touched, but the "can't write it, doesn't
   exist" blocker is gone.

7. **`sarfaesi_law_wiki.md` token budget — RAISED 2026-08-06, not trimmed.**
   Was ~76,700 tokens against a 65,000 budget (`xfail` in
   `tests/test_judgment_retrieval.py::test_wiki_token_budget`). Budget raised
   to 85,000 (and third_party_law_wiki.md's to 60,000) rather than trimming
   statute text — this wiki became compulsory context in every
   `applicability.py` call (not just `nlp_layer.py`) as of the same date, so
   trimming it now affects judgment-relevance reasoning quality, not just
   extraction. Still full_text=True by design for legal completeness;
   not something to silently truncate.
