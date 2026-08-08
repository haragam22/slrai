---
citation: "(2016) 12 SCC 18"
title: "Axis Bank v. SBS Organics Private Limited and Another"
short_name: "Axis Bank v. SBS Organics"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2016-04-22"
overruled: false
overruled_by: null
distinguished_by: []
favor: BORROWER
favor_verified: true
ground_codes: ["REPLY_NOT_GIVEN"]
statutory_basis: ACT
act_sections: ["Section 18", "Section 17", "Section 13(10)"]
rules_sections: ["Rule 11"]
slrai_modules: ["M2"]
keywords: ["Section 18 deposit", "fifty per cent deposit", "refund of deposit", "pre-deposit for appeal", "withdrawal of appeal", "Section 13(10)", "Rule 11", "lien on deposit", "entertain appeal"]
retrieval_condition: "Applies when the borrower deposited 50% of the debt for appeal under Section 18 but the appeal became infructuous or was withdrawn and no appropriation order was passed."
source: SC_FULL_TEXT
ik_doc_id: "64381220"
ik_url: "https://indiankanoon.org/doc/64381220/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower(s) alleged that the deposit made before the DRAT under Section 18 of the SARFAESI Act for the purpose of entertaining their appeal was not a secured asset and did not create any security interest in favour of the bank. They contended that since the appeal had become infructuous and they had sought withdrawal, the deposit must be refunded unconditionally. They further argued that the bank had no right to appropriate the deposit towards the borrower's dues in the absence of an express order or consent, and that the bank's claim of lien under Section 171 of the Indian Contract Act was inapplicable as the deposit was with the tribunal, not with the bank. The prayer before the Supreme Court was to direct the refund of the Rs. 50 lakh deposit made before the DRAT.

## HOLDING SUMMARY

Section 18 of the SARFAESI Act mandates a pre-deposit of 50% (or 25% if reduced by the DRAT) of the debt as a condition for the Appellate Tribunal to entertain an appeal against a DRT order under Section 17. This deposit is not a secured asset, nor does it create a security interest in favour of the secured creditor. The deposit remains with the tribunal and is not subject to the bank's lien under Section 171 of the Indian Contract Act, as it is not a bailment to the bank. Upon withdrawal, dismissal, or the appeal becoming infructuous, the deposit must be refunded to the depositor unless (i) the tribunal has passed an order appropriating the amount with the depositor’s consent, (ii) the amount has been attached in proceedings under Section 13(10) read with Rule 11, or (iii) there is a valid attachment under any other law. The purpose of the deposit is to prevent frivolous appeals, not to create a recoverable asset for the bank. This applies when: the borrower made a Section 18 deposit, the appeal was withdrawn or became infructuous, and no appropriation or attachment order exists.

## KEY FACTS OF THIS CASE

Axis Bank initiated SARFAESI proceedings against SBS Organics Pvt. Ltd. for default in repayment. The borrower challenged the enforcement measures before the DRT, Ahmedabad, under Section 17. After the DRT vacated interim relief, the borrower filed an appeal before the DRAT under Section 18, depositing Rs. 50 lakhs as required by the proviso to Section 18(1). During the pendency of the appeal, the DRT disposed of the original Securitisation Application by setting aside the sale. Realizing the appeal had become infructuous, the borrower sought to withdraw it and requested a refund of the deposit. The DRAT permitted withdrawal but made it subject to the result of the appeal. The borrower then approached the Gujarat High Court, which directed unconditional refund. The bank appealed to the Supreme Court, which dismissed the appeal and upheld the refund.

## WHAT THE COURT DECIDED

The Supreme Court dismissed the appeal filed by Axis Bank and upheld the Gujarat High Court’s order directing the unconditional refund of the Rs. 50 lakh deposit made under Section 18. The Court held that the deposit was not a secured asset, did not create a security interest, and was not subject to the bank’s lien. In the absence of any order of appropriation, attachment under Section 13(10), or consent, the deposit must be refunded to the borrower upon withdrawal or when the appeal becomes infructuous. The dismissal was without prejudice to the bank’s right to pursue recovery of the balance amount under Section 13(10) read with Rule 11.

## KEY QUOTE

