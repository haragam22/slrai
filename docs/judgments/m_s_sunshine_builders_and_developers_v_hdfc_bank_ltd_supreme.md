---
citation: "2025 INSC 10875"
title: "M/s Sunshine Builders and Developers v. HDFC Bank Limited through the Branch Manager & Ors."
short_name: "Sunshine Builders"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2025-04-17"
overruled: false
overruled_by: null
distinguished_by: []
favor: BORROWER
favor_verified: true
ground_codes: ["UNKNOWN"]
statutory_basis: ACT
act_sections: ["Section 18", "Section 17"]
rules_sections: []
slrai_modules: ["M1"]
keywords: ["pre-deposit", "Section 18", "appeal under Section 17", "implead auction purchaser", "procedural order", "no pre-deposit", "Section 2(1)(f)", "mortgagor as borrower"]
retrieval_condition: "Applies when a mortgagor challenges a procedural order (e.g., refusal to implead auction purchaser) and the High Court mandates pre-deposit under Section 18 without considering whether the order is 17"
source: SC_FULL_TEXT
ik_doc_id: "52635464"
ik_url: "https://indiankanoon.org/doc/52635464/"
has_verified_conditions: false
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower, M/s Sunshine Builders and Developers, alleged that the High Court erred in upholding the DRAT’s direction to deposit Rs. 125 crores as pre-deposit under Section 18 of the SARFAESI Act. They contended that the order challenged before the DRAT — the refusal to implead auction purchasers in the pending Securitisation Application — was a procedural interim order under Section 17 and did not determine substantive liability. They argued that Section 18’s pre-deposit requirement should not apply to such procedural appeals, and that the High Court failed to consider this distinction. The prayer was to set aside the pre-deposit condition and allow the appeal to proceed without financial burden.

## HOLDING SUMMARY

Section 18 of the SARFAESI Act mandates a pre-deposit of up to 50% of the claimed debt for appeals filed before the DRAT under Section 17, with a proviso allowing reduction to 25% at the tribunal’s discretion. However, the Supreme Court in this case has prima facie observed that the term "any order" under Section 18 must be interpreted meaningfully and not mechanically applied to all orders, especially procedural ones that do not determine substantive liability. The Court expressed concern that applying pre-deposit requirements to appeals against purely procedural orders — such as the refusal to implead a party — could defeat the very purpose of access to justice. It held that the High Court failed to consider whether the challenged order was of a nature that warranted pre-deposit under Section 18, and remanded the matter for reconsideration. This applies when: a mortgagor challenges a procedural order under Section 17 and the High Court imposes pre-deposit without examining the nature of the order.

## KEY FACTS OF THIS CASE

M/s Sunshine Builders and Developers had mortgaged properties to secure a loan from HDFC Bank, which later classified the account as NPA and initiated SARFAESI proceedings. A Securitisation Application (SA) under Section 17 was pending before the DRT, in which the appellant filed two interim applications — IA No. 183/2021 and IA No. 1652/2022 — seeking to implead auction purchasers in the proceedings. These applications were rejected by the DRT, and the appellant appealed to the DRAT. The DRAT directed a pre-deposit of Rs. 125 crores under Section 18, which was upheld by the Bombay High Court. The appellant challenged this before the Supreme Court, arguing that the pre-deposit should not apply to procedural appeals.

## WHAT THE COURT DECIDED

The Supreme Court set aside the impugned order of the Bombay High Court and remanded the matter for fresh consideration. It held that the High Court failed to examine whether the order refusing to implead auction purchasers was of a nature that warranted pre-deposit under Section 18. The Court directed the High Court to reconsider whether Section 18’s pre-deposit requirement applies to procedural orders under Section 17, and to decide the writ petition afresh. The appellant was granted liberty to approach the Supreme Court again if an adverse order is passed on remand.

## KEY QUOTE

