---
citation: "2023 INSC 838"
title: "Celir LLP v. Bafna Motors (Mumbai) Pvt. Ltd. & Ors."
short_name: "Celir LLP"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2023-09-21"
overruled: false
overruled_by: null
distinguished_by: ["E. Muthurathinasabathy"]
favor: BANK
favor_verified: true
ground_codes: ["AUCTION_PURCHASER", "RIGHT_OF_REDEMPTION", "PENDING_SA_CONCEALED"]
statutory_basis: ACT
act_sections: ["Section 13(8)", "Section 35", "Section 37"]
rules_sections: ["Rule 9(2)", "Rule 9(6)"]
slrai_modules: ["M10", "M3"]
keywords: ["Section 13(8)", "right of redemption", "sale certificate", "vested right", "sanctity of auction", "Rule 9(6)", "confirmation of sale", "equity follows law", "Article 226"]
retrieval_condition: "Applies when the auction purchaser has paid the full bid amount and the bank confirmed the sale, but the borrower seeks redemption after publication of auction notice."
source: SC_FULL_TEXT
ik_doc_id: "149474401"
ik_url: "https://indiankanoon.org/doc/149474401/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers alleged that despite the publication of the auction notice, they retained the right to redeem the mortgage under Section 60 of the Transfer of Property Act, 1882, which survives until the execution of a registered conveyance. They contended that the amended Section 13(8) of the SARFAESI Act only restricts the secured creditor's right to deal with the asset and does not extinguish the borrower's right of redemption. They further argued that the High Court, in exercise of its equitable jurisdiction under Article 226 of the Constitution, could permit redemption even after the auction was confirmed, especially since the bank consented to the arrangement and the borrowers offered a higher amount. The prayer before the High Court was to allow redemption of the mortgage and set aside the auction sale in favour of the appellant.

## HOLDING SUMMARY

The amended Section 13(8) of the SARFAESI Act extinguishes the borrower's right of redemption upon the publication of the auction notice, not upon the issuance of the sale certificate. Once the auction is confirmed and the full bid amount is paid, the auction purchaser acquires a vested right to the secured asset, and the bank is under a mandatory obligation under Rule 9(6) to issue a sale certificate. The sanctity of the public auction process must be preserved, and courts should not interfere under Article 226 on equitable grounds when a statutory remedy under Section 17 is available and the auction has attained finality. The bank cannot enter into a private arrangement with the borrower to permit redemption after the auction has been confirmed. This applies when: the auction purchaser has paid the full bid amount, the bank has confirmed the sale, and the borrower seeks redemption after the publication of the auction notice.

## KEY FACTS OF THIS CASE

Bafna Motors (Mumbai) Pvt. Ltd. availed a credit facility of Rs. 100 crore from Union Bank of India, secured by a mortgage on land in Navi Mumbai. The account was classified as an NPA due to default. The bank issued a demand notice under Section 13(2) and conducted multiple failed auctions. A pending Securitisation Application (SA) challenging the demand notice and sale notice was already before the DRT. On June 27, 2023, the appellant, Celir LLP, emerged as the highest bidder in the 9th auction with a bid of Rs. 105.05 crore and paid the full amount by July 27, 2023. The bank confirmed the sale. The borrowers then filed a redemption application before the DRT and simultaneously filed a writ petition before the Bombay High Court, which allowed redemption upon payment of Rs. 129 crore. The bank, which had opposed redemption before the DRT, consented to the High Court's order.

## WHAT THE COURT DECIDED

The Supreme Court allowed the appeals filed by the auction purchaser and set aside the Bombay High Court's judgment. It held that the borrower's right of redemption was extinguished upon the publication of the auction notice. The auction purchaser, having paid the full bid amount, had a vested right to the asset. The bank was directed to issue the sale certificate to the appellant and hand over possession. The bank was ordered to refund the Rs. 129 crore paid by the borrowers for redemption. The appellant was directed to pay an additional Rs. 23.95 crore to the bank to match the higher offer.

## KEY QUOTE

