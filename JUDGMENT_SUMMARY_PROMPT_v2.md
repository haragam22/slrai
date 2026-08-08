# SLRAI Judgment Summarization Prompt
## For AI Models (Claude / Gemini Pro)
## Version 2.0 — Updated for Blueprint v5.4

---

## INSTRUCTIONS FOR THE AI MODEL

You will be given the full text of a SARFAESI-related judgment. Your task is to
produce a structured summary in the exact format specified below. This summary
will be ingested by a legal AI system called SLRAI and stored in a vector database.
Every field you fill in has a downstream consequence — wrong values cause wrong
legal analysis for Indian banks.

**Before you begin, read this entire prompt. Do not start writing the summary until
you have read every section including the GUARDRAILS at the bottom.**

---

## WHAT SLRAI IS — CONTEXT YOU NEED

SLRAI analyses Securitisation Applications (SAs) filed by borrowers before the
Debt Recovery Tribunal (DRT) under Section 17 of the SARFAESI Act 2002. When a
bank conducts a SARFAESI enforcement action (demand notice, possession, auction)
and the borrower challenges it, SLRAI:

1. Extracts facts from the SA document
2. Runs compliance rules against those facts
3. Retrieves relevant precedents from a judgment database
4. Determines which precedents APPLY to the specific facts of this case
5. Generates a risk report for the bank

Your summary is what the system uses in step 3 and 4. The `ground_codes` field
determines retrieval. The `CONDITION: WHEN THIS JUDGMENT APPLIES` section
drives applicability. The `BORROWER'S CLAIM` section helps the system
recognise when a future SA is raising the same argument.

If your summary is wrong, the bank may get incorrect legal risk advice.

---

## THE COMPLETE TEMPLATE

Produce EXACTLY this structure. Do not add sections. Do not remove sections.
Do not rename headings. Output the result as a single markdown block.

```markdown
---
# IDENTITY
citation: ""
title: ""
short_name: ""
court: ""
high_court_state: null
bench_strength: 0
judgment_date: ""
overruled: false
overruled_by: null
distinguished_by: []

# CLASSIFICATION
favor: ""
favor_verified: true
ground_codes: []
statutory_basis: ""
act_sections: []
rules_sections: []

# SLRAI ROUTING
slrai_modules: []
keywords: []
retrieval_condition: ""

# SOURCE
source: ""
ik_doc_id: ""
ik_url: ""
has_verified_conditions: true
---

## BORROWER'S CLAIM

## HOLDING SUMMARY

## KEY FACTS OF THIS CASE

## WHAT THE COURT DECIDED

## KEY QUOTE

## CONDITION: WHEN THIS JUDGMENT APPLIES

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

## STATUTORY CONTEXT

## RELATIONSHIP TO OTHER JUDGMENTS

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

## WIN-RATE CONTRIBUTION
favor:
counted_in_ground:
```

---

## FIELD-BY-FIELD INSTRUCTIONS

### `citation` — REQUIRED

The formal legal citation. Use the strongest available:
- Supreme Court: `"(2024) 2 SCC 1"` or `"2026 INSC 303"` or `"AIR 2024 SC 1234"`
- High Court: `"2019 (3) Bom CR 445"` or `"(2022) 4 GLH 210"`
- DRAT: `"(2024) ibclaw.in 47 DRAT"`
- If neutral citation and SCC both available, use SCC. If only neutral citation
  (like 2026 INSC 303), use that.
- Never leave blank. If truly unknown, write `"CITATION_UNKNOWN — [full title]"`.

### `title` — REQUIRED

Full formal title exactly as it appears on the judgment heading. Copy verbatim.

### `short_name` — REQUIRED

How practitioners refer to this case in argument. Maximum 60 characters.
The first significant party name is usually sufficient:
- "Kanaiyalal" not "Kanaiyalal Lalchand Sachdev and Ors. v. State of Maharashtra"
- "Celir LLP" not "Celir LLP v. Bafna Motors Pvt. Ltd."
- "ITC Blue Coast" for "ITC Limited v. Blue Coast Hotels Ltd."
Use the name lawyers would say in court.

### `court` — REQUIRED

Exactly one of these values:
```
SUPREME_COURT
HIGH_COURT
DRAT
DRT
```

### `high_court_state` — REQUIRED only if court = HIGH_COURT

Write the state name exactly: `"Maharashtra"`, `"Delhi"`, `"Tamil Nadu"`,
`"Gujarat"`, `"Karnataka"`, `"Kerala"`, `"Uttar Pradesh"`, `"Punjab"`,
`"Rajasthan"`, `"West Bengal"`, `"Andhra Pradesh"`, `"Telangana"`,
`"Madhya Pradesh"`, `"Odisha"`, `"Jharkhand"`, `"Chhattisgarh"`, etc.
Write `null` for SUPREME_COURT, DRAT, DRT.

### `bench_strength` — REQUIRED

