---
citation: "2018 (15) SCC 99"
title: "ITC Limited vs Blue Coast Hotels Ltd."
short_name: "ITC Blue Coast"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2018-03-19"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["REPLY_NOT_GIVEN", "SERVICE_DEFECT", "POSSESSION_DEFECT", "AUCTION_PURCHASER"]
statutory_basis: ACT
act_sections: ["Section 13(2)", "Section 13(3A)", "Section 13(4)", "Section 14", "Section 31(i)"]
rules_sections: []
slrai_modules: ["M1", "M2", "M3", "M10"]
keywords: ["Section 13(3A)", "no reply to objection", "symbolic possession", "agricultural land", "secured creditor status", "Section 14 application", "without prejudice", "fraud and collusion", "transfer of rights"]
retrieval_condition: "Applies when the secured creditor took symbolic possession and transferred the asset to the auction purchaser before obtaining physical possession, and the borrower claims the creditor ceased to be a "
source: SC_FULL_TEXT
ik_doc_id: "124691580"
ik_url: "https://indiankanoon.org/doc/124691580/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower, Blue Coast Hotels Ltd., challenged the enforcement proceedings initiated by IFCI, arguing that the creditor failed to reply to its representation dated 27.05.2013 under Section 13(3A) of the SARFAESI Act, rendering the entire process illegal. They contended that the creditor’s failure to communicate reasons for non-acceptance of the representation invalidated subsequent actions. The borrower further alleged that the mortgaged property included agricultural land, which is exempt from SARFAESI enforcement under Section 31(i), and that symbolic possession taken by the creditor was insufficient to enable a valid sale. They also claimed that the creditor, having transferred the asset to ITC Ltd., ceased to be a secured creditor and thus lacked locus to apply under Section 14 for physical possession. The prayer was to set aside the auction sale and all enforcement steps.

## HOLDING SUMMARY

Section 13(3A) of the SARFAESI Act imposes a mandatory duty on the secured creditor to consider and respond to a borrower’s representation with reasons, but non-compliance does not automatically invalidate enforcement if the creditor has in substance considered the borrower’s proposals through negotiations. The Court held that where the borrower repeatedly sought time extensions and induced the creditor into negotiations, equitable relief under Article 226 is denied due to unclean hands. The inclusion of agricultural land in the security interest does not vitiate proceedings if the land is not used for agriculture and the mortgage covers a commercial property. Symbolic possession under Section 13(4) is legally valid, and the secured creditor retains status as a secured creditor even after transferring the asset to the auction purchaser, enabling it to apply under Section 14 for physical possession. A sale conducted through public auction, with full payment, cannot be invalidated on grounds of fraud or collusion merely because the auction purchaser was aware of pending disputes. This applies when: the creditor failed to formally reply under Section 13(3A) but substantively considered the borrower’s proposals through negotiations and the borrower acted in bad faith.

## KEY FACTS OF THIS CASE

Blue Coast Hotels Ltd. availed a corporate loan of Rs. 150 crores from IFCI, secured by a mortgage on a five-star hotel property in Goa, including parcels of land classified as agricultural in revenue records. The account was declared NPA as of 30.09.2012. A demand notice under Section 13(2) was issued on 26.03.2013. The borrower responded on 27.05.2013 with a proposal for rescheduling. IFCI did not issue a formal written reply under Section 13(3A). On 18.06.2013, IFCI took symbolic possession. Multiple auction attempts were made, with the final sale to ITC Ltd. on 25.02.2015. The creditor applied under Section 14 for physical possession on the same day. The borrower challenged the sale in the Bombay High Court, which set aside the proceedings on grounds of non-compliance with Section 13(3A), inclusion of agricultural land, and lack of secured creditor status. The Supreme Court reversed the High Court’s decision.

## WHAT THE COURT DECIDED

The Supreme Court set aside the Bombay High Court’s judgment and upheld the validity of the auction sale to ITC Ltd. It held that the creditor’s failure to formally reply under Section 13(3A) did not invalidate the proceedings, given the borrower’s conduct in seeking repeated extensions and negotiating in bad faith. The Court affirmed that symbolic possession is valid and that the creditor remained a secured creditor entitled to apply under Section 14. The auction sale was upheld, and the borrower was directed to hand over physical possession to the auction purchaser within six months.

## KEY QUOTE

Non-compliance of sub-section (3A) of Section 13 cannot be of any avail to the debtor whose conduct has been merely to seek time and not repay the loan as promised on several occasions.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `objection_filed` is TRUE — the borrower filed an objection under Section 13(3A)
2. `bank_reply_given` is FALSE — the secured creditor did not formally reply to the objection
3. `bank_reply_gives_reasons` is FALSE — no reasons were communicated for non-acceptance
4. `borrower_conducted_negotiations` is TRUE — the borrower engaged in negotiations, submitted cheques, and gave undertakings
5. `unclean_hands_evident` is TRUE — the borrower repeatedly sought time extensions without repayment and induced delay
6. `possession_taken_date` is not null — symbolic possession was taken under Section 13(4)
7. `sale_certificate_issued` is TRUE — the asset was transferred to the auction purchaser
8. `secured_creditor_applied_section_14` is TRUE — the creditor applied for physical possession under Section 14

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the secured creditor completely ignored the borrower’s representation and took no steps to consider it — in that case, *Kanaiyalal Lalchand Sachdev v. State of Maharashtra* applies, and the enforcement action is void.
   SLRAI ROUTING: if `objection_filed` = TRUE AND `bank_reply_given` = FALSE AND `borrower_conducted_negotiations` = FALSE → Kanaiyalal applies.

