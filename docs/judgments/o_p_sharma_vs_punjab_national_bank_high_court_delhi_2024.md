---
citation: "(2024) ibclaw.in 47 DRAT"
title: "O.P. Sharma vs Punjab National Bank & Anr"
short_name: "O.P. Sharma"
court: HIGH_COURT
high_court_state: "Delhi"
bench_strength: 2
judgment_date: "2024-05-22"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["THIRD_PARTY_ATS", "TENANCY_CLAIM"]
statutory_basis: TPA
act_sections: []
rules_sections: []
slrai_modules: ["M5", "M10"]
keywords: ["customary documents", "unregistered ATS", "GPA sale", "SPA sale", "Power of Attorney sale", "Section 53-A TPA", "circle rate", "registered sale deed required", "equitable rights", "title not transferred"]
retrieval_condition: "Applies when a third party claims ownership of mortgaged property based on unregistered ATS, GPA, SPA, or other customary documents without a registered sale deed."
source: IK_SUMMARY
ik_doc_id: "162053097"
ik_url: "https://indiankanoon.org/doc/162053097/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The petitioner claimed that he was a bona fide purchaser of Flat No. 301 from the guarantor (Respondent No. 2) on 12th June 2002, prior to the mortgage created in 2005, and thus the mortgage could not bind him. He contended that ownership and equitable rights in the flat were transferred through "customary documents" — an unregistered Agreement to Sell (ATS), Special Power of Attorney (SPA), General Power of Attorney (GPA), registered Will, cash receipt, and possession letter — all dated 12th June 2002. He further argued that he had been in continuous possession of the flat since 2002 and had paid Rs. 1.50 lakhs in cash, and therefore, the bank could not enforce the mortgage against his portion of the property. The prayer was to set aside the DRAT and DRT orders and declare that the bank cannot evict him from Flat No. 301.

## HOLDING SUMMARY

The Transfer of Property Act, 1882 and the Indian Registration Act, 1908 mandate that no right, title, or interest in immovable property can be legally transferred without a registered conveyance deed. An unregistered Agreement to Sell, even when accompanied by GPA, SPA, or other customary documents, does not confer ownership or legal title. Section 53-A of the TPA provides only limited protection to a transferee in possession under a contract, but does not transfer title. The Supreme Court has consistently held that so-called "Power of Attorney sales" do not constitute valid transfer of property. Therefore, the petitioner’s reliance on unregistered and non-compliant documents cannot defeat the bank’s secured interest created via a valid mortgage by deposit of title deeds. The bank’s enforcement action under SARFAESI is not barred by such an inchoate claim. This applies when: a third party claims ownership of mortgaged property based solely on unregistered ATS, GPA, or SPA without a registered sale deed.

## KEY FACTS OF THIS CASE

The guarantor (Respondent No. 2) purchased the entire third floor of a property in New Delhi via a registered sale deed dated 24th April 1996 and later created a mortgage in favour of Punjab National Bank on 21st February 2005 by deposit of title deeds, as security for a loan to M/s Right Channel Resources. The borrower defaulted, leading to SARFAESI proceedings. The petitioner, O.P. Sharma, claimed to have purchased Flat No. 301 from the guarantor in 2002 via unregistered ATS and related customary documents, and had been in possession since. He challenged the bank’s Section 13(4) notice before the DRT under Section 17. The DRT (2012) and DRAT (2014) dismissed his application, holding that no valid title was transferred. The High Court of Delhi dismissed the writ petition, affirming the lower tribunals’ findings.

## WHAT THE COURT DECIDED

The Delhi High Court dismissed the writ petition, upholding the DRAT and DRT orders. It held that the petitioner did not acquire any legal title to Flat No. 301 through the unregistered ATS and allied documents. The mortgage created by the guarantor in 2005 was valid and enforceable. The bank was entitled to proceed with the auction of the entire mortgaged property, including Flat No. 301. The interim stay orders were vacated.

## KEY QUOTE

