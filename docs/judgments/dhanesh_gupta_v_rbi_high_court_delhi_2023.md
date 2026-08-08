---
citation: "2023/DHC/000148"
title: "Mr. Dhanesh Gupta And Ors vs Reserve Bank Of India And Anr"
short_name: "Dhanesh Gupta"
court: HIGH_COURT
high_court_state: "Delhi"
bench_strength: 2
judgment_date: "2023-01-09"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["SERVICE_DEFECT"]
statutory_basis: ACT
act_sections: ["Section 13(2)", "Section 13(4)", "Section 14", "Section 17"]
rules_sections: []
slrai_modules: ["M1", "M4"]
keywords: ["Section 17", "alternative remedy", "writ petition not maintainable", "DRT jurisdiction", "aggrieved by Section 13(4)"]
retrieval_condition: "Applies when the borrower files a writ petition challenging SARFAESI measures instead of a Section 17 application before the DRT."
source: HC_FULL_TEXT
ik_doc_id: "73548054"
ik_url: "https://indiankanoon.org/doc/73548054/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers alleged that due to the financial hardship caused by the COVID-19 pandemic and associated lockdowns, they were unable to service their EMIs from October to December 2019, and therefore, the bank’s initiation of SARFAESI proceedings was unjust. They contended that the writ petition was maintainable as they sought quashing of the Section 13(4) notice and the CMM order under Section 14, and prayed for a writ of certiorari to quash those actions, a writ of mandamus to restore the loan account to regular status, and an interim stay on possession. They further argued that the High Court should exercise its writ jurisdiction in light of the exceptional circumstances.

## HOLDING SUMMARY

The High Court reaffirmed that where a statutory remedy under Section 17 of the SARFAESI Act is available, a writ petition under Article 226 is not maintainable, even if the borrower raises equitable arguments such as pandemic-related hardship. Section 17 provides an efficacious alternative remedy for any person aggrieved by measures taken under Section 13(4), including taking possession or applying to the CMM. The existence of this exclusive remedy bars the High Court from entertaining writ petitions challenging SARFAESI enforcement actions. The court emphasized that the Debt Recovery Tribunal is the designated forum to adjudicate disputes concerning the legality of SARFAESI measures, and the High Court should not interfere unless no effective remedy exists. This applies when: the borrower challenges SARFAESI measures through a writ petition instead of filing a Section 17 application before the DRT.

## KEY FACTS OF THIS CASE

The appellants, Mr. Dhanesh Gupta and others, obtained a loan of Rs. 2.68 crore from Standard Chartered Bank, secured by mortgage of a property in Hauz Khas, New Delhi, with disbursement in February 2018. They defaulted on EMIs from October to December 2019, leading the bank to issue a Section 13(2) demand notice and declare the account as NPA. After non-payment, the bank took possession under Section 13(4) and obtained an order from the CMM under Section 14 on 15.09.2020. The borrowers filed a writ petition before the Delhi High Court challenging these actions, which was dismissed by the Single Judge on grounds of alternative remedy. The present LPA was filed against that dismissal.

## WHAT THE COURT DECIDED

The Division Bench dismissed the appeal, upholding the Single Judge’s order that the writ petition was not maintainable due to the availability of an efficacious alternative remedy under Section 17 of the SARFAESI Act. The court declined to interfere with the bank’s enforcement actions, clarifying that all contentions and rights of the parties remain open for adjudication before the DRT. No interim relief or quashing of SARFAESI measures was granted.

## KEY QUOTE

An action under Section 14 of the Act constitutes an action taken after the stage of Section 13(4), and therefore, the same would fall within the ambit of Section 17(1) of the Act. Thus, the Act itself contemplates an efficacious remedy for the borrower or any person affected by an action under Section 13(4) of the Act, by providing for an appeal before the DRT.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when the borrower files a writ petition challenging SARFAESI measures instead of a Section 17 application before the DRT.

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the borrower has already filed a Section 17 application before the DRT — in that case, the DRT is seized of the matter and this judgment does not bar relief; the focus shifts to merits of the SA.
   SLRAI ROUTING: if `sa_filing_date` is not null → DRT jurisdiction applies; this judgment does not apply.

2. When the borrower is challenging an auction sale and seeks relief under Section 17 after auction — in that case, the timing and grounds of the SA determine applicability of auction-specific precedents like Celir LLP or E. Muthurathinasabathy.
   SLRAI ROUTING: if `auction_date` is not null → auction-specific judgments apply.

3. When the writ petition raises constitutional issues not covered under Section 17 — in such rare cases, the High Court may exercise writ jurisdiction.
   SLRAI ROUTING: if `prayer_scope_covers_current_measure` is FALSE and constitutional issue raised → High Court jurisdiction may apply.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002  
Primary provision: Section 17(1) — "Any person (including borrower), aggrieved by any of the measures referred to in sub-section (4) of section 13 taken by the secured creditor or his authorised officer under this Chapter, may make an application... to the Debts Recovery Tribunal having jurisdiction in the matter within forty five days from the date on which such measure had been taken"  
Instrument level: ACT  
Nature of provision: MANDATORY — the provision creates an exclusive remedy, making DRT the sole forum for challenging SARFAESI measures under Section 13(4)

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Kanaiyalal Lalchand Sachdev & Ors. v. State of Maharashtra and Ors. (2011) 2 SCC 782  
  Affirmed that actions under Section 14 fall within Section 17(1) and DRT is the appropriate forum.  
  SLRAI ROUTING: if `measure_type` = "possession" → Kanaiyalal applies; this judgment reinforces it.

Follows: United Bank of India v. Satyawati Tondon and Ors. (2010) SCC Online SC 776  
  Reiterated that writ petitions are not maintainable when an efficacious statutory remedy under SARFAESI exists.  
  SLRAI ROUTING: if `sa_filing_date` = null → this judgment applies; if filed → DRT jurisdiction applies.

Distinguishes: Phoenix ARC Pvt. Ltd. v. Vishwa Bharti Vidya Mandir and Ors. (2022) SCC Online SC 44  
  Phoenix ARC reaffirmed that writ petitions are not maintainable when Section 17 remedy exists. This case applies the same principle to pandemic-related hardship claims.  
  SLRAI ROUTING: if hardship claimed due to external factors → still, Section 17 applies; writ not maintainable.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

No new fields, rules, or ground codes required. Fits within existing schema.

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: SERVICE_DEFECT