2. When the mortgaged agricultural land is actively used for cultivation and not part of a commercial property — in that case, *Kunjabai Saheb v. State of Kerala* applies, and Section 31(i) bars enforcement.
   SLRAI ROUTING: if `property_classification` = "agricultural" AND `lease_predates_mortgage` = FALSE → Kunjabai Saheb applies.

3. When the auction purchaser is a related party or there is evidence of bid manipulation — in that case, *Celir LLP v. Bafna Motors* applies, and fraud can vitiate the sale.
   SLRAI ROUTING: if `auction_purchaser_related_to_creditor` = TRUE → Celir LLP applies.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002  
Primary provision: Section 13(3A) — "If, on receipt of the notice under sub-section (2), the borrower makes any representation or raises any objection, the secured creditor shall consider such representation or objection and if the secured creditor comes to the conclusion that such representation or objection is not acceptable or tenable, he shall communicate within fifteen days of receipt of such representation or objection the reasons for non-acceptance of the representation or objection to the borrower."  
Instrument level: ACT  
Nature of provision: MANDATORY — court held the duty to consider and communicate reasons is mandatory, but non-compliance may be excused based on equitable principles and borrower conduct.

Secondary: Section 31(i) — "The provisions of this Act shall not apply to any security interest created in agricultural land."  
Nature: MANDATORY — but the character of land is determined by actual use, not revenue classification.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Mardia Chemicals Ltd. v. Union of India (2004) 4 SCC 311  
  Affirmed that Section 13(3A) requires meaningful consideration of borrower’s objections and communication of reasons, but non-compliance does not automatically invalidate proceedings.

Distinguishes: Kanaiyalal Lalchand Sachdev v. State of Maharashtra (2019) 1 SCC 1  
  Kanaiyalal held that non-reply to Section 13(3A) objection renders the enforcement void. Here, the Court distinguished on grounds of equitable conduct — the borrower’s bad faith negated relief.  
  SLRAI ROUTING: if `objection_filed` = TRUE AND `bank_reply_given` = FALSE AND `unclean_hands_evident` = TRUE → ITC Blue Coast applies; if FALSE → Kanaiyalal applies.

Distinguishes: Celir LLP v. Bafna Motors (2024) 2 SCC 1  
  Celir LLP held that a confirmed sale has statutory finality. Here, the sale was challenged on creditor’s status post-transfer. This judgment upholds the creditor’s right to apply under Section 14.  
  SLRAI ROUTING: if `challenges_auction` = TRUE AND `fraud_alleged` = TRUE → Celir LLP applies; if `challenges_section_14_application` = TRUE → ITC Blue Coast applies.

Affirmed: State of Maharashtra v. Digambar (1995) 4 SCC 683  
  Reaffirmed that High Court relief under Article 226 is discretionary and denied to those with unclean hands.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: borrower_conducted_negotiations  
Type: FactEntry[bool]  
Description: True if borrower submitted proposals, cheques, or undertakings post-13(2) notice  
Module: M2  

Field name: unclean_hands_evident  
Type: FactEntry[bool]  
Description: Computed — True if borrower sought time extensions, gave dishonored cheques, and failed to repay  
Module: M2  

Field name: secured_creditor_applied_section_14  
Type: FactEntry[bool]  
Description: True if secured creditor applied under Section 14 after symbolic possession and sale  
Module: M3  

**B. New YAML Rule Needed:**
Module: M2  
Rule ID: M2_C3_13_3A_no_reply_but_negotiations  
Conditions: objection_filed=True AND bank_reply_given=False AND unclean_hands_evident=True  
Severity: WARNING  
Message: "Creditor failed to reply under Section 13(3A), but borrower engaged in negotiations and acted in bad faith. Enforcement may still be upheld per ITC Blue Coast."  
Judgment tags: ["ITC_BLUE_COAST"]  
Statutory basis: ACT  

**C. No New Ground Codes Needed**  
The arguments fit within existing codes: REPLY_NOT_GIVEN, POSSESSION_DEFECT, AUCTION_PURCHASER.

**D. Existing Judgments to Update:**
File: kanaiyalal_lalchand_sachdev.md  
Section: ## RELATIONSHIP TO OTHER JUDGMENTS  
Add line: "Distinguished by: ITC Blue Coast (2018) 15 SCC 99 — held that non-reply under Section 13(3A) may not invalidate enforcement if borrower acted in bad faith and engaged in dilatory negotiations."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: REPLY_NOT_GIVEN
