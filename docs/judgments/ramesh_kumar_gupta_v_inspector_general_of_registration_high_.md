---
citation: "CBI v. Ram Kumar Singh & Ors., AC No. 66/11/2008, RC No. SIB-2007-E-0001, Judgment dated 22.09.2015"
title: "IN THE COURT OF JITENDRA KUMAR MISHRA SPECIAL JUDGE (PC ACT) CBI, KARKARDOOMA COURTS : EAST DISTRICT DELHI"
short_name: "Ram Kumar Singh"
court: DRT
high_court_state: null
bench_strength: 1
judgment_date: "2015-09-22"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["UNKNOWN"]
statutory_basis: OTHER
act_sections: []
rules_sections: []
slrai_modules: []
keywords: []
retrieval_condition: "Applies when a public servant fails to act against unauthorized construction in collusion with builders, leading to pecuniary gain."
source: IK_SUMMARY
ik_doc_id: "161580504"
ik_url: "https://indiankanoon.org/doc/161580504/"
has_verified_conditions: false
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

This judgment does not involve a SARFAESI enforcement or a borrower challenging a bank's action. It is a criminal prosecution by the Central Bureau of Investigation (CBI) against a public servant (a Junior Engineer, Ram Kumar Singh) and two builders (Anil Kumar Arora and Rakesh Aggarwal) for criminal conspiracy and corruption under the Prevention of Corruption Act, 1988. The "claim" in this context is the prosecution's case, which alleged that the public servant, by abusing his official position, failed to take any action against the unauthorized construction carried out by the builders on properties in Shakarpur, Delhi. The prosecution contended that this inaction was part of a criminal conspiracy, which allowed the builders to illegally construct and sell flats, thereby causing pecuniary gain to the builders and wrongful loss to the public exchequer. The prosecution's prayer was for the conviction of the accused under Section 120-B IPC and Sections 13(1)(d) and 13(2) of the PC Act.

## HOLDING SUMMARY

A public servant commits criminal misconduct under Section 13(1)(d) of the Prevention of Corruption Act, 1988, if they abuse their official position to obtain a pecuniary advantage for another person without any public interest. The court held that the Junior Engineer (A-1), by deliberately failing to book, seal, or initiate demolition proceedings against the unauthorized construction on properties D-15 and B-53 in Shakarpur, Delhi, abused his position. This inaction, in collusion with the builders (A-2 and A-3), facilitated the illegal construction and sale of 15 flats, resulting in a pecuniary gain for the builders. The court found that the builder's act of constructing without a sanctioned plan constituted "wrongful gain," and the public servant's failure to act, despite it being his duty, amounted to obtaining this gain for another person. The court rejected the defense that the construction was regularized or that the public servant was unaware, concluding that the evidence proved a criminal conspiracy beyond a reasonable doubt. This applies when a public servant, entrusted with enforcing building regulations, intentionally fails to act against unauthorized construction in collusion with the builder, thereby enabling the builder to gain financially.

## KEY FACTS OF THIS CASE

The case arose from a large-scale inquiry into the nexus between MCD officials and builders in Delhi, initiated by the Delhi High Court. The accused, Ram Kumar Singh, was a Junior Engineer (JE) posted in Ward 71/72, Shahdara South Zone, MCD, from August 2004 to August 2005. During this period, the builder-accused, Anil Kumar Arora and Rakesh Aggarwal, purchased two plots (D-15 and B-53, Shakarpur) and constructed unauthorized buildings comprising 15 flats in total. The prosecution alleged that the JE, despite receiving complaints and having a duty to act, took no steps to book the properties, issue show-cause notices, or initiate demolition. The CBI registered a case based on these allegations, and after a trial, the Special Judge convicted all three accused. The conviction was based on the failure of the public servant to perform his statutory duties, which allowed the builders to profit from illegal construction.

## WHAT THE COURT DECIDED

