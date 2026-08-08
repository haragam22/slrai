---
citation: "2025 INSC 328"
title: "M/s Shri Sendhur Agro & Oil Industries vs Kotak Mahindra Bank Ltd"
short_name: "Shri Sendhur Agro"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2025-03-06"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["UNKNOWN"]
statutory_basis: RBI
act_sections: []
rules_sections: []
slrai_modules: []
keywords: []
retrieval_condition: "Applies when a borrower challenges the territorial jurisdiction of a Section 138 NI Act complaint filed in Chandigarh despite the bank's collection branch being located there."
source: SC_FULL_TEXT
ik_doc_id: "93179288"
ik_url: "https://indiankanoon.org/doc/93179288/"
has_verified_conditions: false
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower, M/s Shri Sendhur Agro & Oil Industries, alleged that the criminal complaint under Section 138 of the Negotiable Instruments Act, 1881, filed by Kotak Mahindra Bank in Chandigarh, was not maintainable due to lack of territorial jurisdiction. They contended that the entire transaction, including loan processing, EMI deductions, and SARFAESI proceedings, occurred in Coimbatore, Tamil Nadu, and that the bank's choice of Chandigarh was solely based on the location of its collection account, which was not a valid cause of action. The borrower further argued that this choice of forum was intended to harass them, as they would face significant hardship in attending proceedings in Chandigarh, including language barriers and travel difficulties. The prayer was to transfer the proceedings to Coimbatore.

## HOLDING SUMMARY

The Supreme Court held that the jurisdiction for a complaint under Section 138 of the Negotiable Instruments Act, 1881, is determined by Section 142(2) of the Act, which allows the complainant bank to file the complaint in the court within whose jurisdiction the branch where the cheque is delivered for collection through the payee's account is situated. The Court emphasized that the cause of action arises at the place of collection, not merely where the transaction occurred. The power under Section 406 of the CrPC to transfer cases is discretionary and must be exercised only when it is expedient for the ends of justice, which requires a reasonable apprehension of bias or a failure of justice, not mere inconvenience. The Court dismissed the transfer petition, upholding the bank's right to choose a forum based on the statutory jurisdiction provided by Section 142(2). This applies when: a borrower challenges the jurisdiction of a Section 138 complaint based on the location of the bank's collection branch.

## KEY FACTS OF THIS CASE

M/s Shri Sendhur Agro & Oil Industries, a proprietary concern based in Coimbatore, Tamil Nadu, availed an overdraft facility from Kotak Mahindra Bank's Coimbatore branch, secured by properties in Kangeyam, Tiruppur. The loan was processed, and EMIs were deducted from the borrower's account in Coimbatore. In 2018, the account was declared NPA, and the bank initiated SARFAESI proceedings in Coimbatore. Separately, the bank filed a criminal complaint under Section 138 of the NI Act in Chandigarh, where its collection account for the cheque was located. The borrower challenged the jurisdiction of the Chandigarh court, leading to a transfer petition before the Supreme Court.

## WHAT THE COURT DECIDED

The Supreme Court dismissed the transfer petition, holding that the Chandigarh court had valid jurisdiction under Section 142(2)(a) of the Negotiable Instruments Act, 1881, as the cheque was delivered for collection through an account maintained at the Chandigarh branch. The Court ruled that the mere inconvenience of the borrower in attending proceedings in Chandigarh did not constitute a "reasonable apprehension" of failure of justice required for a transfer under Section 406 of the CrPC. The proceedings in Chandigarh were allowed to continue.

## KEY QUOTE

Jurisdiction of a court to conduct criminal prosecution is based on the provisions of the Code of Criminal Procedure. Often either the complainant or the accused have to travel across an entire State to attend to criminal proceedings before a jurisdictional court.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when: a borrower challenges the jurisdiction of a Section 138 complaint based on the location of the bank's collection branch.

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the dispute is related to SARFAESI Act enforcement actions (demand notice, possession, auction) — in that scenario, judgments like Kanaiyalal or Celir LLP apply.
2. When the borrower is challenging the validity of the debt or the NPA classification — in that scenario, judgments like M. Rajendran or ITC Blue Coast apply.

## STATUTORY CONTEXT

Primary law: Negotiable Instruments Act, 1881
Primary provision: Section 142(2)(a) — "The offence under section 138 shall be inquired into and tried only by a court within whose local jurisdiction, — (a) if the cheque is delivered for collection through an account, the branch of the bank where the payee or holder in due course, as the case may be, maintains the account, is situated."
Instrument level: ACT
Nature of provision: MANDATORY — the court held that the jurisdiction is strictly determined by the location of the collection branch.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Kaushik Chatterjee v. State of Haryana (2020) 10 SCC 99 — Affirmed that mere inconvenience of the accused is not a valid ground for transfer of a criminal case.
Distinguishes: Dashrath Rupsingh Rathod v. State of Maharashtra (2014) 9 SCC 129 — This judgment was overruled by the 2015 amendment to Section 142, which now vests jurisdiction in the court where the payee's account is maintained, not where the cheque is dishonoured.
SLRAI ROUTING: if `ni_act_complaint_jurisdiction_challenged` = TRUE → this judgment applies; if `ni_act_complaint_jurisdiction_challenged` = FALSE → SARFAESI-specific judgments apply.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: ni_act_complaint_jurisdiction_challenged
Type: FactEntry[bool]
Description: True if the borrower is challenging the territorial jurisdiction of a Section 138 NI Act complaint
Module: Not applicable (NI Act context)
Computed from: Presence of grounds related to jurisdiction in the SA or transfer petition

Field name: collection_branch_location
Type: FactEntry[str]
Description: The location of the bank's branch where the cheque is delivered for collection
Module: Not applicable (NI Act context)
Extraction: From bank's complaint or transfer petition

**B. New YAML Rules Needed:**
Module: Not applicable
Rule ID: Not applicable
Conditions: Not applicable
Severity: Not applicable
Judgment tags: Not applicable
Statutory basis: ACT

**C. New Ground Codes Needed:**
Suggested code: NI_ACT_JURISDICTION_CHALLENGE
Description: Borrower challenging the territorial jurisdiction of a Section 138 NI Act complaint based on the location of the bank's collection branch
Module: Not applicable (NI Act context)

**D. Existing Judgments to Update:**
File: dashrath_rupsingh_rathod.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add line: "Overruled by: Shri Sendhur Agro (2025 INSC 328) — held that Section 142(2) of the NI Act, as amended in 2015, vests jurisdiction in the court where the payee's account is maintained, not where the cheque is dishonoured."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: UNKNOWN
