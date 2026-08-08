---
citation: "2025 INSC 1137"
title: "M. Rajendran vs M/S Kpk Oils And Proteins India Pvt. Ltd"
short_name: "M. Rajendran"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2025-09-22"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["RIGHT_OF_REDEMPTION", "AUCTION_PURCHASER"]
statutory_basis: ACT
act_sections: ["Section 13(8)"]
rules_sections: []
slrai_modules: ["M10"]
keywords: ["Section 13(8)", "publication of notice", "right of redemption", "amended Section 13(8)", "auction notice", "date of publication", "Rule 8(6)", "Rule 9(1)", "composite notice", "30-day gap"]
retrieval_condition: "Applies when the borrower seeks to redeem after the publication of auction notice under Section 13(8) of the SARFAESI Act."
source: SC_FULL_TEXT
ik_doc_id: "47367203"
ik_url: "https://indiankanoon.org/doc/47367203/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers alleged that they retained the right to redeem the mortgaged property under Section 13(8) of the SARFAESI Act even after the auction sale, as they had tendered the full outstanding dues to the bank. They contended that the right of redemption, as a constitutional right under Article 300-A, survives until the sale is fully completed by a registered deed, relying on the pre-amendment interpretation in Mathew Varghese v. Amritha Kumar. They further argued that the 2016 amendment to Section 13(8) does not have retrospective effect, and since their loan was availed before the amendment, the unamended provision should apply. The prayer before the High Court was to quash the sale certificate and permit redemption.

## HOLDING SUMMARY

The Supreme Court held that the 2016 amendment to Section 13(8) of the SARFAESI Act drastically curtails the borrower's right of redemption, which now stands extinguished upon the publication of the auction notice. The Court clarified that the right to redeem is available only before the date of publication of the notice for public auction or invitation of quotations, and not until the completion of the sale by a registered deed. This interpretation overrides the general law under Section 60 of the Transfer of Property Act, as the SARFAESI Act is a special statute with an overriding effect under Section 35. The decision in Bafna Motors (2024) was affirmed, establishing that the auction purchaser acquires a vested right upon confirmation of sale, and the bank cannot withhold the sale certificate to allow redemption. This applies when: the auction notice has been published and the borrower tenders payment after that date.

## KEY FACTS OF THIS CASE

The borrowers, M/S KPK Oils and Proteins India Pvt. Ltd., availed credit facilities of Rs. 5 crore and a term loan of Rs. 30 lakh from the bank on 06.01.2016, secured by an equitable mortgage over immovable property. The account was classified as NPA on 31.12.2019. A demand notice under Section 13(2) was issued on 12.02.2020. After possession and auction notices, an e-auction was conducted on 26.02.2021, where the appellants (auction purchasers) emerged as the highest bidders and deposited the full sale consideration of Rs. 1,25,60,000 by 20.03.2021. The bank issued a sale certificate on 22.03.2021. The borrowers, who had not filed any objection under Section 13(3A), later paid substantial amounts towards the loan and challenged the sale certificate in the Madras High Court, which allowed their writ petition. The auction purchasers appealed to the Supreme Court.

## WHAT THE COURT DECIDED

The Supreme Court allowed the appeals filed by the auction purchasers and set aside the judgment of the Madras High Court. It held that the borrowers' right to redeem was extinguished upon the publication of the auction notice on 22.01.2021, and their subsequent tender of payment was invalid. The sale certificate issued to the auction purchasers was upheld, and the bank was directed to transfer possession of the secured asset. The Court dismissed the borrowers' contention that the right of redemption survives until the sale deed is registered, affirming the sanctity of the auction process and the vested rights of the auction purchaser.

## KEY QUOTE

