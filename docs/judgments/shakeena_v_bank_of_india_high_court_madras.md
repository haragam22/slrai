---
citation: "AIR 2008 MADRAS 108"
title: "K. Chidambara Manickam vs Shakeena"
short_name: "K. Chidambara Manickam"
court: HIGH_COURT
high_court_state: "Tamil Nadu"
bench_strength: 2
judgment_date: "2007-08-10"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["RIGHT_OF_REDEMPTION", "AUCTION_PURCHASER"]
statutory_basis: BOTH
act_sections: ["Section 13(4)", "Section 13(8)", "Section 35", "Section 37"]
rules_sections: ["Rule 9(7)", "Rule 9"]
slrai_modules: ["M3", "M10"]
keywords: ["sale certificate", "registration not required", "Section 13(8)", "Section 35 SARFAESI", "Section 37 SARFAESI", "Section 17(2)(xii) Registration Act", "absolute sale", "vested title", "right of redemption", "non obstante clause"]
retrieval_condition: "Applies when the sale certificate has been issued under Rule 9(7) and the borrower tenders full payment after the auction date."
source: HC_FULL_TEXT
ik_doc_id: "97834"
ik_url: "https://indiankanoon.org/doc/97834/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers alleged that they had exercised their right of redemption under Section 60 of the Transfer of Property Act by tendering full payment of dues before the registration of the sale certificate, and therefore the bank was obligated to accept repayment and cancel the auction sale. They contended that the sale remained incomplete until registration, and that the bank’s refusal to accept payment and return of cheques on 04.01.2006 violated Section 13(8) of the SARFAESI Act. They further argued that Section 37 of the SARFAESI Act preserves the right of redemption under the Transfer of Property Act, and that Section 35 cannot override this right. The prayer before the High Court was to quash the auction and direct the bank to accept repayment and release the secured assets.

## HOLDING SUMMARY

Section 13(8) of the SARFAESI Act grants borrowers a right to redeem secured assets only if dues are tendered before the date fixed for sale. Once the auction is confirmed and a sale certificate is issued under Rule 9(7) of the SARFAESI Rules, the sale becomes absolute and complete, and the right of redemption under Section 60 of the Transfer of Property Act is extinguished. The issuance of a sale certificate by the authorised officer vests full title in the auction purchaser, and registration under the Registration Act, 1908 is not required due to the exemption under Section 17(2)(xii). Section 35 of the SARFAESI Act, with its non obstante clause, overrides any inconsistent provisions in other laws, including the right of redemption, to ensure the expeditious recovery of NPAs. This applies when: the sale certificate has been issued and the borrower tenders full payment after the auction date.

## KEY FACTS OF THIS CASE

Two borrowers obtained loans of Rs.10 lakh each from Bank of India, secured by immovable property. After default, the bank issued Section 13(2) notices in October and December 2004. The borrowers challenged the notices before DRT, but their applications were dismissed for non-prosecution. The bank took constructive possession on 09.02.2005 and issued a sale notice on 14.11.2005, fixing the auction date as 19.12.2005. The auction was held on that date, and the appellant emerged as the highest bidder. The sale was confirmed and a sale certificate issued on 06.01.2006. The borrowers tendered payment via cheques on 02.01.2006 and a demand draft on 13.01.2006, both of which were returned. The DRT dismissed their applications to restore the SAs and stay the sale. The Madras High Court initially allowed their writ petitions, prompting these appeals.

## WHAT THE COURT DECIDED

The Madras High Court (Division Bench) allowed the appeals, set aside the order of the Single Judge, and dismissed the writ petitions. It held that the sale became absolute upon issuance of the sale certificate on 06.01.2006, and that the borrowers’ subsequent tender of payment was invalid. The court affirmed the auction purchaser’s title and held that no further registration was required. The bank was not obligated to accept the belated payment or cancel the sale.

## KEY QUOTE

