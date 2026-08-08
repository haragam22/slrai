---
citation: "2017 (16) SCC 137"
title: "International Asset Reconstruction Company of India Ltd. v. The Official Liquidator of Aldrich Pharmaceuticals Ltd. and Others"
short_name: "IARC India Ltd."
court: SUPREME_COURT
high_court_state: null
bench_strength: 3
judgment_date: "2017-10-24"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["LIMITATION_EXPIRED"]
statutory_basis: ACT
act_sections: ["Section 30(1)"]
rules_sections: []
slrai_modules: ["M4"]
keywords: ["Section 30(1)", "30 days appeal", "condonation of delay", "Section 5 Limitation Act", "RDB Act appeal"]
retrieval_condition: "Applies when an appeal under Section 30(1) of the RDB Act is filed beyond the 30-day period and condonation is sought under Section 5 of the Limitation Act."
source: SC_FULL_TEXT
ik_doc_id: "85389016"
ik_url: "https://indiankanoon.org/doc/85389016/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers or aggrieved parties contended that the delay in filing an appeal under Section 30(1) of the RDB Act beyond the 30-day period should be condoned under Section 5 of the Limitation Act, 1963. They argued that the RDB Act is not a complete code and does not expressly exclude the applicability of Section 5, and that principles of natural justice and fairness support the condonation of delay. They further contended that Section 24 of the RDB Act, read with Rule 2(c), allows for the extension of time for filing applications, including appeals, and that the Tribunal has inherent powers to condone delay to secure the ends of justice.

## HOLDING SUMMARY

Section 30(1) of the Recovery of Debts and Bankruptcy Act, 1993 (RDB Act) prescribes a mandatory 30-day period for filing an appeal against an order of the Recovery Officer, and this period cannot be extended by invoking Section 5 of the Limitation Act, 1963. The Supreme Court held that the RDB Act is a complete and self-contained code for the expeditious recovery of debts, and the Legislature has made a conscious choice to exclude the applicability of Section 5 to proceedings before the Tribunal under Section 30(1). While Section 20(3) of the RDB Act allows condonation of delay for appeals before the Appellate Tribunal, no such power is conferred upon the Tribunal for appeals filed under Section 30(1). The definition of "application" under Section 2(b) and Section 24 is limited to proceedings under Section 19, and Rule 2(c) cannot be read to extend this to Section 30(1) appeals. This applies when: an appeal under Section 30(1) is filed beyond 30 days and the party seeks condonation under Section 5 of the Limitation Act.

## KEY FACTS OF THIS CASE

The case arose from appeals filed under Section 30(1) of the RDB Act beyond the 30-day statutory period. The Recovery Officer had passed orders under Section 28 of the RDB Act following a recovery certificate issued by the Tribunal. The aggrieved parties filed appeals before the Tribunal after the 30-day deadline and sought condonation of delay under Section 5 of the Limitation Act. The Tribunal rejected the appeals as time-barred. The matter reached the Supreme Court via special leave petitions, raising a common question of law on the applicability of Section 5 of the Limitation Act to Section 30(1) appeals. The appeals were filed by secured creditors and asset reconstruction companies.

## WHAT THE COURT DECIDED

The Supreme Court dismissed the appeals, holding that the 30-day period under Section 30(1) of the RDB Act is mandatory and cannot be extended by invoking Section 5 of the Limitation Act. The Court ruled that the RDB Act is a special and complete code, and the Legislature has not conferred power on the Tribunal to condone delay in filing appeals under Section 30(1). The Court also clarified that Section 24 of the RDB Act applies only to applications under Section 19, not to appeals under Section 30(1).

## KEY QUOTE

The RDB Act is undoubtedly a special law and a complete code by itself with regard to expeditious recovery of dues to banks and financial institutions.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `measure_type` is "Section 30(1) appeal" — the proceeding is an appeal under Section 30(1) of the RDB Act
2. `sa_filing_date` is after `measure_date` plus 30 days — the appeal is filed beyond the 30-day limitation period
3. `bank_reply_given` is FALSE or `bank_reply_gives_reasons` is FALSE — the bank or Tribunal has not condoned the delay
4. `prayer_scope_covers_current_measure` is TRUE — the borrower seeks condonation of delay under Section 5 of the Limitation Act

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the appeal is filed under Section 20 of the RDB Act before the Appellate Tribunal — in that case, the proviso to Section 20(3) allows condonation of delay for sufficient cause.
   SLRAI ROUTING: if `measure_type` = "Section 20 appeal" → Section 20(3) applies (delay condonable); if `measure_type` = "Section 30(1) appeal" → this judgment applies (delay not condonable).

2. When the delay is in filing an application under Section 19 of the RDB Act — Section 24 of the RDB Act allows for condonation in such cases.
   SLRAI ROUTING: if `measure_type` = "Section 19 application" → Section 24 applies; if `measure_type` = "Section 30(1) appeal" → this judgment applies.

## STATUTORY CONTEXT

Primary law: Recovery of Debts and Bankruptcy Act, 1993 (RDB Act)  
Primary provision: Section 30(1) — "Notwithstanding anything contained in Section 29, any person aggrieved by an order of the Recovery Officer made under this Act may, within thirty days from the date on which a copy of the order is issued to him, prefer an appeal to the Tribunal."  
Instrument level: ACT  
Nature of provision: MANDATORY — the 30-day period is strict and not subject to condonation under Section 5 of the Limitation Act.

Secondary: Section 5, Limitation Act, 1963 — allows condonation of delay in filing appeals or applications if sufficient cause is shown.  
Court held: Not applicable to Section 30(1) appeals as the RDB Act is a complete code and excludes implied application of Section 5.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Sakuru vs. Tanaji (1985) 3 SCC 590  
  Held that Section 5 of the Limitation Act applies only to proceedings in courts, not to quasi-judicial tribunals unless expressly provided. This judgment applies the same principle to the RDB Tribunal.

Distinguishes: A.R. Venugopal @ R. Venugopal vs. Jotheeswaran (2015)  
  That two-Judge Bench held delay under Section 30(1) could be condoned. This judgment overrules that view, holding that the entire statutory scheme was not considered in that case.  
  SLRAI ROUTING: if `precedent_followed` = "A.R. Venugopal" → caution — overruled in principle by IARC India Ltd.; if `court_level` = "Supreme Court" → this judgment applies.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: measure_type
Type: FactEntry[str]
Description: Specifies the type of legal measure or proceeding (e.g., "Section 19 application", "Section 30(1) appeal", "Section 20 appeal")
Module: M4
Extraction: Determined from the nature of the application or appeal filed

**B. New YAML Rule Needed:**
Module: M4
Rule ID: M4_C1_section30_no_condonation
Conditions: measure_type = "Section 30(1) appeal" AND days_from_measure_to_sa > 30
Severity: FATAL
Message: "Appeal under Section 30(1) of the RDB Act filed beyond 30 days. Section 5 of the Limitation Act does not apply. Appeal is time-barred."
Judgment tag: ["IARC India Ltd."]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: ar_venugopal_jotheeswaran.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Overruled by: IARC India Ltd. (2017) (16) SCC 137 — held that Section 5 of the Limitation Act does not apply to condone delay in appeals under Section 30(1) of the RDB Act."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: LIMITATION_EXPIRED
