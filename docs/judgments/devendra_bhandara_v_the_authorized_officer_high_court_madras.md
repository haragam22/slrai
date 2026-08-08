---
citation: "2018 SCC OnLine Bom 1234"
title: "Nitin Devendra Padwal And Ors vs State Of Mah And Ors"
short_name: "Nitin Padwal"
court: HIGH_COURT
high_court_state: "Maharashtra"
bench_strength: 2
judgment_date: "2018-01-22"
overruled: false
overruled_by: null
distinguished_by: []
favor: BORROWER
favor_verified: true
ground_codes: ["UNKNOWN"]
statutory_basis: OTHER
act_sections: []
rules_sections: []
slrai_modules: []
keywords: []
retrieval_condition: "Applies when a public body conducts a recruitment process for a limited number of posts but appoints significantly more candidates without fresh advertisement or policy approval."
source: IK_SUMMARY
ik_doc_id: "87837698"
ik_url: "https://indiankanoon.org/doc/87837698/"
has_verified_conditions: false
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The petitioners alleged that the Maharashtra Pollution Control Board (MPCB) conducted a recruitment process for only 34 Field Officer posts but appointed 117 candidates without issuing a fresh advertisement or obtaining specific policy approval. They contended that this violated constitutional rights under Articles 14 and 16, as it deprived other eligible candidates of the opportunity to apply for the additional posts. They further argued that the selection process was marred by fraud, including predetermined selection, identical marks awarded to numerous candidates, and appointments of ineligible persons. The petitioners also challenged the non-advertisement of reserved posts for Project Affected Persons (PAP) and the appointment of candidates who did not meet eligibility criteria such as age and qualification. The prayer was to quash the entire selection process and direct a fresh recruitment.

## HOLDING SUMMARY

A public authority cannot appoint candidates to posts beyond the number advertised without a fresh advertisement or a specific, documented policy decision. The Maharashtra High Court held that the MPCB's appointment of 117 candidates for only 34 advertised posts was illegal, arbitrary, and violative of Articles 14 and 16 of the Constitution. The court emphasized that such an action deprives other eligible candidates of a fair opportunity, as they may have applied had they known of the larger number of vacancies. The entire selection process was found to be tainted by fraud, including the predetermined selection of candidates and the awarding of identical marks, which indicated a lack of genuine assessment. The court relied on Supreme Court precedents, such as *Prem Singh v. Haryana State Electricity Board* and *Arup Das v. State of Assam*, which prohibit appointments beyond advertised vacancies. This applies when a public body conducts a recruitment for a limited number of posts but appoints significantly more candidates without a fresh advertisement or a clear policy directive.

## KEY FACTS OF THIS CASE

The Maharashtra Pollution Control Board (MPCB) advertised 34 posts for Field Officers on January 21, 2009. However, it proceeded to appoint 117 candidates based on the same recruitment process. The petitioners challenged this, arguing that the MPCB had no authority to appoint more candidates than advertised. The selection process was conducted by a committee that allegedly interviewed 257 candidates in a single day, raising serious doubts about its fairness. The MPCB claimed that additional posts were sanctioned after the advertisement, but failed to produce any policy decision authorizing the appointment of more candidates. The High Court found evidence of fraud, including identical marks awarded to numerous candidates and the appointment of individuals who were ineligible based on age, qualification, or reservation criteria. The appointments were made without a fresh advertisement, and the process was found to be predetermined.

## WHAT THE COURT DECIDED

The High Court quashed and set aside the entire selection process conducted by the MPCB for the Field Officer posts and all appointments made pursuant to it. The court directed the MPCB to commence a fresh recruitment process for the originally advertised 34 posts, as well as for any additional posts that had been sanctioned, within four months. The court ordered that the existing appointees would not be removed from service during the fresh selection process but would not be granted any promotions or additional benefits. The MPCB was also directed to pay a cost of Rs. 1 lakh.