Once the auction is confirmed and the entire bid amount is paid, the auction purchaser acquires a vested right to the secured asset.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `challenges_auction` is TRUE — the borrower is challenging the auction process
2. `auction_notice_published` is TRUE — the notice for public auction has been published in newspapers
3. `auction_conducted` is TRUE — the auction has been held
4. `auction_confirmed` is TRUE — the bank has confirmed the sale in favour of the highest bidder
5. `balance_consideration_paid` is TRUE — the auction purchaser has paid the full balance consideration
6. `right_of_redemption_extinguished` is TRUE — the borrower's right of redemption is extinguished upon publication of the auction notice
7. `sale_certificate_issued` is FALSE — the sale certificate has not yet been issued, but the obligation to issue it is triggered

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the auction purchaser has not paid the full balance consideration within the stipulated time (e.g., 90 days under Rule 9(4)) — in that scenario, E. Muthurathinasabathy applies and the sale is inchoate, allowing the borrower to redeem.
   SLRAI ROUTING: `balance_consideration_paid_within_90_days` = FALSE → E. Muthurathinasabathy applies; TRUE → Celir LLP applies.

2. When the auction notice has not yet been published — the borrower's right of redemption is still available under Section 13(8) to tender the dues.

3. When the bank's action is challenged before the auction is confirmed — the case would fall under pre-auction challenges, not post-finality sanctity.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002
Primary provision: Section 13(8) — "Where the amount of dues of the secured creditor together with all costs, charges and expenses incurred by him is tendered to the secured creditor at any time before the date of publication of notice for public auction or inviting quotations or tender from public or private treaty for transfer by way of lease, assignment or sale of the secured assets,— (i) the secured assets shall not be transferred by way of lease assignment or sale by the secured creditor; and (ii) in case, any step has been taken by the secured creditor for transfer by way of lease or assignment or sale of the assets before tendering of such amount under this sub-section, no further step shall be taken by such secured creditor for transfer by way of lease or assignment or sale of such secured assets."
Instrument level: ACT
Nature of provision: MANDATORY — court held the publication of the auction notice is the bright-line rule for extinguishing the right of redemption.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Valji Khimji and Company v. Official Liquidator of Hindustan Nitro Product (Gujarat) Ltd. and Ors. (2008) 9 SCC 299
  Established the principle that a confirmed auction sale can only be set aside on very limited grounds like fraud, to protect the sanctity of the auction process.

Distinguishes: Concern Readymix, rep. by its Proprietor, Smt. Y. Sunitha v. Authorised Officer, Corporation Bank and Anr. (2018 SCC OnLine Hyd 783)
  Concern Readymix held that the right of redemption continues until the issuance of the sale certificate. Celir LLP overrules this, holding that the right is extinguished upon publication of the auction notice.
  SLRAI ROUTING: if `right_of_redemption_extinguished` = TRUE upon `auction_notice_published` → Celir LLP applies; if FALSE → Concern Readymix applies.

Distinguishes: E. Muthurathinasabathy & Ors. v. M/s. Sri International & Ors. (2026 INSC 303)
  E. Muthurathinasabathy held that a sale is inchoate if the auction purchaser fails to pay the balance within 90 days, allowing redemption. Celir LLP applies when the sale is complete and the auction purchaser has paid in full.
  SLRAI ROUTING: if `balance_consideration_paid` = TRUE → Celir LLP applies; if FALSE → E. Muthurathinasabathy applies.

Affirms: Satyawati Tondon & Ors. v. United Bank of India (2010) 8 SCC 110
  Reaffirmed that the High Court should not entertain writ petitions under Article 226 when an effective alternative remedy under Section 17 of the SARFAESI Act is available.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: auction_confirmed
Type: FactEntry[bool]
Description: True if the bank has confirmed the sale in favour of the highest bidder
Module: M10
Extraction: From bank's confirmation letter or email

**B. New YAML Rule Needed:**
Module: M10
Rule ID: M10_C8_sale_confirmation_vested_right
Conditions: auction_confirmed=True AND balance_consideration_paid=True
Severity: FATAL
Message: "Auction purchaser has a vested right to the asset. The borrower's right of redemption is extinguished. The bank must issue the sale certificate under Rule 9(6)."
Judgment tag: ["Celir LLP"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: e_muthurathinasabathy.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add line: "Distinguished by: Celir LLP v. Bafna Motors (2023 INSC 838) — held that a confirmed sale with timely payment has statutory finality and the borrower's right of redemption is extinguished upon publication of the auction notice."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: AUCTION_PURCHASER