We are of the view, of course prima facie that the expression 'any order' should be given some meaningful interpretation. Should any and every order that may be passed by DRT, if sought to be challenged, be made subject to pre-deposit?

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `sa_filing_date` is not null — a Securitisation Application is pending before the DRT
2. `interim_application_filed` is TRUE — borrower filed an interim application (e.g., to implead party)
3. `interim_application_rejected` is TRUE — DRT rejected the interim application
4. `appeal_against_interim_order` is TRUE — appeal filed before DRAT against procedural order
5. `pre_deposit_required_by_drat` is TRUE — DRAT or High Court imposed pre-deposit under Section 18
6. [PENDING FIELD] `order_type` is "procedural" — the challenged order does not determine substantive liability

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the appeal is against a final order determining the borrower’s liability or the validity of enforcement — in that case, Section 18 pre-deposit applies strictly per standard interpretation.
   SLRAI ROUTING: `order_type` = "final/substantive" → standard pre-deposit rules apply.

2. When the borrower is the principal debtor or guarantor and the appeal directly challenges debt quantification — this judgment’s nuance on mortgagor status does not override core pre-deposit obligations.

3. When no appeal is filed under Section 17 — this judgment only applies to challenges under Section 17 read with Section 18.

## STATUTORY CONTEXT

Primary law: The Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002  
Primary provision: Section 18(1) — "Any person aggrieved, by any order made by the Debts Recovery Tribunal under section 17, may prefer an appeal... Provided further that no appeal shall be entertained unless the borrower has deposited... fifty per cent. of the amount of debt due..."  
Instrument level: ACT  
Nature of provision: MANDATORY — but court questioned whether "any order" should be interpreted as mandatory across all contexts, especially procedural ones.

Secondary: Section 17 — allows filing of Securitisation Applications and appeals against DRT orders.  
Court examined whether interim procedural orders under Section 17 attract Section 18’s pre-deposit, suggesting a contextual reading.

## RELATIONSHIP TO OTHER JUDGMENTS

Distinguishes: Mardia Chemicals Ltd. v. Union of India (2004) 7 SCC 588  
  Mardia established procedural safeguards under SARFAESI but did not address pre-deposit for procedural appeals.  
  SLRAI ROUTING: if `appeal_against_interim_order` = TRUE → Sunshine Builders applies; if `appeal_against_final_order` = TRUE → Mardia framework applies.

Follows: V. Padmakumar v. Union of India (2017) 1 SCC 713  
  Reiterated that access to justice must not be fettered by mechanical interpretation of procedural bars.  
  This case applies similar reasoning to pre-deposit under Section 18.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: interim_application_filed
Type: FactEntry[bool]
Description: True if borrower filed an interim application in the SA (e.g., to implead party)
Module: M1
Extraction: From SA or writ petition filings

Field name: interim_application_rejected
Type: FactEntry[bool]
Description: True if DRT rejected the interim application
Module: M1

Field name: appeal_against_interim_order
Type: FactEntry[bool]
Description: True if appeal is against a procedural/interim order, not final determination
Module: M1

Field name: order_type
Type: FactEntry[str]
Description: "procedural" or "final" — nature of the DRT order challenged
Module: M1

**B. New YAML Rule Needed:**
Module: M1
Rule ID: M1_C8_section18_procedural_order_exception
Conditions: appeal_against_interim_order=True AND order_type="procedural"
Severity: WARNING
Message: "Section 18 pre-deposit may not apply to procedural orders. Court in Sunshine Builders (2025) remanded where High Court mechanically applied pre-deposit to appeal against refusal to implead auction purchaser."
Judgment tag: ["Sunshine_Builders"]
Statutory basis: ACT

**C. New Ground Codes Needed:**
Suggested code: PRE_DEPOSIT_CHALLENGE
Description: Borrower challenges the applicability of Section 18 pre-deposit to a procedural appeal under Section 17
Module: M1

**D. Existing Judgments to Update:**
File: mardia_chemicals.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Sunshine Builders (2025 INSC 10875) — held that pre-deposit under Section 18 may not apply to appeals against procedural orders such as refusal to implead parties."

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: UNKNOWN
