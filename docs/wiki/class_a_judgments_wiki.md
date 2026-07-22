# Class A Judgment Wiki

1 verified judgments — loaded into Chain B context.

### [SUPREME_COURT] E. Muthurathinasabathy
**Citation:** 2026 INSC 303
**Favor:** BORROWER | **Statutory basis:** RULES
**Ground codes:** RIGHT_OF_REDEMPTION, AUCTION_PURCHASER, AUCTION_GAP_DEFECT
**Modules:** M3, M10

**Borrower's claim:**
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

**Holding:**
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

**Applies when:**
This judgment applies when:
1. `sale_certificate_issued` is TRUE — a sale certificate was issued to the auction purchaser
2. `right_of_redemption_extinguished` is FALSE — borrower claims redemption right survives
3. `payments_post_npa_total` is greater than zero — borrower has made payments toward dues
4. `balance_consideration_paid_within_90_days` is FALSE — the auction purchaser failed
   to pay the balance 75% within the 90-day maximum under Rule 9(4) (computed field —
   see app/services/compliance/engine.py COMPUTED_FIELD_RESOLVERS)

**Does NOT apply when:**
1. When the auction purchaser paid the balance consideration within 90 days of the
   auction date — in that scenario, Celir LLP v. Bafna Motors (2024) applies and
   the sale has statutory finality.
   SLRAI ROUTING: `balance_consideration_paid_within_90_days = TRUE` → Celir LLP applies.

2. When the borrower has not tendered the outstanding dues at all — a bare challenge
   to the auction without payment does not attract this judgment's ratio.

3. When the right of redemption under Section 13(8) was extinguished before the Rule 9(4)
   deadline — e.g., borrower tendered after publication of auction notice (M. Rajendran
   (2025) interpretation) — see RELATIONSHIP section.