Number of judges who signed the judgment.
- Constitution bench: 5 or more
- Division bench (SC): 3
- Two-judge bench (SC): 2
- Single judge (HC): 1
- If you cannot determine from the judgment, write `1` with a note in
  NEW REQUIREMENTS section.

### `judgment_date` — REQUIRED

Format: `"YYYY-MM-DD"`. Read from the judgment's date line.
If exact date is not stated, use `"YYYY-MM-01"` for the first of the month
and note the uncertainty in NEW REQUIREMENTS.

### `overruled` — REQUIRED

`false` for all judgments unless you have seen specific language in a later
judgment that expressly overrules this one. Do NOT set to `true` based on
your training knowledge alone — only set `true` if the judgment itself or
a later judgment in the same file explicitly uses "overruled" or "per incuriam".

### `overruled_by` — REQUIRED only if overruled = true

Citation of the overruling judgment. Write `null` otherwise.

### `distinguished_by` — OPTIONAL

List of later judgment short names that explicitly distinguished this one.
Write `[]` if unknown. Add only if the later judgment is mentioned in the
text you are reading.

---

### `favor` — REQUIRED — READ THIS CAREFULLY

Who won the specific case you are summarising?

```
BANK     — Bank's enforcement action was upheld. Borrower's SA dismissed.
           DRT / DRAT / HC / SC ruled in favour of the bank/secured creditor.
BORROWER — Borrower's SA was allowed. Bank's enforcement action set aside.
           DRT / DRAT / HC / SC ruled in favour of the borrower/guarantor.
NEUTRAL  — Genuine mixed outcome. Matter remanded with directions that do
           not clearly favour either side. Constitutional validity confirmed
           but a specific provision struck down. Use sparingly.
```

**GUARDRAIL ON FAVOR:**
Do NOT use NEUTRAL just because the matter was remanded. If the court
set aside the bank's enforcement action and sent it back for compliance
(like Kanaiyalal — 13(3A) reply remand), that is BORROWER-favored even
though it is technically a remand. Ask yourself: who got what they came for?

Do NOT use BORROWER just because the borrower made some arguments.
If the bank's auction sale was upheld despite the borrower's challenge, that is BANK.

Do NOT infer favor from who is the "good party" morally. Only from who won the
legal dispute.

### `favor_verified` — REQUIRED

Always write `true`. You are the verifying AI. When a human advocate reviews
this file, they can change it to `false` if they disagree with your favor
classification. You are responsible for getting it right.

### `ground_codes` — REQUIRED — NEVER LEAVE EMPTY

**⚠️ CRITICAL GUARDRAIL: `ground_codes: []` is never acceptable.**
**If you cannot identify a ground code, use `["UNKNOWN"]`.**
**An empty list makes this judgment invisible to the retrieval system.**

List ALL ground codes that apply. Put the PRIMARY ground first.
A judgment can address multiple grounds — list all that are genuinely addressed.

**Complete list of valid ground codes:**

```
SERVICE_DEFECT          — Section 13(2) demand notice was not properly served
AMOUNT_DISPUTE          — Debt amount in demand notice was wrong or inflated
REPLY_NOT_GIVEN         — Bank did not reply to borrower's Section 13(3A) objection
AUCTION_GAP_DEFECT      — Less than 30 clear days between sale notice and auction
NEWSPAPER_PUB_DEFECT    — Required newspaper publication was defective or absent
LIMITATION_EXPIRED      — SA was filed after the 45-day limit (this HELPS the bank)
TENANCY_CLAIM           — Tenant or lessee is claiming protection against eviction
VALUATION_DISPUTE       — Property valuation is challenged as wrong or defective
NOTICE_ALL_PARTIES      — Not all borrowers/guarantors received the demand notice
NPA_PREMATURE           — Account classified NPA before 90-day period elapsed
NPA_DURING_RESTRUC      — Account classified NPA while restructuring was pending
MSME_RESTRUC_SKIPPED    — Bank did not offer MSME one-time restructuring before NPA
POSSESSION_DEFECT       — Possession notice or physical possession was defective
NOTICE_FORMAT_DEFECT    — Demand notice format or content did not comply with rules
AO_AUTHORIZATION        — Authorised Officer was not properly authorised by the bank
AUCTION_NOTICE_AFFIXING — Auction notice was not physically affixed at the property
AUCTION_DURING_STAY     — Auction was conducted while a DRT/court stay was in force
PENDING_SA_CONCEALED    — Bank concealed pending SA in Section 14 petition to CMM
THIRD_PARTY_ATS         — Third party holding an Agreement to Sell is challenging
AUCTION_PURCHASER       — Auction purchaser's rights are being challenged or defended
RIGHT_OF_REDEMPTION     — Borrower claiming right to redeem mortgage before/after sale
SECOND_SA_FRESH_CAUSE   — Second SA on a fresh/different cause of action
UNKNOWN                 — Cannot be classified — use only as last resort with explanation
```

