---
citation: "(2022) 4 RCR (Civil) 445"
title: "M/S Shri Santosh Saw Mill Through Its Proprietor-Ved Prakash Rekhan and Another v. Allahabad Bank and Others"
short_name: "Shri Santosh Saw Mill"
court: HIGH_COURT
high_court_state: "Punjab and Haryana"
bench_strength: 2
judgment_date: "2022-10-12"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["THIRD_PARTY_ATS", "AUCTION_PURCHASER", "SERVICE_DEFECT"]
statutory_basis: ACT
act_sections: ["Section 13(2)", "Section 13(4)", "Section 17", "Section 14"]
rules_sections: []
slrai_modules: ["M1", "M3", "M10"]
keywords: ["sealed tender opened", "inter-se bidding", "person aggrieved", "symbolic possession", "no locus to claim", "GPA not transfer", "adverse possession inconsistent", "third party possession", "auction bidder rights", "DRT interim sale direction"]
retrieval_condition: "Applies when a third party in permissive possession challenges auction and DRT directs sale in their favour without auction participation."
source: HC_FULL_TEXT
ik_doc_id: "96642647"
ik_url: "https://indiankanoon.org/doc/96642647/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers alleged that they were in continuous and settled possession of the secured property since 1972 and had acquired title through a general power of attorney (GPA) and relinquishment by the original owner. They contended that the bank’s sale notice was barred by limitation under Article 62 of the Limitation Act, 1963, as the loan became due in 1992. They further argued that the bank could not conduct a sale without taking actual physical possession and that the DRT was justified in directing the sale in their favour upon depositing the bid amount. They claimed the auction purchaser had no locus to challenge the DRT’s interim order since it was only a bidder and not a party to the Securitisation Application.

## HOLDING SUMMARY

A third party in permissive possession of a secured asset cannot claim ownership or seek a sale in their favour merely by virtue of long possession or through a General Power of Attorney, which does not convey title under Section 53-A of the Transfer of Property Act. The right to challenge enforcement measures under Section 17 of the SARFAESI Act is limited to borrowers, guarantors, or persons with a legal interest in the property; mere possessors without title are not entitled to substantive relief. The DRT cannot bypass the auction process and confer ownership on a non-bidding possessor, especially after a valid bid has been submitted. When a sealed bid is opened during proceedings, the bidder becomes a "person aggrieved" and has locus to challenge any order that nullifies their bid. This applies when: a third party in permissive possession seeks ownership via DRT interim order without participating in the auction, and a valid bid has already been submitted.

## KEY FACTS OF THIS CASE

The secured property in Yamuna Nagar, Haryana, was originally owned by Santosh Kumar Aggarwala (Respondent No.4), who mortgaged it to Allahabad Bank for a loan taken by another firm. The petitioners, M/S Shri Santosh Saw Mill, were in permissive possession of the property since 1972 as a business unit but were neither borrowers nor guarantors. The bank issued a Section 13(2) demand notice in 2011 and a sale notice in December 2011. During the pendency of SA 17 of 2012 filed by the petitioners to set aside the sale, the DRT permitted the opening of sealed bids, revealing that M/s Globe Panel Industries (Respondent No.5) had bid ₹2.40 crores. The DRT then allowed the petitioners to deposit the same amount and issued them a sale certificate. The DRAT later set aside this direction, and the High Court upheld the DRAT’s decision, confirming the auction purchaser’s rights.

## WHAT THE COURT DECIDED

The High Court dismissed both writ petitions filed by the petitioners. It held that the petitioners had no legal right or title to the property and were merely permissive occupants. The court affirmed the DRAT’s order setting aside the DRT’s direction to issue a sale certificate to the petitioners. It dismissed SA 144 of 2018 (formerly SA 17 of 2012) and upheld the DRAT’s order confirming the sale in favour of the auction purchaser. The bank was directed to refund ₹2.40 crores with 6% interest to the petitioners, but the auction purchaser’s rights were upheld.

## KEY QUOTE

