---
citation: "(2021) ibclaw.in 11067 Mad"
title: "The South Indian Bank Limited vs The Sub-Registrar on 31 March, 2021"
short_name: "South Indian Bank v. Sub-Registrar"
court: HIGH_COURT
high_court_state: "Tamil Nadu"
bench_strength: 1
judgment_date: "2021-03-31"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["AUCTION_PURCHASER"]
statutory_basis: ACT
act_sections: ["Section 13(8)", "Section 31B"]
rules_sections: []
slrai_modules: ["M10"]
keywords: ["sale certificate registration", "secured creditor priority", "Section 31B", "notwithstanding clause", "attachment before judgment", "mortgage prior to attachment", "interim attachment", "encumbrance certificate", "right of secured creditor", "subsequent attachment"]
retrieval_condition: "Applies when a sale certificate issued under SARFAESI is refused registration due to a subsequent attachment order in arbitration or civil proceedings."
source: HC_FULL_TEXT
ik_doc_id: "172198139"
ik_url: "https://indiankanoon.org/doc/172198139/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower did not file a claim in this case. The challenge arose from the refusal of the Sub-Registrar to register the sale certificate issued in favour of the auction purchaser due to a prior interim attachment order passed by an Arbitrator in proceedings to which the bank was not a party. The 2nd respondent (Equitas SFB), as an unsecured creditor, had obtained an interim attachment order on 23.04.2018, which was reflected in the encumbrance certificate. The Sub-Registrar relied on this attachment to refuse registration of the sale certificate, effectively allowing a subsequent encumbrance to override the secured creditor’s rights under SARFAESI.

## HOLDING SUMMARY

A sale certificate issued by a secured creditor under the SARFAESI Act cannot be refused registration by a Sub-Registrar solely on the ground of a subsequent attachment order, even if passed by a civil court or arbitral tribunal. The rights of a secured creditor under SARFAESI, especially after the introduction of Section 31B of the RDDBFI Act (via the 2016 Amendment), have statutory primacy over all other debts and claims, including those arising from interim orders in arbitration. The "notwithstanding anything contained in any other law" clause in Section 31B establishes the supremacy of secured creditors’ rights to realise assets. A prior mortgage and valid auction sale under SARFAESI render any subsequent attachment ineffective against the bank’s rights. This applies when: a sale certificate is refused registration due to a subsequent attachment order despite the bank having a prior mortgage and completed SARFAESI sale.

## KEY FACTS OF THIS CASE

The South Indian Bank had a loan outstanding against M/s. Shree Sharavana Traders, secured by a memorandum of deposit of title deeds dated 14.12.2015 for 64 cents of land in Madurai. The account turned NPA, and the bank conducted a valid SARFAESI auction, issuing a sale certificate in favour of the 6th respondent (auction purchaser). However, on 23.04.2018, Equitas SFB (2nd respondent), an unsecured creditor, obtained an interim attachment order from an Arbitrator, which the Sub-Registrar recorded in the encumbrance register. Based on this, the Sub-Registrar refused to register the bank’s sale certificate. The bank challenged this refusal in writ, arguing its prior secured status and statutory rights under SARFAESI and Section 31B.

## WHAT THE COURT DECIDED

The Madras High Court allowed the writ petition, set aside the Sub-Registrar’s refusal dated 26.05.2020, and directed the Sub-Registrar to register the sale certificate in favour of the auction purchaser, provided all other formalities were met. The court held that the subsequent attachment order could not override the secured creditor’s statutory rights under SARFAESI and Section 31B of the RDDBFI Act. The encumbrance based on the attachment was declared ineffective against the bank’s prior mortgage and completed enforcement action.

## KEY QUOTE

