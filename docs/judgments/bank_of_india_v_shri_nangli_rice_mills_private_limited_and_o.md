---
citation: "2025 INSC 765"
title: "Bank Of India vs M/S Sri Nangli Rice Mills Pvt. Ltd."
short_name: "Bank of India v. Sri Nangli Rice Mills"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2025-05-23"
overruled: false
overruled_by: null
distinguished_by: []
favor: BORROWER
favor_verified: true
ground_codes: ["THIRD_PARTY_ATS"]
statutory_basis: ACT
act_sections: ["Section 11"]
rules_sections: []
slrai_modules: ["M10"]
keywords: ["Section 11 SARFAESI", "inter-bank dispute", "arbitration between banks", "statutory arbitration", "no DRT jurisdiction", "non-payment of amount due", "dispute between secured creditors", "priority of charge", "hypothecation vs pledge", "deemed arbitration agreement"]
retrieval_condition: "Applies when a dispute over priority of security interest arises between two banks concerning non-payment of dues by a common borrower."
source: SC_FULL_TEXT
ik_doc_id: "187283529"
ik_url: "https://indiankanoon.org/doc/187283529/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The appellant bank (Bank of India) contended that it had a prior charge by way of hypothecation over the stocks of paddy and rice of the borrower, having sanctioned credit facilities as early as 2003, and that the respondent bank (Punjab National Bank) had created a subsequent charge by way of pledge in 2013 without verifying the existence of the prior charge. It argued that the Debt Recovery Tribunal (DRT) had jurisdiction to adjudicate the priority of charges between two secured creditors and that Section 11 of the SARFAESI Act did not apply, particularly because the respondent bank’s charge was by pledge, which is excluded under Section 31(b) of the Act. The appellant further contended that no written arbitration agreement existed between the banks, and that the dispute was maintainable before the DRT under Section 17.

## HOLDING SUMMARY

Section 11 of the SARFAESI Act mandates that any dispute relating to securitisation, reconstruction, or non-payment of any amount due, including interest, arising amongst banks, financial institutions, asset reconstruction companies, or qualified buyers, shall be settled by arbitration or conciliation under the Arbitration and Conciliation Act, 1996. The provision creates a statutory arbitration mechanism, deeming an arbitration agreement to exist between the specified parties even in the absence of a written agreement, as indicated by the phrase "as if the parties... have consented in writing". The term "non-payment of any amount due" includes disputes between secured creditors over priority of charge arising from a borrower's default. The use of "shall" makes Section 11 mandatory, ousting the jurisdiction of the DRT. This applies when a dispute over the priority of security interest arises between two banks concerning the non-payment of dues by a common borrower.

## KEY FACTS OF THIS CASE

Bank of India (appellant) had sanctioned a credit facility to M/s Sri Nangli Rice Mills (borrower) in 2003, secured by hypothecation of stocks of paddy and rice. The borrower defaulted in 2015, and the account was classified as NPA. Bank of India issued a Section 13(2) demand notice for Rs. 62.10 crore and took symbolic possession. It was then discovered that Punjab National Bank (respondent) had also created a charge over the same stocks by way of pledge in 2013, with National Bulk Handling Corporation as collateral manager. A dispute arose between the two banks over the priority of their charges. The DRT initially allowed Bank of India's SA, but the DRAT remanded it, holding Section 17 not maintainable. On remand, the DRT held it lacked jurisdiction and directed the parties to arbitration under Section 11. The High Court upheld this, leading to the present appeal.

## WHAT THE COURT DECIDED

The Supreme Court dismissed the appeal, holding that the dispute between Bank of India and Punjab National Bank over the priority of their security interests, arising from the borrower's non-payment of dues, fell squarely within the ambit of Section 11 of the SARFAESI Act. The Court ruled that Section 11 provides for mandatory statutory arbitration between secured creditors, creating a deemed arbitration agreement, and ousts the jurisdiction of the DRT. The Court affirmed the High Court's order directing the parties to resolve their dispute through arbitration.

## KEY QUOTE

