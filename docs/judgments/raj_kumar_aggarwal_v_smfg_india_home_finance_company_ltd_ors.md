---
citation: "(2024) SCC OnLine Del 3256"
title: "Raj Kumar Aggarwal vs Smfg India Home Finance Company Ltd & Ors."
short_name: "Raj Kumar Aggarwal"
court: HIGH_COURT
high_court_state: "Delhi"
bench_strength: 2
judgment_date: "2024-05-28"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["THIRD_PARTY_ATS"]
statutory_basis: TPA
act_sections: []
rules_sections: []
slrai_modules: ["M10"]
keywords: ["unregistered ATS", "unregistered GPA", "customary documents", "no valid title", "Section 17 Registration Act", "Section 54 Transfer of Property Act", "possessory title", "locus to challenge", "equitable mortgage", "registered sale deed"]
retrieval_condition: "Applies when a third party challenges SARFAESI enforcement based on an unregistered Agreement to Sell and unregistered General Power of Attorney."
source: IK_SUMMARY
ik_doc_id: "52115382"
ik_url: "https://indiankanoon.org/doc/52115382/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The petitioner, a third-party claimant, alleged that he had purchased the subject property through an unregistered Agreement to Sell (ATS) and unregistered General Power of Attorney (GPA), both dated 07.07.2012, and had been in continuous possession for 12 years. He contended that under Ghanshyam v. Yogendra Rathi, he possessed a valid possessory title which entitled him to resist the auction of the property. He further argued that the mortgage in favor of the bank was based on a potentially forged sale deed dated 28.05.1984, and thus the secured creditor’s claim was invalid. The prayer was to set aside the DRT and DRAT orders and restrain the bank from proceeding with possession and auction.

## HOLDING SUMMARY

A third party claiming rights under an unregistered Agreement to Sell (ATS) and unregistered General Power of Attorney (GPA) does not acquire any valid legal or equitable title to the immovable property and therefore lacks locus standi to challenge SARFAESI enforcement proceedings. The Supreme Court in Shakeel Ahmed v. Syed Akhlaq Hussain has categorically held that such customary documents, even if accompanied by possession and full payment, do not confer any legally enforceable right or title under Section 54 of the Transfer of Property Act, 1882, and Section 17 of the Registration Act, 1908. An unregistered ATS cannot be admitted in evidence to establish title, and possession derived from such documents does not elevate into ownership. The right to resist enforcement under SARFAESI is limited to borrowers, guarantors, or persons with registered title. This applies when: `ats_registered` is FALSE and `gpa_registered` is FALSE and the applicant is not the borrower or guarantor.

## KEY FACTS OF THIS CASE

Raj Kumar Aggarwal, a third-party purchaser, claimed to have bought Plot No. 80 and 80A, Khasra No. 60/7, Mohan Garden, Dwarka (200 sq. yds.) for Rs. 10 lakhs in 2012 via an unregistered ATS and unregistered GPA. The property was mortgaged by the borrower, Sh. Vishab Singh Bharti, to SMFG India Home Finance Ltd., which classified the loan as NPA on 05.09.2023. The bank issued a possession notice on 16.03.2024 and an auction notice on 23.04.2024. The petitioner challenged these actions before the DRT, which dismissed his SA on 17.05.2024; the DRAT upheld the dismissal on 24.05.2024. The High Court dismissed the writ petition, affirming that the petitioner had no legal title to resist enforcement.

## WHAT THE COURT DECIDED

The Delhi High Court dismissed the writ petition, affirming the DRT and DRAT orders. It held that the petitioner, having no valid legal title due to the unregistered nature of the ATS and GPA, lacked locus to challenge the SARFAESI proceedings. The enforcement actions by the bank, based on a registered sale deed in the borrower’s name, were upheld. The auction of the property was permitted to proceed.

## KEY QUOTE

No right, title or interest in immovable property can be conferred without a registered document. Even the judgment of this Court in the case of Suraj Lamps & Industries (supra) lays down the same proposition.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `sa_applicant_type` is "Third Party" — the applicant is not the borrower or guarantor
2. `ats_registered` is FALSE — the Agreement to Sell relied upon by the third party is unregistered
3. `gpa_registered` is FALSE — the General Power of Attorney is unregistered
4. `challenges_auction` is TRUE — the third party is challenging the auction or possession
5. `prayer_scope_covers_current_measure` is TRUE — the relief sought includes setting aside the auction or possession notice

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the third party holds a registered sale deed or registered conveyance — in that case, the claimant may have valid title and locus; see *Ghanshyam v. Yogendra Rathi*.
   SLRAI ROUTING: if `ats_registered` = TRUE and `gpa_registered` = TRUE and `payment_proof_exists` = TRUE → *Ghanshyam* may apply depending on possession.

