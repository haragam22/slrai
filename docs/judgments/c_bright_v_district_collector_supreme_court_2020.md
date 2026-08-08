---
citation: "AIR 2020 SC 5747"
title: "C. Bright v. The District Collector & Ors."
short_name: "C. Bright"
court: SUPREME_COURT
high_court_state: null
bench_strength: 3
judgment_date: "2020-11-05"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["POSSESSION_DEFECT"]
statutory_basis: ACT
act_sections: ["Section 14"]
rules_sections: []
slrai_modules: ["M3"]
keywords: ["Section 14", "30 days", "60 days", "shall", "directory provision", "District Magistrate", "possession delay"]
retrieval_condition: "Applies when the District Magistrate failed to pass an order for possession under Section 14 within 60 days from the application date."
source: SC_FULL_TEXT
ik_doc_id: "166859104"
ik_url: "https://indiankanoon.org/doc/166859104/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower(s) alleged that Section 14 of the SARFAESI Act, which mandates the District Magistrate to pass an order for possession of secured assets within 30 days (extendable to 60 days), is a mandatory provision. They contended that failure to pass such an order within the stipulated time renders the proceedings invalid and abates the process. The prayer before the DRT/HC/SC was to set aside the enforcement proceedings on the ground that the District Magistrate failed to act within the statutory timeframe, thereby violating the mandatory nature of Section 14.

## HOLDING SUMMARY

Section 14 of the SARFAESI Act, which requires the District Magistrate to pass an order for possession of secured assets within 30 days (extendable to 60 days upon recording reasons), is a directory provision and not mandatory. The use of the word "shall" does not automatically render a provision mandatory; the court must examine the object and purpose of the statute. The primary objective of Section 14 is to ensure expeditious recovery by banks and financial institutions, and interpreting it as mandatory would defeat this purpose by allowing borrowers to delay proceedings. Non-compliance with the time limit does not divest the District Magistrate of jurisdiction or render the proceedings void. The provision imposes a duty to act diligently but does not result in abatement of proceedings. This applies when: the District Magistrate failed to pass an order within 60 days but continues to act in the matter.

## KEY FACTS OF THIS CASE

The case arose from a challenge to the Kerala High Court's ruling that Section 14 of the SARFAESI Act is directory, not mandatory. The appellant, C. Bright, had defaulted on a loan secured by immovable property. After the bank issued a demand notice and took steps under Section 13(4), it filed an application under Section 14 before the District Magistrate for assistance in taking possession. The District Magistrate did not pass an order within the 30-day period or even within the extended 60-day period. The borrower challenged the validity of the enforcement action on this ground. The High Court upheld the bank's position, and the matter reached the Supreme Court on appeal.

## WHAT THE COURT DECIDED

The Supreme Court dismissed the appeal, upholding the Kerala High Court's finding that Section 14 is directory and not mandatory. It held that the failure of the District Magistrate to pass an order within 30 or even 60 days does not abate the proceedings or divest the authority of jurisdiction. The District Magistrate remains under an obligation to facilitate possession at the earliest. The secured creditor's remedy under Section 14 is not rendered redundant by delay in passing orders.

## KEY QUOTE

the time limit stipulation in the amended Section 14 of the SARFAESI Act is directory and not mandatory.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `drt_interim_stay_granted` is FALSE — no stay was granted by DRT or court that delayed possession
2. `possession_taken_date` is not null — possession was eventually taken
3. `possession_notice_date` is not null — notice for possession was issued
4. `days_from_measure_to_sa` > 60 — more than 60 days elapsed between the measure (application under Section 14) and the SA filing
5. `challenges_demand_notice` is FALSE — the challenge is specifically about delay in possession, not the demand notice itself

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the delay in possession was due to a court-ordered stay — in that scenario, *Hindon Forge Private Limited v. State of Uttar Pradesh* applies, and the secured creditor is not at fault.
   SLRAI ROUTING: if `drt_interim_stay_granted` = TRUE → Hindon Forge applies.

2. When the challenge is to the validity of the demand notice under Section 13(2) — in that case, *Mardia Chemicals* or *Kanaiyalal* applies depending on the nature of the defect.

## STATUTORY CONTEXT

Primary law: Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002  
Primary provision: Section 14(1) — "Provided, further that on receipt of the affidavit from the Authorised Officer, the District Magistrate or the Chief Metropolitan Magistrate, as the case may be, shall, after satisfying the contents of the affidavit pass suitable orders for the purpose of taking possession of the secured asset within a period of thirty days from the date of application: Provided also that if no order is passed by the Chief Metropolitan Magistrate or District Magistrate within the said period of thirty days for reasons beyond his control, he may, after recording reasons in writing for the same, pass the order within such period not exceeding in the aggregate sixty days."  
Instrument level: ACT  
Nature of provision: DIRECTORY — court held that non-compliance does not render proceedings void

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Nasiruddin & Ors. v. Sita Ram Agarwal (2003) 2 SCC 577  
  Held that time limits for public functionaries are directory unless consequences of non-compliance are specified.

Distinguishes: A.K. Pandey (2009) 10 SCC 552  
  A.K. Pandey dealt with a mandatory procedural safeguard for accused in court-martial; here, the provision is administrative and procedural, not affecting fundamental rights.  
  SLRAI ROUTING: if `ao_has_written_authorization` = FALSE → A.K. Pandey applies; if `possession_delay` = TRUE → C. Bright applies.

Distinguishes: Harshad Govardhan Sondagar (2014) 6 SCC 1  
  That case dealt with tenancy rights and jurisdiction of DRT; this case concerns statutory interpretation of time limits for public authorities.

Affirmed: Hindon Forge Private Limited & Anr. v. State of Uttar Pradesh (2019) 2 SCC 198  
  Affirmed the object of the Act as enabling speedy recovery and the role of Magistrate in facilitating possession.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed**  
Field name: days_from_measure_to_sa  
Type: FactEntry[int]  
Description: Number of days between the enforcement measure (e.g., Section 14 application) and filing of SA  
Computed from: sa_filing_date - measure_date  
Module: M3  

Field name: possession_delay  
Type: FactEntry[bool]  
Description: True if possession order not passed within 60 days of Section 14 application  
Computed from: (possession_notice_date to possession_taken_date) > 60 days  
Module: M3  

**B. New YAML Rules Needed**  
Module: M3  
Rule ID: M3_C1_section14_directory  
Conditions: challenges_demand_notice = FALSE AND possession_delay = TRUE  
Severity: WARNING  
Message: "Section 14 delay does not invalidate proceedings per C. Bright. The provision is directory, not mandatory."  
Judgment tag: ["C_Bright"]  
Statutory basis: ACT  

**C. Existing Judgments to Update**  
File: hindon_forge_v_state_of_up.md  
Section: ## RELATIONSHIP TO OTHER JUDGMENTS  
Add: "Distinguished by: C. Bright (2020) — held that delay by District Magistrate under Section 14 does not abate proceedings, whereas Hindon Forge applies when stay orders cause delay."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: POSSESSION_DEFECT
