---
citation: "(2017) 4 MLJ 675"
title: "S.Shanmuganathan vs The Authorized Officer"
short_name: "S.Shanmuganathan"
court: HIGH_COURT
high_court_state: "Tamil Nadu"
bench_strength: 2
judgment_date: "2017-04-28"
overruled: false
overruled_by: null
distinguished_by: []
favor: BORROWER
favor_verified: true
ground_codes: ["AUCTION_PURCHASER", "AUCTION_NOTICE_AFFIXING", "NEWSPAPER_PUB_DEFECT"]
statutory_basis: RULES
act_sections: ["Section 13(4)", "Section 14"]
rules_sections: ["Rule 8(6)", "Rule 8(6)(a)", "Rule 8(6)(f)", "Rule 9(9)", "Rule 9(10)"]
slrai_modules: ["M3", "M10"]
keywords: ["Rule 8(6)", "encumbrances known to secured creditor", "pending litigations not disclosed", "as is where is", "free from encumbrances", "Rule 9(9)", "Rule 9(10)", "sale certificate", "vacant possession"]
retrieval_condition: "Applies when the bank failed to disclose pending litigations and encumbrances in the auction notice and the purchaser was not put in vacant possession."
source: HC_FULL_TEXT
ik_doc_id: "91487387"
ik_url: "https://indiankanoon.org/doc/91487387/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The petitioner, an auction purchaser, alleged that the bank failed to disclose the existence of pending civil suits and criminal proceedings relating to the title of the secured asset in the auction notice, despite being aware of them. He contended that the auction notice falsely represented that the property was free from encumbrances and that vacant possession would be delivered, inducing him to participate and pay the full sale consideration of Rs.62,00,000/-. He further argued that the bank violated Rule 8(6)(a) and Rule 8(6)(f) of the SARFAESI Rules by not disclosing material encumbrances and pending litigations. The petitioner claimed that due to the bank’s failure to deliver physical possession for over nine years and its suppression of material facts, he was entitled to a refund of the sale amount with interest.

## HOLDING SUMMARY

Rule 8(6)(a) and Rule 8(6)(f) of the Security Interest (Enforcement) Rules, 2002 impose a mandatory obligation on the secured creditor to disclose all encumbrances and other material facts, including pending litigations, in the auction notice to enable bidders to make informed decisions. The failure to disclose such information renders the auction process defective and unjust. When a bank conducts a sale while concealing known litigation and encumbrances, and fails to deliver vacant possession, the purchaser is entitled to seek refund of the sale consideration. The principle of caveat emptor does not absolve the bank of its statutory duty to disclose title defects within its knowledge. The bank’s conduct in suppressing material facts violates fairness and transparency expected from public sector institutions. This applies when: the bank failed to disclose known encumbrances or pending litigations in the auction notice and the purchaser was not put in vacant possession.

## KEY FACTS OF THIS CASE

The petitioner participated in a public auction conducted by Indian Overseas Bank on 21.06.2008 for a property mortgaged by a borrower, paying 25% of the bid amount (Rs.15.5 lakh) on the same day and the balance (Rs.46.5 lakh) by 24.07.2008. The bank had taken symbolic possession under Section 13(4) but was aware of two pending civil suits — O.S.No.4552/2006 (challenging the mortgage validity) and O.S.No.7998/2008 (title dispute) — neither of which were disclosed in the auction notice. Despite repeated assurances, the bank failed to deliver physical possession for nine years. A revised sale certificate was issued in 2014, but the petitioner ultimately sought refund due to unresolved litigation. The writ petition was filed in 2016 seeking refund with 24% interest.

## WHAT THE COURT DECIDED

The Madras High Court allowed the writ petition, holding that the bank’s failure to disclose pending litigations and encumbrances in the auction notice violated mandatory provisions of Rule 8(6)(a) and Rule 8(6)(f) of the SARFAESI Rules. The court directed the bank to refund the entire sale consideration of Rs.62,00,000/- with interest at 12% per annum from the date of deposit (24.07.2008) within four weeks. The bank was also granted liberty to cancel the sale certificate. The court rejected the bank’s argument that the purchaser should have conducted due diligence, emphasizing the bank’s statutory duty to disclose known encumbrances.

## KEY QUOTE

