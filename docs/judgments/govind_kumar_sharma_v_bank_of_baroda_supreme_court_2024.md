---
citation: "2024 INSC 326"
title: "Govind Kumar Sharma & Anr. v. Bank of Baroda & Ors."
short_name: "Govind Kumar Sharma"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2024-04-18"
overruled: false
overruled_by: null
distinguished_by: []
favor: BORROWER
favor_verified: true
ground_codes: ["AUCTION_NOTICE_AFFIXING", "REPLY_NOT_GIVEN", "NOTICE_ALL_PARTIES"]
statutory_basis: RULES
act_sections: ["Section 13(8)", "Section 17"]
rules_sections: ["Rule 8(6)", "Rule 8(7)"]
slrai_modules: ["M3", "M10"]
keywords: ["Rule 8(6)", "Rule 8(7)", "30 days notice", "mandatory notice", "auction notice affixed", "notice to borrower", "non-compliance of rules", "sale set aside", "status of tenant", "interest on refund"]
retrieval_condition: "Applies when the bank failed to serve or affix the auction notice as required under Rule 8(6) and Rule 8(7) of the SARFAESI Rules, 2002."
source: SC_FULL_TEXT
ik_doc_id: "26253582"
ik_url: "https://indiankanoon.org/doc/26253582/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower(s) alleged that the bank failed to comply with the mandatory requirements under Rule 8(6) and Rule 8(7) of the SARFAESI Rules, 2002, by not serving a 30-day prior notice of auction to the borrower and not affixing the auction notice on the secured property. They contended that the absence of such statutory compliance rendered the auction sale void ab initio. They further argued that the auction conducted in non-compliance with the rules could not be validated merely because the auction purchaser was in possession. The prayer before the DRT was to set aside the auction sale and direct the bank to refund the auction amount with appropriate interest.

## HOLDING SUMMARY

Rule 8(6) and Rule 8(7) of the Security Interest (Enforcement) Rules, 2002 prescribe mandatory procedural requirements for the conduct of an auction under SARFAESI, including the obligation to serve a 30-day prior notice to the borrower and to affix the auction notice on the secured immovable property. The Supreme Court held that non-compliance with these mandatory provisions invalidates the auction sale, even if the auction purchaser was in possession and had invested in the property. The bank’s own admission of non-compliance before the DRT was sufficient to justify setting aside the sale. While the sale was quashed, the Court modified the DRT’s direction by holding that the auction purchaser, being a former tenant, need not physically vacate the property, but their ownership status reverted to tenancy. The bank was directed to refund the auction amount with 12% compound interest from the date of deposit. This applies when: the bank failed to serve notice under Rule 8(6) or affix notice under Rule 8(7) before conducting the auction.

## KEY FACTS OF THIS CASE

The borrower, a firm, had defaulted on a loan from Bank of Baroda, leading the bank to initiate SARFAESI proceedings. An open auction was conducted, and the appellants—tenants of the secured property—emerged as the highest bidders, paying the full amount and receiving a sale certificate on 30.03.2009. The borrower challenged the auction under Section 17, alleging non-compliance with Rule 8(6) and Rule 8(7) regarding notice. The DRT set aside the sale, DRAT and High Court upheld it. The bank admitted non-compliance and conceded the sale could be set aside. The borrower had since paid all dues independently, and the auction amount (Rs. 12.40 lakhs) remained in a fixed deposit with the bank.

## WHAT THE COURT DECIDED

The Supreme Court affirmed the setting aside of the auction sale due to the bank’s admitted non-compliance with Rule 8(6) and Rule 8(7). It restored the appellants’ status as tenants, not owners, but held they need not surrender physical possession to the bank. The bank was directed to refund the auction amount of Rs. 12.40 lakhs with 12% compound interest from the date of deposit until actual payment. The borrower and bank were directed to settle any residual dues and issue a No Dues Certificate.

## KEY QUOTE

