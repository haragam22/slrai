---
citation: "2025:CHC-AS:1805-DB"
title: "Dr. Tushar Kanti Karmakar vs Shilabati Hospital Private Limited & Ors."
short_name: "Dr. Tushar Kanti Karmakar"
court: HIGH_COURT
high_court_state: "West Bengal"
bench_strength: 2
judgment_date: "2025-09-16"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["AUCTION_PURCHASER", "LIMITATION_EXPIRED", "PENDING_SA_CONCEALED"]
statutory_basis: RULES
act_sections: ["Section 13(8)"]
rules_sections: ["Rule 8(8)", "Rule 8(6)", "Rule 9(4)"]
slrai_modules: ["M3", "M10"]
keywords: ["Rule 8(8)", "private treaty", "parties in writing", "written agreement", "sale by private treaty", "amendment clarificatory", "borrower not party", "terms settled between parties", "secured creditor and purchaser", "no consent from borrower"]
retrieval_condition: "Applies when the bank sold secured property by private treaty without written agreement with borrower or guarantor, and Rule 8(8) was interpreted as requiring only agreement between secured creditor\u548cp"
source: HC_FULL_TEXT
ik_doc_id: "69232309"
ik_url: "https://indiankanoon.org/doc/69232309/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers alleged that the sale of the mortgaged property by private treaty to Dr. T.K. Karmakar was invalid because the bank failed to enter into a written agreement with all parties affected by the property, including the borrower and guarantor, as required under Rule 8(8) of the SARFAESI Rules, 2002. They contended that the term "parties" in Rule 8(8) includes the borrower and guarantor, and that the absence of their written consent rendered the sale wholly without jurisdiction. The prayer before the DRT/HC was to declare the sale void, cancel the sale, restore possession, and direct the bank to accept their revised payment schedule.

## HOLDING SUMMARY

Rule 8(8) of the Security Interest (Enforcement) Rules, 2002, which governs sale by private treaty, requires that terms be settled in writing only between the secured creditor (bank) and the proposed purchaser, not with the borrower or guarantor. The amendment to Rule 8(8) in 2016, which explicitly clarified that "parties" means the secured creditor and the proposed purchaser, is clarificatory and retrospective, confirming the legislative intent from the original enactment. The borrower’s right to object is satisfied by the 30-day notice under Rule 8(6), and failure to submit a superior offer constitutes deemed consent. A sale conducted in compliance with Rule 8(6) and Rule 8(8), as clarified, is valid and binding, and the borrower’s subsequent invocation of Article 226 is not maintainable after exhausting remedies under Section 17. This applies when: the bank sells by private treaty without written agreement with the borrower or guarantor, and the purchaser has fully paid the consideration.

## KEY FACTS OF THIS CASE

A hospital company and its directors (borrowers) took a term loan of Rs. 200 lakhs from State Bank of India in 2003, secured by two plots of land. The account was classified as NPA on 31.03.2004. After multiple failed public auctions, the bank received an offer from Dr. T.K. Karmakar to purchase the property for Rs. 200 lakhs via private treaty. The bank issued a 30-day sale notice to the borrower under Rule 8(6), inviting a better offer. The borrower responded with a counter-offer of Rs. 205 lakhs payable in 46 monthly instalments, which the bank rejected as commercially unviable. The sale to Dr. Karmakar was completed on 07.06.2010. The borrower challenged the sale before the DRT in 2010, but the application was dismissed. The High Court initially set aside the sale in 2018, but this judgment reversed that order.

## WHAT THE COURT DECIDED

The High Court allowed the appeals filed by the State Bank of India and Dr. T.K. Karmakar, setting aside the impugned orders of the Single Judge dated 11.12.2018, 30.09.2020, and 02.12.2020. The court held that the sale by private treaty was valid and in compliance with the SARFAESI Act and Rules. The borrower’s writ petition was dismissed, and the sale in favour of Dr. Karmakar was upheld. The interim orders restraining the purchaser from dealing with the property were vacated.

## KEY QUOTE

the term 'parties' under Rule 8(8) must be read as confined to the Bank and the proposed purchaser, the latter being a borrower, guarantor, or third party, if such person chooses to purchase the secured asset under private treaty.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `auction_type` is "private treaty" — the sale was conducted by private treaty, not public auction or tender
2. `auction_notice_affixed_on_property` is TRUE — the sale notice was affixed on the property
3. `newspaper_publication_done` is TRUE — the sale notice was published in two leading newspapers
4. `borrowers_served_notice` is TRUE — the borrower was served with the 30-day sale notice under Rule 8(6)
5. `auction_conducted_despite_stay` is FALSE — no stay order was in force during the sale
6. `pending_sa_existed_at_auction_date` is FALSE — no pending Section 17 application was concealed from the CMM
7. `balance_consideration_paid_within_90_days` is TRUE — the auction purchaser paid the balance consideration within 90 days of confirmation
8. `right_of_redemption_extinguished` is TRUE — the borrower failed to tender full dues before the sale

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the sale by private treaty was conducted without issuing a 30-day notice to the borrower under Rule 8(6) — in that case, *Mathew Varghese v. M. Amritha Kumar* applies, which mandates strict compliance with notice requirements.
   SLRAI ROUTING: if `borrowers_served_notice` = FALSE → Mathew Varghese applies.

