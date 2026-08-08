---
citation: "(2026) ibclaw.in 47 DRAT"
title: "Anil Ankush Pawar and Anr. v. The Authorized Officer, Union Bank of India and Ors."
short_name: "Anil Ankush Pawar"
court: HIGH_COURT
high_court_state: "Maharashtra"
bench_strength: 2
judgment_date: "2026-03-04"
overruled: false
overruled_by: null
distinguished_by: []
favor: BORROWER
favor_verified: true
ground_codes: ["AUCTION_PURCHASER"]
statutory_basis: ACT
act_sections: ["Section 18"]
rules_sections: []
slrai_modules: ["M10"]
keywords: ["Section 18", "pre-deposit waiver", "interim relief", "blanket interim direction", "procedural infirmity", "DRAT order", "auction purchaser rights", "revenue record change", "third party interest"]
retrieval_condition: "Applies when the DRAT granted interim relief restraining auction purchasers from creating third-party interest or changing revenue records while only deciding a pre-deposit waiver application under S "
source: HC_FULL_TEXT
ik_doc_id: "157729275"
ik_url: "https://indiankanoon.org/doc/157729275/"
has_verified_conditions: false
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The petitioners, who were auction purchasers, alleged that the DRAT committed a serious procedural irregularity by granting interim relief in an order that was limited to deciding an application for waiver of pre-deposit under Section 18 of the SARFAESI Act. They contended that the DRAT, without hearing them or considering the standard parameters for interim relief — such as prima facie case, balance of convenience, and irreparable injury — issued a blanket direction restraining them from creating third-party interests or effecting changes in revenue records. They argued that such relief could not be granted without a separate adjudication on the pending application for interim relief, and that the impugned order caused them prejudice by unlawfully restricting their rights as registered auction purchasers.

## HOLDING SUMMARY

The High Court held that the DRAT committed a serious procedural infirmity by granting interim relief to the original borrowers in an order that was confined to deciding only their application for waiver of pre-deposit under Section 18 of the SARFAESI Act. The Court emphasized that interim relief cannot be granted as a matter of course upon the direction of pre-deposit; instead, it must be adjudicated separately after considering the established legal parameters — including existence of a prima facie case, balance of convenience, and risk of irreparable injury. The DRAT’s failure to conduct such an inquiry rendered the interim direction legally unsustainable. The Court clarified that even though the appeal was not yet formally numbered, the pre-deposit direction alone did not entitle the borrowers to automatic interim protection. The impugned direction restraining the auction purchasers from creating third-party interests or altering revenue records was quashed on this limited ground. This applies when: interim relief is granted by the DRAT without a dedicated hearing or reasoning, while only adjudicating a pre-deposit waiver application.

## KEY FACTS OF THIS CASE

The petitioners were auction purchasers who acquired the secured asset through a SARFAESI auction conducted by Union Bank of India. The original borrowers (Respondent Nos. 2 and 3) filed an appeal before the DRAT challenging the DRT’s dismissal of their delayed Securitization Application. They also filed an application seeking waiver of pre-deposit under Section 18 of the SARFAESI Act and a separate application for interim relief. On 14th May 2025, the DRAT rejected the waiver application and directed the borrowers to deposit 40% of the claimed amount, but in the same order, without any reasoning, restrained the auction purchasers from creating third-party interests or changing revenue records upon deposit. The auction purchasers challenged this direction in a writ petition before the Bombay High Court, which found the interim relief to be procedurally flawed and set it aside.

## WHAT THE COURT DECIDED

The Bombay High Court quashed the interim direction issued by the DRAT that restrained the auction purchasers from creating third-party interests or effecting changes in revenue records. The Court held that the direction was procedurally infirm as it was issued without a dedicated hearing or consideration of the necessary legal parameters for interim relief. The Court directed the DRAT to take up the pending application for interim relief on 2nd April 2026 and decide it within two weeks, after hearing all parties. The remainder of the DRAT’s order — directing pre-deposit — was left undisturbed.

## KEY QUOTE

