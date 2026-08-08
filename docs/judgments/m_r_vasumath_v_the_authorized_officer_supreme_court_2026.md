---
citation: "2026 INSC 633"
title: "M. R. Vasumathi vs The Authorized Officer & Ors."
short_name: "M.R. Vasumathi"
court: SUPREME_COURT
high_court_state: null
bench_strength: 1
judgment_date: "2026-06-09"
overruled: false
overruled_by: null
distinguished_by: []
favor: BORROWER
favor_verified: true
ground_codes: ["AUCTION_GAP_DEFECT", "REPLY_NOT_GIVEN", "VALUATION_DISPUTE"]
statutory_basis: RULES
act_sections: ["Section 13(2)", "Section 13(4)", "Section 2(ha)"]
rules_sections: ["Rule 9(3)", "Rule 9(4)", "Rule 9(5)", "Rule 8(5)"]
slrai_modules: ["M3", "M1", "M6"]
keywords: ["Rule 9(3)", "Rule 9(4)", "balance 75% payment", "15-day confirmation", "immediate deposit 25%", "written agreement extension", "forfeiture on default", "valuation by borrower", "fraudulent valuation", "delay in balance payment"]
retrieval_condition: "Applies when the auction purchaser paid the balance 75% of sale consideration after the 15-day confirmation period without a written agreement for extension under Rule 9(4)."
source: SC_FULL_TEXT
ik_doc_id: "133020478"
ik_url: "https://indiankanoon.org/doc/133020478/"
has_verified_conditions: false
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower (legal heir of the deceased guarantor) alleged that the auction sale conducted on 11.03.2010 was vitiated due to non-compliance with Rule 9(3) and Rule 9(4) of the SARFAESI Rules, as the auction purchaser failed to deposit 25% immediately on the date of sale and paid the balance 75% only on 31.03.2010 — beyond the mandatory 15-day period from confirmation of sale. They contended that the secured creditor unilaterally waived the delay without a written agreement between the parties, rendering the sale void. They further alleged that the valuation report was fraudulently obtained from the original borrower, violating Rule 8(5), and that only a portion of the property should have been sold to satisfy the debt. The prayer was to set aside the auction sale and allow redemption of the secured asset.

## HOLDING SUMMARY

Rule 9(3) and Rule 9(4) of the Security Interest (Enforcement) Rules, 2002 are mandatory provisions governing the deposit of 25% of the sale price immediately on the date of sale and the payment of the remaining 75% within 15 days of confirmation of sale, or within an extended period agreed upon in writing between the parties. The failure to comply with these timelines, in the absence of a demonstrable written agreement extending the period, renders the auction sale legally invalid and subject to being set aside. The secured creditor cannot unilaterally waive the statutory timeline without mutual written consent. While the provisions are mandatory, they may be waived by the parties for whose benefit they are intended, but such waiver must be evidenced. The sale certificate issued without compliance does not confer finality. This applies when: the balance 75% was paid after the 15-day confirmation period and no written agreement for extension exists between the secured creditor and auction purchaser.

## KEY FACTS OF THIS CASE

A loan was availed in 1984 by S. Murugesan, secured by a mortgage from guarantor G. Ramanujam. A preliminary decree for recovery was passed in 1997. After G. Ramanujam’s death in 2001, his heirs failed to settle the dues. The secured creditor issued a Section 13(2) demand notice in 2009 and conducted an auction on 11.03.2010, where the auction purchaser paid 25% on 10.03.2010/11.03.2010 but the balance 75% only on 31.03.2010 — beyond the 15-day confirmation period. The DRT, DRAT, and Madras High Court upheld the sale. The heirs challenged the auction, arguing procedural non-compliance, and the Supreme Court ultimately quashed the sale.

## WHAT THE COURT DECIDED

The Supreme Court allowed the appeal in part, setting aside the impugned judgment of the High Court and the orders of the DRAT and DRT. The auction sale of 11.03.2010 was quashed due to non-compliance with Rule 9(4) timelines and absence of a written extension agreement. The auction purchaser was entitled to a refund of the entire amount deposited with 7% interest from the respective dates of deposit. The appellant (legal heir) was granted a one-time opportunity to redeem the mortgaged property by paying Rs. 95,42,372.52 plus 5% interest from the date of the Section 13(2) notice. If redemption is not completed within the stipulated time, the asset may be re-auctioned after a fresh valuation.

## KEY QUOTE

