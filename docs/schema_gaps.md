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

1. **Extraction coverage — CLOSED for `balance_payment_date` specifically,
   but exposed a much bigger systemic gap.** `balance_payment_date` is now
   wired end-to-end: `nlp_layer.py`'s `BATCH_USER_TEMPLATE` extracts it into
   a new `date_facts` object, and `chain_a.py::task_nlp_extract_facts`
   persists it (mirroring the existing `boolean_facts` loop).

   While wiring this, found that **every other named date field the rule
   engine depends on has the same gap and is NOT extracted or persisted at
   all**: `auction_date`, `demand_notice_date`, `sale_certificate_date`,
   `mortgage_date`, `lease_date`, `valuation_date`, `npa_classification_date`,
   `objection_date`, `bank_reply_date`, `possession_notice_date`,
   `sale_notice_date`, `drt_stay_order_date`, `ats_date`, `measure_date`,
   `sa_filing_date`, `date_of_last_payment`. The template's generic
   `"dates": [{date, context}]` array (unstructured, one entry per date
   mentioned in a paragraph) is parsed by Claude but **never persisted to
   any CaseFact row** — `task_nlp_extract_facts` only reads `boolean_facts`
   and (now) `date_facts`, and nothing maps the generic `dates` array to
   named fields. Every date-dependent computed field and YAML rule
   (`sixty_day_period_elapsed`, `auction_gap_days`, `M1_C1`, `M3_C1`, etc.)
   currently can only be populated by a human confirming the fact manually
   in the workbench — there is no AI-extraction path for any of them.

   This is a pre-existing gap from an earlier phase, not something
   introduced by adding `balance_payment_date`. Fixing it properly means
   adding all ~16 fields to `date_facts` (or a similar named structure) and
   is a deliberate scope decision, not something to do silently as a
   side-effect of one field's fix.

2. **New ground code — decided NOT needed.** The source doc's Scenario A
   suggested `BALANCE_PAYMENT_DELAY` as a possible new ground code. Resolved
   without one: `M10_C7`'s `ground_codes` reuses `AUCTION_PURCHASER` and
   `RIGHT_OF_REDEMPTION` (matches the source doc's own stated resolution
   "expand `AUCTION_PURCHASER` and `RIGHT_OF_REDEMPTION` to cover it").

3. **`celir_llp_bafna_motors.md` does not exist yet.** The E. Muthurathinasabathy
   fixture's `RELATIONSHIP TO OTHER JUDGMENTS` section references and
   distinguishes Celir LLP v. Bafna Motors, and per the source doc's item C,
   `celir_llp_bafna_motors.md` should get a `Distinguished by:` line added to
   its own `RELATIONSHIP TO OTHER JUDGMENTS` section. That file is part of the
   real 75+7 corpus you're supplying after H10 testing — can't write it now
   without fabricating a judgment summary. Do this when the real corpus lands.

4. **`sarfaesi_law_wiki.md` token budget** — currently ~79,500 tokens against
   a 65,000 budget (see `tests/test_judgment_retrieval.py::test_wiki_token_budget`,
   marked `xfail` with this same note). Pre-existing from an earlier phase's
   `build_law_wiki.py` output, not introduced in H7. Needs a real decision
   (trim statute text? raise the budget? split into two loaded contexts?) —
   not something to silently truncate.