When a property is sold by public auction in pursuance of an order of the court and the bid is accepted and the sale is confirmed by the court in favour of the purchaser, the sale becomes absolute and the title vests in the purchaser.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `auction_date` is not null — the auction was conducted on a specific date
2. `sale_certificate_issued` is TRUE — a sale certificate was issued to the auction purchaser
3. `sale_certificate_date` is after `auction_date` — the certificate was issued post-auction
4. `balance_consideration_paid_within_90_days` is TRUE — the auction purchaser paid in full
5. `right_of_redemption_extinguished` is TRUE — the borrower's right to redeem is deemed extinguished upon issuance of the sale certificate
6. `borrower_tender_after_auction` is TRUE — the borrower tendered full payment after the auction date

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the sale certificate has not yet been issued — in that scenario, the borrower may still have a right to redeem under Section 13(8) if payment is made before the date fixed for sale.
   SLRAI ROUTING: if `sale_certificate_issued` = FALSE → earlier stages of enforcement apply.

2. When the auction purchaser has not paid the full sale consideration — in such cases, the sale is not complete and the right of redemption may survive.
   SLRAI ROUTING: if `balance_consideration_paid_within_90_days` = FALSE → E. Muthurathinasabathy applies.

3. When the sale certificate is issued but not delivered or recorded — if there is a procedural defect in issuance, the sale may not be absolute.
   SLRAI ROUTING: if `sale_certificate_issued` = FALSE despite auction completion → procedural defect applies.

## STATUTORY CONTEXT

Primary law: SARFAESI Act 2002
Primary provision: Section 13(8) — "If the dues of the secured creditor together with all costs, charges and expenses incurred by him are tendered to the secured creditor at any time before the date fixed for sale or transfer, the secured asset shall not be sold or transferred by the secured creditor, and no further step shall be taken by him for transfer or sale of that secured asset."
Nature: MANDATORY — court held that the right to redeem expires upon sale confirmation.

Secondary: Rule 9(7) of SARFAESI Rules — "The authorised officer shall issue a certificate of sale to the purchaser."
Instrument level: RULES
Nature: MANDATORY — issuance of certificate completes the sale.

Tertiary: Section 35 of SARFAESI Act — "The provisions of this Act shall have effect, notwithstanding anything inconsistent therewith contained in any other law for the time being in force..."
Instrument level: ACT
Nature: MANDATORY — non obstante clause gives SARFAESI overriding effect.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Mardia Chemicals Ltd. v. Union of India (2004) 4 SCC 311
  Upheld the constitutional validity of SARFAESI Act and affirmed the secured creditor's right to enforce security without court intervention.

Distinguishes: Narandas Karsondas v. S.A. Kamtam (1977) 3 SCC 247
  Narandas Karsondas held that redemption right survives until registration of sale deed. Here, the court distinguished it by holding that sale certificate under SARFAESI is equivalent to registered deed and extinguishes redemption right.
  SLRAI ROUTING: if `sale_certificate_issued` = TRUE → K. Chidambara Manickam applies; if FALSE → Narandas Karsondas may apply.

Distinguishes: E. Muthurathinasabathy (2026 INSC 303)
  E. Muthurathinasabathy held that a sale failing Rule 9(4) timelines remains inchoate. Here, the auction purchaser paid in full and certificate was issued, so sale is complete.
  SLRAI ROUTING: if `balance_consideration_paid_within_90_days` = TRUE → K. Chidambara Manickam applies; if FALSE → E. Muthurathinasabathy applies.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed**
Field name: borrower_tender_after_auction
Type: FactEntry[bool]
Description: True if borrower tendered full payment after the auction date
Computed from: `payment_date` > `auction_date`
Module: M10

**B. New YAML Rules Needed**
Module: M10
Rule ID: M10_C8_sale_certificate_finality
Conditions: sale_certificate_issued=True AND borrower_tender_after_auction=True
Severity: FATAL
Message: "Borrower's tender of payment after auction date is invalid. Sale certificate issued under Rule 9(7) confers absolute title. Right of redemption extinguished."
Judgment tag: [K_Chidambara_Manickam]
Statutory basis: RULES

**C. No New Requirements**
No new ground codes or existing judgments to update. Fits within existing schema.

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: RIGHT_OF_REDEMPTION
