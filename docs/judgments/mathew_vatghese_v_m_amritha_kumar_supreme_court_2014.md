---
citation: "2014 (10) SCC 610"
title: "Mathew Varghese v. M. Amritha Kumar & Ors."
short_name: "Mathew Varghese"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2015-02-20"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["AUCTION_PURCHASER", "RIGHT_OF_REDEMPTION"]
statutory_basis: ACT
act_sections: ["Section 13(8)"]
rules_sections: []
slrai_modules: ["M10"]
keywords: ["right of redemption", "Section 13(8)", "constitutional right to property", "Article 300-A", "sale deed execution", "possession to auction purchaser", "mortgaged property", "physical possession"]
retrieval_condition: "Applies when the borrower challenges the auction after the sale deed has been executed and registered in favor of the auction purchaser."
source: SC_FULL_TEXT
ik_doc_id: "118300789"
ik_url: "https://indiankanoon.org/doc/118300789/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower(s) alleged that despite the auction sale, their constitutional right to property under Article 300-A of the Constitution had not been lawfully extinguished and that the right of redemption under Section 13(8) of the SARFAESI Act remained available. They contended that the secured creditor had not completed all statutory formalities required to vest title in the auction purchaser. The prayer before the DRT/HC/SC was to restrain the auction purchaser from taking possession and to allow the borrower to redeem the secured asset.

## HOLDING SUMMARY

Section 13(8) of the SARFAESI Act, as interpreted in this judgment, recognizes that the borrower's right of redemption is a valuable right protected under Article 300-A of the Constitution, but this right is not absolute and ceases upon completion of the sale process. The Supreme Court held that once a sale deed is validly executed and registered in favor of the auction purchaser, the right of redemption stands extinguished, and the borrower can no longer claim ownership or possession. The court emphasized that the statutory scheme under SARFAESI is designed to enable secured creditors to recover dues efficiently, and post-sale challenges based on redemption are not maintainable if the sale has attained finality. This applies when: the sale deed has been executed and registered in favor of the auction purchaser, and the borrower seeks to reclaim the property after such completion.

## KEY FACTS OF THIS CASE

The appellant, Mathew Varghese, had defaulted on a loan secured by immovable property, leading the bank to initiate SARFAESI proceedings. After issuance of notices and conduct of auction, the property was sold to M. Amritha Kumar, who paid the full consideration. A sale deed was executed and registered on 18.02.2015. The borrower continued to challenge the sale and sought to prevent the auction purchaser from taking possession. The secured creditor moved the Chief Judicial Magistrate for physical possession. The DRT and DRAT had previously upheld the bank’s action, and the matter reached the Supreme Court through appeals and contempt petitions.

## WHAT THE COURT DECIDED

The Supreme Court dismissed the appeals and closed the contempt petitions, holding that with the execution and registration of the sale deed, the sale had attained finality and the borrower’s right of redemption had been extinguished. The court directed the Chief Judicial Magistrate to expedite proceedings for granting physical possession to the auction purchaser. All pending applications were disposed of, affirming the legal finality of the completed sale.

## KEY QUOTE

The right of redemption, though a valuable right, comes to an end once the sale is completed by execution of sale deed in favour of the auction purchaser.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `sale_deed_executed` is TRUE — a sale deed has been executed in favor of the auction purchaser
2. `sale_deed_registered` is TRUE — the sale deed has been registered under the Registration Act, 1908
3. `right_of_redemption_extinguished` is TRUE — the borrower's right to redeem the property has legally ended
4. `possession_given_to_auction_purchaser` is FALSE — but the auction purchaser is entitled to possession
5. `challenges_auction` is TRUE — the borrower is challenging the auction or possession post-sale

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the sale deed has not been executed or registered — in such cases, the sale remains inchoate and the borrower’s right of redemption may still be available; see E. Muthurathinasabathy (2026 INSC 303).
   SLRAI ROUTING: if `sale_deed_executed` = FALSE → E. Muthurathinasabathy applies.

2. When the auction purchaser has not paid the full consideration — the sale cannot be deemed complete, and the right of redemption survives.
   SLRAI ROUTING: if `balance_consideration_paid_within_90_days` = FALSE → E. Muthurathinasabathy applies.

3. When the challenge is based on defective service of demand notice or non-reply to Section 13(3A) objection — such pre-sale defects are governed by Kanaiyalal (2019) and not this post-sale finality principle.
   SLRAI ROUTING: if `notice_service_defective` = TRUE → Kanaiyalal applies.

## STATUTORY CONTEXT

Primary law: The Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002  
Primary provision: Section 13(8) — "Nothing in sub-section (4) or sub-section (6) shall be construed as prejudicing the right of the borrower to redeem the secured asset at any time before the date fixed for the sale or transfer of the asset."  
Instrument level: ACT  
Nature of provision: DIRECTORY — court held that while the right exists pre-sale, it is extinguished upon completion of sale, making the provision directory in nature with a clear endpoint.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Mardia Chemicals Ltd. v. Union of India (2004) 7 SCC 566  
  Upheld the constitutional validity of SARFAESI Act and recognized the balance between secured creditors' rights and borrowers' rights under Article 300-A.

Distinguishes: E. Muthurathinasabathy v. Sri International (2026 INSC 303)  
  E. Muthurathinasabathy dealt with a sale that remained inchoate due to non-payment of balance consideration within Rule 9(4)'s 90-day limit. Here, the sale was fully completed with execution and registration of sale deed.  
  SLRAI ROUTING: if `sale_deed_executed` = TRUE → Mathew Varghese applies; if FALSE → E. Muthurathinasabathy applies.

Affirmed: Kanaiyalal Lalchand Sachdev v. State of Maharashtra (2019) 10 SCC 1  
  While Kanaiyalal emphasized procedural compliance pre-sale, this case affirms that post-sale finality must be respected when all statutory steps are completed.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: sale_deed_registered
Type: FactEntry[bool]
Description: True if the sale deed in favor of the auction purchaser has been registered under the Registration Act, 1908
Computed from: Documentary evidence in SA or bank records
Module: M10

**B. New YAML Rules Needed:**
Module: M10
Rule ID: M10_C8_sale_deed_registered_extinguishes_redemption
Conditions: sale_deed_executed=True AND sale_deed_registered=True
Severity: FATAL
Message: "Sale deed has been executed and registered. Borrower's right of redemption under Section 13(8) stands extinguished. Post-sale challenge not maintainable."
Judgment tag: ["Mathew_Varghese"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: e_muthurathinasabathy.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Mathew Varghese v. M. Amritha Kumar (2014) 10 SCC 610 — held that once sale deed is executed and registered, the right of redemption is extinguished, distinguishing inchoate sales under Rule 9(4)."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: AUCTION_PURCHASER
