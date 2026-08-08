---
citation: "2022 SCC OnLine SC 1"
title: "Arce Polymers Pvt. Ltd. vs M/S Alphine Pharmaceuticals Pvt. Ltd."
short_name: "Arce Polymers"
court: SUPREME_COURT
high_court_state: null
bench_strength: 3
judgment_date: "2021-12-03"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["REPLY_NOT_GIVEN", "LIMITATION_EXPIRED", "VALUATION_DISPUTE"]
statutory_basis: ACT
act_sections: ["Section 13(2)", "Section 13(3A)", "Section 13(4)", "Section 17"]
rules_sections: []
slrai_modules: ["M1", "M2", "M6"]
keywords: ["Section 13(3A)", "waiver of reply", "estoppel", "continuing cause of action", "restructuring proposal", "delay and laches", "third party rights", "forbearance", "disclaimer of rights"]
retrieval_condition: "Applies when the borrower made post-notice representations seeking restructuring but later challenged the bank's failure to reply under Section 13(3A), after third-party rights were created."
source: SC_FULL_TEXT
ik_doc_id: "6610062"
ik_url: "https://indiankanoon.org/doc/6610062/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower(s) alleged that the bank violated Section 13(3A) of the SARFAESI Act by failing to respond to their representations dated 1st and 6th November 2016, which were submitted after the Section 13(2) notice. They contended that the bank's non-reply rendered the entire enforcement process, including possession and auction, illegal and void. They further argued that the challenge to the enforcement measures was not barred by limitation, as the cause of action was continuing from the date of the Section 13(2) notice to the issuance of the sale certificate. The prayer before the High Court was to quash all enforcement proceedings and restore possession of the secured asset.

## HOLDING SUMMARY

While Section 13(3A) of the SARFAESI Act imposes a mandatory duty on the secured creditor to reply to the borrower's representation, the failure to do so may be waived by the borrower's subsequent conduct. Where the borrower, after the issuance of the Section 13(2) notice, actively seeks forbearance, proposes restructuring, and induces the bank to delay enforcement, such conduct constitutes an implied waiver of the statutory right to a reply. In such cases, equitable estoppel bars the borrower from later challenging the enforcement on grounds of non-compliance with Section 13(3A), especially when third-party rights have been created. The principle of limitation under Section 17 does not permit a borrower to remain silent during enforcement and challenge the entire process after the sale. This applies when: the borrower made post-notice representations seeking restructuring, the bank deferred action in reliance on those representations, and the borrower later challenged the enforcement after third-party rights were created.

## KEY FACTS OF THIS CASE

The borrower, Alphine Pharmaceuticals, had availed a term loan of Rs. 1.52 crore and working capital of Rs. 35 lakh from Andhra Bank, secured by a plot in Hyderabad. The account was declared NPA on 31.07.2016. A Section 13(2) notice was issued on 01.08.2016. The borrower responded on 01.11.2016 and 06.11.2016, not disputing the default but requesting a 12-month moratorium and proposing restructuring. The bank, in a letter dated 07.11.2016, recommended deferring SARFAESI action. The bank issued a possession notice under Section 13(4) on 03.03.2017 and took physical possession in May 2017. Multiple auctions failed until 11.09.2018, when the property was sold. The borrower filed an application before the DRT on 01.10.2018, challenging the entire process. The DRT dismissed it, but the Telangana High Court allowed the writ petition, setting aside the sale. The Supreme Court reversed the High Court's decision.

## WHAT THE COURT DECIDED

The Supreme Court allowed the appeals filed by the bank and the second purchaser, setting aside the impugned judgment of the Telangana High Court. It held that the borrower's conduct in seeking restructuring and forbearance after the Section 13(2) notice amounted to a waiver of its right to a reply under Section 13(3A). The Court upheld the DRT's order, confirming the validity of the auction sale and the transfer of the property. It ruled that the borrower was estopped from challenging the enforcement proceedings due to its own dilatory and inconsistent conduct, particularly after third-party rights had been created. No order as to costs was passed.

## KEY QUOTE