The Purchaser should be put on specific notice about all the encumbrances and other materials so as to enable him to take a conscious decision with regard to his participation in the auction and the amount to be quoted in his bid.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `newspaper_publication_done` is TRUE — auction notice was published in newspaper
2. `pending_sa_existed_at_auction_date` is TRUE — there were pending civil suits affecting title at the time of auction
3. `auction_notice_discloses_pending_sa` is FALSE — the auction notice did not disclose the pending litigations
4. `encumbrances_known_to_bank` is TRUE — the bank was aware of encumbrances or title disputes
5. `possession_given_to_auction_purchaser` is FALSE — the auction purchaser was not put in physical or vacant possession
6. `sa_applicant_type` is "AUCTION_PURCHASER" — the applicant in the SA/writ is the auction purchaser, not the borrower

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the auction notice explicitly disclosed all pending litigations and encumbrances — in such case, the purchaser is deemed to have participated with full knowledge and cannot claim refund on this ground.
   SLRAI ROUTING: if `auction_notice_discloses_pending_sa` = TRUE → this judgment does not apply; see *Jai Logistics* for disclosure-compliant cases.

2. When the applicant is the borrower challenging the auction on grounds unrelated to purchaser’s rights — this judgment protects auction purchasers, not borrowers.
   SLRAI ROUTING: if `sa_applicant_type` = "BORROWER" → this judgment does not apply; see *Kanaiyalal* or *Celir LLP* as applicable.

3. When the purchaser has already been put in physical possession — the core grievance of non-possession is absent.
   SLRAI ROUTING: if `possession_given_to_auction_purchaser` = TRUE → this judgment does not apply.

## STATUTORY CONTEXT

Primary law: Security Interest (Enforcement) Rules, 2002  
Primary provision: Rule 8(6)(a) — "the description of the immovable property to be sold, including the details of the encumbrances known to the secured creditor"  
Rule 8(6)(f) — "any other thing which the authorised officer considers it material for a purchaser to know, in order to judge the nature and value of the property"  
Rule 9(9) — "the authorised officer shall deliver the property to the purchaser free from encumbrances known to the secured creditor on deposit of money"  
Rule 9(10) — "the certificate of sale issued under sub-rule (6) shall specifically mention that whether the purchaser had purchased the immovable secured asset free from any encumbrances known to the secured creditor or not"  
Instrument level: RULES  
Nature of provision: MANDATORY — court held that disclosure is not a mere formality but a statutory obligation essential for fairness.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Jai Logistics vs. Authorised Officer, Syndicate Bank (2010) 4 CTC 627  
  Reaffirmed that Rule 8(6)(f) requires disclosure of encumbrances and that suppression invalidates the sale process.  
  SLRAI ROUTING: both judgments apply when `auction_notice_discloses_pending_sa` = FALSE.

Distinguishes: Sulochana Chandrakant Galande vs. Pune Municipal Transport (2010) 8 SCC 467  
  That case defined "encumbrance" as a charge on property; this case expands it to include pending litigations affecting title.  
  SLRAI ROUTING: if `pending_sa_existed_at_auction_date` = TRUE → this judgment applies; if only financial lien → *Sulochana* may apply.

Distinguishes: Mathew Varghese vs. M. Amritha Kumar (2014) 5 SCC 610  
  That case dealt with borrower’s right of redemption; this case concerns rights of auction purchasers.  
  SLRAI ROUTING: if `sa_applicant_type` = "BORROWER" → *Mathew Varghese* applies; if "AUCTION_PURCHASER" → this judgment applies.

Follows: Ambalavanan vs. Canara Bank (2016) — upheld entitlement to interest when sale is set aside and amount retained by bank.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: encumbrances_known_to_bank
Type: FactEntry[bool]
Description: True if the bank was aware of any legal encumbrances (e.g., pending suits, criminal cases) affecting the title of the secured asset
Module: M3
Computed from: Bank’s knowledge from counter affidavit or admission in SA

Field name: auction_notice_discloses_pending_sa
Type: FactEntry[bool]
Description: True if the auction notice explicitly mentions any pending civil or criminal proceedings affecting the property
Module: M3
Extraction: From auction notice document in SA file

**B. New YAML Rule Needed:**
Module: M3
Rule ID: M3_C8_pending_litigation_undisclosed
Conditions: pending_sa_existed_at_auction_date=True AND auction_notice_discloses_pending_sa=False
Severity: FATAL
Message: "Bank failed to disclose pending litigation in auction notice. Violation of Rule 8(6)(a) and (f). Auction purchaser may be entitled to refund."
Judgment tags: ["S_Shanmuganathan", "Jai_Logistics"]
Statutory basis: RULES

**C. Existing Judgments to Update:**
File: jai_logistics_syndicate_bank.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Followed by: S.Shanmuganathan (2017) 4 MLJ 675 — reaffirmed mandatory disclosure of pending litigations under Rule 8(6)(f) when known to secured creditor."

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: AUCTION_PURCHASER
