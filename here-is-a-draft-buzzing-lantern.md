# SLRAI Master Roadmap — Phases H11–H36

## Context

This supersedes the previous two-part document. Original scope: a 20-item
cost/quality wishlist ("Part 1") plus a separate 8-block product/production
addendum ("Part 2", phases H11–H17). Per explicit instruction, both are now
merged into one continuous, phase-numbered series — no more "Part 1 items"
vs "Part 2 phases," everything is an `H`-phase, matching the numbering
convention the project's own docs already use for completed work (H1–H10,
referenced throughout `CLAUDE_v51.md`/`API_ENDPOINTS.md`/`docs/schema_gaps.md`
as already-shipped history). Phases are rebalanced for comparable scope —
several small items that used to sit alone are bundled (e.g. three
independent one-file fixes now share a phase), and two of the largest former
phases are split in two, so no phase is a five-minute fix sitting next to a
multi-week migration.

**New first phase, added per explicit instruction:** H11 — fixing and
populating the Indian Kanoon judgment ingestion pipeline. This was
investigated fresh this pass (not carried over from either prior document)
and turned up the most severe concrete bug found in this entire audit
sequence: the only currently-functioning judgment-ingestion code path in the
repo produces judgments that are structurally invisible to retrieval. See
H11 below — this is why it leads the series rather than sitting wherever a
generic "add more judgments" task would otherwise land.

**Confirmed this pass, not carried over as an assumption:** production
routes 100% through AWS — Claude via Bedrock, and "all other services via
AWS, or anything else [AWS-native]." This was previously framed as one
addendum block (old Block 8); it's now the explicit, confirmed target for
every AWS-adjacent phase (H30, H31–H35), and H11 is written to account for it
directly (the ingestion script's own direct Anthropic client needs the same
Bedrock swap H30 does, or it becomes the one caller left behind).

**Docs sync, requested explicitly ("each doc is on the same page"):** the
five project docs (`CLAUDE_v51.md`, `README.md`, `API_ENDPOINTS.md`,
`docs/schema_gaps.md`, `SLRAI_Blueprint_v5.md`) are being updated directly in
the repo alongside this plan — see the **Docs Sync** section at the end for
exactly what changed in each and why. Three doc/code mismatches were found
across this and prior passes (`M_CROSS_1` claimed but absent, image upload
types claimed but never implemented, an `IBC_CATEGORY_TO_GROUND_CODE`
mapping and an ibclaw.in bulk-ingestion path both claimed but neither
exists) — all three are fixed in the docs sync, not left for "later."

**What carries forward unchanged from prior passes (verified, not
re-litigated):** cache_control locations (`nlp_layer.py:47-52`,
`applicability.py:114-119`), the third-party-wiki revert reasoning
(`applicability.py:40-46`), `fact_persistence.py`'s conflict routing
(lines 41-71), the retry/error contract (`chain_a.py:206-257`,
`nlp_layer.py:235-255`), `reports/generator.py` having zero Claude calls
today, Redis already running (`settings.redis_url`), `CaseFactSchema` not
existing (only `RuleResult`, a dataclass, in `schemas.py`), `drt_bench`
already on `Case` (`db.py:179`), and SAMB confirmed as an intra-bank
Stressed-Assets-Management-Branch, not a separate organization (see H29).

