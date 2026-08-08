---
citation: "(2022) 4 GLH 210"
title: "Agp City Gas Private Limited vs M/S. Lynx Properties & Developers"
short_name: "Agp City Gas"
court: HIGH_COURT
high_court_state: "Kerala"
bench_strength: 1
judgment_date: "2022-05-18"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["AUCTION_PURCHASER", "AMOUNT_DISPUTE", "POSSESSION_DEFECT"]
statutory_basis: ACT
act_sections: ["Section 13(2)", "Section 13(3A)"]
rules_sections: []
slrai_modules: ["M1", "M3", "M10"]
keywords: ["private treaty sale", "bonafide purchaser", "status quo order", "waiver of objection", "de facto possession", "higher quantum demanded", "estoppel against borrower", "protection of auction purchaser", "no physical possession challenge", "Sridhar case distinguished"]
retrieval_condition: "Applies when the borrower challenges a private treaty sale after remaining silent despite notice, and the auction purchaser is a bonafide third party."
source: HC_FULL_TEXT
ik_doc_id: "60411019"
ik_url: "https://indiankanoon.org/doc/60411019/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers alleged that the demand notice dated 21.11.2018 was invalid because it demanded a higher quantum of debt (Rs.4.10 crore) than the amount adjudicated by the DRT in O.A. No.430 of 2014 (Rs.3.84 crore), rendering the entire enforcement proceeding illegal. They contended that the sale conducted under private treaty was void ab initio as it was built on an illegal foundation. They further argued that actual physical possession of the secured asset was never taken by the bank prior to the sale, relying on V. Sridhar v. Authorised Officer (AIR 2018 Madras 87), and that the sale certificate issued did not conform to Appendix V of the SARFAESI Rules. The prayer was to set aside the sale and maintain status quo in S.A. No.177/2021.

## HOLDING SUMMARY

A demand notice under Section 13(2) of the SARFAESI Act remains valid even if it demands a higher quantum than previously adjudicated, provided the borrower fails to raise an objection under Section 13(3A). The borrower's silence constitutes waiver and estoppel, precluding them from challenging the enforcement proceedings at a later stage. Physical possession taken by the secured creditor prior to sale, supported by notice, publication, and unchallenged communication, satisfies the requirement under the Act. A private treaty sale to a bonafide third-party purchaser, conducted after due process and for a premium price, cannot be interfered with by an ad interim status quo order from the DRT, especially when the borrower remained passive throughout. The protection of bonafide auction purchasers is essential to maintain the credibility of SARFAESI enforcement. This applies when: the borrower received notice, did not object under Section 13(3A), and a bonafide purchaser acquired the asset via private treaty.

## KEY FACTS OF THIS CASE

The borrower, Lynx Properties & Developers, had defaulted on a loan from Bank of Baroda, leading to a recovery certificate issued by DRT in 2016 for Rs.3.84 crore. Despite multiple auction attempts failing even at a reduced reserve price of Rs.2.25 crore, the bank eventually entered into a private treaty sale with AGP City Gas Private Limited on 28.02.2020 for Rs.3.15 crore. The bank had issued a Section 13(2) demand notice on 21.11.2018 for Rs.4.10 crore, served on the borrower’s partners, with publication in newspapers. Possession was claimed to have been taken on 06.09.2019, communicated to the borrower on 24.12.2019, with no objection raised. The borrower later challenged the sale in S.A. No.177/2021, obtaining an ex parte status quo order from DRT on 27.08.2021, which the purchaser challenged via this writ petition under Article 227.

## WHAT THE COURT DECIDED

The High Court set aside the ad interim ex parte status quo order dated 27.08.2021 passed by the DRT in S.A. No.177/2021, holding it caused irreparable prejudice to the bonafide purchaser. The Court declined to issue a declaration that the SA was without jurisdiction but allowed the original petition in part. The DRT was directed to proceed with the SA untrammelled by the observations in this judgment. The sale to AGP City Gas was upheld as valid and protected.

## KEY QUOTE

