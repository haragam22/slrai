---
citation: "2022 SCC OnLine SC 45"
title: "Phoenix ARC Private Limited v. Vishwa Bharati Vidya Mandir & Ors."
short_name: "Phoenix ARC v. Vishwa Bharati"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2022-01-12"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["PENDING_SA_CONCEALED"]
statutory_basis: ACT
act_sections: ["Section 13(4)", "Section 17"]
rules_sections: []
slrai_modules: ["M1", "M4"]
keywords: ["Section 17 alternative remedy", "writ petition maintainability", "private ARC as party", "abuse of process Article 226", "interim stay against SARFAESI"]
retrieval_condition: "Applies when a borrower files a writ petition under Article 226 against a private ARC's proposed SARFAESI action despite the availability of an effective alternative remedy under Section 17."
source: SC_FULL_TEXT
ik_doc_id: "186727474"
ik_url: "https://indiankanoon.org/doc/186727474/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers alleged that the communication dated 13.08.2015 issued by the ARC was a de facto possession notice under Section 13(4) of the SARFAESI Act and that it violated Rule 8(1) and Rule 8(2) of the Security Interest (Enforcement) Rules, 2002, as no formal possession notice was issued or published. They contended that the ARC, though a private entity, was performing public functions and thus amenable to writ jurisdiction under Article 226 of the Constitution. They further argued that the alternative remedy under Section 17 was not an absolute bar to approaching the High Court, especially when the action was allegedly illegal or contrary to statutory requirements. The prayer before the High Court was to quash the communication and maintain status quo on the secured assets.

## HOLDING SUMMARY

The Supreme Court held that a writ petition under Article 226 of the Constitution is not maintainable against a private Asset Reconstruction Company (ARC) for proposed or contemplated SARFAESI actions, particularly when an efficacious alternative remedy under Section 17 of the SARFAESI Act is available. The Court reaffirmed that the statutory remedy under Section 17 is both expeditious and effective, and the High Court must insist on exhaustion of such remedies before entertaining writ petitions, especially in financial recovery matters. Granting interim relief in such cases, which effectively stalls SARFAESI proceedings, constitutes an abuse of process and causes serious prejudice to the financial health of secured creditors. This applies when: a borrower files a writ petition under Article 226 against a private ARC’s proposed enforcement action despite the availability of a statutory appeal under Section 17.

## KEY FACTS OF THIS CASE

The respondents, educational societies, had availed credit facilities totaling Rs. 125.65 crores from Saraswat Co-operative Bank, secured by equitable mortgage via deposit of title deeds. The accounts were classified as NPA in April 2013. After restructuring failed, the NPA was assigned to Phoenix ARC in March 2014. The ARC issued a communication on 13.08.2015 proposing to take possession under Section 13(4) if dues were not paid within 15 days. The borrowers challenged this communication via writ petitions before the Karnataka High Court, which granted repeated interim orders directing status quo upon payment of Rs. 3 crores in total. The ARC appealed to the Supreme Court, arguing the writ petitions were non-maintainable.

## WHAT THE COURT DECIDED

The Supreme Court allowed the appeals, holding that the writ petitions were not maintainable against a private ARC and that the High Court erred in entertaining them and granting interim relief. The Court dismissed the writ petitions and vacated the ex-parte interim orders dated 26.08.2015, 28.02.2017, and 27.03.2018. The borrowers were directed to pay costs of Rs. 1 lakh to the ARC. The Court emphasized that such writ petitions amount to an abuse of process when a statutory remedy under Section 17 is available.

## KEY QUOTE

Filing of the writ petitions by the borrowers before the High Court under Article 226 of the Constitution of India is an abuse of process of the Court.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `sa_applicant_type` is "Borrower" — the applicant in the current case is the borrower
2. `challenges_demand_notice` is FALSE — the challenge is not to the Section 13(2) notice
3. `challenges_auction` is FALSE — the challenge is not to an auction or sale
4. `prayer_scope_covers_current_measure` is TRUE — the prayer includes interim stay on SARFAESI action
5. `measure_type` is "Possession Notice (Proposed)" — the measure challenged is a proposed action under Section 13(4)
6. `previous_sa_filed` is FALSE — no prior Section 17 application has been filed
7. `drt_interim_stay_granted` is FALSE — no stay has been granted by DRT
8. `court` is "HIGH_COURT" — the petition is filed under Article 226 in the High Court
9. `respondent_type` is "Private ARC" — the respondent is a private Asset Reconstruction Company

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the SARFAESI action has already been taken (e.g., possession physically taken or auction conducted) — in that case, the borrower may have grounds to file under Article 226 if the action is patently illegal or violates fundamental rights. SLRAI ROUTING: if `possession_taken_date` is not null → this judgment does not apply; consider *Kanaiyalal* or *Mathew Varghese* instead.

