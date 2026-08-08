---
citation: "(2026) ibclaw.in 47 DRAT"
title: "Mr.D.V.Vijay Anand vs The Authorized Officer"
short_name: "D.V. Vijay Anand"
court: HIGH_COURT
high_court_state: "Tamil Nadu"
bench_strength: 2
judgment_date: "2026-02-12"
overruled: false
overruled_by: null
distinguished_by: []
favor: BORROWER
favor_verified: true
ground_codes: ["VALUATION_DISPUTE", "AMOUNT_DISPUTE", "SERVICE_DEFECT"]
statutory_basis: ACT
act_sections: ["Section 13(2)", "Section 13(4)", "Section 31(i)", "Section 31(j)"]
rules_sections: []
slrai_modules: ["M1", "M6", "M8"]
keywords: ["Section 31(i)", "Section 31(j)", "less than 20% of loan amount", "agricultural land", "Punja land", "upset price", "Adangal extract", "Tahsildar certificate", "Rule 8(5)", "fair market value"]
retrieval_condition: "Applies when the outstanding amount due is less than 20% of the sanctioned loan and the mortgaged property is agricultural land."
source: HC_FULL_TEXT
ik_doc_id: "146240562"
ik_url: "https://indiankanoon.org/doc/146240562/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers alleged that the SARFAESI proceedings were invalid because the outstanding dues of Rs.14–18 lakhs were less than 20% of the Rs.2 crore overdraft facility sanctioned, invoking the bar under Section 31(j) of the SARFAESI Act. They contended that the mortgaged properties were agricultural lands (classified as 'Punja lands' in revenue records), and thus exempt from SARFAESI enforcement under Section 31(i). They further argued that the reserve price fixed at Rs.24.10–24.35 lakhs was grossly undervalued compared to the original valuation of over Rs.4 crores, violating Rule 8(5) of the SARFAESI Rules on fair market value. The prayer was to set aside the demand notice, possession, and sale certificate, and cancel the auction.

## HOLDING SUMMARY

Section 31(j) of the SARFAESI Act bars enforcement proceedings when the amount due is less than 20% of the principal loan amount and interest. The court held that this provision applies even if a large facility was sanctioned but only a small amount was disbursed and due. Additionally, Section 31(i) exempts agricultural lands from SARFAESI enforcement, and the nature of the land is determined by its actual use at the time of security creation, supported by Adangal extracts from the Village Administrative Officer. The court emphasized that revenue records and actual cultivation (e.g., maize crops) are reliable indicators. The reserve price fixed at less than 1% of the original valuation violated Rule 8(5)'s requirement of fair market value, rendering the auction vitiated. This applies when: the outstanding amount is less than 20% of the sanctioned loan and the mortgaged property is agricultural land used for cultivation.

## KEY FACTS OF THIS CASE

Two brothers, Mr. D.V. Vijay Anand and Mr. R.V. Vinothkumar, availed overdraft facilities of Rs.2 crore each from Central Bank of India, secured by agricultural properties in Virudhunagar and Tirunelveli districts, Tamil Nadu. The properties were classified as 'Punja lands' and used for maize cultivation. Although Rs.2 crore was sanctioned, only Rs.13.25 lakh was disbursed (for insurance), and the rest was withdrawn by the bank. The borrowers defaulted on dues of Rs.14.11 lakh and Rs.13.85 lakh respectively. The bank issued a Section 13(2) demand notice, took symbolic possession under Section 13(4), and issued an e-auction notice with a reserve price of Rs.24.10–24.35 lakh. The borrowers challenged the auction before DRT, which dismissed the SA; DRAT upheld it. The Madras HC, in revision, set aside the proceedings.

## WHAT THE COURT DECIDED

The Madras High Court allowed the Civil Revision Petitions, set aside the Section 13(2) demand notice and Section 13(4) possession notice, and cancelled the sale certificates issued in favor of the auction purchaser. The court directed the bank to refund the sale consideration paid by the auction purchaser within two weeks. The interim injunction was upheld, and the connected miscellaneous petitions were closed. No costs were awarded.

## KEY QUOTE

