---
citation: "2026 INSC 237"
title: "Om Sakthi Sekar v. V. Sukumar & Ors."
short_name: "Om Sakthi Sekar"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2026-03-13"
overruled: false
overruled_by: null
distinguished_by: []
favor: BORROWER
favor_verified: true
ground_codes: ["VALUATION_DISPUTE", "AUCTION_GAP_DEFECT"]
statutory_basis: OTHER
act_sections: []
rules_sections: []
slrai_modules: ["M6", "M3"]
keywords: ["valuation report", "reserve price fixation", "competitive bidding", "best possible value", "reconsideration of valuation", "adequacy of valuation", "secured asset value", "finality of auction", "underbidding", "fairness in sale"]
retrieval_condition: "Applies when the High Court remands the matter to the DRT for reconsideration of valuation of secured assets despite confirmation of auction sale."
source: SC_FULL_TEXT
ik_doc_id: "188157275"
ik_url: "https://indiankanoon.org/doc/188157275/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers (guarantors) alleged that the auction sale of the mortgaged properties was conducted at a reserve price significantly lower than their actual market value, resulting in inadequate realization of the secured asset. They contended that the valuation adopted by the Recovery Officer was flawed and failed to reflect the true worth of the Schedule A to E properties, thereby prejudicing their interests. They further argued that the process leading to the fixation of the reserve price lacked transparency and did not ensure competitive bidding, potentially enabling underbidding. The prayer before the High Court was to quash the DRAT’s order affirming the auction and to set aside the sale proceedings, or in the alternative, to direct a fresh valuation of the properties.

## HOLDING SUMMARY

While confirmed auction sales are generally protected to ensure finality and protect bona fide purchasers, the supervisory jurisdiction of the High Court permits limited remand for reconsideration of valuation where concerns about the adequacy of the reserve price or fairness of the bidding process arise. The objective of recovery proceedings is not merely to complete the sale but to realize the maximum possible value of the secured asset, balancing the interests of both creditor and borrower. A remand for fresh valuation by the DRT, without setting aside the sale or questioning the purchaser’s status, does not vitiate the auction or undermine its finality if it is confined to assessing whether the original valuation and reserve price were justifiable. This applies when: the High Court remands the valuation issue to the DRT despite upholding the auction’s validity and the purchaser’s rights.

## KEY FACTS OF THIS CASE

The appellant, Om Sakthi Sekar, purchased Schedule A to E properties in an auction conducted by the Recovery Officer on 29.10.2010 under DRC No. 68/2010, pursuant to a recovery certificate issued in O.A. No. 536 of 1998. The properties were mortgaged by guarantors to secure a bank facility. The appellant, a third-party bidder, emerged as the highest bidder with a bid of Rs. 2,10,98,765/-, paid 25% upfront, and later the full balance, leading to confirmation of sale and issuance of a registered sale certificate in 2011. The guarantors challenged the recovery proceedings and the auction, arguing the reserve price was too low. The DRAT upheld the auction in 2017, but the Madras High Court in 2020, while affirming the auction’s validity, remanded the valuation issue to the DRT for fresh consideration.

## WHAT THE COURT DECIDED

The Supreme Court dismissed the appeal, upholding the Madras High Court’s decision to remand the matter to the DRT for reconsideration of the valuation of the secured properties. It held that the High Court’s limited remand did not disturb the confirmed auction sale or the appellant’s status as a purchaser, but was a valid exercise of supervisory jurisdiction to ensure the recovery process secured the best possible value. The Court declined to interfere, finding no legal error in the High Court’s approach, and confirmed that the DRT must now decide the valuation issue afresh.

## KEY QUOTE

The direction issued by the High Court merely remits the matter to the DRT for examination of the valuation... Such a limited remand does not prejudge the rights of the auction purchaser, but enables the DRT to assess whether the valuation and fixation of the reserve price were in accordance with law.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `challenges_auction` is TRUE — the borrower challenges the auction process
2. `valuation_challenged_by_borrower` is TRUE — the borrower specifically disputes the valuation or reserve price
3. `auction_conducted_despite_stay` is FALSE — no stay was in force during the auction
4. `sale_certificate_issued` is TRUE — a sale certificate has been issued to the purchaser
5. `drt_stay_order_date` is null — no DRT stay order exists
6. `prayer_scope_covers_current_measure` is TRUE — the borrower's prayer includes reconsideration of valuation
7. `reserve_price_vs_valuation_pct` is less than 50 — the reserve price was significantly lower than the valuation report
8. `drt_interim_stay_granted` is FALSE — no interim stay was granted by DRT

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the auction sale itself is set aside for fraud or procedural illegality — in that case, *Janatha Textiles v. Tax Recovery Officer* applies, which allows setting aside the sale entirely.
   SLRAI ROUTING: if `auction_conducted_despite_stay` = TRUE → Janatha Textiles applies.

