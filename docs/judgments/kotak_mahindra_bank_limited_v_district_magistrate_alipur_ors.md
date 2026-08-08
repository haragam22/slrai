---
citation: "(2021) ibclaw.in 1339 DRT"
title: "Sh. Dara Singh vs M/S Kotak Mahindra Bank Ltd. (KMBL)"
short_name: "Dara Singh"
court: DRT
high_court_state: null
bench_strength: 1
judgment_date: "2021-02-25"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["UNKNOWN"]
statutory_basis: OTHER
act_sections: []
rules_sections: []
slrai_modules: ["M10"]
keywords: ["arbitration award", "Section 34 Arbitration Act", "unilateral appointment", "limitation of arbitration", "jurisdiction of arbitrator"]
retrieval_condition: "Applies when a borrower challenges an arbitration award under Section 34 of the Arbitration and Conciliation Act 1996 on grounds of unilateral appointment, limitation, or jurisdiction."
source: DRAT_FULL_TEXT
ik_doc_id: "154990820"
ik_url: "https://indiankanoon.org/doc/154990820/"
has_verified_conditions: false
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower alleged that the arbitral award dated 01.03.2018 was void ab initio as it resulted from a unilateral appointment of the arbitrator without his consent, rendering the proceedings biased and illegal. He contended that the claim was barred by limitation since the loan agreement dated 24.08.2009 and the last EMI fell due on 05.09.2013, making the 2016 arbitration proceedings time-barred. He further claimed that the loan documents, including the agreement and application, were forged, with signatures obtained on blank papers, and that he had already repaid 36 EMIs up to September 2012. Additionally, he argued that the arbitrator lacked jurisdiction because the arbitration clause specified Delhi as the venue, while the exclusive jurisdiction clause referred to Gurgaon courts, creating inconsistency. He also alleged that the arbitrator acted in collusion with the bank and failed to consider his application for a handwriting expert.

## HOLDING SUMMARY

An arbitral award passed under the Arbitration and Conciliation Act, 1996 cannot be set aside merely on allegations of bias, unilateral appointment, or procedural irregularities unless there is a clear violation of natural justice or public policy. The court emphasized that under Section 34, interference is limited to cases involving patent illegality, perversity, or a complete lack of judicial approach. The limitation period for initiating arbitration begins from the date of the last communication between the parties if settlement efforts were ongoing, not from the date of default. The venue of arbitration, as contractually agreed, governs the jurisdiction for enforcement and challenge of the award, and a concurrent clause assigning exclusive jurisdiction to a court does not invalidate the arbitration venue. The award, being reasoned and supported by evidence, does not warrant interference even if the arbitrator extended the timeline with mutual consent. This applies when: a borrower challenges an arbitration award on grounds of unilateral appointment, limitation, or jurisdiction, but the award is reasoned and based on contractual terms.

## KEY FACTS OF THIS CASE

Dara Singh availed a personal loan of ₹2,85,000 from Citi Financial Consumer Finance India Ltd. (CFCFIL) in August 2009, repayable in 48 EMIs of ₹10,268 each, with the last installment due on 05.09.2013. The loan was later assigned to Kotak Mahindra Bank Ltd. (KMBL). After Singh defaulted, KMBL issued a legal notice on 26.08.2016 recalling the loan and initiating arbitration under Clause 29 of the loan agreement. Sh. B.L. Garg was appointed as Sole Arbitrator on 10.09.2016. The borrower contested the claim, alleging forgery, prior repayment, and lack of consent to arbitration. The arbitrator passed an award on 01.03.2018 in favor of KMBL for ₹2,11,816.75 with interest. Singh filed a Section 34 petition before the DRT to set aside the award, raising multiple grounds including limitation, jurisdiction, and procedural defects. The DRT dismissed the petition, upholding the award.

## WHAT THE COURT DECIDED

