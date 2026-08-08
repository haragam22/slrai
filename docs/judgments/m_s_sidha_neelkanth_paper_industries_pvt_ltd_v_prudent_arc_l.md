---
citation: "2023 INSC 12"
title: "Sidha Neelkanth Paper Industries Private Limited & Another v. Prudent ARC Limited & Others"
short_name: "Sidha Neelkanth"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2023-01-05"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["SECOND_SA_FRESH_CAUSE"]
statutory_basis: ACT
act_sections: ["Section 18", "Section 13(2)"]
rules_sections: []
slrai_modules: ["M2"]
keywords: ["Section 18 pre-deposit", "50% debt due", "adjustment of auction proceeds", "borrower cannot blow hot and cold", "debt due includes interest"]
retrieval_condition: "Applies when the borrower challenges the auction sale and seeks to adjust auction proceeds towards the Section 18 pre-deposit requirement."
source: SC_FULL_TEXT
ik_doc_id: "197077609"
ik_url: "https://indiankanoon.org/doc/197077609/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers alleged that the requirement to deposit 50% of the "debt due" under Section 18 of the SARFAESI Act should be waived or reduced because the auction purchaser had already deposited the full sale consideration of Rs. 12.5 crores, which exceeded 50% of the original debt of Rs. 16.61 crores. They contended that the amount realised from the sale of the secured asset should be adjusted or appropriated towards the pre-deposit obligation, thereby discharging their liability to make any further payment. They further argued that the "debt due" for the purpose of Section 18 should exclude future interest and be calculated after deducting amounts recovered through auction.

## HOLDING SUMMARY

Section 18 of the SARFAESI Act mandates that a borrower must deposit 50% of the "debt due" as claimed by the secured creditor or determined by the DRT, whichever is less, to file an appeal before the DRAT. The term "debt" under Section 2(ha) of the SARFAESI Act incorporates the definition from Section 2(g) of the RDDB Act, 1993, which includes both principal and interest. The borrower cannot claim adjustment of auction proceeds towards the pre-deposit if they are simultaneously challenging the validity of the auction sale. The Supreme Court held that allowing such adjustment would permit the borrower to "blow hot and cold" — contesting the sale while benefiting from its proceeds — which is impermissible. The pre-deposit requirement is jurisdictional and cannot be waived merely because the secured asset has been sold. This applies when: the borrower challenges the auction sale and seeks to use the auction proceeds to satisfy the Section 18 pre-deposit obligation.

## KEY FACTS OF THIS CASE

Sidha Neelkanth Paper Industries Pvt. Ltd. had availed credit facilities from Andhra Bank, secured by immovable properties. The account was declared NPA, and a Section 13(2) demand notice was issued for Rs. 16.61 crores. After possession and auction, M/s Tejswi Impex Pvt. Ltd. purchased the Delhi property for Rs. 12.5 crores, and the sale certificate was issued. The borrower challenged the enforcement before the DRT and later appealed to the DRAT. The DRAT, relying on the auction proceeds, waived the pre-deposit. The secured creditor challenged this before the Delhi High Court, which partially upheld the waiver. Both parties appealed to the Supreme Court. A similar issue arose in Madhya Pradesh cases involving Bank of Baroda and auction purchasers.

## WHAT THE COURT DECIDED

The Supreme Court allowed the appeals filed by the secured creditor and auction purchasers, setting aside the High Courts' directions to adjust auction proceeds towards the Section 18 pre-deposit. It dismissed the borrower’s appeal and held that the borrower must deposit 50% of the "debt due" as claimed in the Section 13(2) notice, including interest, without adjusting the auction proceeds. The Court clarified that the DRAT has no power to grant a full waiver and may reduce the deposit to 25% only upon recording reasons. No costs were awarded.

## KEY QUOTE