The Special Judge convicted all three accused. Ram Kumar Singh (A-1) was convicted under Section 120-B IPC read with Section 13(2) read with Section 13(1)(d) of the PC Act, and also under Section 217 IPC. Anil Kumar Arora (A-2) and Rakesh Aggarwal (A-3) were convicted under Section 120-B IPC read with Section 13(2) read with Section 13(1)(d) of the PC Act. The court sentenced A-1 to six years of rigorous imprisonment and a fine of Rs. 30 lacs, A-2 to six years of rigorous imprisonment and a fine of Rs. 40 lacs, and A-3 to three and a half years of rigorous imprisonment and a fine of Rs. 15 lacs. All sentences were ordered to run concurrently.

## KEY QUOTE

A-1 by abusing his official position being a public servant committed offences punishable under Section 217 IPC and U/s 13 (2) read with Section 13(1) (d) of P.C. Act.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `sa_applicant_type` is "PUBLIC_SERVANT" — the case involves a public servant accused of misconduct.
2. `property_classification` is "UNAUTHORIZED_CONSTRUCTION" — the core issue is unauthorized construction on a property.
3. `challenges_demand_notice` is FALSE — the case is not about a SARFAESI demand notice or bank enforcement.
4. `prayer_scope_covers_current_measure` is FALSE — the legal proceedings are criminal prosecution, not a civil challenge to a bank's action.
5. The public servant had a statutory duty to act against the unauthorized construction (e.g., a Junior Engineer in a municipal corporation) but failed to do so in collusion with the builder, resulting in pecuniary gain.

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the case involves a SARFAESI Act enforcement action by a bank (e.g., a demand notice, possession, or auction). This judgment is not relevant to Securitisation Applications filed under Section 17 of the SARFAESI Act.
2. When the challenge is to the classification of an account as an NPA or the amount of debt claimed by a bank.
3. When the dispute is between a bank and a borrower over the recovery of a loan, rather than a criminal prosecution for corruption by a public official.

## STATUTORY CONTEXT

Primary law: Prevention of Corruption Act, 1988
Primary provision: Section 13(1)(d) — "A public servant is said to commit the offence of criminal misconduct... if he, while holding office as a public servant, obtains for any person any valuable thing or pecuniary advantage without any public interest."
Instrument level: OTHER
Nature of provision: MANDATORY — the court interpreted the section as being violated when a public servant's inaction leads to a pecuniary gain for another.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: A.K. Ganju v. CBI
  The court distinguished its facts from A.K. Ganju, where the High Court had quashed proceedings, by noting that in the present case, the JE had not performed his duty at all, whereas in A.K. Ganju, the JE had booked the property and issued notices.

Follows: Mir Nagvi Askari v. CBI
  The court relied on this judgment to establish the ingredients of criminal conspiracy, emphasizing that an agreement to commit an illegal act, even without direct evidence, can be inferred from circumstantial evidence.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed**
Field name: property_classification
Type: FactEntry[str]
Description: The legal status of the property (e.g., "AUTHORIZED", "UNAUTHORIZED_CONSTRUCTION", "LAL_DORA")
Module: M5
Extraction: From municipal records, sale deeds, or court findings.

Field name: sa_applicant_type
Type: FactEntry[str]
Description: The category of the party filing the application (e.g., "BORROWER", "GUARANTOR", "PUBLIC_SERVANT", "AUCTION_PURCHASER")
Module: M10
Extraction: From the title of the case and the nature of the allegations.

**B. New YAML Rules Needed**
This judgment does not introduce a new compliance rule for SARFAESI enforcement.

**C. New Ground Codes Needed**
Suggested code: PUBLIC_SERVANT_COLLUSION
Description: A public servant is accused of colluding with a builder by failing to act against unauthorized construction.
Module: M5
Justification: This case is about corruption in urban development, not a standard SARFAESI ground.

**D. Existing Judgments to Update**
No existing Class A judgments need to be updated as this case is not a SARFAESI precedent.

**E. No New Requirements**
The judgment is outside the scope of SARFAESI enforcement and does not require changes to the core schema for Securitisation Applications.

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: UNKNOWN
