Here's the full content of `FIRST_REPORT_CHECKLIST.md`:

---

# Getting Your First Report Out — Checklist

Scope: **only what's needed to get one real report out of the pipeline in 1-2 days.** Not the master roadmap (`H11`–`H36`, in the phase-plan document) — that's the ongoing build-out for after this works. If a task isn't here, it isn't needed for your first report; don't pull anything from the roadmap into this pass.

## Why you don't have a report yet — and what changed in this revision

Two things need to be running for a real (not placeholder-key) first report, per your direction: **Claude via AWS Bedrock specifically** (not a direct `sk-ant-...` key — you want to test on the real production path), and **at least some real judgment corpus fetched via Indian Kanoon**, not an empty one. Both are below. Be aware going in: getting Bedrock invoking successfully is mostly an AWS-account setup problem, not a code problem, and getting judgments beyond the one you already have to **Class A** status (verified, `has_verified_conditions: true`) is a human legal-review step this project has always required (`CLAUDE_v51.md`: "Harasis + advocate sign-off") — not something a script can finish unattended in 2 days. What *is* achievable in that window: Bedrock actually invoking Claude, and a **working, bug-fixed** Indian Kanoon fetch pipeline producing real (Class B) judgments plus your one existing Class A fixture loaded. Honest scope below, not an overpromise.