No title could be transferred with respect to immovable properties on the basis of an unregistered Agreement to Sell or on the basis of an unregistered General Power of Attorney.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `ats_registered` is FALSE — the Agreement to Sell relied upon by the third party is unregistered
2. `ats_possession_given` is TRUE — the third party claims to be in possession under the ATS
3. `sale_deed_executed` is FALSE — no registered sale deed has been executed in favour of the third party
4. `ats_payments_made_to_loan_account` is FALSE — payments under ATS were not made to the loan account or bank
5. `property_classification` is "residential" or "commercial" — the property is immovable and subject to registration laws

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the third party has a registered sale deed — in that case, the transferee may have full ownership and the bank’s mortgage may be subject to prior sale. SLRAI ROUTING: if `sale_deed_executed` = TRUE → *Suraj Lamps* or *Shakeel Ahmed* applies depending on registration and timing.

2. When the bank had actual notice of the prior sale and still proceeded without inquiry — a claim of negligence or bad faith may arise, potentially invoking equitable principles. SLRAI ROUTING: if `bank_noc_for_tenancy_given` = TRUE or `bank_knew_of_ats` = TRUE → *K. Srinivasan v. Muthu Chettiar* or other notice-based precedents may apply.

3. When the transaction is a lease or tenancy and not a purported sale — this judgment deals with ownership claims, not tenancy rights. SLRAI ROUTING: if `lease_type` = "rental" → *M. Rajendran* or *Celina Jaitly* applies.

## STATUTORY CONTEXT

Primary law: Transfer of Property Act, 1882  
Primary provision: Section 54 — "A sale of immovable property can be made only by a registered instrument."  
Verbatim: "Where the whole of the property... is sold for a lump sum... the sale can be made only by a registered instrument."  
Level: TPA  
Nature: MANDATORY — court held that registration is mandatory for transfer of title.

Secondary law: Indian Registration Act, 1908  
Provision: Section 17(1-A) — "No document purporting to create, declare, assign, limit or extinguish any right, title or interest... shall be admitted as evidence of such right... unless it is registered."  
Level: OTHER  
Nature: MANDATORY — unregistered documents inadmissible in evidence.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Shakeel Ahmed v. Syed Akhlaq Hussain (2023) SCC OnLine SC 1526  
  Reaffirmed that unregistered ATS and GPA do not transfer title in immovable property.  
  SLRAI ROUTING: if `ats_registered` = FALSE → Shakeel Ahmed applies.

Follows: Suraj Lamps and Industries Ltd. v. State of Haryana (2011) 8 SCC 1  
  Held that GPA/ATS sales are not valid modes of property transfer; only registered sale deeds confer title.  
  SLRAI ROUTING: if `customary_documents_only` = TRUE → Suraj Lamps applies.

Distinguishes: K. Srinivasan v. Muthu Chettiar (2013) 10 SCC 705  
  K. Srinivasan allowed protection where the bank had actual notice of prior sale.  
  SLRAI ROUTING: if `bank_knew_of_ats` = TRUE → K. Srinivasan applies; if FALSE → this judgment applies.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: customary_documents_only
Type: FactEntry[bool]
Description: True if third party relies only on ATS, GPA, SPA, receipt, etc., without registered sale deed
Module: M10
Computed from: ats_registered=False AND sale_deed_executed=False AND (gpa_registered OR spa_executed OR receipt_present)

Field name: bank_knew_of_ats
Type: FactEntry[bool]
Description: True if bank had actual knowledge of prior ATS (e.g., from file records or possession)
Module: M10
Extraction: From bank’s due diligence records or borrower’s disclosure

**B. New YAML Rule Needed:**
Module: M10
Rule ID: M10_C8_customary_sale_no_title
Conditions: ats_registered=False AND sale_deed_executed=False
Severity: FATAL
Message: "Third party claiming ownership based on unregistered ATS and customary documents only — no legal title transferred. SARFAESI enforcement not barred."
Judgment tag: ["O_P_SHARMA", "SHAKEEL_AHMED", "SURAJ_LAMPS"]
Statutory basis: TPA

**C. Existing Judgments to Update:**
File: suraj_lamps_haryana.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Followed by: O.P. Sharma (2024) ibclaw.in 47 DRAT — reaffirmed that unregistered ATS and GPA do not transfer title in SARFAESI context."

File: shakeel_ahmed_hussain.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Applied in: O.P. Sharma (2024) ibclaw.in 47 DRAT — upheld DRT dismissal of SA where petitioner relied on unregistered ATS and GPA."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: THIRD_PARTY_ATS
