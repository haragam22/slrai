---
citation: "2022 SCC OnLine SC 520"
title: "Rajasthan Financial Corporation Jaipur and Others v. M/s Jain Bandhu Sneh Resorts Private Limited and Another"
short_name: "Rajasthan Financial Corp"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2022-04-27"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["AUCTION_PURCHASER", "VALUATION_DISPUTE"]
statutory_basis: ACT
act_sections: ["Section 13(8)"]
rules_sections: []
slrai_modules: ["M10", "M6"]
keywords: ["price escalation", "interest on bid amount", "prolonged delay", "fresh auction not justified", "sale confirmation", "sole bidder", "mechanical confirmation", "property value increase", "handover of possession"]
retrieval_condition: "Applies when the High Court set aside a confirmed auction sale solely due to unaccounted property price escalation during a multi-year judicial delay, despite no procedural defect in the auction."
source: SC_FULL_TEXT
ik_doc_id: "195470217"
ik_url: "https://indiankanoon.org/doc/195470217/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower alleged that the auction sale of its resort was vitiated by fraud and collusion between the bank and the auction purchaser, and that the property was sold for a paltry amount far below its true market value of Rs. 17 crores. They contended that the High Court rightly set aside the sale due to the bank’s failure to account for five years of property price escalation between the bid confirmation in 2013 and the handover of possession in 2018. The borrower further argued that the bank had not acted in good faith by mechanically confirming the sale without adjusting for inflation or interest, and that the auction purchaser should not benefit from the delay caused by ongoing litigation. The prayer before the DRT/HC/SC was to uphold the High Court’s direction for a fresh auction.

## HOLDING SUMMARY

The Supreme Court held that a confirmed auction sale cannot be set aside solely on the ground that the secured creditor failed to account for property price escalation during a prolonged judicial delay, in the absence of any procedural defect, fraud, or mala fide in the auction process. While the bank had a duty to consider the economic impact of a five-year gap between bid confirmation and possession, this lapse did not invalidate the sale. Instead, the auction purchaser was directed to pay interest at 12% per annum on the bid amount for the period of delay, thereby compensating for the time value of money and market appreciation. The Court emphasized that once a sale is confirmed and the purchaser has made full payment and taken possession, the transaction should not be disturbed unless there is a fundamental flaw. This applies when: the auction was conducted fairly with no procedural irregularity, the purchaser is ready and willing, and the only ground for setting aside is unadjusted price escalation during judicial pendency.

## KEY FACTS OF THIS CASE

The borrower, Jain Bandhu Sneh Resorts, had availed two term loans totaling Rs. 2.55 crores from Rajasthan Financial Corporation (RFC), which defaulted. After multiple opportunities to repay, including a High Court-mandated deadline of 31.03.2009, the borrower failed to clear dues. RFC took possession of the resort in 2012 and issued a sale notice in March 2013. An e-auction was held in May 2013 where Sun On Mount Hotels emerged as the sole bidder with a final bid of Rs. 11.11 crores. However, due to a writ petition and interim stay by the Rajasthan High Court, the sale remained pending for nearly five years. Possession was handed over only in February 2018. The High Court set aside the sale in 2019, citing failure to account for price escalation, and ordered a fresh auction. RFC and the auction purchaser appealed to the Supreme Court.

## WHAT THE COURT DECIDED

The Supreme Court reversed the High Court’s order setting aside the auction sale, holding that the sale in favour of the auction purchaser was valid and should not be annulled. It upheld the confirmation of the sale and the transfer of possession. However, it directed the auction purchaser to pay interest at 12% per annum on the bid amount of Rs. 11.11 crores for the period from 14.06.2013 to 15.01.2018, to account for the delay in finalizing the sale due to judicial proceedings. The appeals were disposed of accordingly, with the sale upheld and interest imposed as compensation.

## KEY QUOTE

