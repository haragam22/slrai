---
# IDENTITY
citation: "2026 INSC 303"
title: "E. Muthurathinasabathy & Ors. v. M/s. Sri International & Ors."
short_name: "E. Muthurathinasabathy"
court: "SUPREME_COURT"
high_court_state: null
bench_strength: 2
judgment_date: "2026-04-01"
overruled: false
overruled_by: null
distinguished_by: []

# CLASSIFICATION
favor: "BORROWER"
favor_verified: true
ground_codes:
  - "RIGHT_OF_REDEMPTION"
  - "AUCTION_PURCHASER"
  - "AUCTION_GAP_DEFECT"
statutory_basis: "RULES"
act_sections:
  - "Section 13(8)"
rules_sections:
  - "Rule 9(4)"
  - "Rule 9(3)"

# SLRAI ROUTING
slrai_modules:
  - "M3"
  - "M10"
keywords:
  - "Rule 9(4)"
  - "balance consideration"
  - "outer limit three months"
  - "inchoate sale"
  - "right of redemption"
  - "statutory finality"
  - "15 days confirmation"
  - "balance 75%"
  - "delay completion sale"

# SOURCE
source: "SC_FULL_TEXT"
ik_doc_id: ""
ik_url: "https://verdictum.in/2026/insc/303"
has_verified_conditions: true
---

## BORROWER'S CLAIM

The borrowers alleged that the e-auction conducted on 04.09.2020 never attained
statutory finality because the auction purchaser deposited the balance 75% of the
sale consideration only on 31.03.2022 — approximately 15 months after the auction —
far exceeding the maximum 90-day period prescribed by Rule 9(4) of the SARFAESI Rules.
They contended that a sale which fails to comply with the mandatory statutory payment
timeline is legally inchoate and cannot extinguish their right to redeem the
mortgaged property under Section 13(8) of the SARFAESI Act. They further alleged that
since they had fully discharged the entire outstanding dues of Rs. 3,89,31,614/-
during the pendency of proceedings, the bank was obligated to accept repayment and
release the secured assets.

## HOLDING SUMMARY

Rule 9(4) of the Security Interest (Enforcement) Rules, 2002 prescribes an absolute
mandatory outer limit of 90 days for the auction purchaser to deposit the balance sale
consideration. A sale that remains inchoate due to non-compliance with this timeline —
even if the delay was partly caused by judicial restraints — cannot defeat the
borrower's right to redeem the mortgaged property. When the statutory conditions for
vesting of title in the auction purchaser are never fulfilled within the mandatory
timeframe, the eventual issuance and registration of a sale certificate does not grant
absolute finality to the sale. The borrower's right of redemption under Section 13(8)
survives until a legally valid, fully completed sale extinguishes it. Celir LLP v.
Bafna Motors (2024) is distinguishable because that sale attained statutory finality
with timely payment and no judicial interdiction. This applies when: the balance
consideration was paid beyond the 90-day Rule 9(4) limit and the borrower has
discharged all outstanding dues in the interim.

## KEY FACTS OF THIS CASE

A partnership firm (M/s. Sri International) had availed credit facilities of Rs. 4
crore from Central Bank of India, secured by four commercial and residential properties.
The loan was classified NPA on 25.11.2018. After demand and possession notices, an
e-auction was conducted on 04.09.2020 in which the appellants emerged as the highest
bidders and deposited 25% of the bid amount. Due to serial interim orders from DRT,
DRAT, and the High Court, the balance 75% was not paid until 31.03.2022 — 15 months
after the auction — despite the High Court's 15.12.2020 order permitting the secured
creditor to accept the balance. During this period, the borrowers progressively
deposited amounts under court direction and fully discharged all dues. DRT and DRAT
both dismissed the SAs; the Madras High Court set aside the auction sale; the Supreme
Court affirmed the High Court.

## WHAT THE COURT DECIDED