The DRT dismissed the Section 34 petition, holding that the arbitral award was valid, reasoned, and not liable to be set aside on any ground under Section 34 of the Arbitration and Conciliation Act, 1996. The court found no merit in the allegations of bias, unilateral appointment, or lack of jurisdiction, noting that the arbitration clause clearly designated Delhi as the venue. It ruled that the limitation period commenced from the last communication between the parties, not from the date of default, and that the arbitrator had validly extended the timeline with mutual consent. The court also rejected the forgery claim due to lack of supporting evidence and failure to prove the documents were not signed by the borrower.

## KEY QUOTE

The said award is based on the finding of the facts recorded by ld. Arbitrator which did not warrant any interference by this court while exercising the power under Section 34 of the Act.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when: a borrower challenges an arbitration award on grounds of unilateral appointment, limitation, or jurisdiction, but the award is reasoned and based on contractual terms.

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the enforcement action is under SARFAESI Act and not based on an arbitral award — in that case, judgments like *Kanaiyalal* or *Celir LLP* apply.
   SLRAI ROUTING: if `measure_type` = "SARFAESI" → Kanaiyalal applies; if `measure_type` = "Arbitration Award" → this judgment applies.

2. When the borrower has not filed a Section 34 petition but is challenging a SARFAESI demand notice or possession — this judgment is irrelevant to SARFAESI compliance.

3. When the arbitration award is challenged on grounds of fraud in the agreement itself, and not merely procedural defects — a different level of scrutiny may apply under public policy.

## STATUTORY CONTEXT

Primary law: Arbitration and Conciliation Act, 1996  
Primary provision: Section 34 — "An arbitral award may be set aside by the Court only if the party making the application furnishes proof that the party was under some incapacity, or the arbitration agreement is not valid, or the party was not given proper notice, or the award deals with a dispute not contemplated, or the composition of the arbitral tribunal was not in accordance with the agreement, or the award is in conflict with the public policy of India."  
Instrument level: OTHER  
Nature of provision: MANDATORY — the grounds for setting aside an award are exhaustive and narrowly interpreted.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: ONGC v. Saw Pipes Ltd. (2003) 5 SCC 705  
  Established that an award can be set aside only if it is patently illegal or shocks the conscience of the court. This judgment applies the same principle to reject a challenge based on procedural allegations.

Follows: M.P. Power Generation Co. Ltd. v. Ansaldi Energia SPA (2018) 4 SCC 71  
  Reaffirmed that courts must not re-appreciate evidence or substitute their view for that of the arbitrator. This judgment follows that principle in upholding the award.

Distinguishes: Bhandari Udyog Ltd. v. Industrial Facilitation Council (2015) 1320 SCC  
  Bhandari Udyog dealt with territorial jurisdiction of courts in relation to arbitral seats. This judgment distinguishes it by holding that the arbitration clause specifying Delhi as venue governs, and the Gurgaon jurisdiction clause does not conflict.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: arbitration_clause_exists
Type: FactEntry[bool]
Description: True if the loan agreement contains an arbitration clause
Module: M10
Extraction: Check loan agreement for Clause 29 or similar arbitration clause

Field name: arbitrator_appointed_unilaterally
Type: FactEntry[bool]
Description: True if the borrower claims the arbitrator was appointed without mutual consent
Module: M10

Field name: award_challenged_under_section_34
Type: FactEntry[bool]
Description: True if the petition is filed under Section 34 of the Arbitration Act
Module: M10

**B. New YAML Rule Needed:**
Module: M10
Rule ID: M10_C8_arbitration_award_challenge
Conditions: arbitration_clause_exists=True AND award_challenged_under_section_34=True
Severity: MEDIUM
Message: "Borrower challenging arbitral award under Section 34. Ensure challenge is based on public policy, natural justice, or patent illegality — not mere procedural dissatisfaction."
Judgment tag: ["Dara_Singh"]
Statutory basis: OTHER

**C. New Ground Codes Needed:**
Suggested code: ARBITRATION_AWARD_CHALLENGE
Description: Borrower challenging enforcement based on an arbitral award under Section 34
Module: M10

**D. Existing Judgments to Update:**
None

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: UNKNOWN