2. When the respondent is a public sector bank or a State authority — in such cases, Article 226 jurisdiction is clearly maintainable. SLRAI ROUTING: if `respondent_type` is "Public Sector Bank" → this judgment does not apply.

3. When the borrower has already filed a Section 17 application before the DRT — the alternative remedy is exhausted, and a writ may be maintainable on grounds of inordinate delay. SLRAI ROUTING: if `previous_sa_filed` = TRUE → this judgment does not apply.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002  
Primary provision: Section 17 — "Any person (including the borrower), aggrieved by any measure taken by the authorised officer under sub-section (4) of section 13 may make an application to the Debts Recovery Tribunal..."  
Verbatim text: "Any person (including the borrower), aggrieved by any measure taken by the authorised officer under sub-section (4) of section 13 may make an application to the Debts Recovery Tribunal having jurisdiction in the region, within thirty days from the date on which the measure was taken..."  
Level: ACT  
Nature: MANDATORY — the Court held that Section 17 provides an efficacious and exclusive remedy, making writ jurisdiction inapplicable when this remedy is available.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: United Bank of India v. Satyawati Tondon (2010) 8 SCC 110  
  Reaffirmed that when an effective statutory remedy exists under SARFAESI, High Court should not entertain writ petitions under Article 226.

Follows: Kanaiyalal Lalchand Sachdev v. State of Maharashtra (2011) 2 SCC 782  
  Affirmed the principle that Section 17 is an efficacious alternative remedy, and writ jurisdiction should not be used to bypass it.

Distinguishes: J. Rajiv Subramaniyan v. Pandiyas (2014) 5 SCC 651  
  The borrowers relied on this case to argue that ARCs perform public functions, but the Court noted that in J. Rajiv Subramaniyan, the maintainability of the writ was not contested, so it does not support the proposition.  
  SLRAI ROUTING: if `respondent_type` = "Private ARC" AND `writ_issued` = TRUE → *Phoenix ARC* applies (writ not maintainable); if `respondent_type` = "Public Bank" → *J. Rajiv Subramaniyan* may apply.

Overruled: None  
Affirmed: General Manager, Sri Siddeshwara Co-op Bank v. Ikbal (2013) 10 SCC 83  
  Reaffirmed that statutory remedies under SARFAESI must be exhausted before approaching High Court.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: respondent_type
Type: FactEntry[str]
Description: Type of respondent in the writ petition — "Private ARC", "Public Sector Bank", "State Authority", etc.
Module: M1
Extraction: From the respondent's identity in the writ petition or SA

Field name: measure_type
Type: FactEntry[str]
Description: Nature of the SARFAESI measure challenged — "Proposed Action", "Possession Taken", "Auction Conducted", etc.
Module: M1
Extraction: From the nature of the communication or action challenged

**B. New YAML Rules Needed:**
Module: M1
Rule ID: M1_C8_writ_against_private_arc
Conditions: respondent_type="Private ARC" AND measure_type="Proposed Action" AND previous_sa_filed=False
Severity: FATAL
Message: "Writ petition under Article 226 against a private ARC's proposed SARFAESI action is not maintainable. Section 17 provides an efficacious alternative remedy. Filing such a petition may constitute abuse of process."
Judgment tag: ["Phoenix ARC v. Vishwa Bharati"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: j_rajiv_subramaniyan_pandiyas.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Phoenix ARC v. Vishwa Bharati (2022 SCC OnLine SC 45) — held that writ jurisdiction is not maintainable against a private ARC when an alternative remedy under Section 17 is available, and that J. Rajiv Subramaniyan does not support maintainability where the issue was not contested."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: PENDING_SA_CONCEALED
