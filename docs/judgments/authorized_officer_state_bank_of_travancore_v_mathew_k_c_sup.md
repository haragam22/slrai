---
citation: "2018 (3) SCC 85"
title: "Authorized Officer, State Bank Of Travancore And Another v. Mathew K.C."
short_name: "Mathew K.C."
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2018-01-30"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["SERVICE_DEFECT"]
statutory_basis: ACT
act_sections: ["Section 13(2)", "Section 13(3A)", "Section 13(4)", "Section 17"]
rules_sections: []
slrai_modules: ["M1", "M2"]
keywords: ["Section 17", "alternate remedy", "Article 226", "interim stay", "writ petition", "Section 13(4)", "Section 13(3A)", "maintainability", "natural justice"]
retrieval_condition: "Applies when the borrower files a writ petition under Article 226 to challenge SARFAESI proceedings despite the availability of an effective alternate remedy under Section 17."
source: SC_FULL_TEXT
ik_doc_id: "28622663"
ik_url: "https://indiankanoon.org/doc/28622663/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower alleged that the bank failed to consider his genuine request for loan account regularisation and that the SARFAESI proceedings were unjust due to market fluctuations beyond his control. He contended that the principles of natural justice were violated as the bank did not properly consider his objections under Section 13(3A). He further argued that the collateral included agricultural land, which should be excluded under Section 31 of the SARFAESI Act. The prayer before the High Court was to stay further proceedings under Section 13(4) of the SARFAESI Act upon deposit of Rs. 3,50,000.

## HOLDING SUMMARY

The Supreme Court reaffirmed that the SARFAESI Act provides a complete code for recovery of non-performing assets, with an efficacious alternate remedy under Section 17 before the Debt Recovery Tribunal. A writ petition under Article 226 of the Constitution is not maintainable merely to challenge the initiation of SARFAESI proceedings when an effective statutory remedy is available. The High Court erred in granting interim relief without recording special reasons or considering the availability of the Section 17 remedy. The mere allegation of violation of natural justice without specific pleading or prejudice does not justify bypassing the statutory mechanism. This applies when: a borrower files a writ petition under Article 226 to stall SARFAESI enforcement despite the availability of an effective alternate remedy under Section 17.

## KEY FACTS OF THIS CASE

The borrower had availed a loan facility which was declared NPA on 28.12.2014, with outstanding dues of Rs. 41,82,560. A Section 13(2) demand notice was issued on 21.01.2015, and objections under Section 13(3A) were rejected on 31.03.2015. The bank issued a possession notice under Section 13(4) read with Rule 8 of the SARFAESI Rules on 21.04.2015. The borrower filed a writ petition under Article 226 before the Kerala High Court, which granted interim stay of proceedings upon deposit of Rs. 3,50,000. The Division Bench declined to interfere, prompting the bank to appeal to the Supreme Court.

## WHAT THE COURT DECIDED

The Supreme Court set aside the impugned interim orders of the High Court and allowed the appeal. It held that the writ petition was not maintainable due to the availability of an efficacious alternate remedy under Section 17 of the SARFAESI Act. The Court directed that all questions of law and fact remain open for determination before the statutory forum under the SARFAESI Act. The bank was permitted to proceed with enforcement actions under Section 13(4).

## KEY QUOTE

The High Court ought not to have entertained the writ petition in view of the adequate alternate statutory remedies available to the Respondent.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `challenges_auction` is FALSE — the borrower is not challenging auction but earlier stages
2. `challenges_demand_notice` is TRUE — the borrower challenges initiation of SARFAESI proceedings
3. `previous_sa_filed` is FALSE — no prior SA under Section 17 has been filed
4. `drt_interim_stay_granted` is FALSE — no interim stay from DRT
5. `ibc_moratorium_active` is FALSE — no IBC moratorium in force
6. `prayer_scope_covers_current_measure` is TRUE — the prayer seeks to stay current SARFAESI measure
7. `sa_applicant_type` is "Borrower" — the applicant is the borrower, not a third party

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the borrower has already filed an application under Section 17 before the DRT — in that case, the DRT has jurisdiction and the writ petition is not maintainable, but the issue is governed by procedural law rather than this precedent.
   SLRAI ROUTING: if `previous_sa_filed` = TRUE → this judgment does not apply; DRT jurisdiction established.

2. When the action is taken in violation of fundamental principles of natural justice with specific pleading and prejudice — in such cases, the exception to alternate remedy applies and the High Court may entertain the writ petition.
   SLRAI ROUTING: if `objection_filed` = TRUE AND `bank_reply_gives_reasons` = FALSE → consider jurisdiction under natural justice exceptions.

3. When the SARFAESI action involves agricultural land exclusively — Section 31 may bar enforcement, making the alternate remedy ineffective.
   SLRAI ROUTING: if `property_classification` = "Agricultural Land" → check Section 31 applicability; this judgment may not apply.

## STATUTORY CONTEXT

Primary law: SARFAESI Act 2002
Primary provision: Section 17 — "Any person (including the borrower), aggrieved by the action of the authorised officer under Section 13(4) may make an application to the Debts Recovery Tribunal."
Instrument level: ACT
Nature of provision: MANDATORY — the statute creates an exclusive alternate remedy.

Secondary: Section 13(4) — "If the borrower fails to discharge his liabilities within 60 days, the secured creditor may take possession of the secured asset."
Instrument level: ACT
Nature: MANDATORY — triggers enforcement rights.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: United Bank of India v. Satyawati Tandon (2010) 8 SCC 110
  Reaffirmed that writ petitions under Article 226 are not maintainable when an efficacious alternate remedy under Section 17 is available.

Follows: General Manager, Sri Siddeshwara Cooperative Bank v. Ikbal (2013) 10 SCC 83
  Applied the principle that SARFAESI proceedings cannot be circumvented by filing writ petitions.

Distinguishes: Punjab National Bank v. Imperial Gift House (2013) 14 SCC 622
  Both cases hold that writ petitions are not maintainable, but Imperial Gift House involved quashing of proceedings, whereas here interim stay was granted. SLRAI ROUTING: if `prayer_scope_covers_current_measure` = TRUE → Mathew K.C. applies; if seeking quashing → Imperial Gift House applies.

Affirmed: Kanaiyalal Lalchand Sachdev v. State of Maharashtra (2011) 2 SCC 782
  Reiterated that availability of Section 17 remedy bars writ jurisdiction under Article 226.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: challenges_demand_notice
Type: FactEntry[bool]
Description: True if borrower challenges the initiation of SARFAESI proceedings under Section 13(2)/(3A)
Module: M1

Field name: challenges_auction
Type: FactEntry[bool]
Description: True if borrower challenges auction proceedings under Section 13(4)/Rule 8
Module: M3

**B. New YAML Rules Needed:**
Module: M1
Rule ID: M1_C1_writ_during_sarfaesi
Conditions: challenges_demand_notice=True AND previous_sa_filed=False AND drt_interim_stay_granted=False
Severity: FATAL
Message: "Borrower has filed writ petition under Article 226 despite availability of efficacious alternate remedy under Section 17. Writ not maintainable."
Judgment tag: ["Mathew_K_C"]
Statutory basis: ACT

**C. No New Requirements**
No new ground codes or major schema changes required. Existing infrastructure sufficient.

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: SERVICE_DEFECT