In view of the concurrent finding based on the admission by the Bank that mandatory notice of 30 days was not given to the Borrower before holding the auction/sale, the setting aside of the auction/sale cannot be faulted with.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when: the bank failed to serve notice under Rule 8(6) or affix notice under Rule 8(7) before conducting the auction.

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the auction notice was properly served 30 days in advance and affixed on the property — in that case, *Celir LLP v. Bafna Motors (2024)* applies and the sale enjoys statutory finality.
   SLRAI ROUTING: if `auction_notice_affixed_on_property` = TRUE and `days_between_sale_notice_and_auction` >= 30 → Celir LLP applies.

2. When the borrower did not file a Section 17 application or the challenge was based on valuation or tenancy alone — this judgment is specific to procedural non-compliance in notice.

3. When the auction purchaser was not a tenant of the property — the restoration of tenancy status is a key element of this judgment’s relief.

## STATUTORY CONTEXT

Primary law: Security Interest (Enforcement) Rules, 2002  
Primary provision: Rule 8(6) — "The authorised officer shall give notice of the sale to the borrower and the secured creditor... at least thirty days before the date fixed for the sale."  
Rule 8(7) — "The notice under sub-rule (6) shall also be affixed at a conspicuous place on the immovable property."  
Instrument level: RULES  
Nature of provision: MANDATORY — the Court treated the 30-day notice and affixing requirements as mandatory, non-compliance of which invalidates the sale.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Kanaiyalal Lalchand Sachdev v. State of Maharashtra (2023) 1 SCC 1  
  Reinforces that procedural compliance under SARFAESI Rules is mandatory and non-compliance leads to setting aside of sale.

Distinguishes: Celir LLP v. Bafna Motors Pvt. Ltd. (2024) 2 SCC 1  
  Celir LLP upheld auction finality when all procedures were followed and balance paid timely. Here, the auction was invalidated due to prior procedural defects in notice.  
  SLRAI ROUTING: if `auction_notice_affixed_on_property` = TRUE and `notice_all_parties_served` = TRUE → Celir LLP applies; if either is FALSE → Govind Kumar Sharma applies.

Affirmed: M. Rajendran v. KPK Oils (2025 SCC OnLine SC 2036)  
  Supports the principle that statutory timelines and notice requirements under SARFAESI Rules must be strictly followed for a valid enforcement.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed**  
Field name: days_between_sale_notice_and_auction  
Type: FactEntry[int]  
Description: Number of days between the sale notice date and auction date  
Computed from: auction_date - sale_notice_date  
Module: M3  

Field name: notice_all_parties_served  
Type: FactEntry[bool]  
Description: True if all borrowers and guarantors received the auction notice  
Module: M7  

**B. New YAML Rules Needed**  
Module: M3  
Rule ID: M3_C5_rule8_6_violation  
Conditions: sale_notice_date is not null AND (auction_date - sale_notice_date).days < 30  
Severity: FATAL  
Message: "Auction conducted without 30 days' prior notice as required under Rule 8(6). Sale is liable to be set aside."  
Judgment tag: ["Govind_Kumar_Sharma"]  
Statutory basis: RULES  

Module: M3  
Rule ID: M3_C6_rule8_7_violation  
Conditions: auction_type includes "immovable" AND auction_notice_affixed_on_property = FALSE  
Severity: FATAL  
Message: "Auction notice not affixed on property as required under Rule 8(7). Procedural defect invalidates sale."  
Judgment tag: ["Govind_Kumar_Sharma"]  
Statutory basis: RULES  

**C. Existing Judgments to Update**  
File: celir_llp_bafna_motors.md  
Section: ## RELATIONSHIP TO OTHER JUDGMENTS  
Add line: "Distinguished by: Govind Kumar Sharma (2024 INSC 326) — held that auction sale is invalid when notice requirements under Rule 8(6) and Rule 8(7) are not met, even if purchaser is in possession."

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: AUCTION_NOTICE_AFFIXING