2. When the applicant is the borrower or guarantor — this judgment does not apply as locus is not in question; standard SARFAESI grounds apply (e.g., service defect, reply not given).
   SLRAI ROUTING: if `sa_applicant_type` = "Borrower" → apply M1–M9 modules instead.

3. When the unregistered ATS is accompanied by a registered deed of declaration or court decree — such documents may confer enforceable rights despite lack of registration of ATS.
   SLRAI ROUTING: if `title_document_registered` = TRUE → this judgment does not apply.

## STATUTORY CONTEXT

Primary law: Transfer of Property Act, 1882  
Primary provision: Section 54 — "Sale of immovable property defined. A sale is a transfer of ownership in exchange for a price paid or promised or part-paid and part-promised."  
Verbatim: "Where the whole of the purchase-money has been paid, the vendor is deemed to have an equitable mortgage."  
Level: TPA  
Nature: MANDATORY — court held that transfer of title requires a registered instrument; oral or unregistered agreements cannot confer ownership.

Secondary law: Registration Act, 1908  
Provision: Section 17(1)(a) — "Documents of which registration is compulsory: (a) instruments of gift of immovable property; (b) other non-testamentary instruments which purport or operate to create, declare, assign, limit or extinguish, whether in present or in future, any right, title or interest, for a value exceeding one hundred rupees, in immovable property."  
Level: ACT  
Nature: MANDATORY — unregistered documents of this nature have no legal effect.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Shakeel Ahmed v. Syed Akhlaq Hussain (2023) SCC OnLine SC 1526  
  Affirmed that unregistered ATS and GPA do not confer title or enforceable rights; reliance on customary documents is legally impermissible.  
  SLRAI ROUTING: if `ats_registered` = FALSE and `gpa_registered` = FALSE → Shakeel Ahmed applies.

Distinguishes: Ghanshyam v. Yogendra Rathi (2023) 7 SCC 361  
  Ghanshyam dealt with a transferee already in possession who could resist eviction by the transferor; this case involves a third party challenging a secured creditor’s enforcement.  
  SLRAI ROUTING: if `challenges_auction` = TRUE and `secured_creditor_involved` = TRUE → Raj Kumar Aggarwal applies; if `challenges_eviction_by_transferor` = TRUE → Ghanshyam may apply.

Overruled: Veer Bala Gulati v. MCD (2003) SCC OnLine Del 345  
  The Delhi High Court’s earlier view that unregistered ATS with GPA constitutes a transaction to sell is rejected as not in consonance with Section 54 TPA and Shakeel Ahmed.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: gpa_registered
Type: FactEntry[bool]
Description: Whether the General Power of Attorney relied upon by the third party is registered
Module: M10
Extraction: From SA documents or title records

Field name: sa_applicant_type
Type: FactEntry[str]
Description: Type of applicant — "Borrower", "Guarantor", "Third Party"
Module: M10
Extraction: From SA filing details and relationship to loan

**B. New YAML Rule Needed:**
Module: M10
Rule ID: M10_T3_unregistered_ats_gpa_no_locus
Conditions: sa_applicant_type="Third Party" AND ats_registered=False AND gpa_registered=False
Severity: FATAL
Message: "Third party lacks locus to challenge SARFAESI enforcement based on unregistered ATS and GPA. No valid title conferred under Section 54 TPA and Section 17 Registration Act."
Judgment tag: ["Raj_Kumar_Aggarwal", "Shakeel_Ahmed"]
Statutory basis: TPA

**C. No New Ground Codes Needed**  
The argument fits within `THIRD_PARTY_ATS` as the third party is relying on an ATS, even if unregistered.

**D. Existing Judgments to Update:**
File: ghanshyam_v_yogendra_rathi.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Raj Kumar Aggarwal (2024 SCC OnLine Del 3256) — held that a third party with unregistered ATS and GPA lacks locus to challenge SARFAESI auction by a secured creditor, unlike Ghanshyam which involved a dispute between transferor and transferee."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: THIRD_PARTY_ATS
