---
citation: "2008 (4) AIR KANT HCR 285"
title: "M/S.Lakshmi Shankar Mills (P) Ltd vs The Authorised Officer/Chief Manager"
short_name: "Lakshmi Shankar Mills"
court: HIGH_COURT
high_court_state: "Tamil Nadu"
bench_strength: 3
judgment_date: "2008-04-15"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["NOTICE_ALL_PARTIES", "REPLY_NOT_GIVEN", "LIMITATION_EXPIRED"]
statutory_basis: ACT
act_sections: ["Section 13(4)", "Section 17"]
rules_sections: []
slrai_modules: ["M1", "M2", "M4"]
keywords: ["Section 17 appeal", "automatic stay", "deposit condition", "interim order DRT", "scope of Section 17", "no automatic stay", "Tribunal ancillary powers", "final determination"]
retrieval_condition: "Applies when a borrower files a Section 17 application but no interim stay is granted, and the bank proceeds with auction despite the pending challenge."
source: HC_FULL_TEXT
ik_doc_id: "1555930"
ik_url: "https://indiankanoon.org/doc/1555930/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers contended that the filing of an application under Section 17 of the SARFAESI Act automatically stays all enforcement proceedings, including auction, even in the absence of a formal interim order from the DRT. They argued that the secured creditor cannot proceed with any measure under Section 13(4) until the DRT has declared, under Section 17(4), that the bank's action was in accordance with the Act. They further claimed that the Tribunal lacks power to impose a deposit condition for granting stay and that the merits of their objections to the bank's demand must be fully adjudicated during the Section 17 proceedings.

## HOLDING SUMMARY

The filing of an application under Section 17 of the SARFAESI Act does not automatically stay the secured creditor's enforcement actions under Section 13(4). The right to proceed with auction or other measures remains with the bank unless the Debt Recovery Tribunal explicitly grants an interim stay. The Tribunal has ancillary powers under Section 19(12) of the RDDBFI Act, read with Section 17(7), to pass interim orders, including stay, subject to conditions such as deposit. However, the Tribunal cannot issue a mandatory interim order for restoration of possession or management before final determination of the Section 17 application. The scope of inquiry under Section 17 includes whether the bank's actions were in accordance with the Act and rules, allowing borrowers to raise all legal objections, but not requiring adjudication of the exact quantum of debt. This applies when: a Section 17 application is filed without an interim stay, and the bank proceeds with auction.

## KEY FACTS OF THIS CASE

Two sets of petitions were consolidated before the Madras High Court: one by Lakshmi Shankar Mills challenging Indian Bank's auction after DRT imposed a deposit condition, and another by Canara Bank challenging a reduced deposit order by DRAT. In both cases, borrowers had defaulted on loans secured by immovable property. The banks issued demand notices under Section 13(2), classified the accounts as NPAs, and took possession under Section 13(4). The borrowers filed applications under Section 17 before the DRT, which imposed deposit conditions for stay. When the borrowers failed to comply, the banks proceeded with auction. The DRT and DRAT decisions were challenged, leading to this reference on the interpretation of Sections 13 and 17.

## WHAT THE COURT DECIDED

The High Court held that there is no automatic stay upon filing of a Section 17 application, and the secured creditor may proceed with auction unless an interim order of stay is passed by the Tribunal. It affirmed the Tribunal's power to impose deposit conditions while granting interim relief. The Court also ruled that the Tribunal cannot pass interim mandatory orders for restoration of possession or management before final determination of the Section 17 application. The reference was answered in favour of the banks, upholding the validity of the enforcement actions.

## KEY QUOTE

The corollary is that, there is no automatic stay or prohibition on the secured creditor to take recourse to one or more measures under sub-section (4) to Section 13 of the SARFAESI Act to recover its secured debts, till an interim order is passed by the Tribunal.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `challenges_auction` is TRUE — borrower has filed a challenge to the bank's auction
2. `drt_interim_stay_granted` is FALSE — no interim stay was granted by the DRT
3. `prayer_scope_covers_current_measure` is TRUE — the SA includes a prayer to set aside auction
4. `measure_type` is "auction" — the contested measure is an auction
5. `previous_sa_filed` is TRUE — a prior Section 17 application was filed without interim relief

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the DRT has granted an interim stay of auction — in that case, the bank proceeding with auction would be in violation of court orders and a different set of precedents applies.
   SLRAI ROUTING: if `drt_interim_stay_granted` = TRUE → judgment does not apply; if FALSE → this judgment applies.

2. When the borrower has not filed any application under Section 17 — this judgment specifically addresses the legal effect of such filing, and absence of filing is governed by general SARFAESI enforcement principles.

3. When the challenge is based solely on defective service of notice or non-receipt of Section 13(2) notice — such cases fall under service defect jurisprudence (e.g., Kanaiyalal) and are not governed by this judgment on post-possession challenges.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002  
Primary provision: Section 17(4) — "If, the Debts Recovery Tribunal declares the recourse taken by a secured creditor under sub-section (4) of section 13, is in accordance with the provisions of this Act and the rules made thereunder, then, notwithstanding anything contained in any other law for the time being in force, the secured creditor shall be entitled to take recourse to one or more of the measures specified under sub-section (4) of section 13 to recover his secured debt."  
Instrument level: ACT  
Nature of provision: MANDATORY — court interpreted the absence of automatic stay as legislative intent to enable speedy recovery.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Mardia Chemicals Ltd. v. Union of India (2004) 4 SCC 311  
  Affirmed that Section 17 provides a meaningful remedy but rejected the argument that it creates an automatic stay. Upheld the Tribunal's ancillary power to grant interim relief.

Distinguishes: Ramco Super Leathers Ltd. v. UCO Bank (2007) 5 MLJ 986  
  This judgment affirms the reasoning in Ramco Super Leathers that there is no automatic stay. SLRAI ROUTING: both judgments apply when `drt_interim_stay_granted` = FALSE; Ramco Super Leathers supports the same principle.

Affirmed: Transcore v. Union of India (2006) 5 CTC 753  
  Endorsed the view that SARFAESI proceedings are summary in nature and not meant for detailed adjudication of debt quantum, but allow challenge to legality of enforcement actions.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed**  
No new fields required. All conditions are supported by existing schema.

**B. New YAML Rules Needed**  
Module: M3  
Rule ID: M3_C1_no_automatic_stay  
Conditions: challenges_auction=True AND drt_interim_stay_granted=False  
Severity: WARNING  
Message: "No automatic stay arises upon filing of Section 17 application. Bank may proceed with auction unless interim stay is granted."  
Judgment tag: ["Lakshmi_Shankar_Mills"]  
Statutory basis: ACT  

**C. New Ground Codes Needed**  
No new ground codes required. The issues are covered under existing codes: LIMITATION_EXPIRED (for time-bound challenges), REPLY_NOT_GIVEN, and NOTICE_ALL_PARTIES.

**D. Existing Judgments to Update**  
File: ramco_super_leathers_v_uco_bank.md  
Section: ## RELATIONSHIP TO OTHER JUDGMENTS  
Add: "Followed by: Lakshmi Shankar Mills (2008 AIR Kant HCR 285) — affirmed that no automatic stay arises upon filing of Section 17 application and bank may proceed with auction."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: NOTICE_ALL_PARTIES