The borrower cannot be allowed blow hot and cold. In a case where the borrower also challenges the auction sale and does not accept the same and also challenges the steps taken under Section 13(2)/13(4) of the SARFAESI Act with respect to secured assets, the borrower has to deposit 50% of the amount claimed by the secured creditor along with interest.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when: the borrower challenges the auction sale and seeks to use the auction proceeds to satisfy the Section 18 pre-deposit obligation.

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the borrower accepts the auction sale and does not challenge its validity — in that case, the principle of pre-deposit may be revisited on grounds of equity, but this judgment does not govern.
   SLRAI ROUTING: if `challenges_auction` = FALSE → this judgment does not apply.

2. When the auction sale itself is void due to procedural defects (e.g., no notice, during stay) — in such cases, the sale is invalid ab initio, and the borrower may argue against pre-deposit on different grounds.
   SLRAI ROUTING: if `auction_conducted_despite_stay` = TRUE → Kanaiyalal or other stay violation precedents apply.

3. When the applicant is not the borrower but a third-party purchaser or guarantor — the "blow hot and cold" principle is specific to borrowers.
   SLRAI ROUTING: if `sa_applicant_type` ≠ "BORROWER" → this judgment does not apply.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002  
Primary provision: Section 18 — "No appeal shall be entertained unless the borrower has deposited with the Appellate Tribunal fifty per cent. of the amount of debt due from him, as claimed by the secured creditors or determined by the Debts Recovery Tribunal, whichever is less."  
Secondary: Section 2(ha) — defines "debt" to mean as per Section 2(g) of the RDDB Act, 1993  
Tertiary: Section 2(g) RDDB Act — "debt means any liability (inclusive of interest) which is claimed as due from any person..."  
Level: ACT  
Nature: MANDATORY — the deposit is a jurisdictional requirement; non-compliance bars the DRAT from entertaining the appeal.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Eskays Construction Pvt. Ltd. v. Soma Papers & Industries Ltd. (2016 SCC OnLine Bom 9827)  
  Held that auction proceeds cannot be adjusted towards pre-deposit if the borrower challenges the sale. Supreme Court affirmed this reasoning and dismissed SLP, giving it binding effect.  
  SLRAI ROUTING: if `challenges_auction` = TRUE → Eskays Construction applies; if FALSE → borrower may seek adjustment.

Follows: Axis Bank v. SBS Organics Private Limited (2016) 12 SCC 18  
  Reaffirmed that pre-deposit under Section 18 is for bona fides and to prevent frivolous litigation, and the amount is refundable. Supports the mandatory nature of the deposit.

Distinguishes: Shilpa Shares and Securities v. National Cooperative Bank Ltd. (SLP(C) No. 14717/2022, decided 21.11.2022)  
  That case held that amounts deposited pursuant to Supreme Court orders cannot be adjusted towards pre-deposit. This judgment extends the principle to auction proceeds when sale is challenged.  
  SLRAI ROUTING: if payment source is court-ordered deposit → Shilpa Shares applies; if auction proceeds → this judgment applies.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**  
Field name: challenges_auction  
Type: FactEntry[bool]  
Description: True if the borrower's SA explicitly challenges the validity of the auction sale  
Module: M3  
Extraction: From SA prayer and grounds — e.g., "set aside auction", "sale void", "no valid sale"

**B. New YAML Rule Needed:**  
Module: M2  
Rule ID: M2_C5_predeposit_auction_conflict  
Conditions: sa_applicant_type="BORROWER" AND challenges_auction=True AND balance_consideration_paid_within_90_days=True  
Severity: FATAL  
Message: "Borrower cannot claim adjustment of auction proceeds towards Section 18 pre-deposit while challenging the auction sale. Pre-deposit of 50% of debt due (including interest) is mandatory."  
Judgment tag: ["Sidha_Neelkanth", "Eskays_Construction"]  
Statutory basis: ACT

**C. Existing Judgments to Update:**  
File: eskays_construction_soma_papers.md  
Section: ## RELATIONSHIP TO OTHER JUDGMENTS  
Add: "Affirmed by: Sidha Neelkanth (2023 INSC 12) — Supreme Court upheld the principle that auction proceeds cannot be adjusted towards pre-deposit if borrower challenges the sale."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: SECOND_SA_FRESH_CAUSE
