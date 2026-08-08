---
citation: "2016 INSC 303"
title: "Indian Bank v. M/S Nippon Enterprises South & Ors."
short_name: "Indian Bank v. Nippon Enterprises"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2016-02-17"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["TENANCY_CLAIM"]
statutory_basis: ACT
act_sections: ["Section 13(4)"]
rules_sections: []
slrai_modules: ["M5"]
keywords: ["tenancy claim", "eviction under Rent Control Act", "SARFAESI cannot override tenancy", "due process for tenant eviction", "stultifying statutory rights"]
retrieval_condition: "Applies when the bank seeks to evict a tenant using SARFAESI without following the Rent Control Act."
source: SC_FULL_TEXT
ik_doc_id: "163250772"
ik_url: "https://indiankanoon.org/doc/163250772/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The respondents, who were tenants in the secured premises, alleged that the bank, having succeeded in SARFAESI proceedings against the borrower-owner, could not automatically evict them without following the due process of the applicable Rent Control Act. They contended that their tenancy rights, once validly created, are protected under special tenancy laws and cannot be circumvented by invoking the SARFAESI Act. The prayer before the DRT and higher forums was to restrain the bank from dispossessing them without initiating and completing eviction proceedings under the relevant Rent Control legislation.

## HOLDING SUMMARY

Section 13(4) of the SARFAESI Act does not empower a secured creditor to bypass statutory tenancy protections and summarily evict a tenant. Once a valid tenancy is established, the tenant can only be evicted by following the due process of law prescribed under the applicable Rent Control Act. The SARFAESI Act cannot be used to stultify or override the statutory rights granted to tenants under special tenancy laws. Any attempt to evict a tenant without such compliance is unlawful and violates the tenant’s statutory protection. This principle was reaffirmed in Vishal N. Kalsaria v. Bank of India (2016) 1 SCALE 172, which held that SARFAESI cannot be weaponized to circumvent tenancy rights. This applies when: a tenant occupies the secured property under a valid lease and the bank attempts eviction solely through SARFAESI without initiating proceedings under the Rent Control Act.

## KEY FACTS OF THIS CASE

Indian Bank initiated SARFAESI proceedings against the owner of certain secured commercial premises after the loan account turned into NPA. The bank successfully took possession and sought to dispossess M/S Nippon Enterprises South, which was operating as a tenant in the premises. The tenant challenged the eviction, asserting its rights under tenancy law. The DRT and DRAT upheld the tenant’s claim, leading the bank to appeal to the Supreme Court. The core dispute was whether SARFAESI enforcement against the borrower also extinguished the tenant’s rights without separate eviction proceedings.

## WHAT THE COURT DECIDED

The Supreme Court dismissed the appeals filed by Indian Bank, affirming that SARFAESI proceedings do not confer automatic rights over tenants in possession. The Court clarified that the bank must pursue eviction of the tenant through the due process of the Rent Control Act and cannot rely solely on SARFAESI possession. However, the dismissal was without costs, and the Court noted that the bank remains free to initiate appropriate legal proceedings under tenancy law to evict the tenant.

## KEY QUOTE

A tenant cannot be arbitrarily evicted by using the provisions of the SARFAESI Act as that would amount to stultifying the statutory rights of protection given to the tenant.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `tenancy_claimed` is TRUE — the respondent asserts tenancy in the secured property
2. `lease_registered` is TRUE or `lease_type` is "protected tenancy" — the tenancy is governed by a Rent Control Act
3. `challenges_auction` is FALSE — the challenge is not to auction but to physical eviction
4. `prayer_scope_covers_current_measure` is TRUE — the borrower/tenant seeks protection from dispossession
5. `drt_interim_stay_granted` is TRUE — interim relief granted against eviction

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the tenancy was created after the mortgage or without the bank’s consent and is deemed not binding — in such cases, the bank may proceed under SARFAESI without tenancy compliance.
   SLRAI ROUTING: if `lease_predates_mortgage` = FALSE → this judgment does not apply; bank may evict under SARFAESI.

2. When the tenant is a mere licensee or permissive occupant without statutory protection — the Rent Control Act does not apply, and SARFAESI possession may suffice.
   SLRAI ROUTING: if `lease_type` = "license" → this judgment does not apply.

3. When the challenge is to the demand notice or auction validity, not to eviction — this judgment is limited to tenancy-based eviction disputes.
   SLRAI ROUTING: if `challenges_demand_notice` = TRUE → other judgments apply.

## STATUTORY CONTEXT

Primary law: The Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002  
Primary provision: Section 13(4) — "The secured creditor may take possession of the secured assets... and the borrower shall not have any right to interfere in the possession or vesting of such assets."  
Instrument level: ACT  
Nature of provision: DIRECTORY — the Court held that this power is subject to other statutory protections like tenancy laws; it does not override Rent Control Acts.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Vishal N. Kalsaria v. Bank of India (2016) 1 SCALE 172  
  Reaffirmed that SARFAESI cannot be used to circumvent due process under Rent Control Acts; tenant eviction requires separate proceedings.

Distinguishes: Mardia Chemicals Ltd. v. Union of India (2004) 4 SCC 311  
  Mardia Chemicals upheld the constitutional validity of SARFAESI but did not address tenancy rights. This case clarifies that SARFAESI powers are not absolute and yield to other statutory protections.
  SLRAI ROUTING: if `tenancy_claimed` = TRUE → this judgment applies; if no tenancy → Mardia applies.

Affirmed: Karnataka Board of Wakf v. State of Karnataka (2004) 10 SCC 779  
  Recognized that special statutes like Rent Control Acts provide overriding protection to tenants, which enforcement mechanisms must respect.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed**  
Field name: lease_type  
Type: FactEntry[str]  
Description: Specifies whether the tenancy is statutory, protected, contractual, or license  
Module: M5  
Extraction: From lease deed or tenant’s affidavit in SA

Field name: bank_noc_for_tenancy_given  
Type: FactEntry[bool]  
Description: Whether the bank granted No Objection Certificate (NOC) for the tenancy  
Module: M5  
Extraction: From bank records or correspondence

**B. New YAML Rules Needed**  
Module: M5  
Rule ID: M5_T2_tenancy_protection_override  
Conditions: tenancy_claimed=True AND lease_type IN ["protected tenancy", "statutory tenancy"] AND bank_noc_for_tenancy_given=False  
Severity: HIGH  
Message: "Tenant enjoys statutory protection under Rent Control Act. SARFAESI cannot be used for summary eviction. Separate tenancy proceedings required."  
Judgment tag: ["Indian_Bank_v_Nippon_Enterprises", "Vishal_Kalsaria"]  
Statutory basis: ACT

**C. Existing Judgments to Update**  
File: vishal_kalsaria_bank_of_india.md  
Section: ## RELATIONSHIP TO OTHER JUDGMENTS  
Add: "Followed by: Indian Bank v. Nippon Enterprises (2016 INSC 303) — reaffirmed that SARFAESI cannot override statutory tenancy rights under Rent Control Acts."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: TENANCY_CLAIM