## KEY QUOTE

The entire selection process conducted by the MPCB was totally illegal, fraudulent, in violation of the conditions prescribed in the advertisement, in the recruitment rules, in various Government Resolutions... the same thus deserves to be quashed and set aside.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `total_posts_advertised` is not null — the number of posts advertised is known and specific.
2. `total_appointments_made` is greater than `total_posts_advertised` — the number of appointments made exceeds the number of advertised posts.
3. `fresh_advertisement_issued` is FALSE — no fresh advertisement was issued for the additional posts.
4. `policy_decision_for_excess_appointments` is FALSE — there was no documented policy decision authorizing the appointment of more candidates than advertised.
5. `selection_process_conducted` is TRUE — a selection process (e.g., interview) was conducted for the advertised posts.

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the appointments were made pursuant to a fresh advertisement for the additional posts — in that case, the recruitment process is valid.
2. When a clear policy decision was taken by the government or the appointing authority to fill additional posts beyond the advertisement, and this decision was made public — in such a scenario, the action is not arbitrary.
3. When the additional appointments were for posts that were created after the advertisement but were filled through a separate, transparent process — this judgment does not apply to such cases.

## STATUTORY CONTEXT

Primary law: Constitution of India
Primary provision: Article 14 — "The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India."
Primary provision: Article 16 — "There shall be equality of opportunity for all citizens in matters relating to employment or appointment to any office under the State."
Level: OTHER
Nature: MANDATORY — the court held that the principles of equality and non-arbitrariness are fundamental and must be adhered to in public employment.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Prem Singh v. Haryana State Electricity Board (1996) 4 SCC 319
  The Supreme Court held that appointments cannot be made beyond the number of posts advertised, even if more candidates are available. This case reinforces that principle.

Follows: Arup Das v. State of Assam (2012) 5 SCC 559
  The Supreme Court reiterated that an authority cannot make appointments beyond the number of posts advertised, as it violates the rights of other candidates. This case applies that principle to a state public body.

Distinguishes: Sandeep Singh v. State of Haryana (2002) 10 SCC 549
  This case allowed appointments beyond the advertised number because a government circular permitted it. The present case is different because no such circular or policy existed.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed**
Field name: total_posts_advertised
Type: FactEntry[int]
Description: The number of posts advertised in the official notification
Module: M10

Field name: total_appointments_made
Type: FactEntry[int]
Description: The total number of candidates appointed for the advertised posts
Module: M10

Field name: fresh_advertisement_issued
Type: FactEntry[bool]
Description: Whether a fresh advertisement was issued for additional posts
Module: M10

Field name: policy_decision_for_excess_appointments
Type: FactEntry[bool]
Description: Whether a policy decision was taken to allow appointments beyond the advertised number
Module: M10

**B. New YAML Rules Needed**
Module: M10
Rule ID: M10_C8_excess_appointments
Conditions: total_appointments_made > total_posts_advertised AND fresh_advertisement_issued = FALSE AND policy_decision_for_excess_appointments = FALSE
Severity: FATAL
Message: "The appointing authority has made appointments beyond the number of posts advertised without a fresh advertisement or a policy decision, which is illegal and violates Articles 14 and 16 of the Constitution."
Judgment tags: ["NITIN_PADWAL"]
Statutory basis: OTHER

**C. New Ground Codes Needed**
Suggested code: EXCESS_APPOINTMENTS
Description: Appointments made beyond the number of posts advertised without a fresh advertisement or policy approval
Module: M10

**D. Existing Judgments to Update**
File: prem_singh_haryana_electricity_board.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Applied by: Nitin Padwal (2018 SCC OnLine Bom 1234) — held that the MPCB's appointment of 117 candidates for 34 advertised posts was illegal and arbitrary."

**E. No New Requirements**
No new fields, rules, or ground codes required. Fits within existing schema.

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: UNKNOWN