The said dues are nothing but the amount which were prescribed for insurance policy. When the loan amount itself was returned to the Bank without permitting the petitioners to avail Over Draft credit facility, nothing survives in the policy...

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `amount_due_less_than_20_percent` is TRUE — the outstanding amount due is less than 20% of the total sanctioned loan amount
2. `property_classification` is "agricultural" — the mortgaged property is agricultural land, as evidenced by revenue records (e.g., Adangal extract)
3. `tenancy_claimed` is TRUE — the borrower was actively cultivating the land (e.g., maize crops) at the time of security creation
4. `reserve_price_vs_valuation_pct` is less than 10 — the reserve price is grossly disproportionate to the original valuation (e.g., <10%)
5. `challenges_auction` is TRUE — the borrower challenges the auction on grounds of undervaluation and inapplicability of SARFAESI

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the outstanding amount due exceeds 20% of the sanctioned loan — in that case, Section 31(j) does not apply, and standard SARFAESI enforcement is valid.
   SLRAI ROUTING: if `amount_due_less_than_20_percent` = FALSE → standard enforcement applies.

2. When the mortgaged property is non-agricultural or used for non-agricultural purposes — Section 31(i) exemption does not apply.
   SLRAI ROUTING: if `property_classification` ≠ "agricultural" → K. Sreedhar v. Raus Constructions (2023) applies.

3. When the reserve price is reasonably close to the market valuation — Rule 8(5) is satisfied, and valuation challenge fails.
   SLRAI ROUTING: if `reserve_price_vs_valuation_pct` ≥ 50 → standard auction validity applies.

## STATUTORY CONTEXT

Primary law: Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002  
Primary provision: Section 31(j) — "The provisions of this Act shall not apply to any case in which the amount due is less than twenty per cent of the principal amount and interest thereon."  
Instrument level: ACT  
Nature of provision: MANDATORY — court held the bar is absolute when the threshold is met.

Secondary provision: Section 31(i) — "The provisions of this Act shall not apply to any security interest created in agricultural land."  
Nature: MANDATORY — applies when land is actually used for agriculture, supported by Adangal and cultivation evidence.

Rule 8(5) of SARFAESI Rules — requires reserve price to reflect fair market value based on valuer's report.  
Nature: DIRECTORY in form but MANDATORY in effect when gross undervaluation is shown.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: K. Sreedhar vs. Raus Constructions Private Ltd. (2023) 11 SCC 169  
  Affirmed that actual use of land, not just revenue classification, determines agricultural status under Section 31(i).  
  SLRAI ROUTING: if `property_classification` = "agricultural" AND `tenancy_claimed` = TRUE → this judgment applies; if no cultivation evidence → K. Sreedhar applies.

Distinguishes: Blue Coast Hotels Ltd. v. Bank of India (2020) 10 SCC 707  
  Blue Coast held that mere revenue classification as agricultural is insufficient; actual use matters.  
  This case distinguishes by showing actual cultivation (maize) and valid Adangal, making Section 31(i) applicable.  
  SLRAI ROUTING: if `tenancy_claimed` = TRUE → this judgment applies; if no cultivation → Blue Coast applies.

Follows: M. Rajendran v. KPK Oils (2025) SCC OnLine SC 2036  
  Reinforces that procedural defects in SARFAESI enforcement, especially valuation and jurisdictional bars, must be strictly examined.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: amount_due_less_than_20_percent
Type: FactEntry[bool]
Description: True if the outstanding amount due is less than 20% of the total sanctioned loan amount
Computed from: (actual_outstanding_amount / total_sanctioned_amount) < 0.20
Module: M8

Field name: total_sanctioned_amount
Type: FactEntry[float]
Description: The total loan amount sanctioned by the bank, regardless of disbursement
Module: M8

**B. New YAML Rules Needed:**
Module: M8
Rule ID: M8_C3_section31j_violation
Conditions: amount_due_less_than_20_percent=True
Severity: FATAL
Message: "SARFAESI proceedings barred under Section 31(j): amount due is less than 20% of sanctioned loan."
Judgment tag: ["D_V_Vijay_Anand"]
Statutory basis: ACT

Module: M6
Rule ID: M6_C4_gross_undervaluation
Conditions: reserve_price_vs_valuation_pct < 10
Severity: FATAL
Message: "Reserve price grossly below valuation (<10%) violates Rule 8(5) and principles of fair market value."
Judgment tag: ["D_V_Vijay_Anand"]
Statutory basis: RULES

**C. Existing Judgments to Update:**
File: k_sreedhar_raus_constructions.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: D.V. Vijay Anand (2026) — where actual cultivation and valid Adangal extract established agricultural use, making Section 31(i) applicable despite bank's contrary certificate."

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: VALUATION_DISPUTE