The amended provisions of Section 13(8) of the Sarfaesi Act, make it clear that the right of the borrower to redeem the secured asset stands extinguished thereunder on the very date of publication of the notice for public auction under Rule 9(1) of the 2002 Rules.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `challenges_auction` is TRUE — the borrower is challenging the auction sale
2. `auction_notice_discloses_pending_sa` is FALSE — the auction notice did not disclose a pending SA
3. `sale_certificate_issued` is TRUE — a sale certificate has been issued to the auction purchaser
4. `right_of_redemption_extinguished` is TRUE — the borrower's right to redeem is extinguished upon publication of the auction notice
5. `notice_dispatch_proof_present` is TRUE — proof of dispatch of the auction notice is available
6. `auction_notice_affixed_on_property` is TRUE — the auction notice was affixed on the property
7. `newspaper_publication_done` is TRUE — the auction notice was published in two leading newspapers

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the auction notice was not published in accordance with Rule 8(6) and Rule 9(1) — in that scenario, Kanaiyalal v. State of Maharashtra applies, and the borrower may have a valid claim for procedural defect.
   SLRAI ROUTING: `newspaper_publication_done` = FALSE → Kanaiyalal applies.

2. When the borrower filed a valid objection under Section 13(3A) and the bank failed to reply — in that case, the bank's enforcement action is invalid from inception, and the borrower's right to redeem is not extinguished.
   SLRAI ROUTING: `objection_filed` = TRUE AND `bank_reply_given` = FALSE → Kanaiyalal applies.

3. When the auction purchaser failed to pay the balance consideration within 90 days of the auction — in that case, E. Muthurathinasabathy applies, and the sale is inchoate, preserving the borrower's right to redeem.
   SLRAI ROUTING: `balance_consideration_paid_within_90_days` = FALSE → E. Muthurathinasabathy applies.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002
Primary provision: Section 13(8) — "Where the amount of dues of the secured creditor together with all costs, charges and expenses incurred by him is tendered to the secured creditor at any time before the date of publication of notice for public auction or inviting quotations or tender from public or private treaty for transfer by way of lease, assignment or sale of the secured assets,— (i) the secured assets shall not be transferred by way of lease, assignment or sale by the secured creditor; and (ii) in case, any step has been taken by the secured creditor for transfer by way of lease or assignment or sale of the assets before tendering of such amount under this sub-section, no further step shall be taken by such secured creditor for transfer by way of lease or assignment or sale of such secured assets."
Instrument level: ACT
Nature of provision: MANDATORY — the Court held that the right of redemption is extinguished upon publication of the auction notice, making compliance mandatory.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Celir LLP v. Bafna Motors (2024) 2 SCC 1
  Affirmed the principle that the auction purchaser acquires a vested right upon confirmation of sale, and the bank cannot withhold the sale certificate to allow redemption.

Distinguishes: Mathew Varghese v. Amritha Kumar (2014) 5 SCC 610
  Mathew Varghese dealt with the unamended Section 13(8), where the right of redemption survived until the sale was completed by a registered deed. This case applies the post-2016 amended Section 13(8), where the right is extinguished upon publication of the auction notice.
  SLRAI ROUTING: if `amended_section_13_8_applies` = TRUE → M. Rajendran applies; if FALSE → Mathew Varghese applies.

Distinguishes: Concern Readymix v. Corporation Bank (2018) SCC OnLine Hyd 783
  Concern Readymix held that the right of redemption continues until the sale certificate is registered. This judgment overrules that view, holding that the right is extinguished upon publication of the auction notice.
  SLRAI ROUTING: if `right_of_redemption_extinguished` = TRUE → M. Rajendran applies; if FALSE → Concern Readymix applies.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: amended_section_13_8_applies
Type: FactEntry[bool]
Description: True if the 2016 amendment to Section 13(8) applies to the case
Module: M10
Extraction: Based on the date of the loan and the date of the auction notice

**B. New YAML Rule Needed:**
Module: M10
Rule ID: M10_C8_amended_section_13_8
Conditions: sale_certificate_issued=True AND right_of_redemption_extinguished=True
Severity: FATAL
Message: "The borrower's right to redeem is extinguished upon publication of the auction notice under amended Section 13(8). The sale certificate is valid, and the auction purchaser has a vested right."
Judgment tags: ["M_RAJENDRAN", "CELIR_LLP"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: mathew_varghese_amritha_kumar.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: M. Rajendran (2025 INSC 1137) — held that the right of redemption under Section 13(8) is extinguished upon publication of the auction notice under the amended provision, overruling the pre-amendment interpretation."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: RIGHT_OF_REDEMPTION