2. When the bank concealed a pending Section 17 application while filing a Section 14 petition before the CMM — in that case, *Celir LLP v. Bafna Motors* applies, which holds such concealment as a fatal flaw.
   SLRAI ROUTING: if `pending_sa_existed_at_auction_date` = TRUE → Celir LLP applies.

3. When the auction purchaser failed to pay the balance 75% of the sale consideration within 90 days of confirmation — in that case, *E. Muthurathinasabathy* applies, which holds that such a sale remains inchoate and does not extinguish the borrower's right of redemption.
   SLRAI ROUTING: if `balance_consideration_paid_within_90_days` = FALSE → E. Muthurathinasabathy applies.

## STATUTORY CONTEXT

Primary law: Security Interest (Enforcement) Rules 2002  
Primary provision: Rule 8(8) — "Sale by any method other than public auction or public tender shall be on such terms as may be settled between the secured creditor and the proposed purchaser in writing."  
Instrument level: RULES  
Nature of provision: MANDATORY — the court held that the terms must be settled in writing between the secured creditor and the purchaser, and the 2016 amendment was clarificatory of the original intent.

Secondary provision: Rule 8(6) — requires a 30-day notice of sale to the borrower.  
Nature: MANDATORY — failure to serve notice invalidates the sale process.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Celir LLP v. Bafna Motors (2024) 2 SCC 1  
  Affirmed that a completed sale under SARFAESI confers statutory finality on the purchaser and extinguishes the borrower's right of redemption.  
  SLRAI ROUTING: if `auction_type` = "private treaty" AND `balance_consideration_paid_within_90_days` = TRUE → this judgment applies; if `auction_type` = "public auction" → Celir LLP applies.

Distinguishes: Mathew Varghese v. M. Amritha Kumar (2014) 5 SCC 610  
  Mathew Varghese was concerned with the failure to give 30-day notice under Rule 8(6) before a subsequent sale, not the interpretation of "parties" in Rule 8(8).  
  SLRAI ROUTING: if `borrowers_served_notice` = FALSE → Mathew Varghese applies; if TRUE → this judgment applies.

Distinguishes: E. Muthurathinasabathy (2026 INSC 303)  
  E. Muthurathinasabathy dealt with a sale where the balance consideration was paid after 90 days, rendering the sale inchoate. This case involves timely payment and a completed sale.  
  SLRAI ROUTING: if `balance_consideration_paid_within_90_days` = TRUE → this judgment applies; if FALSE → E. Muthurathinasabathy applies.

Affirmed: Dwarika Prasad v. State of U.P. (2018) 5 SCC 491  
  Reiterated that the right of redemption under Section 13(8) is extinguished upon a valid, completed sale to a third party.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**  
Field name: auction_type  
Type: FactEntry[str]  
Description: The method by which the secured asset was sold — "public auction", "public tender", "private treaty", "e-auction"  
Module: M3  
Extraction: From auction notice, sale certificate, or bank records

Field name: terms_settled_with_borrower  
Type: FactEntry[bool]  
Description: Whether the bank entered into a written agreement with the borrower regarding the sale terms  
Module: M3  
Extraction: From bank correspondence or sale documents

**B. New YAML Rule Needed:**  
Module: M3  
Rule ID: M3_C8_rule8_8_private_treaty  
Conditions: auction_type="private treaty" AND terms_settled_with_borrower=False  
Severity: INFO  
Message: "Sale by private treaty does not require written agreement with borrower or guarantor per Dr. Tushar Kanti Karmakar (2025:CHC-AS:1805-DB). Rule 8(8) requires agreement only between secured creditor and purchaser."  
Judgment tags: ["DR_TUSHAR_KANTI_KARMAKAR"]  
Statutory basis: RULES

**C. Existing Judgments to Update:**  
File: mathew_varghese_amritha_kumar.md  
Section: ## RELATIONSHIP TO OTHER JUDGMENTS  
Add: "Distinguished by: Dr. Tushar Kanti Karmakar (2025:CHC-AS:1805-DB) — held that Rule 8(8) does not require written agreement with borrower or guarantor for private treaty sale, and that the 2016 amendment is clarificatory."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: AUCTION_PURCHASER