**How to choose:**
- Read the ground or issue the borrower raised in their SA or writ petition
- Match that argument to the closest ground code above
- If multiple grounds were raised, list all of them
- If this judgment addresses a ground not in this list, write `UNKNOWN` and
  describe the new ground in the NEW REQUIREMENTS section

### `statutory_basis` — REQUIRED

```
ACT   — judgment primarily interprets the SARFAESI Act 2002 itself
RULES — judgment primarily interprets the Security Interest (Enforcement) Rules 2002
BOTH  — judgment substantially addresses both Act and Rules
RBI   — judgment primarily interprets an RBI circular or direction
TPA   — judgment primarily interprets the Transfer of Property Act 1882
IBC   — judgment primarily interprets the Insolvency and Bankruptcy Code 2016
OTHER — other legislation (Registration Act, Stamp Act, Companies Act etc.)
```

### `act_sections` — REQUIRED if statutory_basis is ACT or BOTH

List the specific SARFAESI Act sections the judgment interprets:
```yaml
act_sections:
  - "Section 13(2)"
  - "Section 13(3A)"
  - "Section 17"
```

### `rules_sections` — REQUIRED if statutory_basis is RULES or BOTH

List the specific Rules provisions:
```yaml
rules_sections:
  - "Rule 8(6)"
  - "Rule 8(6)(7)"
  - "Rule 9(4)"
```

---

### `slrai_modules` — REQUIRED — NEW FIELD

Which SLRAI compliance modules is this judgment most relevant to?
Use one or more values from:

```
M1  — Demand notice compliance (Section 13(2), service, amount, AO authorization)
M2  — Reply compliance (Section 13(3A), bank's duty to reply with reasons)
M3  — Auction procedure (Rule 8/9, notice gap, newspaper, affixing, stay violations)
M4  — Limitation (45-day period under Section 17)
M5  — Tenancy and lease disputes
M6  — Valuation disputes
M7  — Multi-party notice (all borrowers and guarantors served)
M8  — NPA classification timing and upgradation
M9  — MSME restructuring requirements
M10 — Third party rights (ATS holders, auction purchasers, right of redemption)
```

```yaml
slrai_modules:
  - "M3"
  - "M10"
```

### `keywords` — REQUIRED — NEW FIELD

5-10 specific legal phrases that appear verbatim in SA filings when borrowers
raise the argument this judgment addresses. These are used for keyword-based
retrieval when the ground_code filter and vector search return too few results.

**Rules for keywords:**
- Write phrases as borrowers and their advocates actually write them in SAs
- These should be specific enough to identify this type of dispute
- Do NOT write generic terms like "SARFAESI" or "auction" — every judgment has those
- DO write specific terms like "Rule 9(4)", "90 days", "balance consideration",
  "inchoate sale", "right of redemption", "affixing notice"

```yaml
keywords:
  - "Rule 9(4)"
  - "balance consideration"
  - "outer limit three months"
  - "inchoate sale"
  - "statutory finality"
```

### `retrieval_condition` — REQUIRED — NEW FIELD

One sentence, under 200 characters, stating the specific factual condition
under which this judgment applies. This is the cheap pre-filter sentence the
pipeline checks before doing anything expensive with the full judgment —
it must stand alone without reading HOLDING SUMMARY or any other section.

**Rules:**
- Start with "Applies when" and state the condition in plain terms
- Must be consistent with the CONDITION: WHEN THIS JUDGMENT APPLIES section
  and with the last sentence of HOLDING SUMMARY — same fact pattern, just
  compressed to one line
