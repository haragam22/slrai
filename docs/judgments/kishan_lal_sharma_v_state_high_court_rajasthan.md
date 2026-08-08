---
citation: "2008 (3) RLW 1234"
title: "Sheela Sharma vs State & Ors"
short_name: "Sheela Sharma"
court: HIGH_COURT
high_court_state: "Rajasthan"
bench_strength: 1
judgment_date: "2008-09-12"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["UNKNOWN"]
statutory_basis: OTHER
act_sections: []
rules_sections: []
slrai_modules: ["M1"]
keywords: ["discrimination in selection", "Article 14 violation", "NTT certificate", "BSTC training", "professional qualification"]
retrieval_condition: "Applies when the petitioner challenges denial of appointment due to lack of NTT certificate despite undergoing BSTC/B.Ed. training."
source: IK_SUMMARY
ik_doc_id: "51934891"
ik_url: "https://indiankanoon.org/doc/51934891/"
has_verified_conditions: false
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The petitioners, who were undergoing BSTC/B.Ed. training or had appeared in the BSTC examination with supplementary results, alleged that the respondents discriminated against them by permitting candidates with NTT or Pre-Primary Teachers Training certificates to participate in the selection process while denying them similar treatment. They contended that there was no justifiable reason to treat them differently from those holding NTT certificates, especially since both categories were awaiting formal qualifications. They argued that this differential treatment violated their rights under Articles 14 and 16 of the Constitution of India. The prayer before the Court was to direct the respondents to allow them to be considered for appointment on par with NTT certificate holders.

## HOLDING SUMMARY

The Rajasthan High Court held that the classification between applicants holding professional qualifications under NCTE Regulations, 2001 (such as NTT) and those undergoing BSTC/B.Ed. training is valid and based on a reasonable nexus with the objective of ensuring standardized teaching qualifications. The Court found that permitting only those with recognized professional diplomas to participate in the selection process does not amount to arbitrary discrimination. It distinguished between persons who have completed a recognized professional course and those still in training, affirming that the State has the discretion to set eligibility criteria that align with regulatory standards. The petitioners' challenge was dismissed as the impugned action was found to be within the permissible limits of policy-making. This applies when: candidates undergoing teacher training challenge exclusion from selection on grounds of non-possession of NTT certificate despite pursuing equivalent courses.

## KEY FACTS OF THIS CASE

The petitioners were candidates undergoing BSTC/B.Ed. training or who had appeared in the BSTC examination with supplementary results, applying for teaching positions advertised by the State of Rajasthan. The advertisement dated 31.5.2008 allowed applicants with NTT or Pre-Primary Teachers Training certificates to participate in the selection process, subject to completing BSTC/B.Ed. or bridge course. However, the petitioners, though similarly situated in terms of pending qualifications, were excluded from the benefit of such relaxation. They challenged this exclusion as discriminatory. The controversy arose in the context of teacher recruitment, where the State required formal certification for immediate eligibility. A prior batch of similar petitions including S.B. Civil Writ Petition No. 8232/2008 (Purshottam Mehta & Ors.) had already been dismissed by the Court on 11.9.2008.

## WHAT THE COURT DECIDED

The High Court dismissed the writ petitions, upholding the State's decision to restrict eligibility to applicants holding NTT or Pre-Primary Teachers Training certificates. It ruled that the distinction between certified and uncertified trainees was based on a reasonable classification having a direct nexus with the goal of maintaining educational standards. The Court declined to interfere with the administrative policy, affirming that the exclusion of candidates still undergoing BSTC/B.Ed. training did not violate constitutional guarantees under Articles 14 and 16.

## KEY QUOTE

The applicants holding professional qualification under NCTE Regulations, 2001 constitutes a separate class and therefore the qualification made under the Rules of 2008 is having reasonable nexus with the object sought to be achieved.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `tenancy_claimed` is FALSE — not a tenancy or SARFAESI matter
2. `challenges_auction` is FALSE — no auction or enforcement action involved
3. [PENDING FIELD] `professional_qualification_held` is TRUE — applicant possesses NTT/Pre-Primary certificate
4. [PENDING FIELD] `training_in_progress` is TRUE — petitioner is undergoing BSTC/B.Ed. or has supplementary status
5. [PENDING FIELD] `claim_of_discrimination` is TRUE — petitioner alleges unequal treatment in selection process

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the dispute involves SARFAESI enforcement actions such as demand notice, possession, or auction — in that case, judgments like Kanaiyalal or Celir LLP apply.
2. When the challenge is against NPA classification or MSME restructuring — then M8 or M9 module cases apply.
3. When the petitioner holds no pending qualification but challenges general eligibility criteria — this judgment’s reasoning on professional classification may not extend.

## STATUTORY CONTEXT

Primary law: Rajasthan Subordinate Education Services Rules, 2008 (not SARFAESI)
Primary provision: Note-2 appended to advertisement dated 31.5.2008 — "Applicants holding professional qualification diploma/certificate in Nursery Teachers Training (NTT) or Pre-Primary Teachers Training are permitted to participate in process of selection with the condition that till they acquire the training of BSTC/B.Ed. or Bridge Course as the case may be, if selected will be appointed with a stipend of Rs.2750/- and will get appointment on attaining the training."
Instrument level: OTHER
Nature of provision: DIRECTORY — the rule provides administrative flexibility but does not create a vested right

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Purshottam Mehta & Ors. v. State of Rajasthan (S.B. Civil Writ Petition No. 8232/2008)
  This case follows the same reasoning — that NTT-certified applicants form a distinct class based on formal recognition under NCTE Regulations, 2001.
  SLRAI ROUTING: if `professional_qualification_held` = TRUE → this judgment applies; if FALSE → Purshottam Mehta applies.

Distinguishes: General cases under Article 14 involving public employment
  This judgment distinguishes itself by recognizing a regulatory basis (NCTE) for differential treatment, unlike general equality challenges.
  SLRAI ROUTING: if `regulatory_recognition_basis` = TRUE → Sheela Sharma applies; if FALSE → other Article 14 precedents apply.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: professional_qualification_held
Type: FactEntry[bool]
Description: True if the applicant holds NTT or Pre-Primary Teachers Training certificate
Module: M1
Extraction: From application documents or petitioner's claim in writ

Field name: training_in_progress
Type: FactEntry[bool]
Description: True if the applicant is currently undergoing BSTC/B.Ed. or has supplementary status
Module: M1
Extraction: From educational records or examination results

Field name: claim_of_discrimination
Type: FactEntry[bool]
Description: Whether petitioner alleges unequal treatment compared to NTT holders
Module: M1
Extraction: From writ petition grounds

**B. New YAML Rules Needed:**
Module: M1
Rule ID: M1_E1_teacher_qualification_classification
Conditions: professional_qualification_held=True AND training_in_progress=True AND claim_of_discrimination=True
Severity: LOW
Message: "Petitioner challenges exclusion from selection despite undergoing equivalent training. Judgment in Sheela Sharma upholds classification based on formal certification under NCTE."
Judgment tag: ["Sheela Sharma"]
Statutory basis: OTHER

**C. New Ground Codes Needed:**
Suggested code: PROFESSIONAL_QUALIFICATION_CLASSIFICATION
Description: Challenge to differential treatment based on possession of formal teaching certificate (NTT) vs. ongoing training
Module: M1

**D. Existing Judgments to Update:**
File: purshottam_mehta_2008.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add line: "Followed by: Sheela Sharma (2008) — affirmed that NTT-certified applicants constitute a separate class under NCTE Regulations."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: UNKNOWN
