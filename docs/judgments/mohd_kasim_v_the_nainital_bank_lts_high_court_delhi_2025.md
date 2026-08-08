---
citation: "(2025) 208 DLT 459"
title: "Mohd. Kasim vs The Nainital Bank Ltd & Anr"
short_name: "Mohd. Kasim"
court: HIGH_COURT
high_court_state: "Delhi"
bench_strength: 2
judgment_date: "2025-06-04"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["AUCTION_DURING_STAY", "REPLY_NOT_GIVEN", "NOTICE_ALL_PARTIES"]
statutory_basis: ACT
act_sections: ["Section 13(2)", "Section 13(4)", "Section 17"]
rules_sections: []
slrai_modules: ["M3", "M2"]
keywords: ["OTS terms", "demonetization delay", "bonafide auction purchaser", "status quo during appeal", "abuse of process", "revocation of OTS", "set aside auction", "legitimate expectation", "equitable relief"]
retrieval_condition: "Applies when the borrower failed to complete OTS payment despite multiple extensions and the DRT set aside a legally conducted auction during pending appeal."
source: HC_FULL_TEXT
ik_doc_id: "94547050"
ik_url: "https://indiankanoon.org/doc/94547050/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower alleged that the auction sale of his residential property was invalid because it was conducted while an appeal was pending before the DRAT and the auction purchaser was aware of ongoing litigation. He contended that the bank unilaterally withdrew the One Time Settlement (OTS) despite his substantial compliance, including payment of Rs. 2.15 crores and eventual clearance of the remaining Rs. 35 lakhs with interest, citing demonetization as a valid reason for delay. He further argued that the bank’s conduct violated the doctrine of legitimate expectation and that the DRT had the power to set aside the auction due to the bank’s arbitrary actions. The prayer before the High Court was to uphold the DRT’s order setting aside the auction and direct the bank to refund the auction amount.

## HOLDING SUMMARY

A borrower who defaults on a legally binding One Time Settlement (OTS) agreement cannot later challenge enforcement proceedings under SARFAESI when the bank revokes the settlement in accordance with its terms. The DRT lacks jurisdiction to set aside a legally conducted auction merely on equitable grounds when the borrower has repeatedly defaulted and failed to challenge the validity of initial SARFAESI notices. While Article 226 allows equitable relief, courts must not override statutory recovery mechanisms to reward defaulters, especially when public interest and financial discipline are at stake. The DRT’s order setting aside an auction conducted during pending litigation, without finding procedural illegality, constitutes an overreach of its powers. This applies when: the borrower failed to honor OTS timelines despite multiple extensions and the DRT set aside a valid auction without statutory basis.

## KEY FACTS OF THIS CASE

Mohd. Kasim had taken loans from The Nainital Bank Ltd., secured by two properties. After default, the account was declared NPA and a Section 13(2) notice was issued on 03.10.2013. The borrower approached the DRT, which ordered repayment by 31.03.2016. Upon failure, the bank took possession. The borrower later sought an OTS, which the bank conditionally accepted on 30.07.2016 for Rs. 2.50 crores, with Rs. 2.15 crores due within 30 days and the balance within 90 days. The first part was paid, but the remaining Rs. 35 lakhs were delayed due to demonetization. The bank revoked the OTS on 24.02.2017 and re-initiated SARFAESI proceedings. An auction was conducted on 07.07.2017 in favor of Respondent No. 2. The DRT later set aside the auction, but the DRAT reversed it. The High Court upheld the DRAT’s decision.

## WHAT THE COURT DECIDED

The Delhi High Court dismissed the writ petition challenging the DRAT’s order, affirming that the auction sale was legally valid and could not be set aside by the DRT on equitable grounds. The court held that the borrower had repeatedly defaulted, failed to challenge initial SARFAESI actions, and could not claim protection under OTS after breach. The DRT’s interference with a completed auction, absent procedural illegality, was found to be an overreach. The bank was entitled to proceed with recovery, and the auction purchaser was entitled to possession.

## KEY QUOTE

Any other approach would render the High Court a normal Court of Appeal, which it is not.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `previous_sa_filed` is TRUE — the borrower had already filed a prior SA which ended in a binding repayment order
2. `restructuring_offered_pre_npa` is TRUE — the bank offered an OTS after NPA classification
3. `bank_reply_given` is FALSE — the borrower did not file a formal objection under Section 13(3A)
4. `objection_filed` is TRUE — the borrower filed a second SA after defaulting on OTS
5. `auction_conducted_despite_stay` is FALSE — no formal stay was in force, but litigation was pending
6. `prayer_scope_covers_current_measure` is TRUE — the SA sought to set aside auction despite no specific challenge to revocation of OTS

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the bank accepted delayed payments and explicitly extended the OTS deadline in writing — in such cases, revocation may be unjustified and *Ambience Pvt. Ltd. v. Punjab & Sind Bank* applies.
   SLRAI ROUTING: if `ots_extended_in_writing` = TRUE → Ambience applies; if FALSE → this judgment applies.

2. When the borrower successfully completed all OTS payments within agreed timelines — in that case, the bank’s revocation would be arbitrary and *SBI v. Vijay Kumar* applies.

3. When the auction was conducted in violation of a formal court stay order — in that scenario, *Celir LLP v. Bafna Motors* applies and the sale is void.

## STATUTORY CONTEXT

Primary law: Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002
Primary provision: Section 17(1) — "Any person (including the borrower), aggrieved by any of the measures taken by the authorised officer under sub-section (4) of Section 13, may file an application before the DRT..."
Instrument level: ACT
Nature of provision: MANDATORY — the right to file under Section 17 is conditional on being "aggrieved" by measures under Section 13(4), and such grievance must be timely and legally valid.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: M.S. Sanjay v. Indian Bank (2025 SCC OnLine SC 368)
  Reinforces that Article 226 relief is discretionary and courts must balance equity with public interest in financial recovery.

Distinguishes: Ambience Pvt. Ltd. v. Punjab & Sind Bank (2014) 208 DLT 459
  Ambience held that legitimate expectation arises when a bank makes a clear promise. Here, the OTS was conditional and revoked for default.
  SLRAI ROUTING: if `ots_breached_by_borrower` = TRUE → Mohd. Kasim applies; if FALSE → Ambience applies.

Distinguishes: SBI v. Vijay Kumar (2007) 11 SCC 369
  SBI v. Vijay Kumar protected substantial performance under settlement. Here, the borrower failed to meet deadlines and cheques were dishonored — performance was not substantial.

Affirmed: P. D’Souza v. Shondrilo Naidu (2004) 6 SCC 649
  While estoppel may apply in commercial settlements, it does not override SARFAESI enforcement when the borrower defaults on agreed terms.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: ots_offered_post_npa
Type: FactEntry[bool]
Description: True if the bank offered an OTS after NPA classification
Module: M8

Field name: ots_breached_by_borrower
Type: FactEntry[bool]
Description: True if borrower failed to meet OTS payment deadlines despite reminders
Module: M8

**B. New YAML Rules Needed:**
Module: M8
Rule ID: M8_C1_ots_breach_revival
Conditions: ots_offered_post_npa=True AND ots_breached_by_borrower=True AND sa_filing_date > npa_classification_date
Severity: FATAL
Message: "Borrower defaulted on OTS terms after NPA classification. Bank entitled to revive SARFAESI proceedings."
Judgment tags: ["Mohd_Kasim"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: ambience_pvt_ltd_punjab_sind_bank.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Mohd. Kasim (2025) 208 DLT 459 — held that legitimate expectation does not survive borrower’s breach of OTS terms."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: AUCTION_DURING_STAY
