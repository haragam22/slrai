---
citation: "2004 SCC (Cri) 1"
title: "Mardia Chemicals Ltd. Etc. Etc. vs U.O.I. & Ors. Mardia Chemicals Ltd. Etc. Etc. vs U.O.I. & Ors."
short_name: "Mardia Chemicals"
court: SUPREME_COURT
high_court_state: null
bench_strength: 3
judgment_date: "2004-04-08"
overruled: false
overruled_by: null
distinguished_by: []
favor: BORROWER
favor_verified: true
ground_codes: ["REPLY_NOT_GIVEN", "LIMITATION_EXPIRED", "UNKNOWN"]
statutory_basis: ACT
act_sections: ["Section 13", "Section 17", "Section 34"]
rules_sections: []
slrai_modules: ["M1", "M2", "M4"]
keywords: ["75% deposit", "pre-deposit condition", "Section 17(2)", "right to reply", "communication of reasons", "objection to demand notice", "natural justice", "Article 14", "ultra vires", "unconstitutional"]
retrieval_condition: "Applies when the borrower challenges the 75% pre-deposit requirement under Section 17(2) of the SARFAESI Act."
source: SC_FULL_TEXT
ik_doc_id: "1059476"
ik_url: "https://indiankanoon.org/doc/1059476/"
has_verified_conditions: false
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers challenged the constitutional validity of the SARFAESI Act, 2002, particularly Sections 13, 17, and 34. They contended that the Act granted arbitrary powers to secured creditors without providing an adjudicatory mechanism to resolve disputes regarding the correctness of the demand, validity of the debt, or classification of the account as an NPA. They argued that the requirement under Section 17(2) to deposit 75% of the claimed amount before filing an appeal was oppressive, unreasonable, and rendered the remedy illusory. They further alleged that the bar on civil court jurisdiction under Section 34, combined with the lack of a pre-action hearing, violated principles of natural justice and Article 14 of the Constitution.

## HOLDING SUMMARY

The Supreme Court upheld the constitutional validity of the SARFAESI Act, 2002, including Sections 13 and 34, recognizing the need for a speedy recovery mechanism to address mounting NPAs and serve public interest. However, the Court struck down Section 17(2) as violative of Article 14, holding that the mandatory pre-deposit of 75% of the claimed amount before entertaining an appeal was an unreasonable, arbitrary, and oppressive condition. The Court ruled that while no hearing is required before issuing a Section 13(2) notice, the secured creditor must consider any reply filed by the borrower and communicate the reasons for rejecting the objections. This communication is essential to ensure fairness and transparency, though it does not create a right to challenge the creditor's decision at that stage. This applies when: the borrower has filed a reply to the Section 13(2) notice and the secured creditor has failed to communicate reasons for rejecting the objections, or when the borrower is unable to comply with the 75% pre-deposit requirement under Section 17(2).

## KEY FACTS OF THIS CASE

Mardia Chemicals Ltd. and numerous other borrowers across India challenged the constitutional validity of the SARFAESI Act, 2002, after receiving demand notices under Section 13(2) from banks and financial institutions. The petitioners argued that the Act enabled unilateral enforcement of security without judicial intervention, depriving them of a fair opportunity to contest the debt or the classification of their accounts as NPAs. The central issue was the constitutionality of the 75% pre-deposit requirement under Section 17(2) and the absence of a pre-action adjudicatory mechanism. The case was heard by a three-judge bench of the Supreme Court, consolidating multiple writ petitions and transfer cases.

## WHAT THE COURT DECIDED

The Supreme Court upheld the validity of the SARFAESI Act, 2002, except for Section 17(2), which was declared unconstitutional and struck down for violating Article 14. The Court held that the secured creditor must consider the borrower's reply to the Section 13(2) notice and communicate the reasons for rejecting any objections. The Court clarified that the proceedings under Section 17 are not appellate but original, akin to a civil suit, and therefore the 75% pre-deposit condition was unreasonable. The appeals and writ petitions were partly allowed to the extent of striking down Section 17(2), and dismissed in all other respects.

## KEY QUOTE

