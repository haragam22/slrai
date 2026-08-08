---
citation: "2022 SCC OnLine SC 1234"
title: "Balkrishna Rama Tarle Dead Through Lrs vs Phoenix Arc Private Limited"
short_name: "Balkrishna Rama Tarle"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2022-09-26"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["TENANCY_CLAIM"]
statutory_basis: ACT
act_sections: ["Section 14"]
rules_sections: []
slrai_modules: ["M5"]
keywords: ["Section 14", "District Magistrate", "tenancy rights", "ministerial act", "no adjudication", "possession assistance", "designated authority", "eviction proceedings"]
retrieval_condition: "Applies when the District Magistrate declined to assist in possession under Section 14 on grounds of subsisting tenancy requiring eviction proceedings."
source: SC_FULL_TEXT
ik_doc_id: "90970000"
ik_url: "https://indiankanoon.org/doc/90970000/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The petitioners, claiming to be tenants of the mortgaged property, alleged that the secured creditor could not obtain physical possession through the District Magistrate under Section 14 of the SARFAESI Act without first initiating and completing legal proceedings to evict them. They contended that their tenancy rights, which predated the mortgage, must be terminated through due process of law before possession could be granted. The prayer before the DRT and High Court was to restrain the secured creditor from obtaining possession until their tenancy was lawfully terminated.

## HOLDING SUMMARY

Section 14 of the SARFAESI Act imposes a ministerial duty on the District Magistrate to assist the secured creditor in taking possession of secured assets upon compliance with procedural requirements, without adjudicating disputes between the borrower, third parties, or tenants. The Magistrate is not empowered to condition possession on the outcome of eviction proceedings or to adjudicate tenancy rights. Any dispute regarding tenancy must be raised before the Debt Recovery Tribunal under Section 17, not as a bar to possession under Section 14. The role of the Magistrate is limited to verifying the affidavit and formal compliance by the secured creditor, and not to determine substantive rights. This applies when: the District Magistrate refuses to assist in possession on grounds of subsisting tenancy without referring the dispute to DRT.

## KEY FACTS OF THIS CASE

Religare Finvest Ltd. sanctioned a loan of Rs. 6 crores secured by a registered mortgage. After default, the account was classified as NPA, and a Section 13(2) notice was issued. The loan was later assigned to Phoenix ARC Pvt. Ltd., which took symbolic possession under Section 13(4). The secured creditor then filed an application under Section 14 before the District Magistrate, Nashik, seeking physical possession. The petitioner, claiming to be a tenant of part of the secured property, opposed the application, relying on a civil court order restraining dispossession. The designated authority declined to assist, citing pending tenancy, prompting the secured creditor to file a writ petition in the Bombay High Court, which set aside the order. The tenant appealed to the Supreme Court.

## WHAT THE COURT DECIDED

The Supreme Court dismissed the Special Leave Petition, upholding the Bombay High Court’s decision. It held that the District Magistrate has no authority to refuse assistance under Section 14 on grounds of subsisting tenancy or to condition possession on eviction. The Magistrate’s role is ministerial and confined to verifying compliance with statutory formalities. The petitioners’ remedy, if any, lies under Section 17 before the DRT. The Court affirmed that the application under Section 14 must be disposed of in accordance with law, without adjudicating tenancy disputes.

## KEY QUOTE

The step to be taken by the CMM/DM under Section 14 of the SARFAESI Act is a ministerial step. While disposing of the application under Section 14 of the SARFAESI Act, no element of quasi-judicial function or application of mind would require.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `challenges_auction` is FALSE — the challenge is not to auction but to possession under Section 14
2. `challenges_demand_notice` is FALSE — the dispute is not about demand notice validity
3. `tenancy_claimed` is TRUE — a third party claims tenancy in the secured asset
4. `drt_interim_stay_granted` is FALSE — no stay from DRT is in force
5. `prayer_scope_covers_current_measure` is TRUE — the petition seeks to block possession under Section 14
6. `drt_stay_order_date` is null — no DRT order is pending
7. `ibc_moratorium_active` is FALSE — no IBC moratorium applies

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the tenancy dispute has already been adjudicated and a stay is granted by the DRT — in that case, the secured creditor must await DRT’s decision, and this judgment does not override a statutory stay.
   SLRAI ROUTING: if `drt_interim_stay_granted` = TRUE → DRT stay applies; if FALSE → this judgment applies.

2. When the challenge is to the validity of the demand notice or the NPA classification — such disputes fall under Section 17 and are governed by Kanaiyalal or similar precedents.
   SLRAI ROUTING: if `challenges_demand_notice` = TRUE → Kanaiyalal applies; if FALSE → this judgment applies.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002  
Primary provision: Section 14(1) — "Where the possession of any secured assets is required to be taken by the secured creditor... the secured creditor may... request... the Chief Metropolitan Magistrate or the District Magistrate... to take possession thereof, and the Chief Metropolitan Magistrate or... the District Magistrate shall, on such request being made to him— (a) take possession of such asset and documents relating thereto; and (b) forward such asset and documents to the secured creditor"  
Instrument level: ACT  
Nature of provision: MANDATORY — the word "shall" imposes a duty; the Court held the act is ministerial and non-discretionary.

## RELATIONSHIP TO OTHER JUDGMENTS

Affirmed: NKGSB Cooperative Bank Ltd. v. Subir Chakravarty (2022)  
  Reaffirmed that the role of the Magistrate under Section 14 is ministerial and not quasi-judicial.

Distinguishes: Harshad Govardhan Sondagar v. International Assets Reconstruction Co. Ltd. (2014) 6 SCC 1  
  Harshad Sondagar held that the Magistrate must give notice and hearing to Class 1 or 2 lessees. This case clarifies that such hearing does not involve adjudication of tenancy rights.  
  SLRAI ROUTING: if `tenancy_claimed` = TRUE AND `hearing_given` = FALSE → Harshad Sondagar applies; if `hearing_given` = TRUE but possession refused → this judgment applies.

Distinguishes: Vishal N. Kalsaria v. Bank of India (2016) 3 SCC 762  
  Vishal Kalsaria dealt with conflict between rent control law and SARFAESI; this case clarifies that Section 14 does not allow Magistrate to resolve such conflicts — the remedy lies under Section 17.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed**  
Field name: challenges_section_14  
Type: FactEntry[bool]  
Description: True if the borrower or third party challenges the secured creditor's application under Section 14  
Computed from: `prayer_scope_covers_current_measure` AND `challenges_auction` = FALSE AND `challenges_demand_notice` = FALSE  
Module: M5

**B. New YAML Rules Needed**  
Module: M5  
Rule ID: M5_C1_section_14_ministerial_duty  
Conditions: challenges_section_14=True AND tenancy_claimed=True AND drt_interim_stay_granted=False  
Severity: FATAL  
Message: "The District Magistrate cannot refuse assistance under Section 14 on grounds of tenancy without referring the dispute to DRT under Section 17."  
Judgment tag: ["Balkrishna_Rama_Tarle"]  
Statutory basis: ACT

**C. No New Ground Codes Needed**  
The ground "TENANCY_CLAIM" already covers the issue.

**D. Existing Judgments to Update**  
File: harish_sondagar_intl_arc.md  
Section: ## RELATIONSHIP TO OTHER JUDGMENTS  
Add: "Distinguished by: Balkrishna Rama Tarle (2022 SCC OnLine SC 1234) — held that while notice must be given to lessees under Harshad Sondagar, the Magistrate cannot adjudicate tenancy rights or condition possession on eviction."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: TENANCY_CLAIM
