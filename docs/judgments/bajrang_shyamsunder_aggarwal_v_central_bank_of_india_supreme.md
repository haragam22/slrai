---
citation: "2019 (9) SCC 94"
title: "Bajarang Shyamsunder Agarwal vs Central Bank Of India"
short_name: "Bajarang Agarwal"
court: SUPREME_COURT
high_court_state: null
bench_strength: 3
judgment_date: "2019-09-11"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["TENANCY_CLAIM"]
statutory_basis: ACT
act_sections: ["Section 13(2)", "Section 13(13)", "Section 14", "Section 17", "Section 35"]
rules_sections: []
slrai_modules: ["M5"]
keywords: ["protected tenant", "oral tenancy", "registered instrument", "Section 107 TP Act", "tenant in sufferance", "non-encumbrance certificate", "Section 35 override", "Section 111 TP Act", "prima facie injunction", "bona fide lessee"]
retrieval_condition: "Applies when a tenant claims protection under rent control law but lacks a registered lease and the tenancy is alleged to have been created after mortgage or without bank consent."
source: SC_FULL_TEXT
ik_doc_id: "146571650"
ik_url: "https://indiankanoon.org/doc/146571650/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The appellant-tenant claimed that he was a protected tenant under the Maharashtra Rent Control Act, 1999, having entered into an oral tenancy agreement with the borrower/landlord in January 2000, and had been in continuous possession since then. He contended that the secured creditor could not evict him without determining the validity of his tenancy under Section 111 of the Transfer of Property Act. He further argued that the Small Causes Court had granted him interim injunction, affirming his prima facie right to possession. The prayer was to stay the execution of the order under Section 14 of the SARFAESI Act and protect his tenancy rights.

## HOLDING SUMMARY

The Supreme Court held that the rights of a tenant under rent control legislation do not override the SARFAESI Act when the tenancy lacks documentary proof or was created after mortgage without bank consent. Section 35 of the SARFAESI Act has overriding effect over inconsistent laws, including rent control statutes. A tenant in possession without a registered instrument for a term exceeding one year is not entitled to continued possession beyond the statutory period under Section 107 of the Transfer of Property Act. If a tenancy is not validly established or is determined, the occupant becomes a "tenant in sufferance" with no legal rights, akin to a trespasser. Such a person cannot resist possession proceedings under Section 14. This applies when: a tenant claims protection under rent control law but lacks a registered lease and the tenancy is alleged to have been created after mortgage or without bank consent.

## KEY FACTS OF THIS CASE

The borrower-mortgagor had availed credit facilities from Central Bank of India, secured by a residential flat in Mumbai, mortgaged via equitable mortgage on 20.05.2000. The account turned NPA, and a Section 13(2) demand notice was issued on 30.04.2011. The bank applied under Section 14 for possession, which was granted by the Chief Metropolitan Magistrate on 09.03.2012. The appellant claimed to be a tenant since January 2000 under an oral agreement and filed a suit in the Small Causes Court, obtaining an ex parte interim injunction on 18.09.2012. The bank contested the tenancy, citing a non-encumbrance certificate and a 2016 society letter confirming no tenancy. The appellant failed to produce original rent receipts or any registered lease deed.

## WHAT THE COURT DECIDED

The Supreme Court dismissed the appeal, upholding the rejection of the tenant’s application for stay of execution under Section 14. It held that the appellant failed to prove a valid tenancy and was at best a tenant in sufferance. The court directed the appellant to vacate and hand over possession of the flat to the Assistant Registrar within 12 weeks, who shall deliver it to the bank. The court condemned the use of fabricated tenancy claims to obstruct SARFAESI enforcement.

## KEY QUOTE

A tenant at sufferance is, therefore, one who wrongfully continues in possession after the extinction of a lawful title. There is little difference between him and a trespasser.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `tenancy_claimed` is TRUE — the occupant claims to be a tenant
2. `lease_registered` is FALSE — the tenancy is not supported by a registered instrument
3. `lease_type` is "oral" — the tenancy is based on oral agreement
4. `lease_predates_mortgage` is FALSE or uncertain — the tenancy is alleged to have been created after mortgage or its date is disputed
5. `bank_noc_for_tenancy_given` is FALSE — the bank did not consent to the tenancy
6. `drt_interim_stay_granted` is TRUE — an interim stay was granted by a civil court based on tenancy claim

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the tenant has a registered lease deed executed before the mortgage and the lease is still subsisting — in that case, *Harshad Govardhan Sondagar* applies and the secured creditor cannot disturb possession until the lease is determined under Section 111 of the TP Act.
   SLRAI ROUTING: `lease_registered` = TRUE and `lease_predates_mortgage` = TRUE → Harshad Govardhan applies.

2. When the tenancy is created after the mortgage but with the bank’s written consent — in that case, the tenant may have enforceable rights against the bank.

3. When the property is governed by a rent control law and the tenant is a statutory tenant with court-recognized rights — this judgment does not apply if the tenancy has been substantively adjudicated and not merely granted interim relief.

## STATUTORY CONTEXT

Primary law: The Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002  
Primary provision: Section 35 — "The provisions of this Act shall have effect, notwithstanding anything inconsistent therewith contained in any other law for the time being in force..."  
Instrument level: ACT  
Nature of provision: MANDATORY — court held that Section 35 has broad overriding effect over rent control laws and other inconsistent statutes.

Secondary: Section 13(13) — "After the service of a notice under sub-section (2), the borrower shall not, without the prior written consent of the secured creditor, transfer by way of sale, lease, assignment or mortgage any of his rights, title or interest in the secured asset."  
Nature: MANDATORY — prohibits post-notice leasing without consent.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Harshad Govardhan Sondagar v. International Assets Reconstruction Co. Ltd. (2014) 6 SCC 1  
  Held that a valid lessee in lawful possession cannot be evicted until lease is determined under Section 111 of TP Act. This case follows that principle but distinguishes on facts.

Distinguishes: Vishal N. Kalsaria v. Bank of India (2016) 3 SCC 762  
  Vishal Kalsaria held that SARFAESI cannot override rent control laws. This judgment distinguishes it by holding that Section 35 does override rent control laws when tenancy is not bona fide or unregistered.  
  SLRAI ROUTING: if `tenancy_claimed` = TRUE and `lease_registered` = TRUE → Vishal Kalsaria applies; if `lease_registered` = FALSE → this judgment applies.

Overruled: None  
Affirmed: R.V. Bhupal Prasad v. State of A.P. (AIR 1996 SC 140)  
  Affirmed the definition of "tenant in sufferance" as akin to a trespasser, used to reject protection to unregistered tenants.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**  
No new fields required. All conditions are supported by existing schema.

**B. New YAML Rules Needed:**  
Module: M5  
Rule ID: M5_T1_rent_control_claims  
Conditions: tenancy_claimed=True AND lease_registered=False AND bank_noc_for_tenancy_given=False  
Severity: FATAL  
Message: "Unregistered tenancy claimed after mortgage without bank consent. Occupant is likely a tenant in sufferance. SARFAESI enforcement not barred."  
Judgment tag: ["Bajarang_Agarwal"]  
Statutory basis: ACT  

**C. Existing Judgments to Update:**  
File: vishal_n_kalsaria_banking.md  
Section: ## RELATIONSHIP TO OTHER JUDGMENTS  
Add: "Distinguished by: Bajarang Agarwal (2019) 9 SCC 94 — held that unregistered tenancy without bank consent does not attract protection under rent control laws and Section 35 overrides such claims when tenancy is not bona fide."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: TENANCY_CLAIM