The balance amount of purchase price payable shall be paid by the purchaser to the authorised officer on or before the fifteenth day of confirmation of sale of the immovable property or such extended period as may be agreed upon in writing between the parties.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `auction_date` is not null — auction was conducted on a specific date
2. `confirmation_of_sale_date` is not null — sale was confirmed, triggering Rule 9(4) timeline
3. `balance_payment_date` is after (`confirmation_of_sale_date` + 15 days) — balance 75% paid beyond 15-day period
4. [PENDING FIELD] `written_agreement_for_extension` is FALSE — no written agreement between secured creditor and auction purchaser extending the payment period
5. `sale_certificate_issued` is TRUE — certificate issued despite non-compliance

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the auction purchaser paid the balance 75% within 15 days of confirmation of sale — in that case, the sale is valid and no defect arises.
   SLRAI ROUTING: `balance_payment_date` <= (`confirmation_of_sale_date` + 15 days) → no Rule 9(4) violation.

2. When a valid written agreement extending the payment period was executed between the secured creditor and the auction purchaser — in such case, IDBI Bank Ltd. v. Ramswaroop Daliya (2024) applies and the extension is valid.
   SLRAI ROUTING: `written_agreement_for_extension` = TRUE → extension valid.

3. When the delay in payment was due to court stay or force majeure and the secured creditor acted in good faith — equitable considerations may apply, but this judgment focuses on absence of written agreement.

## STATUTORY CONTEXT

Primary law: Security Interest (Enforcement) Rules, 2002  
Primary provision: Rule 9(4) — "The balance amount of purchase price payable shall be paid by the purchaser to the authorised officer on or before the fifteenth day of confirmation of sale of the immovable property or such extended period as may be agreed upon in writing between the parties."  
Instrument level: RULES  
Nature of provision: MANDATORY — court held the timeline is mandatory but waivable only by mutual written agreement.

Secondary: Rule 9(3) — "On every sale of immovable property, the purchaser shall immediately pay a deposit of twenty-five % of the amount of the sale price... in default of such deposit, the property shall forthwith be sold again."  
Nature: MANDATORY — immediate deposit required, failure triggers resale.

Tertiary: Rule 8(5) — Valuation report must be obtained by the authorised officer, not from the borrower.  
Nature: MANDATORY — valuation by borrower violates procedure.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: IDBI Bank Ltd. v. Ramswaroop Daliya (2024 SCC OnLine SC 2878)  
  Confirmed that Rule 9(4) period is extendable only by written agreement between parties; mere unilateral waiver by secured creditor is insufficient.

Distinguishes: Celir LLP v. Bafna Motors (2024) 2 SCC 1  
  Celir LLP upheld sale finality when balance was paid timely and certificate issued. Here, payment was delayed without written extension, so sale is void.  
  SLRAI ROUTING: if `balance_payment_date` <= (`confirmation_of_sale_date` + 15 days) → Celir LLP applies; if not and no written agreement → M.R. Vasumathi applies.

Follows: Sri Siddeshwara Cooperative Bank Ltd. v. Ikbal (2013) 10 SCC 83  
  Affirmed that Rule 9(3) and (4) are mandatory and for benefit of secured creditor, hence waivable — but waiver must be mutual and in writing.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: confirmation_of_sale_date  
Type: FactEntry[date]  
Description: Date on which the secured creditor confirmed the auction sale, triggering the 15-day period under Rule 9(4)  
Module: M3  
Extraction: From bank's confirmation letter or auction minutes

Field name: written_agreement_for_extension  
Type: FactEntry[bool]  
Description: Whether a written agreement between secured creditor and auction purchaser exists to extend the Rule 9(4) payment period  
Module: M3  
Extraction: From bank records or auction purchaser's application for extension

**B. New YAML Rule Needed:**
Module: M3  
Rule ID: M3_C5_rule9_4_extension_missing  
Conditions: balance_payment_date > (confirmation_of_sale_date + 15 days) AND written_agreement_for_extension = False  
Severity: FATAL  
Message: "Balance 75% paid after 15-day confirmation period without written extension agreement. Auction sale is void under M.R. Vasumathi (2026 INSC 633)."  
Judgment tag: ["M.R._Vasumathi"]  
Statutory basis: RULES

**C. Existing Judgments to Update:**
File: celir_llp_bafna_motors.md  
Section: ## RELATIONSHIP TO OTHER JUDGMENTS  
Add: "Distinguished by: M.R. Vasumathi (2026 INSC 633) — held that a sale where balance payment was made after 15-day confirmation period without written extension agreement is void, unlike Celir LLP where timely payment ensured finality."

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: AUCTION_GAP_DEFECT