- Do not restate the ground code or module name alone ("Applies when
  AUCTION_PURCHASER ground raised" is too vague) — name the actual fact
  ("Applies when the auction purchaser paid the balance 75% after the
  Rule 9(4) 90-day limit")

```yaml
retrieval_condition: "Applies when the auction purchaser paid the balance 75% of sale consideration more than 90 days after the auction date."
```

### `source` — REQUIRED

```
SC_FULL_TEXT      — Full Supreme Court judgment
HC_FULL_TEXT      — Full High Court judgment
DRAT_FULL_TEXT    — Full DRAT judgment
IBC_LAW_SUMMARY   — Summary from ibclaw.in (not full text)
IK_SUMMARY        — Auto-generated summary from Indian Kanoon data
```

### `has_verified_conditions` — REQUIRED

`true` if the CONDITION sections below use actual CaseFactSchema field names
in backticks. `false` if conditions are written in plain English without field names.

**GUARDRAIL:** If you write conditions without field names → set `has_verified_conditions: false`.
If you use proper field names → set `has_verified_conditions: true`.
`true` is strongly preferred. `false` makes this judgment Class B — statistics only,
never used by the applicability engine.

---

## SECTION INSTRUCTIONS

### ## BORROWER'S CLAIM — REQUIRED

3-5 sentences answering: What did the borrower/applicant argue in their SA or writ?

This is NOT the factual background. This is NOT the court's holding.
This is specifically what the borrower claimed the bank did wrong.

**Template for this section:**
```
The borrower(s) alleged that [specific procedural violation or rights violation].
They contended that [the legal consequence of that violation].
They further alleged / claimed / argued that [any additional arguments].
The prayer before the DRT/HC/SC was to [specific relief sought].
```

**Why this matters:**
When a future SA comes in and the extraction engine reads the borrower's
allegation, the system needs to recognise that the same argument was made
in this case. The borrower's claim section is matched against what the
borrower says in the new SA. It is the most important section for retrieval.

**GUARDRAIL:** Do not describe what the bank did (those are facts). Do not
describe what the court held (that is the holding). Only what the borrower argued.

---

### ## HOLDING SUMMARY — REQUIRED

120-200 words. The ratio decidendi only.

This is embedded as a vector in the Qdrant database. The quality of this
section determines whether this judgment is retrieved for the right cases.

**Rules:**
- State the legal RULE the court established — not the facts, not the arguments
- Cite the exact statutory provision being interpreted
- State what the consequence of violation is
- State which side this favors and why
- The LAST SENTENCE must state: "This applies when: [specific factual condition]."

**GUARDRAIL:** Do not begin with "In this case..." or "The borrowers filed...".
Start with the legal principle: "Section 13(3A) is mandatory..." or
"Rule 9(4) prescribes a mandatory outer limit..." etc.

---

### ## KEY FACTS OF THIS CASE — REQUIRED

3-5 sentences describing the factual background that led to this case.
Include:
- Type of loan and approximate amount
- How the account became NPA
- Which SARFAESI step triggered the challenge (demand notice / possession / auction)
- What specific defect or circumstance caused the dispute
- What the DRT/lower court decided before the appeal (if applicable)

**GUARDRAIL:** This section describes WHAT HAPPENED. It is distinct from
BORROWER'S CLAIM (what was argued) and HOLDING SUMMARY (the legal rule).

---

### ## WHAT THE COURT DECIDED — REQUIRED

2-3 sentences. The specific outcome and direction given by the court.
What was set aside? What was upheld? What was remanded and on what terms?
Was the borrower/guarantor/auction purchaser given any specific relief?

---

### ## KEY QUOTE — REQUIRED

The single most important sentence or short passage from the judgment — verbatim.
Under 40 words. In double quotes. No paraphrase.

If no single sentence captures the ratio, quote the sentence that will be most
useful when a lawyer cites this case in argument.

---

### ## CONDITION: WHEN THIS JUDGMENT APPLIES — REQUIRED

Write: "This judgment applies when:" followed by numbered conditions.

**⚠️ CRITICAL GUARDRAIL: Each condition MUST reference a CaseFactSchema
field name in backticks.** Plain English conditions without field names
result in `has_verified_conditions: false` and the judgment is never used
by the applicability engine.

**Complete list of available CaseFactSchema field names:**

M1 — Demand Notice:
`demand_notice_date` `demand_notice_amount` `actual_outstanding_amount`
`notice_service_mode` `notice_service_date` `notice_service_acknowledged`
`notice_dispatch_proof_present` `ao_has_written_authorization` `notice_content_complete`

M2 — Reply Compliance:
`objection_filed` `objection_date` `bank_reply_given` `bank_reply_date`
`bank_reply_gives_reasons` `bank_reply_addresses_objection`

M3 — Auction:
`possession_notice_date` `possession_taken_date` `possession_mode`
`sale_notice_date` `auction_date` `asset_type` `newspaper_publication_done`
`auction_type` `emd_stated_in_notice` `auction_notice_affixed_on_property`
`auction_conducted_despite_stay` `stay_was_operational_on_auction_date`
`auction_notice_discloses_pending_sa` `pending_sa_existed_at_auction_date`

M4 — Limitation:
`measure_date` `measure_type` `sa_filing_date` `days_from_measure_to_sa`
`previous_sa_filed` `previous_sa_number`

M5 — Tenancy:
`tenancy_claimed` `lease_date` `lease_registered` `lease_type`
`lease_duration_months` `mortgage_date` `lease_predates_mortgage`
`bank_noc_for_tenancy_given`

M6 — Valuation:
`valuation_report_present` `valuer_rbi_empanelled` `valuer_section_247_registered`
`valuation_date` `valuation_amount` `reserve_price` `second_valuation_done`
`valuation_challenged_by_borrower` `reserve_price_vs_valuation_pct`

M7 — Multi-party:
`total_borrowers_in_loan` `total_guarantors_in_loan`
`borrowers_served_notice` `guarantors_served_notice`

M8 — NPA Classification:
`date_of_last_payment` `npa_classification_date` `days_from_last_payment_to_npa`
`restructuring_proposal_pending` `loan_account_type` `payments_post_npa_total`
`account_standard_at_auction_date` `overdue_amount_at_auction_date`

M9 — MSME:
`msme_claimed_by_borrower` `udyam_cert_in_bank_file`
`udyam_registration_number` `restructuring_offered_pre_npa`

M10 — Third Party / Auction Purchaser:
`sa_applicant_type` `ats_date` `ats_advance_paid` `ats_registered`
`ats_possession_given` `ats_payments_made_to_loan_account`
`ats_predates_mortgage` `ats_simultaneous_mortgage`
`sale_certificate_issued` `sale_certificate_date` `sale_deed_executed`
`possession_given_to_auction_purchaser` `right_of_redemption_extinguished`
`balance_payment_date` `balance_consideration_paid_within_90_days`

Cross-cutting:
`drt_interim_stay_granted` `drt_stay_order_date` `ibc_moratorium_active`
`property_classification` `challenges_auction` `challenges_demand_notice`
`challenges_sale_notice` `prayer_scope_covers_current_measure`

**If this judgment requires a field not in this list:**
Write the condition in plain English AND add the field name to the
NEW REQUIREMENTS section below with the exact Python type.
Set `has_verified_conditions: false` until the field is added to the system.

**Condition format:**
```
This judgment applies when:
1. `field_name` is TRUE/FALSE/[value] — one sentence explaining the factual meaning
2. `field_name` is not null — explanation
3. `computed_field_name` is TRUE — note that this is a computed field
```

---

### ## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY — REQUIRED

Write "None" if there are no exclusions (rare).
Otherwise list the factual scenarios where this judgment would NOT apply —
specifically the opposite factual situation, or a narrower version of the facts.

This is important because many judgments appear similar but are distinguished
on specific facts. Stating the exclusion prevents the applicability engine
from citing this judgment in a case where Celir LLP or another judgment applies instead.

**For every exclusion, also state which judgment DOES apply in that scenario.**

---

### ## STATUTORY CONTEXT — REQUIRED

Write:
1. The name of the instrument (Act / Rules / Circular)
2. The section/rule number
3. The verbatim text of the provision (copy from the judgment itself — courts quote the statute)
4. Whether the word "shall" or "may" was key to the court's interpretation
5. Level: ACT / RULES / RBI / TPA / IBC
6. Nature: MANDATORY or DIRECTORY — as the court held

If the judgment does not quote the statute verbatim, use the exact statutory text
from memory / training — but mark it: `[text from training — verify against official source]`

---

### ## RELATIONSHIP TO OTHER JUDGMENTS — REQUIRED

For every judgment cited in this judgment that is relevant to SLRAI, write one entry:

```
Follows: [Citation] — [One sentence: what principle from that case was applied here]
Distinguishes: [Citation] — [One sentence: what factual difference makes it not apply here]
                             SLRAI ROUTING: if [field=value] → [that case applies];
                             if [opposite] → [this case applies]
Overruled: [Citation] — [What was overruled]
Affirmed: [Citation] — [What was affirmed]
```

**The SLRAI ROUTING note under Distinguishes is critical.**
When two judgments address the same type of dispute but lead to opposite outcomes,
the system needs to know exactly which field value routes to which judgment.
This prevents the system from citing the wrong precedent.

Example:
```
Distinguishes: Celir LLP v. Bafna Motors (2024) 2 SCC 1
  Celir LLP held that confirmed sale with timely payment has statutory finality.
  SLRAI ROUTING: if `balance_consideration_paid_within_90_days` = TRUE →
  Celir LLP applies (sale has finality); if FALSE → this judgment applies (sale inchoate).
```

---

### ## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES — REQUIRED

**This section is how the system evolves. Every judgment may bring something new.**
Fill this carefully. It is read by the system administrator to update the blueprint.

Sub-sections to fill:

**A. New CaseFactSchema Fields Needed**
If any condition you wrote references a field that is NOT in the CaseFactSchema
field list above, add it here with the exact Python type:
```
Field name: balance_consideration_paid_within_90_days
Type: FactEntry[bool]
Description: True if auction purchaser paid balance 75% within 90 days of auction (Rule 9(4) limit)
Computed from: (balance_payment_date - auction_date).days <= 90
Module: M10
```

**B. New YAML Rules Needed**
If this judgment establishes a principle that should become a compliance rule:
```
Module: M10
Rule ID: M10_C7_rule9_4_violation
Conditions: sale_certificate_issued=True AND balance_consideration_paid_within_90_days=False
Severity: FATAL
Judgment tag: [this judgment's short_name]
Statutory basis: RULES
```

**C. New Ground Codes Needed**
If the borrower's argument doesn't fit any existing ground code:
```
Suggested code: BALANCE_PAYMENT_DELAY
Description: Auction purchaser failed to pay balance 75% within 90 days per Rule 9(4)
Module: M3 or M10
```

**D. Existing Judgments to Update**
If this judgment distinguishes or relies on an existing Class A judgment,
note what needs to be added to that judgment's .md file:
```
File: celir_llp_bafna_motors.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add line: "Distinguished by: E. Muthurathinasabathy (2026) INSC 303 — held inchoate
sale (Rule 9(4) violated) does not follow Celir LLP's finality principle."
```

**E. No New Requirements**
If this judgment fits entirely within existing infrastructure, write:
```
No new fields, rules, or ground codes required. Fits within existing schema.
```

---

### ## WIN-RATE CONTRIBUTION — REQUIRED

```
favor: [copy from CLASSIFICATION above — BANK or BORROWER or NEUTRAL]
counted_in_ground: [the PRIMARY ground_code — first in your list]
```

This tells the statistics engine which win-rate counter to increment.
Only the primary ground_code is used for the count. Secondary codes are
used for retrieval only.

---

## COMPLETE GUARDRAILS CHECKLIST

Run this check before submitting your output.
Every item must be true. If any is false, fix it before outputting.

**Structure:**
☐ The output contains exactly the sections in the template — no additions, no omissions
☐ The YAML front matter opens with `---` and closes with `---`
☐ All markdown section headers use `##` exactly
☐ No section is empty — every section has content

**Ground codes:**
☐ `ground_codes` is NOT empty — at minimum `["UNKNOWN"]` if no code fits
☐ Every ground code used is from the valid values list above
☐ The primary (most relevant) ground code is listed first

**Conditions:**
☐ Every condition in WHEN THIS JUDGMENT APPLIES uses a backtick field name
☐ Every field name used is in the CaseFactSchema field list — or added to NEW REQUIREMENTS
☐ `has_verified_conditions` is `true` if all conditions use field names, `false` otherwise

**Content accuracy:**
☐ BORROWER'S CLAIM describes what the borrower argued — not what happened, not what court held
☐ HOLDING SUMMARY contains the legal rule only — no facts, no arguments
☐ HOLDING SUMMARY is 120-200 words — count and confirm
☐ KEY FACTS describes what happened — separate from the argument and the holding
☐ KEY QUOTE is verbatim, under 40 words, in double quotes

**Favor:**
☐ `favor` is set to the actual winner — not inferred from who "should" have won
☐ If court remanded: ask who got what they came for. Remand ≠ NEUTRAL by default
☐ If the case primarily upheld the bank's enforcement: `favor: "BANK"`
☐ If the case set aside enforcement: `favor: "BORROWER"`

**Relationships:**
☐ Every judgment this case distinguishes from has a SLRAI ROUTING note
☐ The SLRAI ROUTING note gives exact field name and value for routing logic

**New requirements:**
☐ Every field name in conditions that is NOT in the CaseFactSchema list is in NEW REQUIREMENTS
☐ If no new requirements: section explicitly says "No new fields, rules, or ground codes required"

**Keywords:**
☐ `keywords` has 5-10 entries
☐ Keywords are specific phrases — not generic terms like "SARFAESI" or "auction"
☐ Keywords are phrases a lawyer would actually write in an SA filing

**Retrieval condition:**
☐ `retrieval_condition` is present, under 200 characters, one sentence
☐ It names the actual fact pattern, not just the ground code or module name
☐ It is consistent with CONDITION: WHEN THIS JUDGMENT APPLIES and HOLDING SUMMARY's last sentence

---

## HOW TO HANDLE JUDGMENTS THAT DON'T FIT EXISTING CATEGORIES

Every significant SARFAESI judgment adds something to the system. Here is how to handle
the most common "doesn't fit" scenarios:

**Scenario A: The borrower raised a ground not in the ground_codes list**
Use `UNKNOWN` as the code. In NEW REQUIREMENTS, describe the new ground code needed,
what type of cases it covers, and which module it belongs to. Example: the E.
Muthurathinasabathy case exposed that "balance payment delay under Rule 9(4)" is a
distinct ground not captured by any existing code. The solution was to expand
`AUCTION_PURCHASER` and `RIGHT_OF_REDEMPTION` to cover it.

**Scenario B: The judgment requires a fact the system doesn't currently extract**
Write the condition in plain English AND flag it in NEW REQUIREMENTS with the exact
field name, type, and how it would be computed or extracted. Set
`has_verified_conditions: false` until the field is added. Do NOT invent a field name
that doesn't exist — explicitly flag it as missing.

**Scenario C: The judgment directly contradicts an existing Class A judgment's conditions**
In the RELATIONSHIP section, write a clear SLRAI ROUTING note that specifies exactly
which field value routes to which judgment. In NEW REQUIREMENTS, flag that the
contradicted judgment's file needs to be updated. The ingestion system administrator
will update both files before re-running compile_class_a_wiki.py.

**Scenario D: The judgment addresses a completely new area of law (TPA, IBC, stamp duty)**
Set `slrai_modules` appropriately (likely M10 for third-party scenarios, or the relevant
module). Set `statutory_basis` to TPA, IBC, or OTHER as appropriate. In NEW REQUIREMENTS,
note if the sarfaesi_law_wiki.md or third_party_law_wiki.md needs a new section for this
law to support the extraction context.

**Scenario E: The judgment is a HC judgment that contradicts an SC judgment**
The system applies judicial hierarchy: SC > HC > DRAT > DRT. Set `favor` based on the
outcome of THIS specific case. In RELATIONSHIP section, note which SC judgment this HC
judgment may be inconsistent with. The precedence resolver in Chain B will handle the
conflict. Do NOT try to resolve the conflict yourself in the summary.

**Scenario F: The judgment has multiple holdings (the "3 things in one case" problem)**
Split into multiple entries if the holdings are genuinely independent and would apply
to different types of future cases. Use the same citation with a suffix:
`short_name: "Kanaiyalal — Reply Obligation"` and `short_name: "Kanaiyalal — Limitation"`
if the same case addresses two completely separate issues with different conditions.
This keeps the applicability engine accurate — one set of conditions per judgment entry.

---

## EXAMPLE: E. MUTHURATHINASABATHY (2026)

Below is a complete correct output for the judgment you may have as a test case.
Use this to calibrate your output quality.

```markdown
---
# IDENTITY
citation: "2026 INSC 303"
title: "E. Muthurathinasabathy & Ors. v. M/s. Sri International & Ors."
short_name: "E. Muthurathinasabathy"
court: "SUPREME_COURT"
high_court_state: null
bench_strength: 2
judgment_date: "2026-04-01"
overruled: false
overruled_by: null
distinguished_by: []

# CLASSIFICATION
favor: "BORROWER"
favor_verified: true
ground_codes:
  - "RIGHT_OF_REDEMPTION"
  - "AUCTION_PURCHASER"
  - "AUCTION_GAP_DEFECT"
statutory_basis: "RULES"
act_sections:
  - "Section 13(8)"
rules_sections:
  - "Rule 9(4)"
  - "Rule 9(3)"

# SLRAI ROUTING
slrai_modules:
  - "M3"
  - "M10"
keywords:
  - "Rule 9(4)"
  - "balance consideration"
  - "outer limit three months"
  - "inchoate sale"
  - "right of redemption"
  - "statutory finality"
  - "15 days confirmation"
  - "balance 75%"
  - "delay completion sale"
retrieval_condition: "Applies when the auction purchaser paid the balance 75% of sale consideration more than 90 days after the auction date."

# SOURCE
source: "SC_FULL_TEXT"
ik_doc_id: ""
ik_url: "https://verdictum.in/2026/insc/303"
has_verified_conditions: false
---

## BORROWER'S CLAIM

The borrowers alleged that the e-auction conducted on 04.09.2020 never attained
statutory finality because the auction purchaser deposited the balance 75% of the
sale consideration only on 31.03.2022 — approximately 15 months after the auction —
far exceeding the maximum 90-day period prescribed by Rule 9(4) of the SARFAESI Rules.
They contended that a sale which fails to comply with the mandatory statutory payment
timeline is legally inchoate and cannot extinguish their right to redeem the
mortgaged property under Section 13(8) of the SARFAESI Act. They further alleged that
since they had fully discharged the entire outstanding dues of Rs. 3,89,31,614/-
during the pendency of proceedings, the bank was obligated to accept repayment and
release the secured assets.

## HOLDING SUMMARY

Rule 9(4) of the Security Interest (Enforcement) Rules, 2002 prescribes an absolute
mandatory outer limit of 90 days for the auction purchaser to deposit the balance sale
consideration. A sale that remains inchoate due to non-compliance with this timeline —
even if the delay was partly caused by judicial restraints — cannot defeat the
borrower's right to redeem the mortgaged property. When the statutory conditions for
vesting of title in the auction purchaser are never fulfilled within the mandatory
timeframe, the eventual issuance and registration of a sale certificate does not grant
absolute finality to the sale. The borrower's right of redemption under Section 13(8)
survives until a legally valid, fully completed sale extinguishes it. Celir LLP v.
Bafna Motors (2024) is distinguishable because that sale attained statutory finality
with timely payment and no judicial interdiction. This applies when: the balance
consideration was paid beyond the 90-day Rule 9(4) limit and the borrower has
discharged all outstanding dues in the interim.

## KEY FACTS OF THIS CASE

A partnership firm (M/s. Sri International) had availed credit facilities of Rs. 4
crore from Central Bank of India, secured by four commercial and residential properties.
The loan was classified NPA on 25.11.2018. After demand and possession notices, an
e-auction was conducted on 04.09.2020 in which the appellants emerged as the highest
bidders and deposited 25% of the bid amount. Due to serial interim orders from DRT,
DRAT, and the High Court, the balance 75% was not paid until 31.03.2022 — 15 months
after the auction — despite the High Court's 15.12.2020 order permitting the secured
creditor to accept the balance. During this period, the borrowers progressively
deposited amounts under court direction and fully discharged all dues. DRT and DRAT
both dismissed the SAs; the Madras High Court set aside the auction sale; the Supreme
Court affirmed the High Court.

## WHAT THE COURT DECIDED

The Supreme Court dismissed the appeals filed by the auction purchasers and the secured
creditor, holding the auction sale was legally inchoate for violating Rule 9(4)'s
mandatory 90-day payment deadline. The borrowers were entitled to redeem the mortgaged
properties by paying all outstanding dues. The registered sale certificates issued to
the auction purchasers were annulled, and the secured creditor was directed to release
the secured assets and return the title deeds. The auction purchasers were limited to
a refund of their deposited consideration with 12% interest per annum.

## KEY QUOTE

"A sale that remained inchoate in favour of the auction purchasers, owing to
non-compliance with mandatory timelines prescribed under Rule 9(4) of the 2002
Rules, cannot be invoked to defeat the right of the borrowers to redeem."

## CONDITION: WHEN THIS JUDGMENT APPLIES

[NOTE: Field `balance_consideration_paid_within_90_days` does not yet exist in
CaseFactSchema — see NEW REQUIREMENTS. Until added, has_verified_conditions=false]

This judgment applies when:
1. `sale_certificate_issued` is TRUE — a sale certificate was issued to the auction purchaser
2. `right_of_redemption_extinguished` is FALSE — borrower claims redemption right survives
3. `payments_post_npa_total` is greater than zero — borrower has made payments toward dues
4. [PENDING FIELD] `balance_consideration_paid_within_90_days` is FALSE — the auction
   purchaser failed to pay the balance 75% within the 90-day maximum under Rule 9(4)

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the auction purchaser paid the balance consideration within 90 days of the
   auction date — in that scenario, Celir LLP v. Bafna Motors (2024) applies and
   the sale has statutory finality.
   SLRAI ROUTING: `balance_consideration_paid_within_90_days = TRUE` → Celir LLP applies.

2. When the borrower has not tendered the outstanding dues at all — a bare challenge
   to the auction without payment does not attract this judgment's ratio.

3. When the right of redemption under Section 13(8) was extinguished before the Rule 9(4)
   deadline — e.g., borrower tendered after publication of auction notice (M. Rajendran
   (2025) interpretation) — see RELATIONSHIP section.

## STATUTORY CONTEXT

Primary law: Security Interest (Enforcement) Rules 2002
Primary provision: Rule 9(4) — "The balance amount of purchase price payable shall be
paid by the purchaser to the authorised officer on or before the fifteenth day of
confirmation of sale of the immovable property or such extended period as may be
agreed upon in writing between the parties, but in no case exceeding three months."
Instrument level: RULES
Nature of provision: MANDATORY — court confirmed the three-month outer limit is
absolute and cannot be exceeded regardless of judicial delays.

Secondary: Section 13(8) SARFAESI Act — borrower's right to redeem before
"date fixed for sale or transfer". Post-2016 amendment: redemption available
before date of publication of notice for public auction. Court held this right
survives when the sale never attained statutory finality within Rule 9(4) timelines.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Mathew Varghese v. M. Amritha Kumar (2014) 5 SCC 610
  Established that the right of redemption is a constitutional right protected
  under Article 300-A and survives until valid completion of sale by registered deed.

Distinguishes: Celir LLP v. Bafna Motors (2024) 2 SCC 1
  Celir LLP dealt with a sale that attained statutory finality — entire consideration
  paid within prescribed timeframe, sale certificate issued without judicial interdiction.
  This case involves a sale that never attained finality due to Rule 9(4) violation.
  SLRAI ROUTING: if `balance_consideration_paid_within_90_days` = TRUE → Celir LLP
  (sale has finality, set aside requires fraud/fundamental error); if FALSE → this
  judgment (sale inchoate, right of redemption survives).

Distinguishes: M. Rajendran v. KPK Oils (2025 SCC OnLine SC 2036)
  M. Rajendran addressed the curtailed redemption right under amended Section 13(8)
  where a valid completed auction concluded. Here the auction sale never validly
  completed due to Rule 9(4) violation — the Section 13(8) curtailment therefore
  did not bite.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: balance_payment_date
Type: FactEntry[date]
Description: Date when auction purchaser actually deposited the balance 75% of sale consideration
Module: M10
Extraction: Extract from bank records or auction purchaser's payment receipt in the SA

Field name: balance_consideration_paid_within_90_days
Type: FactEntry[bool]
Description: Computed — True if (balance_payment_date - auction_date).days <= 90
Computed from: balance_payment_date, auction_date
Module: M10

**B. New YAML Rule Needed:**
Module: M10
Rule ID: M10_C7_rule9_4_violation
Conditions: sale_certificate_issued=True AND balance_consideration_paid_within_90_days=False
Severity: FATAL
Message: "Auction purchaser paid balance consideration after Rule 9(4)'s 90-day
outer limit. The sale did not attain statutory finality. Borrower's right of
redemption was not extinguished."
Judgment tags: ["E_MUTHURATHINASABATHY", "MATHEW_VARGHESE"]
Statutory basis: RULES

**C. Existing Judgments to Update:**
File: celir_llp_bafna_motors.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: E. Muthurathinasabathy (2026 INSC 303) — held that a sale
where the auction purchaser failed to pay balance within Rule 9(4)'s 90-day outer
limit never attained statutory finality and does not attract Celir LLP's finality
principle."

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: RIGHT_OF_REDEMPTION
```