The preponderance of judicial opinion leads to the irresistible conclusion that the sale of the mortgaged property in favour of the auction purchaser and the sale certificate under the SARFAESI Act in such circumstances is free of all encumbrances.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `sale_certificate_issued` is TRUE — a sale certificate has been issued by the secured creditor
2. `auction_notice_affixed_on_property` is TRUE — the auction notice was properly affixed
3. `newspaper_publication_done` is TRUE — the auction was published in newspapers
4. `mortgage_date` is not null — the mortgage was created prior to any attachment
5. `mortgage_date` < `drt_stay_order_date` or `mortgage_date` < `ibc_moratorium_active` — the mortgage predates any competing claim or order
6. `challenges_auction` is TRUE — the challenge is to the auction or its registration
7. `prayer_scope_covers_current_measure` is TRUE — the prayer includes registration of sale certificate

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the mortgage was created after the attachment order — in that case, the attachment may have priority, and this judgment does not apply.
   SLRAI ROUTING: if `mortgage_date` > `drt_stay_order_date` → attachment may prevail; this judgment does not apply.

2. When the SARFAESI proceedings themselves are challenged on procedural grounds (e.g., defective notice, no reply to 13(3A)) — this judgment assumes valid proceedings and only addresses third-party attachment interference.
   SLRAI ROUTING: if `notice_service_mode` is defective → Kanaiyalal or similar applies, not this case.

## STATUTORY CONTEXT

Primary law: Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002  
Primary provision: Section 13(8) — "The borrower shall have the right to redeem the secured asset before the date fixed for sale or transfer of the right, title and interest in the asset..."  
Secondary provision: Section 31B, Recovery of Debts Due to Banks and Financial Institutions Act, 1993 — "Notwithstanding anything contained in any other law for the time being in force, the rights of secured creditors to realise secured debts... shall have priority..."  
Instrument level: ACT  
Nature of provision: MANDATORY — the "notwithstanding" clause makes the priority absolute and overriding.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Indian Overseas Bank v. Sub-Registrar (2018 SCC Online Mad 5016)  
  Affirmed that Section 31B gives secured creditors priority over all other claims, including government dues and civil court attachments.

Follows: R. Ramesh v. Sub-Registrar, Budalur (W.P(MD) No. 8407 of 2020)  
  Reinforced that a prior mortgage prevails over a subsequent interim attachment in arbitration.

Follows: Tamil Nadu Merchantile Bank Ltd. v. Joint-I Sub Registrar (W.P(MD) Nos. 6976 & 1101 of 2021)  
  Held that a secured creditor’s sale certificate cannot be denied registration due to a later attachment, especially when the mortgage was prior.

Distinguishes: Celir LLP v. Bafna Motors (2024) 2 SCC 1  
  Celir LLP dealt with finality of auction upon confirmation; this case deals with third-party attachment blocking registration.  
  SLRAI ROUTING: if `challenges_auction` = TRUE and `prayer` = "registration refusal" → this judgment applies; if `challenges_sale` = TRUE on procedural grounds → Celir LLP may apply.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**  
Field name: drt_stay_order_date  
Type: FactEntry[date]  
Description: Date of any stay order issued by DRT, DRAT, or civil court that creates an encumbrance  
Module: M10  
Computed from: Extract from encumbrance certificate or court order

Field name: mortgage_date  
Type: FactEntry[date]  
Description: Date when the mortgage or deposit of title deeds was created and registered  
Module: M10  
Computed from: Registered document date of MoD or DoTD

**B. New YAML Rule Needed:**  
Module: M10  
Rule ID: M10_C8_subsequent_attachment  
Conditions: sale_certificate_issued=True AND mortgage_date < drt_stay_order_date  
Severity: FATAL  
Message: "Sale certificate cannot be refused registration due to a subsequent attachment order. Secured creditor’s rights under Section 31B prevail."  
Judgment tag: ["SOUTH_INDIAN_BANK_V_SUB_REGISTRAR"]  
Statutory basis: ACT

**C. Existing Judgments to Update:**  
File: indian_overseas_bank_v_sub_registrar.md  
Section: ## RELATIONSHIP TO OTHER JUDGMENTS  
Add: "Followed by: South Indian Bank v. Sub-Registrar (2021) — reaffirmed that subsequent attachment cannot block registration of SARFAESI sale certificate."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: AUCTION_PURCHASER