**Global reuse rule (unchanged):** every new Claude call goes through the
existing `cache_control: {"type": "ephemeral"}` pattern and the existing
`client.messages.create` retry/error contract — do not reinvent either, and
once H30 lands, every Claude call in the repo (including H11's) goes through
`AnthropicBedrock`, not a direct `anthropic.Anthropic()` client.

---

## Already done — no work needed

- **Prompt caching on Chain A** — `nlp_layer.py:47-52`. Confirmed live.
- **Conditional third-party wiki loading** — deliberately reverted.
  `applicability.py:40-46`: RDB Act DRT-jurisdiction sections are needed for
  every analysis. **Do not re-implement — this would reintroduce a fixed
  bug.**

## Recommend against as literally specified

- **Multi-document priority auto-overwrite** — `fact_persistence.py:14-71`
  routes conflicts to `fact_conflicts` for human resolution, the same "never
  assume, route to human" principle as `CLAUDE_v51.md`'s Silence Check.
  **Build any source-priority signal as a tiebreak shown in the existing
  conflict-resolution UI, never as a silent auto-resolve.** (This principle
  is load-bearing for H20's requirements-sheet auto-confirm too — see there.)

## Deferred — do not build without new information

- **Self-host an open-weight model** (e.g. Qwen-class) to replace Claude
  entirely. Not a code change to this repo — a separate GPU-infra project.
  Breakeven is roughly ~980 reports/month; no volume tracking exists yet to
  know if that's ever hit, and H30 is committing this system to Bedrock in
  production regardless. **Revisit only if AWS Bedrock cost at real volume
  becomes a problem H31/H32's cost metrics actually surface** — don't build
  speculatively against a number nobody has measured yet.

---

## Phase H11 — Indian Kanoon Judgment Corpus Ingestion Pipeline

**Leads the series per explicit instruction.** `docs/judgments/` contains
exactly **one** file today (`e_muthurathinasabathy.md`, hand-authored)
against a stated target of ~75 Class A + thousands of Class B
(`CLAUDE_v51.md`: "~7,500 vectors," "44 Class A total"). `scripts/fetch_from_ik.py`
is real, working code — it genuinely calls the Indian Kanoon API
(`api.indiankanoon.org`, token via `IK_API_TOKEN`, confirmed wired in
`.env.example`) and genuinely drafts a Claude summary with a safety gate
(`SUMMARY_UNCERTAIN` → skip, never guess). But it has three concrete bugs
that make every judgment it produces **functionally invisible to
retrieval** — which is the actual reason the corpus is stuck at 1 file, not
a lack of effort.

**Bug 1 — `holding_summary` is always empty.** `fetch_and_summarize()`
(`fetch_from_ik.py:106-151`) writes `frontmatter + summary + "\n"` with no
`## HOLDING SUMMARY` heading. `_parse_body_sections()`
(`scripts/_judgment_md.py:93-109`) initializes every section key — including
`holding_summary` — to `""`, and only fills one in when a matching
`## HEADING` line precedes the text. Since the raw summary here is never
preceded by any `##` heading, `holding_summary` parses as an empty string
for every judgment fetched this way. `holding_summary` is what
`load_judgments.py:98` embeds: `embedder.encode(r["holding_summary"])` — so
every Indian-Kanoon-fetched judgment gets a Qdrant vector built from an
empty string.

**Bug 2 — `ground_codes` is always `[UNKNOWN]`**, hardcoded in the
frontmatter template (`fetch_from_ik.py:141`). Retrieval filters by
`FieldCondition(key="ground_codes", match=MatchAny(any=[ground_code]))`
(`retrieval.py:213`) against real codes like `SERVICE_DEFECT` — `UNKNOWN`
never matches any real case's query, so these judgments can never surface
regardless of embedding quality.

**Bug 3 — `court` is always hardcoded `"HIGH_COURT"`**
(`fetch_from_ik.py:133`), even though Indian Kanoon search can return
Supreme Court or DRAT/Tribunal results too — silently misclassifies court
tier, which matters for `precedence.py`'s `COURT_RANK` tiebreaking and
`ground_strength.py`'s SC-favor boost logic.

**Net effect:** the only currently-functioning ingestion path produces
output the retrieval system can never see. This also means corpus win-rate
statistics (`get_ground_statistics`, `statistics.py`) and every downstream
scoring phase (H16, H26) have almost no real data yet — this phase is the
actual precondition for those numbers meaning anything, which is exactly why
it leads the series.

**Also found, fix in the docs sync (see end of file):** `CLAUDE_v51.md:149`
claims an `IBC_CATEGORY_TO_GROUND_CODE` mapping "in `scripts/load_judgments.py`"
— grepped, does not exist anywhere in that file. `CLAUDE_v51.md` also
describes a second bulk-ingestion source ("~7,488 HC/DRAT summaries from
ibclaw.in") for which **no fetcher script exists anywhere in `scripts/`** —
only the Indian Kanoon single-query path is real. Both are doc/code
mismatches, on top of the two already known (`M_CROSS_1`, image-upload
`ALLOWED_CONTENT_TYPES`).

**Fix:**
1. Write the summary under a `## HOLDING SUMMARY` heading, matching Format
   v2.0's parser expectation (`_judgment_md.py`'s `SECTION_KEY_MAP`) — the
   minimum fix for non-degenerate embeddings. Go further: extend
   `SUMMARY_DRAFT_PROMPT` (`fetch_from_ik.py:27-40`) to also draft
   `## KEY FACTS OF THIS CASE`, `## WHAT THE COURT DECIDED`, and the two
   `## CONDITION:` sections — these matter for Class A wiki quality later,
   not just Class B retrieval.
2. Replace hardcoded `ground_codes: [UNKNOWN]`/`favor: NEUTRAL` with a
   Claude-drafted classification pass, gated the same way the existing
   `SUMMARY_UNCERTAIN` skip already works (`generate_class_b_summary`,
   `fetch_from_ik.py:43-84`) — never silently guess; write a
   `NEEDS_GROUND_CODE_REVIEW: true` frontmatter flag on low-confidence
   classifications and require human sign-off before `load_judgments.py`
   ingests it. Matches `CLAUDE_v51.md`'s own stated philosophy — judgment
   classification has always been a human-verified step ("Harasis +
   advocate sign-off"), not something to fully automate.
3. Detect actual court tier from the Indian Kanoon search result instead of
   hardcoding `HIGH_COURT` — check `_ik_search`'s response for a real
   court/docsource field; fall back to a `NEEDS_REVIEW` flag if ambiguous,
   don't guess.
4. Create `docs/judgments_manifest.txt` (doesn't exist yet) — this needs
   real, curated SARFAESI/DRT/SC citations, a domain-expert input, not
   something to fabricate. This is the one piece of H11 that needs your (or
   Harasis's) supplied list, matching how `docs/judgments/` is already
   described as "Harasis maintains" in `CLAUDE_v51.md`.
5. Add pacing between manifest entries in the fetch loop
   (`main()`, `fetch_from_ik.py:154-193`, currently no delay at all) — the
   Indian Kanoon API is metered (README: "Free Rs 500 on signup"), don't
   hammer it across a large manifest.
6. **Cross-reference H30:** `generate_class_b_summary()`
   (`fetch_from_ik.py:43-52`) builds its own direct `anthropic.Anthropic(...)`
   client, independent of `nlp_layer.py`/`applicability.py`. When H30
   migrates those two to `AnthropicBedrock`, this script needs the identical
   swap or it becomes the one direct-API caller left over after the AWS
   migration.

**Verify:** run the fixed script against a small (2-3 citation) test
manifest, confirm the resulting `.md` files have non-empty `holding_summary`,
a real (human-reviewed) `ground_codes` list, and correct `court`. Run
`load_judgments.py` against them, then run an actual Qdrant search by the
assigned ground_code and confirm the judgment surfaces — this round-trip is
the real confirmation, not "the script exited 0."

---

## Phase H12 — Extraction Micro-Fixes Bundle

Three small, independent, no-new-infra fixes bundled for balance — none is
substantial enough to be its own phase.

**a) Dynamic `max_tokens` in `applicability.py`.** `applicability.py:126`
(`judgment_count` param, unused for sizing), `applicability.py:151`
(hardcoded `max_tokens=4000`). Replace with
`max_tokens=min(8000, 800 + judgment_count * 120)`, clamped to the model's
ceiling. Verify: compute for `judgment_count=75` (current) and `150`
(projected), confirm both below ceiling.

**b) InLegalBERT embedding cache for ground codes.** `retrieval.py:187-232`
(`retrieve_candidate_judgments`) calls `embedder.encode(ground_code)` fresh
every call (line 206) — ground codes are a small fixed enum (~15 values).
Add an in-process `dict` cache keyed by `ground_code`, next to the existing
`_embedder` module-level cache (lines 22-57). No Redis needed.

**c) OCR confidence flagging before Claude extraction.** `ocr_confidence` is
captured (`docai_ocr.py:142`) and persisted (`db.py:251`,
`layout_parser.py:60,81`) but nothing reads it anywhere in `app/`. Add a
threshold check in `chain_a.py::task_regex_extract_all` (or a new step
before `task_nlp_extract_facts`): for paragraphs with `ocr_confidence < 0.70`,
`upsert_case_fact` a row whose `confidence` is below `CONFIDENCE_THRESHOLD`
(mirror the existing `ocr_failed_{doc_id}` pattern, `chain_a.py:95-101`) —
surfaces through the *existing* live `LOW_CONFIDENCE` workbench query with no
schema change. Exclude these paragraphs from `paragraphs_payload`
(`chain_a.py:239-246`) so they never enter the Claude batch.

---

## Phase H13 — Structured Tool-Use Extraction

`nlp_layer.py:60,213-247`. Replace "return ONLY valid JSON" + manual
`json.loads` + retry-on-parse-failure with Anthropic tool use. No
`CaseFactSchema` Pydantic model exists to derive `.model_json_schema()` from
(verified absent — `schemas.py` has only `RuleResult`, a dataclass). Hand-write
`EXTRACTION_SCHEMA_JSON` as a JSON Schema matching the object shape already
defined in `BATCH_USER_TEMPLATE` (`nlp_layer.py:124-171`), pass as
`tools=[...]`, force
`tool_choice={"type":"tool","name":"extract_legal_facts"}`. Keep the existing
`RateLimitError`/`AuthenticationError`/timeout retry contract unchanged
(lines 241-251); delete the now-dead malformed-JSON retry path.

**Verify:** confirm zero JSON-parse retries fire across the existing fixture
SA PDFs.

---

## Phase H14 — Rule Engine Correctness Bundle

Three fixes bundled because they all touch the compliance engine/extraction
layer and are naturally sequenced together — and because **H15 and H16 both
depend on the third one landing first.**

### a) Cross-module contradiction rule (M_CROSS_1)

`CLAUDE_v51.md:31` claims this exists — grepped `app/services/compliance/`
(`engine.py` + all 10 `rules/*.yaml` files): it does not. Doc/code
mismatch — build what was already promised, fix the doc either way (see
docs sync). Add a new rule file/section in `app/services/compliance/rules/`
following the existing `M{n}_C{n}` pattern; the engine already supports
cross-field `preconditions:` blocks (`engine.py::evaluate_rule`), so this is
data-only. Fires when `service_defect_alleged=true` AND the borrower's own
timeliness argument depends on `notice_service_date` from the same notice.
Verify: fixture one case alleging non-service while relying on the same
notice's date, confirm the rule fires ADVISORY.

### b) Extract all named date fields, not just `balance_payment_date`

`docs/schema_gaps.md` documents this exactly: `nlp_layer.py`'s
`BATCH_USER_TEMPLATE` has a `date_facts` object (lines 151-153) extracting
only `balance_payment_date`; a generic `"dates":[{date, context}]` array is
parsed but never mapped to any named field. `chain_a.py::task_nlp_extract_facts`
(lines 309-331) already has the persistence loop for `date_facts` — this is a
straight extension, not new plumbing. Add the other ~15 named fields:
`auction_date`, `demand_notice_date`, `sale_certificate_date`,
`mortgage_date`, `lease_date`, `valuation_date`, `npa_classification_date`,
`objection_date`, `bank_reply_date`, `possession_notice_date`,
`sale_notice_date`, `drt_stay_order_date`, `ats_date`, `measure_date`,
`sa_filing_date`, `date_of_last_payment`. No engine change needed —
`COMPUTED_FIELD_RESOLVERS` (`engine.py:72-162`) already reference these
names. Verify: run the full eval fixture set, confirm previously-`UNKNOWN`
computed-field rules (`sixty_day_period_elapsed`, `auction_gap_days`, etc.)
now evaluate PASS/FAIL where source dates are present.

### c) Fix compliance/ground-strength polarity conflation — **the one hard dependency in this whole plan**

**This is a correctness bug, not a tuning nitpick.** `H16` (red-flag
pipeline) and `H15` (flag display) are both built directly on this fix and
cannot be built correctly before it lands.

`compute_compliance_score` (`compliance_score.py:14-20`) sums a fixed
deduction for every `ComplianceResult` with `status=="FAIL"`, assuming `FAIL`
always means "the bank's procedure was defective." False for two modules:

- `m4_limitation.yaml` `M4_C1`/`M4_C3` (`ABSOLUTE_BAR`) fire `FAIL` when the
  borrower's own SA is filed outside the 45-day Section 17 window — the
  single most bank-favorable outcome the system can find, not a bank defect.
- `m10_third_party.yaml` `M10_C2` (`HIGH`) fires `FAIL` when an ATS and the
  mortgage were executed on the same date — a fraud/collusion finding that
  supports the *bank's* defense, not a bank defect.

A time-barred SA currently deducts 50 points (`ABSOLUTE_BAR`) from the
*bank's own* compliance score — punishing the bank for the borrower's
mistake. (`M10_C2`'s `HIGH` severity happens to deduct `0` today only because
`HIGH` isn't in the `DEDUCTIONS` dict at all — a second, related bug, see
below — so this specific case is accidentally harmless, not correctly
handled.)

The same conflation reaches ground strength. `chain_b.py:355-364` computes
"worst status per ground (`FAIL` > `UNKNOWN` > `PASS`)" via
`RULE_TO_GROUND_MAP` (`chain_b.py:19-44`), mapping `M4_C1`/`M4_C3` →
`LIMITATION_EXPIRED` and `M10_C2` → `THIRD_PARTY_ATS`.
`compute_ground_strength` (`ground_strength.py:44-49`) sets
`factual_score = 1.0` ("bank's record confirms borrower's allegation")
whenever a ground's controlling status is `FAIL` — so a time-barred SA scores
as the borrower's *strongest possible* ground, the exact opposite of what it
means. Net effect: the case where the bank is most clearly in the right can
produce a depressed `compliance_score` *and* an inflated
`ground_strength`/`litigation_exposure`, pushing `get_recommendation()`
toward `HIGH_RISK`/`DO_NOT_PROCEED` instead of `PROCEED_FAVOURABLE`. The
existing `absolute_bar_triggered` short-circuit (`recommendation.py:25-29`)
only rescues this when `litigation_exposure < 0.30` — with other real grounds
raised alongside the time-bar, exposure sits above that and the broken
scores are used unmediated.

**Second bug found tracing this:** severities not present in
`compliance_score.py`'s `DEDUCTIONS` dict (`FATAL`, `ABSOLUTE_BAR`,
`CURABLE`, `MINOR`, `ADVISORY`, `UNKNOWN`) silently deduct `0` via
`.get(r.severity, 0)` instead of erroring — even though the DB's own
`CheckConstraint` on `compliance_results.severity`
(`db.py`) already lists `HIGH` and `REVIEW_REQUIRED` as valid values,
confirming this is an oversight, not an intentional omission. Confirmed a
genuine miss beyond `M10_C2`: `m5_tenancy.yaml:60-62` pairs
`result_if_true: FAIL` with `severity: REVIEW_REQUIRED` (a registered lease
predating the mortgage, a real bank-unfavorable finding) which currently
contributes zero to the compliance score when it should contribute
something.

**The fix — one explicit field, not inference.** Add `outcome_favors: BANK |
BORROWER` to every YAML check (default `BORROWER` for existing checks that
don't specify it — additive, every rule except the two identified above
keeps current behavior):

- `compute_compliance_score`: sum deductions only where
  `status=="FAIL" and outcome_favors=="BORROWER"`.
- `compute_ground_strength`'s `factual_score`: key off `outcome_favors`
  instead of raw status — `1.0` when `outcome_favors=="BORROWER"`, `0.0` when
  `"BANK"`, `0.4` when `UNKNOWN`.
- Set `M4_C1`/`M4_C3` and `M10_C2` to `outcome_favors: BANK` explicitly.
- Add `HIGH` and `REVIEW_REQUIRED` to `DEDUCTIONS` (`HIGH` between `FATAL`
  and `CURABLE`; `REVIEW_REQUIRED` next to `UNKNOWN`). Log a warning when a
  `FAIL` result's severity has no `DEDUCTIONS` entry, so a future unmapped
  severity is caught, not silently no-op'd.

**Additional gap found in the same audit, fix alongside this:**
`RULE_TO_GROUND_MAP` (`chain_b.py:19-44`) maps every `rule_id` to a
`ground_code` except one — `M10_C7` (Rule 9(4), balance consideration not
paid within 90 days, `FATAL`), confirmed by diffing all 46 `rule_id:`
entries across all 10 YAML files against the map's keys. Its own YAML
declares `ground_codes: [AUCTION_PURCHASER, RIGHT_OF_REDEMPTION]`
(`m10_third_party.yaml:159`) but it's invisible to `status_by_ground`
(`chain_b.py:360`: `if ground_code is None: continue`) and would stay
invisible to H16's red-flag pipeline for the same reason. Add
`"M10_C7": "AUCTION_PURCHASER"` — one ground per rule, matching the
`M10_C4`/`M10_C5` convention already used for dual-ground rules.

**Schema note:** `outcome_favors` needs a new column on `compliance_results`
(currently: `id, case_id, rule_id, module, status, severity, message,
detail_json, judgment_tags, evaluated_at` — `db.py:384-393`) — small
migration, `String`, `CHECK (outcome_favors IN ('BANK','BORROWER'))`,
default `'BORROWER'`.

**Verify:** fixture a case where `days_from_measure_to_sa > 45` (M4_C1
fires) and no other grounds raised — confirm `compliance_score` stays at (or
near) 100 and `get_recommendation()` returns `PROCEED_FAVOURABLE`. Fixture a
second case with the same time-bar *plus* a real M1 service defect — confirm
the score reflects only the M1 deduction. Confirm a `FAIL` result with an
undeclared severity now logs a warning instead of silently deducting 0
(regression test against the `m5_tenancy.yaml:60-62` case).

---

## Phase H15 — Flag Display: CRITICAL / MEDIUM / BASIC Classification

**Depends on H14(c) landing first** — built directly on `outcome_favors`;
building this against pre-fix data would ship a visibly wrong report (a
time-barred SA rendering as a bright-red `CRITICAL` flag, the single most
bank-favorable finding shown as the worst possible news).

Collapse the 5 YAML severities to 3 human-readable tiers for reports/UI:
`ABSOLUTE_BAR`+`FATAL` → `CRITICAL`, `HIGH`+`CURABLE` → `MEDIUM`,
`MINOR`+`ADVISORY` → `BASIC`. Add a `display_severity` property on
`RuleResult`/`ComplianceResult`:

```python
@property
def display_severity(self) -> str:
    if self.outcome_favors == "BANK":
        return "POSITIVE"   # not a red flag at all — see below
    if self.severity in ("ABSOLUTE_BAR", "FATAL"):
        return "CRITICAL"
    if self.severity in ("HIGH", "CURABLE"):
        return "MEDIUM"
    if self.severity in ("MINOR", "ADVISORY", "REVIEW_REQUIRED"):
        return "BASIC"
    raise ValueError(f"Unmapped severity: {self.severity}")  # fail loud, H14's lesson
```

**Two things this must get right that a naive port of the three-tier idea
would miss:**

1. **Must check `outcome_favors` first.** A time-barred SA
   (`M4_C1`/`M4_C3`) must never render as `CRITICAL` — it's the opposite of
   bad news for the bank. Route `outcome_favors=="BANK"` findings to a
   distinct positive/informational badge, off the CRITICAL/MEDIUM/BASIC
   scale entirely, not folded into any of the three.
2. **Must not silently drop `HIGH`/`REVIEW_REQUIRED`** the way a first-pass
   mapping easily would (both were the exact severities H14 found missing
   from `compliance_score.py`'s `DEDUCTIONS` — same class of bug, same fix
   discipline: raise on an unmapped value, don't default it away).

New `compliance_results` column: `display_severity: Text`, computed and
stored on insert (`task_run_compliance_engine`, `chain_b.py`) for query
efficiency. API response for `GET /cases/{case_id}/results/compliance`
groups by tier: `{compliance_score, critical_flags: [...], medium_flags: [...],
basic_flags: [...], critical_count, medium_count, basic_count}`.

**This is the single classification primitive the rest of the plan reuses —
not a competing system.** H16's red-flag pipeline Stage 1 calls
`display_severity` per rule before taking the worst-per-ground, instead of
maintaining its own separate severity-rank table. H21's short bidder report
shows flag counts by these same three tiers.

### Remediation guidance for MEDIUM flags

When a `CURABLE`/`HIGH` (→ `MEDIUM`) flag fires, tell the Authorised Officer
what to actually do about it, not just what's wrong. Add a `remedy:
{action, timeline, authority, caution}` block to every `CURABLE`/`HIGH` rule
across the 10 YAML files, threaded through `RuleResult` → `ComplianceResult`
(new `remedy_action`/`remedy_timeline`/`remedy_authority`/`remedy_caution`
columns) → `report.html.j2` under a "WHAT THE AUTHORISED OFFICER SHOULD DO"
block. Confirm explicitly: **the short bidder report (H21) must never render
remedy blocks** — internal remediation instructions are not bidder-facing.

**Verify:** confirm every `CURABLE`/`HIGH` check across all 10 `rules/*.yaml`
files has a `remedy` block (`m1_demand.yaml`, `m2_reply.yaml`,
`m6_valuation.yaml`, `m8_npa.yaml`, `m9_msme.yaml`, `m10_third_party.yaml`
all have at least one qualifying check per this session's severity grep).
Confirm `M10_C2` (`HIGH`) does not display as `BASIC`. Confirm a
time-barred-only case renders no `CRITICAL` badge, and instead shows the
positive/informational badge. Confirm `display_severity` raises (not
defaults) on any severity value not explicitly mapped.

---

## Phase H16 — Scoring Engine v2: Evidence-Staged Red-Flag Pipeline

**Depends on H14(c) and H15's `display_severity`.** Evaluate three evidence
sources separately — rule engine, Class A judgments, and *all* of this
case's lazily-retrieved Class B judgments — bucket each into a
LOW/MEDIUM/CRITICAL red flag per ground, and derive the case recommendation
from the flag distribution, not from binning blended continuous scores. This
restructures the prior "confidence/sensitivity bolted onto the existing
matrix" approach entirely, per explicit direction received earlier in this
project: the matrix approach dilutes a single severe finding into an
average; Class B judgments — this case's own retrieved similarity matches,
persisted as `JudgmentApplicability` rows with `status="SIMILARITY_RETRIEVED"`,
`chain_b.py:196-206` — currently have **zero quantitative influence**
anywhere (`task_score_grounds`, `chain_b.py:368-373`, only ever queries
`status="APPLICABLE"`); they're rendered in the report and otherwise
discarded.

**New file: `app/services/scoring/red_flags.py`.** Three stage functions,
each returning `(flag: Literal["NONE","LOW","MEDIUM","CRITICAL"], reason: str)`
— every flag traces to a specific rule_id, judgment citation, or count,
never an opaque number.

**Stage 1 — Rule engine, per ground_code.** Input: `ComplianceResult` rows
for this ground (via `RULE_TO_GROUND_MAP`, now including H14's `M10_C7` fix),
each passed through H15's `display_severity`. Only rows where
`status=="FAIL" and outcome_favors=="BORROWER"` count — worst
`display_severity` among those wins (`CRITICAL`→`CRITICAL`,
`MEDIUM`→`MEDIUM`, `BASIC`→`LOW`). No qualifying FAIL but an `UNKNOWN`
result exists for this ground → `LOW` ("needs review"). Neither → `NONE`.

**Stage 2 — Class A, per ground_code.** Input: `JudgmentApplicability` rows
with `status="APPLICABLE"`, taken *after* `task_resolve_precedence` has
already reduced conflicting `APPLICABLE` judgments to one controlling row
(or flipped to `LEGAL_UNCERTAINTY`, `chain_b.py:306-340`) — reuse that
output, don't re-resolve. `LEGAL_UNCERTAINTY` → `LOW` ("needs lawyer review,
can't auto-resolve"). Among `APPLICABLE` rows: any Supreme Court
`favor=="BORROWER"` → `CRITICAL`; any HC/DRAT `favor=="BORROWER"` (no SC) →
`MEDIUM`; otherwise → `NONE`. Zero-applicable-judgment cases are already
separately flagged by `task_check_judgment_coverage`
(`chain_b.py:259-303`, `NO_PRECEDENT`/`WARNING`) — reuse as the "how much do
we trust this `NONE`" annotation.

**Stage 3 — Class B, per ground_code, *all* of this case's retrieved set.**
Input: `JudgmentApplicability` rows with `status="SIMILARITY_RETRIEVED"` —
this case's own lazy-retrieval candidates (not a corpus-wide query). Per
CLAUDE_v51.md's Law #1 (FACTS OVERRIDE VECTORS), unverified similarity is
capped at `MEDIUM` — can never alone produce `CRITICAL`. Shrinkage-weighted
borrower-favor proportion, same formula reused for the corpus-confidence fix
below:

```
PRIOR_STRENGTH = 8          # documented constant, not a fit parameter
CLASS_B_MIN_COUNT = 5
CLASS_B_THRESHOLD = 0.65

shrunk_pct = (borrower_favor_count + PRIOR_STRENGTH * 0.40) / (total_retrieved + PRIOR_STRENGTH)
# total_retrieved == 0                          -> NONE
# shrunk_pct >= 0.65 and total_retrieved >= 5    -> MEDIUM
# shrunk_pct >= 0.65 and total_retrieved < 5     -> LOW
# otherwise                                      -> NONE
```

**Combine → per-ground flag.** `combine_ground_flag(rule_flag, class_a_flag,
class_b_flag)` returns the worst of the three plus concatenated non-`NONE`
reasons — a report line reads *"G03_PHYSICAL_POSSESSION: CRITICAL — rule
engine found M3_C4 (FATAL, notice not affixed); Supreme Court precedent
Mathew Varghese applies against the bank on these facts."* Every flag is a
complete, traceable claim.

**Case-level recommendation, derived from the flag distribution.** Rewrite
`get_recommendation()` (`recommendation.py:23-42`): any ground at `CRITICAL`
→ ceiling `HIGH_RISK`/`DO_NOT_PROCEED` (generalizes the existing
`absolute_bar_triggered` special-case, `recommendation.py:25-29`, from "one
hardcoded M4 check" to "any CRITICAL flag, any stage"); no `CRITICAL` but
≥1 `MEDIUM` → `PROCEED_WITH_CONDITIONS`/`ELEVATED_RISK`; only `LOW`/`NONE` →
`PROCEED`/`PROCEED_WITH_AWARENESS`. `compliance_score`/`litigation_exposure`
(both still computed, both still get H14(c)'s fix) become supporting detail
and an in-tier tiebreak, not the primary driver. "Which single flag, if
resolved, drops the ceiling to the next-best tier" replaces the old
sensitivity-analysis idea — and because Stage 1 only flags
`outcome_favors=="BORROWER"` findings, it can never nonsensically suggest
"fixing" a time-bar.

**Corpus-confidence shrinkage (reused, not reinvented).**
`ground_strength.py:16-22`'s judicial-score currently uses a hard cliff —
`HIGH`/`MEDIUM` confidence (`verified_total >= 5`, `statistics.py:86-91`)
uses the real win rate, otherwise a flat `0.40`, discarding real signal at
`LOW` confidence even with a large "full" corpus. Same formula as Stage 3:
`base_score = (verified_borrower_wins + PRIOR_STRENGTH * 0.40) / (verified_total + PRIOR_STRENGTH)`
— returns exactly `0.40` at zero data, converges smoothly with no
discontinuity at the old `5`/`10` boundaries. **Note: this formula's real
usefulness depends on H11 actually landing** — with the corpus at 1 judgment,
`verified_total` is ~0 for almost every ground regardless of the formula;
this is the scoring-side reason H11 leads the series.

**Storage.** New columns on `GroundScore` (`db.py:476-491`): `rule_flag`,
`class_a_flag`, `class_b_flag`, `combined_flag` (`Text`), `flag_reasons`
(`JSONB`). `Report` (`db.py:501-519`) gets the case-level ceiling embedded
in the existing `report_json` `JSONB` column — no new `Report` columns.

**Verify:** fixture one case per ceiling tier (`CRITICAL` via a real M3
FATAL, `MEDIUM` via Class B skew alone with no rule/Class A finding, clean
`NONE`), confirm ceiling and reasons match by hand. Confirm the
time-barred-only case produces `NONE` everywhere and `PROCEED_FAVOURABLE`.
Confirm Stage 3 can never return `CRITICAL` for any input — enforce this as
an assertion in the function itself (legal-correctness invariant), not just
a test. Confirm the shrinkage formula returns exactly `0.40` at zero data.

---

## Phase H17 — Extraction Cost Optimization Bundle

Three items sharing the same `chain_a.py` insertion point, bundled.

**a) Written amount extraction (Hindi + English words).**
`regex_layer.py:19-23` (`amount_inr`) only matches numeral form. Add a
normalization pass: English word-form ("four crore seventeen lakh rupees")
via a small Indian numbering-system word→digit parser (crore/lakh/thousand
scale — do not reuse a Western-scale library), plus Devanagari digit/word
forms. Feed the same `demand_notice_amount`/`actual_outstanding_amount`
fields through the existing confidence router alongside the regex path.

**b) Skip Layer B for regex-complete paragraphs.** Between
`task_regex_extract_all` and `task_nlp_extract_facts`. Add
`should_skip_layer_b(para, regex_facts)`: skip Claude when
`para.word_count < 40` or the paragraph matches a boilerplate-phrase
detector. Wire into the `paragraphs_payload` filter (`chain_a.py:239-246`).

**c) Semantic paragraph deduplication before batching.** Same insertion
point. Hash each paragraph's cleaned text (`hashlib.sha256` on normalized
whitespace/casing — reuse the pattern in `compute_sha256`, `storage.py:91`),
group identical hashes, send one representative per group to Claude, fan
results back out via the existing per-paragraph `upsert_case_fact` loop
(`chain_a.py:259-331`).

---

## Phase H18 — Judgment Citation Extraction from SA Text

Extend `BATCH_USER_TEMPLATE` (`nlp_layer.py:118-182`) with a
`cited_judgments: list[str]` field — same batched call, no new round-trip.
Add a mapping step in `app/services/judgments/` resolving each citation
against the Qdrant corpus (reuse `retrieve_candidate_judgments`'s embedding
path, `retrieval.py:187-232`, query by case-name similarity). Classify: match
+ bank-favorable → advisory flag; match + borrower-favorable → auto-include
in report precedents; no match → unverified citation noted in report.

---

## Phase H19 — Natural-Language Executive Summary

`app/reports/generator.py` currently has zero Claude calls (confirmed — pure
Jinja2). Add one `client.messages.create` call (temperature 0.0 — Claude
never makes a verdict, only summarizes already-computed ones) with a strict
word cap, English + Hindi variants, inserted into `build_report_context()`
(`generator.py:216-353`). Reuse the client construction/error contract from
`nlp_layer.py`. Auth error is fatal-but-non-blocking: report still
generates, summary section says "[unavailable]" — matches the existing
WeasyPrint-failure precedent (`generator.py:421-433`).

---

## Phase H20 — Document Pipeline: Requirements Sheet + No-SA Mode

### Requirements Sheet + notice categories + source priority

`doc_classifier.py:3-19`'s `DOC_TYPE_KEYWORDS` dict is a flat keyword-scoring
match — add `"REQUIREMENTS_SHEET": [...]` and `"NEWSPAPER_CLIPPING": [...]`
(the latter is currently missing entirely, which means publication proof
keeps classifying as `OTHER`/priority-1 today) plus a `SOURCE_PRIORITY` dict
in `fact_persistence.py`: requirements sheet highest, individual bank
notices next, SA lowest (cross-check only).

**Real interaction bug, fix as part of this, not after:** auto-confirming
every requirements-sheet-extracted field
(`fact_data["human_confirmed"] = True`) runs straight into
`upsert_case_fact`'s existing rule (`fact_persistence.py:41-42`,
`if existing.human_confirmed: return`) — this returns **before** the
conflict-detection block. So if the actual demand notice PDF later extracts
a genuinely different date than the requirements sheet (AO fat-fingered it,
or the notice was amended), the disagreement is **silently discarded** — no
conflict, no flag, nothing. Fix: a narrow carve-out — when
`existing.human_confirmed and existing.extraction_method ==
"requirements_sheet"` and the new value disagrees, still create the
`fact_conflicts` row instead of returning early. The requirements-sheet
value stays authoritative and displayed, but the discrepancy becomes visible
— consistent with this plan's "never silently auto-resolve a disagreement
between documents" principle stated at the top.

### No-SA proactive mode

Add `sa_filed: Mapped[bool] = mapped_column(Boolean, default=True)` to `Case`
and `CreateCaseRequest`. Route on it in Chain A's extraction step and Chain
B's `modules_to_run` (`chain_b.py:93`, currently hardcoded `["M1"..."M9"]`
plus conditional `M10` — extend the same conditional to drop `M4` when
`sa_filed=False`, since Section 17 limitation doesn't apply with no SA
filed). Recommendation label remap (`AUCTION-READY` /
`AUCTION-READY WITH REMEDIATION` / `CANNOT PROCEED — CRITICAL DEFECTS`) and
report banner ("Pre-Auction Compliance Certificate") are template/string
work matching the real `modules_to_run` mechanism exactly.

**Note for H16's red-flag pipeline:** with `sa_filed=False`, there are no
`sa_grounds` rows, so Stages 2/3 (Class A/B, both keyed off
`get_relevant_ground_codes()`) have nothing to evaluate — only Stage 1
produces flags in this mode. Correct behavior, but the report template must
show "Not applicable — no SA filed," not a blank/broken-looking section.

**Verify:** fixture one `sa_filed=False` case with only bank documents,
confirm Chain A completes without ground-code extraction, Chain B skips M4,
report titles as "Pre-Auction Compliance Certificate" with no broken
precedent section.

---

## Phase H21 — Two Output Reports + AO-Directed Language

**Depends on H15** — the short report's flag-summary page needs
`display_severity`'s CRITICAL/MEDIUM/BASIC classification to exist; building
this first would mean a third, competing classification scheme.

### Bidder Opinion Sheet ("Choti Sheet")

Fully anonymized PDF for prospective auction bidders, alongside the existing
full report ("Badi Sheet," what already exists). `generate_report()`
(`generator.py:405-450`) already separates context-building from rendering
from upload, so `generate_short_report()` slotting in right after it in
`task_generate_report` (`chain_b.py:451-456`) is straightforward.

**Completeness invariant needed, not just a field-blocklist.** A naive
`anonymize_context()` that only clears top-level dict keys
(`borrower_name`, `loan_account_number`, etc.) misses that `ComplianceResult.message`
strings are generated from YAML `message_template`s that **already
interpolate PII** (e.g. borrower-name-style template vars via `safe_format`,
`engine.py:194-202`). Fix: `anonymize_context()` must also regenerate (or
strip) `message` on every compliance result, not just top-level context
keys — reuse H15's flag-summary phrasing ("SERVICE DEFECT — Demand notice
service proof requires verification") instead of the raw interpolated
message.

Three-page structure: verdict banner (color-coded by H16's case-level
ceiling) + three metric circles (compliance score, litigation exposure,
corpus win rate) → flag counts by H15's three tiers, one-line generic
phrasing per flag type, no case-specific detail → legal disclaimer. New
`report_type`/`short_report_url` columns on `Report` (`db.py:501-519`).

**Sharing mechanism:** bidders are not SLRAI users — they receive a PDF, not
a login. A signed, time-limited presigned S3 URL (reuse `storage.py`'s
existing client — standard boto3 call) with a short expiry (e.g. 72h),
generated on demand via `POST /cases/{case_id}/report/short/share-link`. No
recipient account, no org model.

### AO-directed report language

Pure copy change across YAML `message_template`s and report template
strings, addressing the Authorised Officer directly ("You did not give a
reasoned reply..." not "The bank failed to give..."). No structural change.
Do this **after** the anonymization fix above within this same phase —
rewriting every template's phrasing and then re-deriving a PII-free version
twice is wasted work.

**Verify:** generate both PDFs for one fixture case, grep the rendered
HTML/PDF text for zero occurrences of borrower name/amounts/dates in the
short version (don't just eyeball it), confirm the full PDF reads in
AO-directed language end to end. Confirm the short report never renders a
remedy block (H15).

---

## Phase H22 — Batch API for Chain A

Swap `client.messages.create` → `client.beta.messages.batches.create` in
`nlp_layer.py`. Batch responses can take up to 24h (typically <1h) vs
seconds today — the workbench must not open before the batch completes.
Needs a Celery polling task (`task_poll_batch_status`, reusing the
`autoretry_for`/`retry_backoff` pattern already on `task_nlp_extract_facts`,
`chain_a.py:206-213`) inserted between submission and completion. Changes
Chain A's shape from a straight `chain()` to submit→poll→continue — the
largest structural change to Chain A in this plan; **build after H12–H19
are stable**, everything upstream should be settled first. **Also confirm
this works under H30's Bedrock client** — Batch API availability/shape on
Bedrock should be checked before committing to this design, not assumed
identical to the direct API.

---

## Phase H23 — Redis Semantic Cache for Boilerplate Paragraphs

**Depends on H17(c)'s paragraph hashing.** Same hash, persisted to Redis
(`settings.redis_url`, already running) with 90-day TTL instead of only
deduping within one case. Add a cache-version key so a prompt/schema change
invalidates all cached entries at once — a bug in one SA's extraction must
not silently poison every future SA sharing the same boilerplate hash.

---

## Phase H24 — Haiku Routing for Pre-Screening

Two narrow uses: (a) plausibility check on an extracted date, (b) "does this
paragraph contain legal content" pre-filter before batching. Both yes/no
classifications — route to Haiku. `config.py:28` currently defines only
`claude_model: str = "claude-sonnet-4-6"` — add a second settings field
(e.g. `claude_haiku_model`). Keep Sonnet for all actual fact extraction.
**Both models route through Bedrock once H30 lands** — confirm the Haiku
model ID is actually available on Bedrock in `ap-south-1` before committing.

---

## Phase H25 — Confidence Calibration Feedback Loop

Add a `fact_corrections` table (`case_id`, `field_name`, `original_value`,
`corrected_value`, `corrected_by`, `corrected_at`) and wire the workbench
PATCH endpoints to write to it — cheap, should start accumulating data now.
The analysis job (promote fields with >15% correction rate to
`ALWAYS_HUMAN_CONFIRM_FIELDS`) is not usefully runnable below ~500 cases —
build it gated behind a manual trigger, not a schedule. **Note:** this same
table is the eventual source of real outcome data for recalibrating H16's
`PRIOR_STRENGTH` and `compliance_score.py`'s deduction constants, which are
hand-authored today for lack of anything to calibrate against yet.

---

## Phase H26 — DRT Bench Profiling + Similar-Case Comparison

Two cold-start analytics features bundled — both need case volume before
they're useful, both build on `Case.drt_bench` (already exists, `db.py:179`).

**a)** Add a `drt_bench_profile` table (bench name, stay-grant rate, avg
disposal time, known positions) and report section wiring. Starts empty;
populate manually/via scripts as real bench-level outcomes are supplied
(same pattern as `docs/judgments/`).

**b)** Query aggregating `reports`/`compliance_results` by
`(ground_code, drt_bench)`. No dependency on (a) beyond eventually wanting
its data. Build the query now, expect "insufficient data" until volume
grows — that's expected, not a bug.

---

## Phase H27 — OCR Tier Selection (Document AI)

`docai_ocr.py` calls one fixed processor (`_processor_name()`,
`settings.gcp_document_ai_processor_id` — a single ID in `.env`). Note: a
*failure-mode* fallback to local pypdf text extraction already exists
(`_extract_local`, triggered on `GoogleAPICallError`) — that's error
handling, not cost-tier selection, don't confuse the two. Add `is_scanned`
detection (text-layer presence check) and branch to a cheaper processor
config for digital-native PDFs. **Blocked on a GCP console step** — needs a
second configured Document AI processor; `.env` only has one processor ID
today. Flag before starting; the code branch has nothing to select between
until that setup exists.

---

## Phase H28 — Auction Purchaser Risk Report Variant

New Jinja2 template (`report_purchaser.html.j2`) alongside `report.html.j2`,
plus a `report_type` param threaded through `generate_report()`. **Blocked
on a product/legal decision:** do banks in this system distribute reports to
external auction purchasers, or is this internal-only? The "Not a legal
advice tool" framing (`CLAUDE_v51.md:23-24`) was written for internal
officer use; a purchaser-facing document may need separate legal review.
Build the template and plumbing; do not treat as ready-to-ship without that
sign-off.

---

## Phase H29 — Branch/SAMB Access Model

SAMB = Stressed Assets Management Branch — a specialized branch *within* a
bank that handles SARFAESI/NPA work, confirmed, not a separate organization.
It is plausibly this tool's primary user, not a read-only outsider — full
case-creation/upload/analysis rights, same as today's officers.

`Bank` (`db.py:119-132`) is already the correct tenant boundary — no rename,
no `org_type`, no separate role needed. Add a `Branch` model under it:

```python
class Branch(Base):
    __tablename__ = "branches"
    id:           Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bank_id:      Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("banks.id", ondelete="CASCADE"), nullable=False)
    name:         Mapped[str]       = mapped_column(Text, nullable=False)
    branch_code:  Mapped[str]       = mapped_column(String(20), nullable=False)
    branch_type:  Mapped[str]       = mapped_column(Text, default="SAMB")
    active:       Mapped[bool]      = mapped_column(Boolean, default=True)
```

Nullable `branch_id` on `User` and `Case` (nullable so a bank with a single
SAMB unit needs zero new configuration — must not become mandatory friction
for the common case). **No new role** — SAMB officers are just
`BANK_OFFICER`/`BANK_ADMIN` with a `branch_id` set.

**Access scoping, additive and bank-opt-in.** `verify_case_bank_access`
(`dependencies.py:92-105`) stays the primary boundary, unchanged. Layer an
*optional* filter gated by `Bank.branch_scoping_enabled: bool = False`
(default off): enabled → `BANK_OFFICER` sees only their branch's cases,
`BANK_ADMIN` sees all branches. Only matters for a large bank running
multiple SAMB units.

**Verify:** confirm `BANK_OFFICER` with `branch_id` set sees only their
branch's cases when `branch_scoping_enabled=True`, all bank cases when
`False`. Confirm H21's share link works unauthenticated and expires.

---

## Phase H30 — AWS Bedrock + RDS + ElastiCache + S3 Migration

**Confirmed direction, not a tentative option:** Claude routes through AWS
Bedrock in production, and everything else routes through AWS-native
services. Every phase from here on assumes this is where production runs.

`nlp_layer.py`'s and `applicability.py`'s `client = anthropic.Anthropic(...)`
(one line each) become `AnthropicBedrock(aws_region="ap-south-1")` —
`cache_control` usage is unchanged (Bedrock supports the same field). **Also
swap H11's `fetch_from_ik.py::generate_class_b_summary()`** — it builds its
own independent direct client (`fetch_from_ik.py:43-52`) and would be the
one caller left on the direct API if missed here.

Model ID format changes for Bedrock (in-region inference profile, not cross-
region — data-localization requirement, see H36's DPDP section). `storage.py`'s
MinIO client → boto3 S3 — check `get_s3_client()`/`ensure_bucket_exists()`/
`upload_document()` call shapes; MinIO is S3-API-compatible so most calls
are identical, but `ensure_bucket_exists()` (called every startup,
`main.py:18-20`) should become a no-op/permission-check in AWS —
RDS/ElastiCache/bucket provisioning is infra-as-code's job, not
app-startup's.

**No infra-as-code exists in this repo today** (only `Dockerfile` +
`docker-compose.yml`) — this phase needs actual Terraform/CDK for RDS,
ElastiCache, ECS task definitions, and IAM policy, not just the app-code
swap.

**Verify:** confirm prompt caching actually reduces token cost on Bedrock
the same way as the direct API (region/model rollout caveats have existed
historically — confirm against `ap-south-1`/the exact model ID, don't assume
parity). Confirm the Bedrock invocation itself doesn't route through a
non-Indian region even with in-region inference profiles configured
correctly.

---

## Phase H31 — API Hardening + Observability

Grounded against what's actually missing (verified, not assumed): no CORS
middleware, no security headers, no rate limiting beyond one Redis check in
`documents.py`, no error tracking, no metrics anywhere in the repo.

1. **Rate limiting + CORS + security headers.** Extend the
   `_check_upload_rate_limit` pattern (`documents.py:34-47`, Redis-backed,
   fails open) into general middleware — per-user and per-bank limits on
   case-creation and report-generation specifically (the expensive ones:
   OCR + Claude calls). `CORSMiddleware` locked to the actual dashboard
   origin(s), not `*`. `HSTS`/`X-Content-Type-Options`/`X-Frame-Options`
   headers.
2. **Observability.** Wire `structlog` consistently (already a dependency —
   audit for stray `logging.getLogger(__name__)` calls bypassing it). Add
   Sentry (or equivalent) for exceptions. Add Prometheus metrics (Celery
   queue depth/task duration, Claude API latency and error rate via H30's
   Bedrock client, OCR failure rate) — these numbers directly inform H25's
   calibration timeline and H30's Bedrock cost/latency comparison.

---

## Phase H32 — Scaling, CI/CD, Backup/DR & Docs Consolidation

**Pairs with H30** — several items only make sense once there's an AWS
account/IAM role to hold secrets in.

1. **Scaling.** DB connection pooling (PgBouncer in front of RDS) sized for
   ~10,000 registered bank officers with bursty, business-hours usage — a
   few hundred concurrent, not consumer-scale concurrency (revise if this
   assumption is wrong). Celery worker autoscaling for OCR/Claude-extraction
   spikes (bulk document upload is the actual burst pattern here). Read
   replica only if load testing (item 4 below) actually shows read
   contention — don't provision speculatively.
2. **CI/CD + secrets.** Move `.env` secrets to AWS Secrets Manager (natural
   pairing with H30's IAM-role-based Bedrock/S3 access — no long-lived
   credentials once both land). Add a CI pipeline (test + lint +
   dependency/CVE scan) gating merges — none exists today.
3. **Backup/DR.** RDS automated backups + point-in-time recovery, and an
   actually-tested restore drill — not just "RDS does backups by default."
4. **Docs consolidation.** `./API_ENDPOINTS.md` and `./docs/API_ENDPOINTS.md`
   are two different files with different structure and content — fixed in
   this pass's docs sync (see end of file), confirming here that no future
   phase should let them diverge again.
5. **Load testing.** Run a load test against the ~10k-user assumption
   (locust/k6 against staging) — specifically batch-upload + Chain A burst
   behavior, since that's this system's actual peak-load shape, not steady
   API traffic.

---

## Phase H33 — Database Hardening

**Depends on H30's RDS migration.**

1. **Multi-AZ RDS**, not a single instance — H32 covers backups/PITR;
   Multi-AZ is what turns "we have backups" into "a zone failure doesn't
   take the pipeline down mid-case."
2. **Least-privilege DB roles.** App connects as a role with exactly the
   grants Chain A/B need, never a superuser. Separate **read-only role** for
   reporting/analytics (H26's bench profiling/similar-case queries) so a bug
   in a reporting query can never write.
3. **Encryption in transit to the DB** — enforce `sslmode=require` (or
   stricter), don't rely on VPC-privacy alone.
4. **Index audit.** `case_facts` has `UNIQUE(case_id, field_name)`,
   `compliance_results`/`ground_scores` have explicit `case_id` indexes
   (`idx_compliance_case_id`, `idx_ground_scores_case_id`) — audit
   `documents`, `paragraphs`, `judgment_applicability` under real query
   patterns from H32's load test before assuming they're covered.
5. **Migration safety.** CI check running every migration against a staging
   DB before merge, house rule against long-locking migrations on tables
   that will get big at scale (`compliance_results`, `audit_log`) — add
   columns nullable first, backfill, then tighten.
6. **Non-prod data hygiene.** Staging/dev never holds real borrower PII —
   build a synthetic/masked fixture dataset rather than copying production
   data down, which is itself a DPDP exposure (H36) waiting to happen.

---

## Phase H34 — Auth Hardening

**Independent of H30 — can start immediately, in parallel with any other
phase, not gated on AWS.** Starting point already confirmed solid: bcrypt
rounds=12, timing-safe login comparison, `bank_id`/`role` JWT claims,
404-not-403 cross-tenant isolation — don't rebuild this, extend it.

1. **Token revocation doesn't exist today.** JWTs are stateless with a flat
   8-hour expiry (`config.py`: `jwt_expire_minutes=480`) — an admin cannot
   force-logout a compromised/offboarded user before natural expiry. Add a
   Redis-backed denylist (same Redis, same pattern as
   `documents.py:34-47`): `POST /auth/logout-all` writes a
   `user_id:invalidated_after` timestamp, `get_current_user` rejects tokens
   issued before it.
2. **No account lockout / brute-force protection.** The timing-safe dummy
   hash stops timing attacks and email enumeration, but nothing stops
   repeated password guesses. Add attempt tracking (Redis) with exponential
   backoff or temporary lockout after N failures, logged to `audit_log`.
3. **No password strength/breach check** beyond `min_length=8`. Add a
   strength check (zxcvbn) and ideally a k-anonymity breach-list check
   (HaveIBeenPwned range API).
4. **MFA for `BANK_ADMIN`/`SYSTEM_ADMIN` at minimum.** TOTP — lowest
   friction, no SMS vendor dependency.
5. **JWT algorithm.** `HS256` is fine while only this service verifies
   tokens. Move to `RS256`/`ES256` before a second verifying service
   exists — not urgent today, decide before it's expensive to change.
6. **Refresh tokens.** Short-lived access tokens (~15-30 min) + a longer-
   lived, revocable refresh token (same denylist as item 1) — an 8-hour
   flat expiry with no refresh is the wrong shape at production scale.
7. **API-key hygiene for H36.** Multiple simultaneously-active keys per
   bank so rotation never causes downtime, plus an expiry reminder.
8. **SSO/SAML — flag, don't build yet.** Larger PSU banks' IT departments
   often require this as a procurement condition; not justified before a
   specific customer asks.

**Verify:** confirm a revoked token is rejected within one Redis round trip.
Confirm account lockout triggers, clears, and logs to `audit_log`.

---

## Phase H35 — Defense-in-Depth

1. **WAF in front of the API** (AWS WAF, pairs with H30) — blocks common
   injection/scanning patterns, adds DDoS mitigation above H31's app-level
   rate limiting.
2. **Malware/virus scanning on uploaded documents.** Real, currently
   unaddressed: SA PDFs are uploaded and fed straight into Document AI OCR
   and Claude — `ALLOWED_CONTENT_TYPES = {"application/pdf"}` and
   `MAX_UPLOAD_SIZE_MB = 25` restrict type/size but don't scan content. Add
   ClamAV or AWS-native S3 malware scanning once H30 lands, before a file
   reaches OCR/extraction.
3. **Network segmentation.** RDS/ElastiCache/Celery workers in private
   subnets, only the API behind a public ALB — part of H30's Terraform gap,
   called out explicitly so it isn't dropped between phases.
4. **Tamper-evident audit trail, not just an audit table.** `audit_log`
   exists (`write_audit_log`, used in `auth.py`) but a row in a normal
   Postgres table can be edited by anyone with DB access, including an
   insider. `CLAUDE_v51.md` already calls the PDF reports "tamper-evident" —
   extend the same principle to the audit log: periodic hash-chaining (each
   row's hash includes the previous row's) or an S3-Object-Lock-backed
   export, so tampering is detectable.
5. **SAST + dependency/CVE scanning as an ongoing practice**, not a
   one-time pre-sale check (H32 adds it to CI; this phase makes it explicit
   this runs continuously).
6. **Ongoing penetration testing cadence** (annually, or on major
   architecture changes), not only a one-time pre-sale review.
7. **Access reviews.** Periodic recertification of who holds
   `BANK_ADMIN`/`SYSTEM_ADMIN` — cheap to define now, easy to forget later.
8. **Compliance certifications — the actual go-to-market gate.** Selling
   into banks almost always means their vendor-risk team asks for **SOC 2
   Type II and/or ISO 27001**, or at minimum a detailed security
   questionnaire response, before procurement signs — this can gate a deal
   for months. **Start this in parallel with H30 onward, not after H36
   ships** — its evidence requirements (access reviews, audit trails,
   encryption, incident response, backup/DR testing) are almost entirely
   satisfied by doing H32–H35 properly; the certification is mostly about
   having already done this list and being able to prove it.

**Verify:** a deliberately malicious test file (EICAR test string, not a
real payload) is caught before reaching OCR/extraction. The audit-log hash
chain detects a manually tampered row in a test environment.

---

## Phase H36 — Sellable External API + DPDP Compliance

**Depends on H29 (Branch/bank model) and H31/H32/H34 (rate limiting,
audit-log, API-key hygiene).** Consumers are the same banks calling in
programmatically (SAMB is intra-bank per H29, not a separate API consumer),
not a public developer signup flow. Keep the endpoint surface small.

1. **Separate auth path from officer JWT.** Per-bank API keys (hashed at
   rest, same `bcrypt`/`passlib` machinery as user passwords) scoped to a
   `bank_id`, distinct from the 8-hour user JWT — a machine client shouldn't
   need a human login flow. Reuse `require_role`'s dependency-factory
   pattern for a `require_api_key` equivalent, and reuse
   `verify_case_bank_access`'s 404-not-403 pattern unchanged.
2. **Small, deliberate endpoint surface.** Submit a case + documents, poll
   pipeline status, fetch the short report, fetch the full report — an API
   key scoped to exactly one `bank_id` makes full-report access a simple
   `bank_id` match, no separate entitlement system needed. Resist adding
   endpoints beyond what a real integration needs — smaller surface is both
   more secure and easier to sell.
3. **Per-bank rate limiting + metering.** Same Redis pattern as H31, keyed
   by API key/bank instead of user — also the natural hook for usage-based
   billing later, even if billing itself isn't built now.
4. **OpenAPI spec + developer docs.** FastAPI generates this automatically —
   the work is curating it (examples, auth flow, error shapes) into
   something presentable to a buyer's engineering team. Feeds off H32's
   consolidated `API_ENDPOINTS.md`.
5. **DPDP Act 2023 compliance — legal/product work, not just code:**
   - **Data Fiduciary vs. Data Processor roles.** The bank remains Data
     Fiduciary for its borrowers' data; SLRAI is very likely a processor.
     Needs an actual Data Processing Agreement template per bank customer —
     a legal deliverable, flag it to whoever owns that.
   - **Data localization** — structurally satisfied once H30 lands
     (RDS/S3/ElastiCache all `ap-south-1`), but confirm Bedrock invocation
     itself doesn't route through a non-Indian region (H30's verify step).
   - **Purpose limitation & retention.** Define and document retention
     periods for `documents`/`case_facts`/`reports` after a case closes,
     and build the actual deletion job — no retention/deletion logic exists
     anywhere in `app/tasks/` today.
   - **Breach notification procedure + grievance/DPO contact** — process
     documentation, should exist before the API is sold, not after an
     incident.
   - **Consent artifacts** — a bank-side obligation, not SLRAI's directly,
     but the bank-onboarding flow (H29) should surface it explicitly to the
     signing customer rather than staying silent.
   - **Extend `audit_log`** to cover API-key-authenticated access too
     (currently written from the dashboard JWT path only) rather than
     building a parallel audit mechanism.
6. **Security review gate.** Before selling to any bank, a focused review
   against the OWASP API Security Top 10 (broken object-level authorization
   is the one `verify_case_bank_access` already guards well — confirm the
   API-key path inherits the same check, not a reimplementation), and an
   external pen-test if the buyer's security questionnaire requires one.

**Verify:** issue a test API key for a fixture bank, confirm it can fetch
that bank's short report and cannot enumerate/fetch another bank's case by
ID (404, not 403). Confirm rate limiting triggers under a burst test.
Confirm every documented endpoint requires either the officer JWT or the API
key — no route reachable unauthenticated except `/auth/login` and
`/auth/register`.

---

## Build order

```
H11 (Indian Kanoon fix) ──────────────────────────────────────────────┐  independent — start first
                                                                        │
H12 (micro-fixes) ──┐                                                  │
H13 (tool-use)       ├─ independent, any order                         │
H14 (rule engine     │                                                 │
     correctness) ───┘                                                 │
        │                                                               │
        ├──▶ H15 (flag display) ──▶ H16 (red-flag pipeline) ◀── H11's   │
        │         │                    corpus data matters here         │
        │         └──▶ H21 (two reports, needs H15's flag counts)      │
        │                    ▲                                          │
        │                    └── H20 (doc pipeline) independent,       │
        │                        can land any time before H21          │
        │                                                               │
H17 (extraction cost) ─┬─▶ H23 (Redis cache, needs H17's hashing)      │
H18 (citation extract)  │                                               │
H19 (exec summary) ─────┘  independent of everything above              │
                                                                          │
H22 (Batch API) ── after H12-H19 stable ─────────────────────────────────┤
                                                                          │
H24, H25, H26, H27, H28 ── independent, parallelizable                  │
   (H27 blocked on GCP setup; H28 blocked on product/legal decision)    │
                                                                          │
H29 (Branch/SAMB) ──┐                                                    │
H30 (AWS migration) ─┴─ independent of each other, both unblocked now ──┤
   H30 also finishes H11's Bedrock-client cross-reference                │
                                                                          │
H34 (auth hardening) ── independent of H30, start anytime ──────────────┤
                                                                          │
H31, H32 ── pair with H30 (secrets/IAM) ─────────────────────────────────┤
H33 (DB hardening) ── depends on H30's RDS ──────────────────────────────┤
H35 (defense-in-depth) ── partially depends on H30 (WAF/network) ───────┤
                                                                          │
H36 (sellable API + DPDP) ── depends on H29 + H31/H32/H34 ──────────────┘
```

1. **H11 first**, as instructed — independent of everything else, and its
   corpus data is a real (if soft) precondition for H16 meaning anything.
2. **H14(c) is the one hard correctness dependency** in the whole plan — it
   must land before H15 and H16; both would ship visibly wrong output
   otherwise (a time-barred SA rendering as the worst possible finding).
3. **H15 before H16 and H21** — `display_severity` is the shared primitive
   both build on; building either first (or worse, both independently)
   creates two competing classification systems.
4. **H20 and H21 are independent** of each other except that H21 needs
   H15's flag-classification to exist — H20 (doc pipeline/no-SA) can land
   whenever convenient relative to H21.
5. **H17(c)'s paragraph hashing gates H23** — same as before.
6. **H22 (Batch API) waits until H12–H19 settle** — it changes Chain A's
   task shape, so extraction-layer work upstream should be stable first.
7. **H24–H28 are flexible** — independent of the core pipeline work,
   parallelizable, with two externally blocked (H27 on GCP console setup,
   H28 on a product/legal decision you need to make, not a technical one).
8. **H29 and H30 are both fully unblocked now** and independent of each
   other.
9. **H34 (auth hardening) has zero AWS dependency** — it can start on day
   one, in parallel with H11, rather than waiting anywhere near H29/H30.
10. **H31–H33, H35 cluster around H30** for the AWS-dependent pieces, but
    each phase's independent items are called out explicitly so they don't
    have to wait idle.
11. **H36 is last** — the only phase genuinely gated on most of the rest.

---

## Docs Sync

Per explicit instruction, the project's own documentation is updated
alongside this plan so every doc reflects the same target, not five
independently-drifting descriptions of the system. Changes made directly in
the repo (not just described here):

**`CLAUDE_v51.md`:**
- Fixed the `M_CROSS_1` claim (line 31) — was asserted as already
  implemented; it is not (grepped, confirmed absent) — now reads as planned
  (H14) with a pointer to this roadmap, not shipped.
- Fixed `ALLOWED_CONTENT_TYPES` (line 260) — was claiming
  `{application/pdf, image/jpeg, image/png, image/tiff}`; the actual code
  (`storage.py:26`) is PDF-only, deliberately (OCR only supports PDF
  end-to-end via pypdf splitting). Doc now matches code.
- Fixed the `IBC_CATEGORY_TO_GROUND_CODE` claim (line 149) — was pointing at
  `scripts/load_judgments.py`; that mapping does not exist there. Removed
  the false pointer, noted the actual state (H11's classification step is
  the real replacement for what this claimed to be).
- Fixed the ibclaw.in bulk-ingestion description — was describing a second
  corpus source with no corresponding script anywhere in `scripts/`. Now
  describes what's actually real: the single Indian Kanoon path
  (`fetch_from_ik.py`, being fixed in H11).
- Added a **Roadmap** pointer section linking to this phase plan, so anyone
  reading `CLAUDE_v51.md` first finds their way to current build status
  instead of a static architecture snapshot with no sense of what's done vs.
  planned.
- Confirmed the AWS/Bedrock production direction in the tech-stack section
  rather than leaving it implicit.

**`README.md`:** Added a short **Roadmap** pointer near the top (mirroring
`CLAUDE_v51.md`'s). Elevated the `IK_API_TOKEN`/Indian Kanoon setup step —
previously a single line under "Running the Stack" — into its own step given
H11 now leads the build sequence; a fresh setup should know this matters
from the start, not discover it three phases in.

**`API_ENDPOINTS.md` — the two-file drift is fixed, not left for H32.**
`./API_ENDPOINTS.md` (comprehensive, 31-endpoint table format, phase-tagged)
and `./docs/API_ENDPOINTS.md` (workbench-only, richer per-endpoint
body/response detail) were confirmed to be two different files with
different content. Consolidated: root `./API_ENDPOINTS.md` stays canonical
(it's the complete one), merged in the richer body-shape documentation from
the `docs/` version's Workbench section (the request/response detail that
version had and the root one lacked), and `./docs/API_ENDPOINTS.md` now
redirects to the root file instead of silently diverging further.

**`docs/schema_gaps.md`:** Cross-referenced its "Still genuinely open" §1
(all ~16 missing named date fields) to H14(b) directly, so the gap doc and
the live roadmap agree on where that work is tracked instead of the gap doc
describing an untracked TODO.

**`SLRAI_Blueprint_v5.md`:** At 10,326 lines (not ~8,600 as `CLAUDE_v51.md`
claimed — fixed that count too), a full rewrite isn't something to attempt
blind. Added a short pointer note at the top, matching the file's own
existing "Authority Note" pattern (`CLAUDE_v51.md` already governs judgment-
architecture conflicts over this file) — extended the same idea to say this
roadmap document governs current build status and phase sequencing; the
blueprint remains the historical v5 design reference and is not being kept
in sync phase-by-phase. Honest boundary: I have not re-verified this file's
~10,300 lines line-by-line against the current codebase this pass, so it's
not safe to represent it as current beyond that pointer.