A third party in permissive possession of the secured asset cannot be allowed to take advantage of the order passed by DRT... permitting petitioners to deposit 2.40 Crores and obtaining a sale certificate... without even making a bid in response to the sale notice.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `sa_applicant_type` is "Third Party" — the applicant in the SA is not the borrower or guarantor
2. `ats_predates_mortgage` is FALSE — no valid Agreement to Sell pre-dating the mortgage exists
3. `possession_mode` is "Permissive" — possession is by consent of the owner, not adverse or under title
4. `auction_notice_affixed_on_property` is TRUE — the bank properly initiated auction proceedings
5. `auction_conducted_despite_stay` is FALSE — no stay was in force during auction
6. `challenges_auction` is TRUE — the SA challenges the auction process
7. `prayer_scope_covers_current_measure` is TRUE — the prayer includes setting aside the auction
8. `sale_certificate_issued` is TRUE — a sale certificate was issued to a non-bidder third party during SA pendency

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the applicant is the borrower or guarantor — in that case, *Kanaiyalal v. State of Maharashtra* applies and the SA is maintainable regardless of possession status.
   SLRAI ROUTING: if `sa_applicant_type` = "Borrower" → Kanaiyalal applies.

2. When the third party has a registered Agreement to Sell predating the mortgage — in that case, *Vishal N. Kalsaria v. Bank of India* applies and tenancy/ATS protection may be available.
   SLRAI ROUTING: if `ats_predates_mortgage` = TRUE → Vishal_N_Kalsaria applies.

3. When the auction purchaser failed to pay the balance within 90 days — in that case, *E. Muthurathinasabathy* applies and the sale may be inchoate.
   SLRAI ROUTING: if `balance_consideration_paid_within_90_days` = FALSE → E_Muthurathinasabathy applies.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002  
Primary provision: Section 17(1) — "Any person, including the borrower, aggrieved by any of the measures referred to in sub-section (4) of Section 13 may, within forty-five days from the date on which the measure referred to in that sub-section is taken, file an application to the Tribunal..."  
Level: ACT  
Nature: MANDATORY — the phrase "any person... aggrieved" was interpreted restrictively to exclude persons without legal interest in the property.

Secondary: Section 13(4) — authorizes secured creditor to take possession and sell.  
Nature: MANDATORY — possession can be symbolic via notice under Rule 8(1), not necessarily physical.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Suraj Lamp & Industries (P) Ltd. v. State of Haryana (2012) 1 SCC 656  
  Held that a General Power of Attorney does not convey title; mere possession under GPA does not create ownership. This case applies the same principle in SARFAESI context.

Distinguishes: Vishal N. Kalsaria v. Bank of India (2016) 3 SCC 762  
  Vishal Kalsaria allowed tenancy protection to a third party with possessory rights. This case distinguishes it by holding that permissive possession without a registered lease or ATS does not confer such rights.  
  SLRAI ROUTING: if `tenancy_claimed` = TRUE and `lease_registered` = TRUE → Vishal_N_Kalsaria applies; if `possession_mode` = "Permissive" and no lease → this judgment applies.

Follows: Hindon Forge (P) Ltd. v. State of U.P. (2019) 2 SCC 198  
  Affirmed that symbolic possession under Section 13(4) is sufficient for enforcement; actual physical possession is not mandatory before auction.

Distinguishes: Celir LLP v. Bafna Motors (2024) 2 SCC 1  
  Celir LLP dealt with a completed auction with timely payment. This case involves a failed attempt to override auction in favour of a non-bidding possessor.  
  SLRAI ROUTING: if `sale_certificate_issued` = TRUE and `balance_consideration_paid_within_90_days` = TRUE → Celir LLP applies; if `sale_certificate_issued` = TRUE but to non-bidder → this judgment applies.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: possession_mode
Type: FactEntry[str]
Description: How the applicant is in possession — "Permissive", "Adverse", "Under Lease", "Under ATS", "Owner"
Module: M5
Extraction: From SA allegations and supporting documents

**B. New YAML Rule Needed:**
Module: M10
Rule ID: M10_C8_third_party_no_title
Conditions: sa_applicant_type="Third Party" AND possession_mode="Permissive" AND ats_predates_mortgage=False
Severity: FATAL
Message: "Third party in permissive possession without title cannot claim ownership or seek sale confirmation under SARFAESI. SA liable to be dismissed."
Judgment tag: ["Shri_Santosh_Saw_Mill"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: vishal_n_kalsaria.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Shri Santosh Saw Mill (2022) 4 RCR (Civil) 445 — held that permissive possession without registered lease or ATS does not attract Kalsaria's protection."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: THIRD_PARTY_ATS