The Division Bench has set aside the confirmation of sale only on the ground that the Corporation has not taken into account the escalation of the prices in property between 14.06.2013 to 15.01.2018. Except this ground, there is no fault found with the auction proceedings and finalization of the sale in favour of the Auction Purchaser.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `auction_conducted_despite_stay` is FALSE — the auction was not conducted during a stay, but finalization was delayed due to ongoing litigation
2. `stay_was_operational_on_auction_date` is TRUE — a valid interim order was in force preventing finalization
3. `auction_type` is "e-auction" or "public auction" — the sale process was transparent and competitive
4. `auction_purchaser_paid_full_amount` is TRUE — the purchaser has fully discharged the bid amount
5. `possession_given_to_auction_purchaser` is TRUE — possession has already been handed over
6. `challenges_auction` is based on "price escalation during delay" — the sole ground for challenge is unadjusted market appreciation during judicial pendency
7. `fraud_alleged` is FALSE — no credible evidence or finding of fraud, collusion or procedural defect in the auction

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the auction itself was vitiated by fraud, collusion, or procedural illegality — in such cases, the sale can be set aside, and *Kanaiyalal* or *Celir LLP* principles may apply depending on the nature of the defect.
   SLRAI ROUTING: if `fraud_alleged` = TRUE and proven → this judgment does not apply; fraud-based challenges follow *Kanaiyalal* or *M. Rajendran*.

2. When the auction purchaser has not yet paid the full amount or taken possession — in such cases, the sale is not final, and the secured creditor may still be required to re-advertise or adjust terms.
   SLRAI ROUTING: if `possession_given_to_auction_purchaser` = FALSE → this judgment does not apply; *E. Muthurathinasabathy* may apply if Rule 9(4) timelines are violated.

3. When the delay in finalization was due to the bank’s inaction, not judicial process — if the bank unreasonably delayed without court orders, the High Court may have wider discretion to order a fresh sale.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002  
Primary provision: Section 13(8) — "The borrower shall have the right to repay the secured debt in full and request the secured creditor to return the possession of the secured assets."  
Verbatim text: "The borrower shall have the right to repay the secured debt in full and request the secured creditor to return the possession of the secured assets."  
Level: ACT  
Nature: MANDATORY — the right exists until a valid sale extinguishes it, but does not entitle the borrower to renege after a completed sale.

The Court also implicitly relied on the principle that once a sale is confirmed and possession transferred, the transaction acquires statutory finality, consistent with *Celir LLP v. Bafna Motors*.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Celir LLP v. Bafna Motors (2024) 2 SCC 1  
  Affirmed the principle that a confirmed auction sale, once completed with full payment and possession, acquires statutory finality and should not be lightly disturbed.

Distinguishes: High Court's mechanical approach in setting aside sale  
  The High Court attempted to correct economic inequity by ordering a fresh auction, but the Supreme Court held that interest compensation is the appropriate remedy, not annulment.  
  SLRAI ROUTING: if `auction_finalized` = TRUE AND `possession_given` = TRUE → Rajasthan Financial Corp applies (sale upheld with interest); if `auction_inchoate` = TRUE → E. Muthurathinasabathy applies (sale not final, redemption possible).

Affirmed: Mathew Varghese v. M. Amritha Kumar (2014) 5 SCC 610  
  Reiterated that the right of redemption under Section 13(8) is valuable but not absolute — it is extinguished upon valid completion of sale.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: auction_purchaser_paid_full_amount
Type: FactEntry[bool]
Description: True if the auction purchaser has paid the entire bid amount to the secured creditor
Module: M10
Computed from: bank payment records or sale certificate

Field name: fraud_alleged
Type: FactEntry[bool]
Description: True if the borrower alleges fraud, collusion, or mala fide in the auction process
Module: M10
Extraction: From SA or writ petition allegations

**B. New YAML Rule Needed:**
Module: M10
Rule ID: M10_C8_price_escalation_compensation
Conditions: auction_conducted_despite_stay=False AND stay_was_operational_on_auction_date=True AND possession_given_to_auction_purchaser=True AND challenges_auction="price escalation during delay" AND fraud_alleged=False
Severity: WARNING
Message: "High Court cannot set aside a completed auction solely for unadjusted price escalation during judicial delay. Remedy is interest compensation, not fresh auction. See Rajasthan Financial Corp (2022)."
Judgment tag: ["Rajasthan_Financial_Corp"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: celir_llp_bafna_motors.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Followed by: Rajasthan Financial Corp (2022 SCC OnLine SC 520) — affirmed that completed sales with possession should not be set aside for economic inequity absent fraud."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: AUCTION_PURCHASER