Chain B does not hard-fail on a sparse corpus either way (`retrieval.py`'s `retrieve_candidate_judgments` returns `([], [])` on empty/unreachable, never raises) — but you asked for real judgments in the first report, so Step 1 gets you that rather than relying on that tolerance.

---

## Step 0 — Get Claude running via AWS Bedrock (~0.5 day code + AWS setup time, which can be the long pole)

**AWS-account side (not code — do this first, it can have approval lag):**
1. In the AWS Bedrock console, request **model access** for the Claude model you're targeting. Anthropic models on Bedrock require explicit per-account approval — this is not instant; check it before you assume the code is broken if invocation fails with an access-denied error.
2. Confirm the model is actually offered in the region you pick. Production target is `ap-south-1` for data-localization (DPDP — see the master roadmap's `H36`), but if Claude-on-Bedrock isn't available there yet, **use a region where it is for this first-report test** (e.g. a US region) and treat narrowing to `ap-south-1` as a follow-up before real production traffic — don't block your first report on a region-availability issue that's separate from "does the pipeline work."
3. Create IAM credentials (or, if running on EC2/ECS later, a role) with `bedrock:InvokeModel` + `bedrock:InvokeModelWithResponseStream` on that model's ARN. For local `docker-compose` testing, pass `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`/`AWS_REGION` into the containers via `.env` — there's no EC2 instance role to fall back on locally.

**Code (small — `boto3==1.34.0` is already a dependency, `anthropic==0.56.0` already includes `AnthropicBedrock`, confirm both before assuming you need new packages):**

1. Add to `app/config.py`: `aws_region: str = "ap-south-1"` (or your chosen test region), keep `anthropic_api_key` optional now instead of required (it's currently a required field with no default — that will hard-fail config load once you're not using it).
2. In `app/services/extraction/nlp_layer.py` and `app/services/judgments/applicability.py`, replace:
   ```python
   import anthropic
   client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
   ```
   with:
   ```python
   from anthropic import AnthropicBedrock
   client = AnthropicBedrock(aws_region=settings.aws_region)
   ```
   `client.messages.create(...)` calls elsewhere in both files stay identical — same API surface. `cache_control` usage (already in both files) is unchanged too — Bedrock supports the same field.
3. Update `settings.claude_model` to the Bedrock model ID format for your chosen model (different string shape than the direct-API model name — check the exact ID in the Bedrock console's model catalog for the region you picked, don't guess it).

**Verify:** upload a test document and confirm in worker logs that extraction actually calls out to Bedrock and returns — not a `401`/`AccessDenied` (means IAM/model-access isn't right yet) and not a region/model-not-found error (means the model ID string or region is wrong).

## Step 1 — Fix and run the Indian Kanoon ingestion pipeline (~1 day)

`scripts/fetch_from_ik.py` genuinely calls the real Indian Kanoon API, but has three bugs that make everything it fetches invisible to retrieval — fixing these is what makes "fetch a real judgment" actually work, not just run without erroring:

1. **`holding_summary` ends up empty.** `fetch_and_summarize()` (`fetch_from_ik.py:106-151`) writes the Claude-drafted summary with no `## HOLDING SUMMARY` markdown heading in front of it. The parser (`scripts/_judgment_md.py`'s `_parse_body_sections`) only captures text that follows a recognized `## HEADING` — unheaded text is silently dropped, and `holding_summary` is exactly what gets embedded into Qdrant (`load_judgments.py:98`). **Fix:** write the summary as `"## HOLDING SUMMARY\n\n" + summary` instead of the bare summary.
2. **`ground_codes` is hardcoded `["UNKNOWN"]`** (`fetch_from_ik.py:141`). Retrieval filters by exact ground_code match — `UNKNOWN` never matches a real query, so the judgment can never surface regardless of how good the embedding is. **Fix:** add one more Claude call per fetched judgment (reuse the same client/gate pattern as `generate_class_b_summary`) asking it to classify `ground_codes` and `favor` (`BANK`/`BORROWER`/`NEUTRAL`) from the judgment text, against the same valid ground_codes list already defined in `nlp_layer.py`'s `BATCH_USER_TEMPLATE`. If uncertain, write `NEEDS_GROUND_CODE_REVIEW: true` in the frontmatter instead of guessing — consistent with this project's "never guess" rule elsewhere — and treat those as needing a quick manual look before you trust them in a report.
3. **`court` is hardcoded `"HIGH_COURT"`** (`fetch_from_ik.py:133`) even though a search hit could be Supreme Court or a Tribunal. **Fix:** read the actual court from the Indian Kanoon search result's own fields instead of hardcoding it; fall back to `NEEDS_REVIEW` if it's genuinely ambiguous rather than guessing.

**Then, to actually get judgments:**

4. Create `docs/judgments_manifest.txt` (doesn't exist yet) — **you need to supply the actual citations or search queries**, one per line. This is real legal research input; nothing here can safely fabricate case citations for you. Even 5-10 well-known SARFAESI/DRT/SC citations is enough to prove the pipeline works end to end.
5. Run it:
   ```bash
   docker compose exec api python scripts/fetch_from_ik.py --citations-file docs/judgments_manifest.txt
   docker compose exec api python scripts/load_judgments.py --dir docs/judgments/
   ```
6. **Also load your existing Class A fixture** — it's sitting on disk but not necessarily loaded yet:
   ```bash
   docker compose exec api python scripts/load_judgments.py --dir docs/judgments/ --file e_muthurathinasabathy.md
   ```
   (The command in step 5 already covers this file too if it's in the same directory — running it again is harmless, upserts by citation.)

**On "at least Class A":** everything `fetch_from_ik.py` produces, even fully fixed, comes out as **Class B** (`has_verified_conditions: false`) by design — the script has no way to auto-generate the `applicable_conditions`/`exclusion_conditions` JSON that Class A status requires, because that's supposed to be a verified legal judgment, not a Claude guess. Promoting a judgment to Class A means someone (you or Harasis) reads it and writes those conditions by hand, the same way `e_muthurathinasabathy.md` was authored. That's real, ongoing work — not something this 1-2 day pass can finish for more than the one you already have. What you'll have after this step: a **working** fetch pipeline producing real, retrievable Class B judgments for whatever citations you feed it, plus your one existing Class A judgment actually loaded and live. If you need more Class A coverage before you're comfortable calling this "working," that's the next real task after this checklist, not a bug to fix in it.

**Verify:** after loading, run a Qdrant search for one of your fetched judgments' assigned ground_code and confirm it comes back — this round-trip is the real confirmation that Steps 1-3's fixes worked, not just "the script exited 0."

---

## Step 2 — Fix the compliance-score/recommendation polarity bug (~1 day)

**Why this matters for your very first report specifically:** if your first test case happens to include a time-barred SA (borrower filed outside the 45-day window) or the specific ATS/mortgage-same-date fact pattern, the recommendation your first report shows will be **backwards** — the case where the bank is most clearly in the right currently scores as the worst possible outcome. This is a real correctness bug, not a style issue, and it's small enough to fix now rather than let your first report be misleading.

**The bug:** `compute_compliance_score` (`app/services/scoring/compliance_score.py:14-20`) treats every `FAIL` `ComplianceResult` as "the bank did something wrong." Two rules use `FAIL` to mean the opposite — `M4_C1`/`M4_C3` in `m4_limitation.yaml` (SA is time-barred — good for the bank) and `M10_C2` in `m10_third_party.yaml` (ATS/mortgage same-date fraud finding — good for the bank). The same conflation inflates `ground_strength.py`'s `factual_score` for these findings instead of deflating it.

**The fix:**
1. Add a nullable `outcome_favors` column to `compliance_results` (`String`, `CHECK (outcome_favors IN ('BANK','BORROWER'))`, default `'BORROWER'`) — small Alembic migration.
2. In `m4_limitation.yaml`, set `outcome_favors: BANK` on the `M4_C1` and `M4_C3` checks. In `m10_third_party.yaml`, set it on `M10_C2`. Leave every other check alone (default `BORROWER` keeps current behavior).
3. `compute_compliance_score`: only sum deductions where `status=="FAIL" and outcome_favors=="BORROWER"`.
4. `compute_ground_strength`'s `factual_score` (`app/services/scoring/ground_strength.py:44-49`): `1.0` when `outcome_favors=="BORROWER"`, `0.0` when `"BANK"`, `0.4` when `UNKNOWN` — replace the current raw-status check.
5. While in `compliance_score.py`, also add `HIGH` and `REVIEW_REQUIRED` to the `DEDUCTIONS` dict (they're valid per the DB's own `CheckConstraint` but missing here, so a `HIGH`-severity fail like `M10_C2` currently silently deducts `0`).

**Verify:** fixture a case where only `days_from_measure_to_sa > 45` is true (nothing else) — confirm `compliance_score` stays near 100 and the recommendation is favorable, not degraded.

*(This is Roadmap `H14(c)`, condensed to just the actionable steps — see the master plan for the full investigation if you want the "why" in more detail.)*

## Step 3 — Fix date-field extraction (~0.5–1 day, optional but strongly worth it)

**Why this matters:** right now, only one date field (`balance_payment_date`) is actually extracted by Claude into a usable fact. Every other date the rule engine depends on — `auction_date`, `demand_notice_date`, `mortgage_date`, `lease_date`, `valuation_date`, `npa_classification_date`, `objection_date`, `bank_reply_date`, `possession_notice_date`, `sale_notice_date`, `drt_stay_order_date`, `ats_date`, `measure_date`, `sa_filing_date`, `date_of_last_payment`, `sale_certificate_date` — is parsed by Claude but never saved anywhere. You will have to type every one of these into the workbench by hand for your first (and every) test case unless you do this fix. Skip this step if you'd rather just hand-enter dates once to see a report faster — it's not a hard blocker, just tedious without it.

**The fix:** `nlp_layer.py`'s `BATCH_USER_TEMPLATE` (around line 151-153) has a `date_facts` object that currently only asks for `balance_payment_date`. Add the ~15 fields above to that same object, same pattern (field name, `DD.MM.YYYY` format, a one-line disambiguating context cue for each — e.g. "date the demand notice under Section 13(2) was issued"). `chain_a.py::task_nlp_extract_facts` (lines 309-331) already loops over `date_facts` and persists whatever's in it — no engine or persistence change needed, this is purely extending the prompt template.

**Verify:** run one fixture SA through Chain A, check the workbench — the date fields listed above should now appear as extracted facts (possibly `LOW_CONFIDENCE`, needing your confirmation) instead of not existing at all.

*(This is Roadmap `H14(b)`.)*

## Step 4 — One-line bonus fix, while you're already in these files (~5 minutes)

`app/tasks/chain_b.py`'s `RULE_TO_GROUND_MAP` dict is missing one entry: `M10_C7` (Rule 9(4), balance consideration not paid within 90 days) has no ground_code mapping, so it's invisible to scoring even when it fires. Add:

```python
"M10_C7": "AUCTION_PURCHASER",
```

Free while Step 2 already has you looking at `chain_b.py`/the M10 rules — skip if you're pressed for time, it only matters for that one specific fact pattern.

---

## Running your first case end to end

Once Step 0 is done (Steps 1-4 are quality/correctness, not hard blockers):

1. `POST /api/v1/auth/register` — bank + admin user, save the token.
2. `POST /api/v1/cases` — create a case.
3. `POST /api/v1/cases/{case_id}/documents` — upload your SA PDF. Watch `docker compose logs worker -f` and poll `GET .../pipeline-status` until status is `PENDING_HUMAN_REVIEW`.
4. `GET /api/v1/cases/{case_id}/workbench` — see what needs confirming. **These fields must all be confirmed before `confirm-all` will succeed** (`REQUIRED_FIELDS` in `app/api/workbench.py`): `notice_served`, `objection_filed`, `bank_reply_given`, `valuer_rbi_empanelled`, `demand_notice_date`, `sa_filing_date`, `sa_applicant_type` (routing field — 422 if unconfirmed), `total_borrowers_in_loan`, `npa_classification_date`, `date_of_last_payment`. Use `PATCH .../facts/{fact_id}` per field.
5. `POST /api/v1/cases/{case_id}/workbench/confirm-all` — fires Chain B.
6. Poll pipeline status again until `COMPLETE`.
7. `GET /api/v1/cases/{case_id}/report` (JSON) or `.../report/pdf` (PDF).

Full `curl` examples for every step are in `README.md` if you want them copy-pasteable.

---

## What not to touch right now

Everything else in the codebase audit — the red-flag scoring pipeline overhaul, the two-report bidder sheet, multi-branch/SAMB access, RDS/S3/ElastiCache migration (Step 0 above is only the Claude-via-Bedrock slice of that, not the rest of `H30`), the sellable API, DPDP compliance work, and growing the judgment corpus past what Step 1 gets you (more citations, more Class A promotions) — is real, scoped, and waiting in the master roadmap document. None of it is needed to get a report out. Come back to it once you've seen your first report and know the core loop actually works end to end.