2. When the borrower does not challenge the valuation but only the underlying recovery certificate — in that scenario, the challenge is to the debt itself, not the sale process, and *Central Bank of India v. C.L. Vimala* governs.

3. When the auction purchaser is the decree-holder or bank — this judgment protects third-party bidders; if the bank is the purchaser, the principle of finality is stronger and *Sadashiv Prasad Singh v. Harendar Singh* applies.

## STATUTORY CONTEXT

Primary law: Recovery of Debts Due to Banks and Financial Institutions Act, 1993 (RDDBFI Act)
Secondary law: Second Schedule to the Income Tax Act, 1961 (Rules 38 and 52(2))
Provision: Procedure for auction and sale in recovery proceedings
Verbatim text: Not quoted verbatim in judgment, but the procedure under Rule 38 and Rule 52(2) of the Second Schedule to the Income Tax Act, 1961 governs the conduct of auction by the Recovery Officer.
Level: OTHER
Nature: MANDATORY — the auction must follow the prescribed procedure, but the Court affirmed that valuation adequacy can be revisited in supervisory jurisdiction.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Rajiv Kumar Jindal v. BCI Staff Welfare Association (2023) 238 Comp Cas 227
  Reaffirmed that the purpose of auction is to secure the most remunerative price through competitive bidding and that courts must ensure fairness in the process.

Distinguishes: Janatha Textiles v. Tax Recovery Officer (2008) 12 SCC 582
  Janatha Textiles allows setting aside a sale if the underlying decree is invalid, but here the sale is upheld and only valuation is remanded.
  SLRAI ROUTING: if `auction_conducted_despite_stay` = TRUE → Janatha Textiles applies; if FALSE and only valuation challenged → Om Sakthi Sekar applies.

Distinguishes: Sadashiv Prasad Singh v. Harendar Singh (2015) 5 SCC 574
  Sadashiv Prasad protects third-party purchasers more strongly; Om Sakthi Sekar allows limited remand for valuation even when purchaser is bona fide.
  SLRAI ROUTING: if `sa_applicant_type` = "Bank" → Sadashiv Prasad applies; if "Third Party" → Om Sakthi Sekar applies.

Follows: Noida Special Economic Zone Authority v. Manish Agarwal (2024 INSC 839)
  Valuation is a question of fact and generally not interfered with unless no material basis exists — but here, High Court’s remand is seen as a valid supervisory exercise.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: reserve_price_vs_valuation_pct
Type: FactEntry[float]
Description: Computed — Percentage of reserve price relative to the valuation amount (e.g., reserve_price / valuation_amount * 100)
Computed from: reserve_price, valuation_amount
Module: M6

**B. New YAML Rule Needed:**
Module: M6
Rule ID: M6_C3_valuation_remand_allowed
Conditions: sale_certificate_issued=True AND valuation_challenged_by_borrower=True AND auction_conducted_despite_stay=False
Severity: WARNING
Message: "High Court may remand valuation issue to DRT for fresh consideration even after sale confirmation, if no stay was in force and challenge is to adequacy of valuation."
Judgment tag: ["Om_Sakthi_Sekar"]
Statutory basis: OTHER

**C. Existing Judgments to Update:**
File: janatha_textiles_tax_recovery_officer.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Om Sakthi Sekar (2026 INSC 237) — held that a remand for reconsideration of valuation, without setting aside the sale, is permissible under supervisory jurisdiction when no stay was in force."

File: sadashiv_prasad_singh_harendar_singh.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Om Sakthi Sekar (2026 INSC 237) — held that even a bona fide third-party purchaser’s sale may be subject to remand on valuation if the process lacked competitive fairness."

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: VALUATION_DISPUTE