Unless such protection is extended to [bonafide third-party purchasers], court auctions would not fetch market value or fair price of the property.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `objection_filed` is FALSE — the borrower or guarantor did not file any objection under Section 13(3A) despite receiving the demand notice
2. `notice_service_acknowledged` is TRUE — the demand notice was served on the borrower or partner, as per Section 24 of the Indian Partnership Act
3. `auction_type` is "private treaty" — the sale was conducted via private treaty, not public auction
4. `sa_applicant_type` is "auction purchaser" — the applicant challenging the SA is the auction purchaser, not the borrower
5. `challenges_auction` is TRUE — the SA seeks to set aside the sale or maintain status quo over the asset
6. `drt_interim_stay_granted` is TRUE — the DRT has passed an ad interim ex parte stay in the SA
7. `right_of_redemption_extinguished` is TRUE — the sale has been confirmed and possession handed over

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the borrower filed a timely objection under Section 13(3A) and the bank failed to reply — in that case, Kanaiyalal v. State of Maharashtra applies and the enforcement action is void.
   SLRAI ROUTING: if `objection_filed` = TRUE and `bank_reply_given` = FALSE → Kanaiyalal applies.

2. When the private treaty sale was conducted without any notice to the borrower or guarantor — in such a case, the sale would be void for lack of due process.
   SLRAI ROUTING: if `notice_service_acknowledged` = FALSE → this judgment does not apply; service defect grounds apply.

3. When the auction purchaser is not a third party but the bank itself or a related entity — the protection for bonafide strangers does not extend to insider transactions.
   SLRAI ROUTING: if `sa_applicant_type` = "bank" or "related party" → this judgment does not apply.

## STATUTORY CONTEXT

Primary law: The Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002  
Primary provision: Section 13(2) — "Where any borrower, who is under a liability to a secured creditor under a security agreement, makes any default in repayment of secured debt or any part thereof, and his account in respect of such debt is classified by the secured creditor as non-performing asset, then the secured creditor may require the borrower by notice in writing to discharge in full his liabilities to the secured creditor within sixty days from the date of receipt of the notice."  
Nature of provision: MANDATORY — but procedural compliance can be waived by conduct  
Level: ACT  
Key word: "may" — court held that while the power is discretionary, once exercised, the procedure must be followed, but defects can be waived by inaction

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: ITC Limited v. Blue Coast Hotels Ltd. (2018) 15 SCC 99  
  Held that a borrower who remains silent after service of notice and allows third-party rights to crystallize cannot later challenge the sale. This case applies the same principle of waiver and estoppel.

Distinguishes: V. Sridhar v. Authorised Officer, Indian Bank (AIR 2018 Madras 87)  
  Sridhar held that sale without possession is invalid. This case distinguishes it by finding de facto possession was taken and communicated, and the borrower did not challenge it.  
  SLRAI ROUTING: if `possession_taken_date` is not null AND `objection_filed` = FALSE → Agp City Gas applies; if `possession_taken_date` is null AND `objection_filed` = TRUE → Sridhar applies.

Follows: Arce Polymers v. Alphine Pharmaceuticals (2022) 2 SCC 221  
  Reaffirmed that waiver by conduct bars a borrower from challenging enforcement after third-party rights are created. This case applies the same ratio to private treaty sales.

Follows: Janatha Textiles v. Tax Recovery Officer (2008) 12 SCC 582  
  Affirmed protection for bonafide third-party purchasers even if the underlying decree is set aside. This case extends that protection to SARFAESI private treaty sales.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**  
Field name: auction_type  
Type: FactEntry[str]  
Description: Type of auction conducted — "public auction", "private treaty", "e-auction"  
Module: M3  
Extraction: From bank records, sale notice, or SA documents

**B. New YAML Rule Needed:**  
Module: M10  
Rule ID: M10_C8_bonafide_purchaser_protection  
Conditions: sa_applicant_type="auction purchaser" AND objection_filed=False AND auction_type="private treaty"  
Severity: WARNING  
Message: "Borrower remained silent after notice; bonafide purchaser protected under Agp City Gas. Interim stay likely to cause prejudice and may be set aside."  
Judgment tag: ["Agp_City_Gas"]  
Statutory basis: ACT

**C. Existing Judgments to Update:**  
File: v_sridhar_ao_indian_bank.md  
Section: ## RELATIONSHIP TO OTHER JUDGMENTS  
Add: "Distinguished by: Agp City Gas (2022) 4 GLH 210 — held that where possession was taken and communicated, and borrower remained silent, private treaty sale to bonafide purchaser is protected, distinguishing Sridhar’s holding on possession."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: AUCTION_PURCHASER