We find that the approach of the DRAT is unsustainable. It appears that the DRAT proceeded on an assumption that the moment a pre-deposit direction was issued... the interim relief would follow as a matter of course.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `challenges_auction` is TRUE — the original borrower is challenging the auction
2. `application_for_interim_relief_pending` is TRUE — a formal application for interim relief is pending before DRAT/DRT
3. `interim_relief_granted_without_hearing` is TRUE — interim relief was granted without a dedicated hearing on the application
4. `interim_relief_granted_in_predeposit_order` is TRUE — the interim direction was issued in an order primarily dealing with pre-deposit under Section 18
5. `reasons_for_interim_relief_absent` is TRUE — the order does not record any reasoning on prima facie case, balance of convenience, or irreparable injury

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the interim relief was granted after a full hearing and detailed reasoning on the application for interim relief — in such cases, the DRAT’s order is valid and this judgment does not apply.
   SLRAI ROUTING: if `interim_relief_granted_after_hearing` = TRUE → standard interim relief jurisprudence applies.

2. When the auction purchaser has not yet been issued a sale certificate or taken possession — in such cases, the purchaser’s rights are not yet crystallized and different principles (e.g., inchoate rights) may apply.

3. When the DRAT or DRT has not granted any interim relief at all — this judgment only applies where such relief was improperly granted, not where it was merely sought.

## STATUTORY CONTEXT

Primary law: Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002  
Primary provision: Section 18 — "Every appeal under this section shall be filed within forty-five days... and the Appellate Tribunal may, if it is satisfied that the appellant was prevented by sufficient cause from filing the appeal within that period, allow it to be filed within a further period of sixty days. Provided that no appeal shall be admitted unless the appellant has deposited, in the manner prescribed, fifty per cent of the amount of debt as determined by the Appellate Tribunal or such amount not exceeding twenty-five per cent as may be specified by the Central Government."

Instrument level: ACT  
Nature of provision: MANDATORY — the pre-deposit requirement is mandatory, but the Court held that it does not automatically entitle the appellant to interim relief.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: M. Rajendran v. KPK Oils (2025 SCC OnLine SC 2036)  
  Reaffirms that procedural fairness and adherence to due process are essential in DRAT proceedings, especially when rights of third parties like auction purchasers are affected.

Distinguishes: Celir LLP v. Bafna Motors (2024) 2 SCC 1  
  Celir LLP dealt with the finality of a completed auction where full payment was made. This case concerns interim orders affecting auction purchasers during appeal, not the substantive validity of the sale.  
  SLRAI ROUTING: if `interim_relief_granted_without_hearing` = TRUE → Anil Ankush Pawar applies; if `balance_consideration_paid_within_90_days` = TRUE → Celir LLP applies.

Affirmed: Mathew Varghese v. M. Amritha Kumar (2014) 5 SCC 610  
  Implicitly supports the principle that rights of auction purchasers, once crystallized, must be protected unless set aside through proper legal process.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: application_for_interim_relief_pending
Type: FactEntry[bool]
Description: True if the borrower has filed an application for interim relief before DRAT/DRT that is still pending
Module: M10
Extraction: Check SA or appeal records for filing of interim relief application

Field name: interim_relief_granted_without_hearing
Type: FactEntry[bool]
Description: True if interim relief was granted without a dedicated hearing on the application
Module: M10

Field name: interim_relief_granted_in_predeposit_order
Type: FactEntry[bool]
Description: True if the interim direction was issued in an order primarily deciding a pre-deposit or waiver application
Module: M10

Field name: reasons_for_interim_relief_absent
Type: FactEntry[bool]
Description: True if the order granting interim relief does not record reasoning on prima facie case, balance of convenience, or irreparable injury
Module: M10

**B. New YAML Rule Needed:**
Module: M10
Rule ID: M10_C8_illegal_interim_relief
Conditions: interim_relief_granted_in_predeposit_order=True AND reasons_for_interim_relief_absent=True
Severity: FATAL
Message: "Interim relief was granted in a pre-deposit order without hearing or reasoning. This constitutes a procedural infirmity under Anil Ankush Pawar (2026). The direction is legally unsustainable."
Judgment tag: ["ANIL_ANKUSH_PAWAR"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: celir_llp_bafna_motors.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Anil Ankush Pawar (2026) ibclaw.in 47 DRAT — held that interim relief granted without hearing in a pre-deposit order is procedurally infirm; does not affect the finality of sale under Celir LLP."

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: AUCTION_PURCHASER