In these circumstances, we have no doubt that the failure to furnish a reply to the representation is not of much significance since we are satisfied that the creditor has undoubtedly considered the representation and the proposal for repayment made therein.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `objection_filed` is TRUE — the borrower submitted representations after the Section 13(2) notice
2. `bank_reply_given` is FALSE — the bank did not formally reply under Section 13(3A)
3. `restructuring_proposal_pending` is TRUE — the borrower proposed restructuring or sought a moratorium after the notice
4. `bank_reply_gives_reasons` is FALSE — the bank did not provide reasons for rejecting the proposal
5. `auction_date` is after `objection_date` — the auction occurred after the borrower's representations
6. `sa_filing_date` is after `sale_certificate_date` — the borrower filed the SA after the sale was completed
7. `sa_applicant_type` is "BORROWER" — the borrower is the one challenging the sale
8. `possession_given_to_auction_purchaser` is TRUE — the auction purchaser has been given possession

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the borrower's representation was a clear objection to the debt or demand notice, and not a request for restructuring or forbearance — in that case, Kanaiyalal v. State of Maharashtra (2020) applies, and the bank's failure to reply is fatal.
   SLRAI ROUTING: if `objection_filed` = TRUE AND `restructuring_proposal_pending` = FALSE → Kanaiyalal applies.

2. When the borrower challenges the enforcement proceedings before the auction or sale, and before any third-party rights are created — in that case, ITC Limited v. Blue Coast Hotels Limited (2018) applies, and the bank's failure to reply under Section 13(3A) is a ground for setting aside the action.

3. When the bank never deferred enforcement action or acted on the borrower's representations — in that case, the conduct does not amount to waiver, and the borrower can validly challenge the non-reply.

## STATUTORY CONTEXT

Primary law: Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002
Primary provision: Section 13(3A) — "If the borrower, within the period of sixty days from the date of notice referred to in sub-section (2), makes any representation or raises any objection in writing, the authorised officer shall consider the representation or objection and if the authorised officer is of the opinion that the representation or objection is not acceptable to him, he shall communicate within one week of the receipt of such representation or objection, the reasons in writing to the borrower."
Instrument level: ACT
Nature of provision: MANDATORY — the court acknowledged the mandatory nature of the duty to reply, but held that the right can be waived by conduct.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: ITC Limited v. Blue Coast Hotels Limited (2018) 15 SCC 99
  Affirmed that Section 13(3A) imposes a mandatory duty on the bank to reply to borrower's representation.

Distinguishes: ITC Limited v. Blue Coast Hotels Limited (2018) 15 SCC 99
  While ITC Blue Coast held non-reply to be fatal, this case holds that such non-reply can be waived by borrower's conduct of seeking forbearance and restructuring. SLRAI ROUTING: if `restructuring_proposal_pending` = TRUE → Arce Polymers applies (waiver by conduct); if FALSE → ITC Blue Coast applies (non-reply is fatal).

Follows: Authorised Officer, Indian Overseas Bank v. Ashok Saw Mill (2009) 8 SCC 366
  Affirmed that a challenge under Section 17 can cover the entire chain of enforcement actions.

Distinguishes: Blue Coast Hotels Limited v. IFCI Limited (2016 SCC OnLine Bom 2663)
  The Bombay High Court held that Section 13(3A) reply is mandatory and time-bound. This SC judgment limits that view by introducing waiver by conduct.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: restructuring_proposal_pending
Type: FactEntry[bool]
Description: True if borrower submitted a formal or informal proposal for loan restructuring, moratorium extension, or forbearance after the Section 13(2) notice
Computed from: borrower's letters, bank's internal memos acknowledging the request
Module: M2

**B. New YAML Rule Needed:**
Module: M2
Rule ID: M2_C5_reply_waiver_by_conduct
Conditions: objection_filed=True AND bank_reply_given=False AND restructuring_proposal_pending=True AND sa_filing_date > sale_certificate_date
Severity: WARNING
Message: "Borrower's challenge to non-reply under Section 13(3A) may be barred by waiver and estoppel as per Arce Polymers. Borrower sought restructuring and challenged sale after third-party rights were created."
Judgment tag: ["Arce_Polymers"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: itc_blue_coast_hotels.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Arce Polymers (2022 SCC OnLine SC 1) — held that borrower's conduct in seeking restructuring after notice may constitute waiver of right to reply under Section 13(3A), especially when challenge is filed after sale."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: REPLY_NOT_GIVEN