The requirement of deposit of 75% of the amount claimed before entertaining an appeal (petition) under Section 17 of the Act is an oppressive, onerous and arbitrary condition against all the canons of reasonableness. Such a condition is invalid and it is liable to be struck down.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `objection_filed` is TRUE — the borrower filed a reply to the Section 13(2) notice
2. `bank_reply_given` is FALSE or `bank_reply_gives_reasons` is FALSE — the secured creditor did not respond or failed to provide reasons for rejecting the objections
3. `sa_filing_date` is within 45 days of the enforcement action — the borrower is filing a Section 17 application
4. `demand_notice_amount` is substantial — the 75% deposit would be a significant financial burden
5. `challenges_auction` or `challenges_demand_notice` is TRUE — the borrower is challenging enforcement action

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the borrower did not file any reply to the Section 13(2) notice — in such cases, the obligation to communicate reasons does not arise.
2. When the enforcement action is challenged solely on grounds of service defect or amount dispute without invoking the 75% deposit issue — other precedents like Kanaiyalal or AMR Investments may apply.
3. When the case involves a post-IBC scenario where Section 14 of IBC overrides SARFAESI enforcement — in such cases, IBC precedents like Innoventive Industries or Swiss Ribbons apply.

## STATUTORY CONTEXT

Primary law: Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002  
Primary provision: Section 17(2) — "Where an appeal is preferred by a borrower, such appeal shall not be entertained by the Debts Recovery Tribunal unless the borrower has deposited with the Debts Recovery Tribunal seventy-five per cent of the amount claimed in the notice referred to in sub-section (2) of section 13"  
Instrument level: ACT  
Nature of provision: MANDATORY — as originally enacted, but held unconstitutional by this judgment.

Secondary: Section 13(2) — requires 60-day notice before enforcement.  
Nature: MANDATORY — but no hearing required before notice.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: L. Chandrakumar v. Union of India (1997) 3 SCC 261  
  Affirmed the need for an adjudicatory mechanism to determine civil rights, especially when statutory actions affect fundamental rights.

Distinguishes: Kanaiyalal Lalchand Sachdev v. State of Maharashtra (2023) 4 SCC 1  
  Kanaiyalal dealt with the mandatory nature of the 13(3A) reply and remand for compliance. Mardia Chemicals addresses constitutional validity and the 75% deposit, not procedural compliance.  
  SLRAI ROUTING: if `objection_filed` = TRUE and `bank_reply_given` = FALSE → Kanaiyalal applies; if `75%_deposit_required` = TRUE → Mardia Chemicals applies.

Overruled: None  
Affirmed: Seth Nandlal v. State of Haryana (1980) Supp SCC 574  
  While Seth Nandlal upheld pre-deposit in land ceiling cases, Mardia Chemicals distinguished it on grounds of the nature of the proceeding (original vs. appeal) and the oppressive burden.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: bank_reply_gives_reasons  
Type: FactEntry[bool]  
Description: True if the secured creditor's reply to the borrower's objection under Section 13(3A) provides substantive reasons for rejection  
Computed from: bank_reply_content analysis  
Module: M2

Field name: bank_reply_addresses_objection  
Type: FactEntry[bool]  
Description: True if the bank's reply specifically responds to the points raised in the borrower's objection  
Module: M2

**B. New YAML Rules Needed:**
Module: M2  
Rule ID: M2_C1_reply_must_contain_reasons  
Conditions: objection_filed=True AND (bank_reply_given=False OR bank_reply_gives_reasons=False)  
Severity: FATAL  
Message: "Secured creditor failed to communicate reasons for rejecting borrower's objection as mandated in Mardia Chemicals. Violation of fair procedure."  
Judgment tag: ["Mardia Chemicals"]  
Statutory basis: ACT

**C. New Ground Codes Needed:**
Suggested code: PRE_DEPOSIT_UNCONSTITUTIONAL  
Description: Challenge to the 75% pre-deposit requirement under Section 17(2) as violative of Article 14  
Module: M4

**D. Existing Judgments to Update:**
File: kanaiyalal_lalchand_sachdev.md  
Section: ## RELATIONSHIP TO OTHER JUDGMENTS  
Add: "Distinguished by: Mardia Chemicals — Mardia Chemicals addresses constitutional validity of Section 17(2) and the duty to communicate reasons, while Kanaiyalal focuses on mandatory reply under Section 13(3A)."

**E. No New Requirements**  
No new fields, rules, or ground codes required. Fits within existing schema.

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: REPLY_NOT_GIVEN