On disposal of the appeal, either on merits or on withdrawal, or on being rendered infructuous, in case, the appellant makes a prayer for refund of the pre-deposit, the same has to be allowed and the pre-deposit has to be returned to the appellant.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `objection_filed` is TRUE — borrower filed an appeal before DRAT under Section 18
2. `objection_date` is not null — date of filing the DRAT appeal is known
3. `bank_reply_given` is FALSE — bank did not file a reply opposing refund (implied by withdrawal)
4. `bank_reply_gives_reasons` is FALSE — no reasons given against refund
5. `previous_sa_filed` is TRUE — original Securitisation Application was filed under Section 17
6. `measure_type` is "SECTION_18_APPEAL" — the measure in question is an appeal under Section 18
7. `sa_applicant_type` is "BORROWER" — the applicant is the borrower
8. `prayer_scope_covers_current_measure` is TRUE — the prayer includes refund of deposit
9. `drt_interim_stay_granted` is FALSE — no stay was operational at time of withdrawal
10. `balance_consideration_paid_within_90_days` is FALSE — not applicable, but used to distinguish from auction purchaser cases

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the DRAT has passed an order appropriating the deposit with the borrower’s consent — in that case, the bank may retain the amount. SLRAI ROUTING: if `bank_reply_gives_reasons` = TRUE AND `objection_filed` = FALSE → appropriation applies.

2. When the deposit has been attached in proceedings under Section 13(10) read with Rule 11 — the bank may recover the shortfall. SLRAI ROUTING: if `pending_sa_existed_at_auction_date` = TRUE → Section 13(10) attachment applies.

3. When the appeal is dismissed on merits (not withdrawn or infructuous) — the deposit may be adjusted only with consent or by order. SLRAI ROUTING: if `objection_filed` = TRUE AND `objection_date` is within 30 days of DRT order → merits dismissal applies.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002
Primary provision: Section 18(1) — "No appeal shall be entertained unless the borrower has deposited with the Appellate Tribunal fifty per cent of the amount of debt due from him, as claimed by the secured creditors or determined by the Debts Recovery Tribunal, whichever is less."
Instrument level: ACT
Nature of provision: MANDATORY — the deposit is a condition precedent to the tribunal entertaining the appeal.

Secondary: Section 13(10) and Rule 11 — allow recovery of shortfall from borrower after sale.
Nature: MANDATORY — but only after sale proceeds are insufficient.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Mardia Chemicals v. Union of India (2004) 4 SCC 311
  Confirmed that Section 17 proceedings are quasi-judicial and allow evidence, but Section 18 is a true appeal.

Follows: Lakshmi Rattan Engineering Works Ltd. v. Asst. Commissioner Sales Tax (1968) AIR SC 488
  Interpreted "entertain" as "admit to consideration", reinforcing that deposit is for admission, not recovery.

Distinguishes: Babu Ganesh Singh Deepnarayan v. Union of India (2009) AIR Guj. 98
  Gujarat High Court in Babu Ganesh held that deposit must be refunded if appeal is dismissed — this judgment affirms and extends that principle to withdrawn/infructuous appeals.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: section_18_deposit_made
Type: FactEntry[bool]
Description: True if borrower deposited 50% (or 25%) of debt before DRAT under Section 18
Module: M2
Extraction: From DRAT records or SA annexures

Field name: section_18_deposit_refund_claimed
Type: FactEntry[bool]
Description: True if borrower has claimed refund of Section 18 deposit
Module: M2
Extraction: From SA prayer or written submissions

**B. New YAML Rule Needed:**
Module: M2
Rule ID: M2_C8_section_18_refund
Conditions: section_18_deposit_made=True AND objection_filed=False AND bank_reply_given=False
Severity: WARNING
Message: "Borrower made Section 18 deposit but appeal withdrawn/infructuous. Refund likely unless appropriation/attachment order exists."
Judgment tag: ["AXIS_BANK_V_SBS_ORGANICS"]
Statutory basis: ACT

**C. No New Ground Codes Needed**
 The issue fits under "REPLY_NOT_GIVEN" as the bank failed to respond to the refund claim with valid grounds.

**D. Existing Judgments to Update:**
File: babu_ganesh_singh_deepnarayan.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Followed by: Axis Bank v. SBS Organics (2016) 12 SCC 18 — affirmed that Section 18 deposit must be refunded when appeal is withdrawn or infructuous."

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: REPLY_NOT_GIVEN
