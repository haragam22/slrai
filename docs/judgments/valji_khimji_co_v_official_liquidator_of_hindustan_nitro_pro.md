---
citation: "(2008) 13 SCC 767"
title: "Valji Khimji & Co v. Official Liquidator of Hindustan Nitro Product (Gujarat) Ltd & Ors."
short_name: "Valji Khimji & Co"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2008-08-12"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["AUCTION_PURCHASER"]
statutory_basis: OTHER
act_sections: []
rules_sections: []
slrai_modules: ["M10"]
keywords: ["confirmed auction sale", "fraud exception", "inadequacy of price", "subsequent higher offer", "no fraud no setting aside"]
retrieval_condition: "Applies when a confirmed auction sale is challenged after confirmation based on a subsequent higher offer without any allegation of fraud."
source: SC_FULL_TEXT
ik_doc_id: "1792395"
ik_url: "https://indiankanoon.org/doc/1792395/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The respondents, including M/s. Manibhadra Sales Corporation and M/s. Castwell Alloys Limited, challenged the confirmation of the auction sale in favour of the appellant, arguing that the valuation of the assets was done as if they were scrap and that the company had intangible benefits such as sales tax exemptions and effluent treatment plant investments which were ignored. They contended that the sale price of Rs. 3.51 crores was inadequate compared to their subsequent offers of Rs. 3.75 crores and Rs. 5 crores, and that the assets should have been valued as a going concern. The prayer was to recall the order confirming the sale and direct a fresh sale at a higher price.

## HOLDING SUMMARY

A confirmed auction sale cannot be set aside merely on the ground of inadequacy of price or the emergence of a subsequent higher offer, in the absence of fraud, collusion, or procedural illegality. The Supreme Court emphasized that once a sale is confirmed by the competent authority—here, the High Court—rights vest in the auction purchaser, and such a sale acquires finality. The mere fact that a later bidder offers a higher amount does not justify reopening the sale, especially when the auction was conducted with adequate publicity and transparency. The Court rejected the argument that the assets were undervalued as scrap, noting no evidence that the valuation or advertisement described them as such. The principle from Divya Manufacturing Company (P) Ltd. was distinguished, as it applied only where fraud was evident. This applies when: a confirmed auction sale is challenged solely on the basis of a subsequent higher offer and no fraud is proven.

## KEY FACTS OF THIS CASE

Hindustan Nitro Product (Gujarat) Ltd. was placed under liquidation, and its assets were proposed for auction. The official liquidator obtained a valuation report estimating the assets at Rs. 2.55 crores. The auction was widely advertised, including in *The Economic Times*. On 25.3.2003, several bids were received, and the highest bid of Rs. 3.51 crores was made by Valji Khimji & Co. The High Court confirmed the sale on 30.7.2003, directing the purchaser to pay 25% within 30 days and the balance within three months, which was complied with. Over a year later, respondent No. 8 offered Rs. 3.75 crores and respondent No. 9 offered Rs. 5 crores, leading to applications to recall the sale. The Single Judge and later the Division Bench of the Gujarat High Court set aside the sale, prompting this appeal.

## WHAT THE COURT DECIDED

The Supreme Court allowed the appeal, set aside the impugned judgments of the Single Judge and Division Bench of the Gujarat High Court, and upheld the confirmation of the auction sale dated 30.7.2003 in favour of Valji Khimji & Co. The Court held that in the absence of fraud or collusion, a confirmed auction sale cannot be reopened merely because a higher offer emerged later. No order as to costs was passed.

## KEY QUOTE

If Court sales are too frequently adjourned with a view to obtaining a still higher price it may prove a self-defeating exercise, for industrialists will lose faith in the actual sale taking place.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when: a confirmed auction sale is challenged solely on the basis of a subsequent higher offer and no fraud is proven.

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the auction was conducted without adequate publicity or transparency — in such cases, *Divya Manufacturing Company (P) Ltd. v. Union Bank of India* (2000) 6 SCC 69 may apply, allowing setting aside of sale even post-confirmation due to fraud or irregularity.
   SLRAI ROUTING: if `newspaper_publication_done` = FALSE → Divya Manufacturing applies.

2. When the challenge is based on proven fraud, collusion, or suppression of material facts — this judgment does not protect a sale vitiated by fraud.
   SLRAI ROUTING: if `fraud_alleged` = TRUE and substantiated → Divya Manufacturing applies.

3. When the sale has not yet been confirmed by the competent authority — prior to confirmation, the sale remains tentative and can be reconsidered.
   SLRAI ROUTING: if `sale_certificate_issued` = FALSE → pre-confirmation rules apply; this judgment does not.

## STATUTORY CONTEXT

Primary law: Companies Act, 1956 (relevant provisions on liquidation and sale of assets by Official Liquidator)
Primary provision: Section 529A and related provisions governing liquidation sales (not explicitly quoted, but contextually applicable)
Instrument level: OTHER
Nature of provision: N/A (this judgment is based on equitable principles and judicial precedent rather than a specific SARFAESI provision)
[Text from training — verify against official source]

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: M/s Kayjay Industries (P) Ltd. v. M/s Asnew Drums (P) Ltd & Ors. (1974) SCC 213
  Affirmed the principle that mere inadequacy of price cannot invalidate a court-confirmed sale.
  SLRAI ROUTING: supports finality of confirmed sales in absence of fraud.

Distinguishes: Divya Manufacturing Company (P) Ltd. v. Union Bank of India (2000) 6 SCC 69
  Divya Manufacturing allowed setting aside a confirmed sale due to proven manipulation and escalation of price under court intervention.
  This case is distinguishable because no fraud or manipulation was found.
  SLRAI ROUTING: if `fraud_alleged` = TRUE → Divya Manufacturing applies; if FALSE → Valji Khimji applies.

Affirmed: General principle of finality of confirmed sales in commercial auctions
  Reinforced that certainty in auction outcomes is essential to maintain investor confidence.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: fraud_alleged
Type: FactEntry[bool]
Description: True if the SA or application alleges fraud, collusion, or suppression in the auction process
Module: M10
Extraction: From borrower’s SA or petition — presence of terms like "fraud", "collusion", "undervaluation", "conspiracy"

**B. New YAML Rule Needed:**
Module: M10
Rule ID: M10_C8_confirmed_sale_finality
Conditions: sale_certificate_issued=True AND fraud_alleged=False
Severity: FATAL
Message: "A confirmed auction sale cannot be set aside merely on grounds of subsequent higher offers or inadequacy of price in absence of fraud. Challenge is not maintainable."
Judgment tag: ["Valji_Khimji_Co"]
Statutory basis: OTHER

**C. Existing Judgments to Update:**
File: divya_manufacturing_p_ltd_v_union_bank_of_india.md
Section: ## CONDITION: WHEN THIS JUDGMENT APPLIES
Add: "Also applies when `fraud_alleged` = TRUE and substantiated by evidence of manipulation or procedural illegality in a confirmed auction."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: AUCTION_PURCHASER