Section 11 of the SARFAESI Act, provides for a statutory arbitration for any dispute mentioned therein between any of the parties enumerated thereunder. There is no need for an explicit written agreement to arbitrate between such parties in order to attract Section 11 of the SARFAESI Act.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `sa_applicant_type` is "SECURED_CREDITOR" — the applicant in the Securitisation Application is another bank, financial institution, ARC, or qualified buyer
2. `challenges_auction` is FALSE — the dispute is not about the auction process but about the underlying rights
3. `prayer_scope_covers_current_measure` is TRUE — the relief sought pertains to the enforcement of security interest
4. `measure_type` is "POSSESSION" or "AUCTION" — the measure challenged is possession or auction of the asset
5. `previous_sa_filed` is TRUE — a prior SA has been filed, indicating an ongoing enforcement process
6. `tenancy_claimed` is FALSE — the dispute does not involve a tenant or lessee
7. `msme_claimed_by_borrower` is FALSE — the borrower is not claiming MSME status
8. `restructuring_proposal_pending` is FALSE — there is no pending restructuring proposal
9. `ibc_moratorium_active` is FALSE — no IBC moratorium is in effect
10. `property_classification` is "MOVABLE" — the secured asset in dispute is movable property (e.g., stocks)

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the dispute is between a secured creditor and the borrower — in that case, the borrower can challenge the enforcement under Section 17, and the DRT has jurisdiction. SLRAI ROUTING: if `sa_applicant_type` = "BORROWER" → standard SARFAESI challenge applies.

2. When one of the parties, though a bank or financial institution, is acting in the capacity of a borrower — Section 11 does not apply to disputes between a lender and a borrower, even if the borrower is a financial entity. SLRAI ROUTING: if `sa_applicant_type` = "BORROWER" and the respondent is a secured creditor → borrower's challenge under Section 17 applies.

3. When the dispute pertains to the enforcement of a pledge — Section 31(b) excludes pledges from the SARFAESI Act, and thus Section 11 may not apply to disputes solely about pledge rights. SLRAI ROUTING: if `asset_type` = "PLEDGE" → dispute falls outside SARFAESI framework.

## STATUTORY CONTEXT

Primary law: Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002
Primary provision: Section 11 — "Where any dispute relating to securitisation or reconstruction or non-payment of any amount due including interest arises amongst any of the parties, namely, the bank or financial institution or asset reconstruction company or qualified buyer, such dispute shall be settled by conciliation or arbitration as provided in the Arbitration and Conciliation Act, 1996, as if the parties to the dispute have consented in writing for determination of such dispute by conciliation or arbitration and the provisions of that Act shall apply accordingly."
Instrument level: ACT
Nature of provision: MANDATORY — the use of "shall" and the legislative intent to create a special mechanism for inter-creditor disputes make the provision mandatory.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Transcore v. Union of India (2008) 1 SCC 125
  Confirmed that Section 11 deals with inter-se disputes between secured creditors, not between a secured creditor and a borrower.

Distinguishes: Federal Bank Ltd. v. LIC Housing Finance Ltd. (2010) SCC OnLine DRAT 138
  Federal Bank held that a written arbitration agreement is required for Section 11 to apply. This judgment overrules that view, holding that Section 11 creates a statutory arbitration with a deemed agreement. SLRAI ROUTING: if `bank_arbitration_agreement_exists` = TRUE → Federal Bank may be cited; if FALSE → this judgment applies (statutory arbitration without written agreement).

Affirms: Oriental Bank of Commerce v. Canara Bank (2011) SCC OnLine DRAT 8
  Affirmed the principle that inter-bank disputes over secured assets must be resolved by arbitration under Section 11, not by DRT adjudication.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: sa_applicant_type
Type: FactEntry[str]
Description: The type of party filing the Securitisation Application (e.g., BORROWER, SECURED_CREDITOR, GUARANTOR)
Module: M10
Extraction: Determined from the identity and role of the applicant in the SA

**B. New YAML Rule Needed:**
Module: M10
Rule ID: M10_C8_section11_inter_creditor_dispute
Conditions: sa_applicant_type="SECURED_CREDITOR" AND challenges_auction=False
Severity: FATAL
Message: "Dispute is between secured creditors over priority of charge. DRT has no jurisdiction. Matter must be referred to arbitration under Section 11 of SARFAESI Act."
Judgment tag: ["Bank_of_India_v_Sri_Nangli_Rice_Mills"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: federal_bank_ltd_v_lic_housing_finance_ltd.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Bank of India v. Sri Nangli Rice Mills (2025 INSC 765) — held that Section 11 of SARFAESI Act creates a statutory arbitration mechanism and does not require a written arbitration agreement between the parties."

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: THIRD_PARTY_ATS