The Supreme Court dismissed the appeals filed by the auction purchasers and the secured
creditor, holding the auction sale was legally inchoate for violating Rule 9(4)'s
mandatory 90-day payment deadline. The borrowers were entitled to redeem the mortgaged
properties by paying all outstanding dues. The registered sale certificates issued to
the auction purchasers were annulled, and the secured creditor was directed to release
the secured assets and return the title deeds. The auction purchasers were limited to
a refund of their deposited consideration with 12% interest per annum.

## KEY QUOTE

"A sale that remained inchoate in favour of the auction purchasers, owing to
non-compliance with mandatory timelines prescribed under Rule 9(4) of the 2002
Rules, cannot be invoked to defeat the right of the borrowers to redeem."

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `sale_certificate_issued` is TRUE — a sale certificate was issued to the auction purchaser
2. `right_of_redemption_extinguished` is FALSE — borrower claims redemption right survives
3. `payments_post_npa_total` is greater than zero — borrower has made payments toward dues
4. `balance_consideration_paid_within_90_days` is FALSE — the auction purchaser failed
   to pay the balance 75% within the 90-day maximum under Rule 9(4) (computed field —
   see app/services/compliance/engine.py COMPUTED_FIELD_RESOLVERS)

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the auction purchaser paid the balance consideration within 90 days of the
   auction date — in that scenario, Celir LLP v. Bafna Motors (2024) applies and
   the sale has statutory finality.
   SLRAI ROUTING: `balance_consideration_paid_within_90_days = TRUE` → Celir LLP applies.

2. When the borrower has not tendered the outstanding dues at all — a bare challenge
   to the auction without payment does not attract this judgment's ratio.

3. When the right of redemption under Section 13(8) was extinguished before the Rule 9(4)
   deadline — e.g., borrower tendered after publication of auction notice (M. Rajendran
   (2025) interpretation) — see RELATIONSHIP section.

## STATUTORY CONTEXT

Primary law: Security Interest (Enforcement) Rules 2002
Primary provision: Rule 9(4) — "The balance amount of purchase price payable shall be
paid by the purchaser to the authorised officer on or before the fifteenth day of
confirmation of sale of the immovable property or such extended period as may be
agreed upon in writing between the parties, but in no case exceeding three months."
Instrument level: RULES
Nature of provision: MANDATORY — court confirmed the three-month outer limit is
absolute and cannot be exceeded regardless of judicial delays.

Secondary: Section 13(8) SARFAESI Act — borrower's right to redeem before
"date fixed for sale or transfer". Post-2016 amendment: redemption available
before date of publication of notice for public auction. Court held this right
survives when the sale never attained statutory finality within Rule 9(4) timelines.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Mathew Varghese v. M. Amritha Kumar (2014) 5 SCC 610
  Established that the right of redemption is a constitutional right protected
  under Article 300-A and survives until valid completion of sale by registered deed.

Distinguishes: Celir LLP v. Bafna Motors (2024) 2 SCC 1
  Celir LLP dealt with a sale that attained statutory finality — entire consideration
  paid within prescribed timeframe, sale certificate issued without judicial interdiction.
  This case involves a sale that never attained finality due to Rule 9(4) violation.
  SLRAI ROUTING: if `balance_consideration_paid_within_90_days` = TRUE → Celir LLP
  (sale has finality, set aside requires fraud/fundamental error); if FALSE → this
  judgment (sale inchoate, right of redemption survives).

Distinguishes: M. Rajendran v. KPK Oils (2025 SCC OnLine SC 2036)
  M. Rajendran addressed the curtailed redemption right under amended Section 13(8)
  where a valid completed auction concluded. Here the auction sale never validly
  completed due to Rule 9(4) violation — the Section 13(8) curtailment therefore
  did not bite.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

No new fields, rules, or ground codes required. Fits within existing schema as of
H7 patch: `balance_payment_date`, `balance_consideration_paid_within_90_days`
(computed), and rule `M10_C7` were added to engine.py / m10_third_party.yaml
directly, ahead of a formal v5.5 blueprint patch. See docs/schema_gaps.md for the
status note on this judgment's original NEW REQUIREMENTS request.

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: RIGHT_OF_REDEMPTION
