---
citation: "2019 (2) SCC 198"
title: "M/S Hindon Forge Pvt. Ltd. vs The State Of Uttar Pradesh Thr. District Magistrate Ghaziabad & Anr."
short_name: "Hindon Forge"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2018-11-01"
overruled: false
overruled_by: null
distinguished_by: []
favor: BORROWER
favor_verified: true
ground_codes: ["POSSESSION_DEFECT", "NOTICE_ALL_PARTIES"]
statutory_basis: ACT
act_sections: ["Section 13(4)", "Section 17(1)"]
rules_sections: ["Rule 8(1)", "Rule 8(2)"]
slrai_modules: ["M3"]
keywords: ["symbolic possession", "constructive possession", "Rule 8(1)", "Rule 8(2)", "possession notice", "affixing notice", "newspaper publication", "actual physical possession", "measure under Section 13(4)", "right to approach DRT"]
retrieval_condition: "Applies when the secured creditor issued a possession notice under Rule 8(1) and published it under Rule 8(2), but did not take actual physical possession."
source: SC_FULL_TEXT
ik_doc_id: "80182706"
ik_url: "https://indiankanoon.org/doc/80182706/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers alleged that the remedy under Section 17(1) of the SARFAESI Act is available immediately upon the secured creditor taking measures under Section 13(4), including issuance of a possession notice under Rule 8(1) and its publication under Rule 8(2), even if actual physical possession is not taken. They contended that the Full Bench of the Allahabad High Court erred in holding that a borrower can only file an application under Section 17(1) after losing actual physical possession. They argued that the statutory scheme, including the Statement of Objects and Reasons and judicial precedents like Mardia Chemicals, supports the maintainability of a Section 17(1) application at the stage of symbolic or constructive possession. The prayer before the Supreme Court was to declare that a borrower can approach the Debts Recovery Tribunal under Section 17(1) upon issuance of a possession notice under Rule 8(1) and 8(2).

## HOLDING SUMMARY

Section 13(4) of the SARFAESI Act, read with Rule 8 of the Security Interest (Enforcement) Rules, 2002, provides that taking possession under Rule 8(1) and 8(2) constitutes a "measure" under Section 13(4), thereby triggering the right of the borrower to file an application under Section 17(1). The issuance of a possession notice delivered to the borrower and affixed on the property, coupled with its publication in two leading newspapers, amounts to statutory possession, whether symbolic or constructive, and does not require actual physical possession to be taken. The right to approach the Debts Recovery Tribunal crystallizes at this stage, ensuring the borrower has a prompt remedy against wrongful enforcement. This interpretation upholds the balance between the secured creditor's power to recover debts and the borrower's right to adjudication. This applies when: the secured creditor has issued a possession notice under Rule 8(1) and published it under Rule 8(2), thereby taking symbolic or constructive possession.

## KEY FACTS OF THIS CASE

The appellants, M/s Hindon Forge Pvt. Ltd., had availed credit facilities secured by immovable properties. Upon default, the secured creditor issued a demand notice under Section 13(2). After the 60-day period, the creditor issued a possession notice under Rule 8(1) and published it in newspapers as per Rule 8(2), claiming to have taken possession. However, no actual physical possession was taken. The borrowers filed an application under Section 17(1) before the DRT, which was dismissed on the ground that no actual physical possession had been taken. The Allahabad High Court, in a Full Bench decision, upheld that a Section 17(1) application is maintainable only after actual physical possession is taken. This appeal was filed to challenge that interpretation.

## WHAT THE COURT DECIDED

The Supreme Court allowed the appeals, set aside the impugned Full Bench judgment of the Allahabad High Court, and declared that a borrower can approach the Debts Recovery Tribunal under Section 17(1) of the SARFAESI Act at the stage when the secured creditor issues a possession notice under Rule 8(1) and publishes it under Rule 8(2), even if actual physical possession is not taken. The Court held that such an act constitutes a "measure" under Section 13(4), thereby triggering the borrower's right to seek relief.

## KEY QUOTE

Thus, the scheme of the provisions of Sections 13 and 17 of the Act, read with Rules 8 and 9 of the Rules, would show that the 'measure' taken under Section 13(4)(a) read with Rule 8 would not be complete unless actual (physical) possession of the secured assets is taken by the Bank/Financial Institutions.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when: the secured creditor has issued a possession notice under Rule 8(1) and published it under Rule 8(2), thereby taking symbolic or constructive possession.

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the secured creditor has taken actual physical possession of the secured asset — in that scenario, the Full Bench judgment of the Allahabad High Court applies, and the borrower's right to approach DRT is clearly established.
   SLRAI ROUTING: if `possession_mode` = "actual" → Full Bench Allahabad HC applies.

2. When the challenge is to the auction process or sale notice, and not to the taking of possession — in that case, judgments like *Canara Bank v. M. Amarender Reddy* govern the 30-day notice requirement under Rule 8(6).

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002
Primary provision: Section 13(4) — "In case the borrower fails to discharge his liability in full within the period specified in sub-section (2), the secured creditor may take recourse to one or more of the following measures to recover his secured debt, namely:— (a) take possession of the secured assets of the borrower including the right to transfer by way of lease, assignment or sale for realising the secured asset;"
Instrument level: ACT
Nature of provision: MANDATORY — the word "may" in Section 13(4) confers a power, but once exercised, the procedural safeguards under Section 17 become mandatory.

Secondary: Rule 8(1) and (2) of the Security Interest (Enforcement) Rules, 2002 — "Where the secured asset is an immovable property, the authorised officer shall take or cause to be taken possession, by delivering a possession notice... and by affixing the notice... The possession notice... shall also be published... in two leading newspapers."
Nature: MANDATORY — the procedure must be followed for lawful taking of possession.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Mardia Chemicals Ltd. v. Union of India (2004) 4 SCC 311
  Mardia Chemicals established that a borrower can approach the DRT under Section 17 only after measures under Section 13(4) are taken. This judgment clarifies that issuance of a possession notice under Rule 8(1) and 8(2) constitutes such a measure.

Distinguishes: Full Bench of Allahabad High Court in the same case
  The Full Bench held that only actual physical possession triggers Section 17(1). This judgment overrules that view.
  SLRAI ROUTING: if `possession_mode` = "actual" → Full Bench applies; if `possession_mode` = "symbolic" or "constructive" → this judgment applies.

Follows: ITC Limited v. Blue Coast Hotels Ltd. (2018) 8 SCC 632
  ITC Blue Coast recognized the concept of symbolic possession under SARFAESI. This judgment builds on that recognition to affirm the right to challenge at that stage.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: possession_mode
Type: FactEntry[str]
Description: The mode of possession taken by the secured creditor — "actual", "symbolic", or "constructive"
Module: M3
Extraction: Determined from whether physical entry occurred or only notice was issued.

**B. New YAML Rule Needed:**
Module: M3
Rule ID: M3_C1_symbolic_possession_triggers_17
Conditions: possession_notice_date is not null AND newspaper_publication_done = True
Severity: CRITICAL
Message: "Possession notice issued and published under Rule 8(1) and 8(2). Borrower's right to file under Section 17(1) has crystallized."
Judgment tag: ["Hindon Forge"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: full_bench_allahabad_hc.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Overruled by: Hindon Forge (2019) 2 SCC 198 — held that a borrower can file under Section 17(1) upon issuance of possession notice under Rule 8(1) and 8(2), even without actual physical possession."

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: POSSESSION_DEFECT
