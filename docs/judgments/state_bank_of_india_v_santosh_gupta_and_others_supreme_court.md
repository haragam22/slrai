---
citation: "2017 (2) SCC 538"
title: "State Bank Of India vs Santosh Gupta And Anr. Etc on 16 December, 2016"
short_name: "Santosh Gupta"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2016-12-16"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["SERVICE_DEFECT", "NOTICE_ALL_PARTIES", "AO_AUTHORIZATION"]
statutory_basis: ACT
act_sections: ["Section 13(2)", "Section 13(4)", "Section 17"]
rules_sections: []
slrai_modules: ["M1", "M7"]
keywords: ["Section 13(2)", "demand notice", "authorised officer", "joint borrowers", "joint liability", "joint liability of guarantors", "joint liability of co-borrowers", "Section 17 appeal", "SARFAESI in Jammu and Kashmir"]
retrieval_condition: "Applies when the SARFAESI Act is challenged as inapplicable to the State of Jammu & Kashmir due to conflict with local property laws."
source: SC_FULL_TEXT
ik_doc_id: "105489743"
ik_url: "https://indiankanoon.org/doc/105489743/"
has_verified_conditions: false
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers alleged that the SARFAESI Act, 2002 is outside the legislative competence of Parliament with respect to the State of Jammu & Kashmir, as it conflicts with Section 140 of the Jammu & Kashmir Transfer of Property Act, 1920, which restricts transfer of immovable property to non-permanent residents. They contended that SARFAESI cannot override these local protections and therefore cannot be enforced in Jammu & Kashmir. The prayer before the High Court was to declare the SARFAESI Act inapplicable to the State of Jammu & Kashmir and to set aside enforcement actions taken under it.

## HOLDING SUMMARY

The SARFAESI Act, 2002 is validly enacted by Parliament under Entries 45 and 95 of List I of the Seventh Schedule to the Constitution of India, which confer exclusive legislative competence over banking and jurisdiction of courts in banking matters. The Act applies to the State of Jammu & Kashmir despite any conflict with local property laws, as Article 246 read with Article 370 ensures that Parliamentary laws on these subjects prevail. Section 140 of the Jammu & Kashmir Transfer of Property Act must give way to SARFAESI, and Rule 8(5) proviso of the SARFAESI Rules explicitly preserves such local restrictions. The Act is thus fully applicable to Jammu & Kashmir, and banks may proceed with enforcement under Section 13. This applies when: the applicability of SARFAESI is challenged in Jammu & Kashmir on grounds of conflict with local property transfer restrictions.

## KEY FACTS OF THIS CASE

The case arose when borrowers in Jammu & Kashmir challenged the applicability of the SARFAESI Act, 2002, arguing that it violated local laws protecting permanent residents' property rights. The High Court of Jammu & Kashmir had declared key provisions of SARFAESI — including Sections 13, 17A, and 18B — as outside Parliament’s legislative competence. The State Bank of India and other banks appealed to the Supreme Court, seeking a declaration that SARFAESI is fully applicable to Jammu & Kashmir. The dispute centered on whether Entry 45 (Banking) and Entry 95 (Jurisdiction of Courts) of List I empower Parliament to override state-specific property transfer laws.

## WHAT THE COURT DECIDED

The Supreme Court set aside the High Court’s judgment and declared that the SARFAESI Act, 2002 is fully applicable to the State of Jammu & Kashmir. It held that Parliament has exclusive legislative competence under Entries 45 and 95 of List I, and that SARFAESI prevails over conflicting state laws. The Court affirmed that enforcement actions under Section 13 are valid and may proceed. It also clarified that Rule 8(5) proviso ensures respect for local transfer restrictions, thereby harmonizing SARFAESI with state law.

## KEY QUOTE

The entire Act, including Sections 17A and 18B, would in pith and substance be referable to Entries 45 and 95 of List I, and that therefore the Act as a whole would necessarily operate in the State of Jammu & Kashmir.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when: the applicability of SARFAESI is challenged in Jammu & Kashmir on grounds of conflict with local property transfer restrictions.

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the challenge to SARFAESI is based on procedural defects like defective service or non-receipt of notice — in that scenario, *Kanaiyalal* applies.
   SLRAI ROUTING: if `notice_service_mode` is defective → *Kanaiyalal* applies.

2. When the property in question is located outside Jammu & Kashmir — this judgment is territory-specific and does not apply.

3. When the borrower challenges SARFAESI on grounds of NPA misclassification or restructuring rights — in that case, *MSME Restructuring* or *NPA_PREMATURE* judgments apply.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002  
Primary provision: Section 13(2) — "The secured creditor may, without the intervention of court or tribunal, issue a notice in writing to the borrower requiring him to discharge his liability within sixty days."  
Instrument level: ACT  
Nature of provision: MANDATORY — court held that enforcement under Section 13 is valid and enforceable across India, including J&K.

Secondary: Section 17 — Right to appeal before DRT within 45 days.  
Level: ACT  
Nature: MANDATORY — the right to challenge enforcement is preserved but does not negate Parliament’s legislative competence.

## RELATIONSHIP TO OTHER JUDGMENTS

Affirmed: Central Bank of India v. State of Kerala (2009) 4 SCC 94  
  Held that SARFAESI is validly enacted under Entry 45 List I and prevails over state laws. This case reaffirms that principle in the context of Jammu & Kashmir.

Distinguishes: State of Jammu & Kashmir v. M.S. Farooqui (1972) 1 SCC 872  
  Farooqui dealt with disciplinary proceedings under state law vs. All India Services Rules. Here, SARFAESI is a central law on banking, which prevails under Entry 45 List I.  
  SLRAI ROUTING: if `loan_account_type` = "banking" → *Santosh Gupta* applies; if `loan_account_type` = "civil service" → *Farooqui* applies.

Follows: Union of India v. Delhi High Court Bar Association (2002) 4 SCC 275  
  Established that recovery of bank debts falls under Entry 45 List I. This judgment applies that principle to SARFAESI enforcement in J&K.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: state_property_law_conflict
Type: FactEntry[bool]
Description: True if local law (e.g., J&K TPA Section 140) restricts transfer of property to non-residents
Module: M1
Extraction: Identify from borrower's SA or state-specific legal provisions cited

Field name: sarfaesi_applied_by_bank
Type: FactEntry[bool]
Description: True if bank initiated SARFAESI proceedings in J&K
Module: M1
Extraction: Confirm from demand notice or possession notice

**B. New YAML Rule Needed:**
Module: M1
Rule ID: M1_JK_1_sarfaesi_applicability
Conditions: high_court_state="Jammu and Kashmir" AND state_property_law_conflict=True
Severity: INFO
Message: "SARFAESI applies in J&K despite local property law restrictions. See Santosh Gupta."
Judgment tags: ["Santosh Gupta"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: central_bank_india_kerala.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Affirmed by: Santosh Gupta (2017) 2 SCC 538 — reaffirmed that SARFAESI, enacted under Entry 45 List I, prevails over state laws including in Jammu & Kashmir."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: SERVICE_DEFECT
