---
citation: "(2023) SCC Online Ker 435"
title: "Sanil Kumar.V vs The Authorised Officer, Indian Overseas Bank"
short_name: "Sanil Kumar.V"
court: HIGH_COURT
high_court_state: "Kerala"
bench_strength: 2
judgment_date: "2023-09-01"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["UNKNOWN"]
statutory_basis: ACT
act_sections: ["Section 13(2)", "Section 17(1)"]
rules_sections: ["Rule 8(6)"]
slrai_modules: ["M1", "M2"]
keywords: ["Section 17(1)", "Article 226", "writ of certiorari", "writ of mandamus", "extraordinary circumstances", "Naveen Mathew Philip", "statutory remedy", "alternative forum", "circumvent tribunal"]
retrieval_condition: "Applies when a borrower files a writ petition under Article 226 seeking to quash a SARFAESI sale notice or obtain time to repay, despite the availability of a statutory remedy under Section 17."
source: IK_SUMMARY
ik_doc_id: "49739423"
ik_url: "https://indiankanoon.org/doc/49739423/"
has_verified_conditions: false
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower alleged that the High Court should exercise its writ jurisdiction under Article 226 to quash the Ext.P2 sale notice dated 22.06.2023 issued under the proviso to Rule 8(6) of the SARFAESI Rules. He contended that he was ready to settle the entire loan amount within three months and sought a writ of mandamus directing the bank to grant him time to repay by selling a portion of the mortgaged property. He further claimed that the Single Judge failed to consider his financial hardship and the payment of Rs.1,50,000/- made on 27.07.2023. The prayer was to quash the sale notice, stay further proceedings, and permit partial sale of the property to close the account.

## HOLDING SUMMARY

The High Court reiterated that writ jurisdiction under Article 226 should not be invoked by borrowers to circumvent the statutory remedy under Section 17 of the SARFAESI Act, absent extraordinary circumstances. The Supreme Court in *Naveen Mathew Philip* (2023) has clearly held that High Courts must refrain from entertaining writ petitions challenging SARFAESI proceedings when an efficacious alternative remedy before the DRT exists. A writ of certiorari cannot be issued merely because a borrower wishes to delay enforcement; there must be a clear error of law apparent on the record. A writ of mandamus cannot be granted to compel a bank to accept repayment in installments contrary to its rights under the Act. The borrower’s failure to comply with a prior court-approved repayment plan negates any claim of hardship. This applies when: a borrower files a writ petition under Article 226 seeking to quash a SARFAESI sale notice or obtain time to repay, despite the availability of a statutory remedy under Section 17.

## KEY FACTS OF THIS CASE

The borrower, Sanil Kumar.V, along with his wife, had availed a loan of Rs.1.145 crore from Indian Overseas Bank, secured by a residential property. The account fell into default, and a Section 13(2) demand notice was issued. In an earlier writ petition (W.P.(C) No.8920 of 2023), the High Court permitted repayment of overdue dues of Rs.7.6 lakh in 12 installments, which the borrower failed to utilize. Subsequently, the bank issued a sale notice under Rule 8(6) proviso. The borrower then filed W.P.(C) No.23832 of 2023 seeking to quash the sale notice and obtain time to repay. The Single Judge dismissed the petition relying on *Naveen Mathew Philip*, and this appeal challenges that dismissal.

## WHAT THE COURT DECIDED

The Division Bench dismissed the writ appeal, affirming the Single Judge’s refusal to interfere with the SARFAESI enforcement. The Court held that the borrower had not made out a case for issuing a writ of certiorari or mandamus, especially after failing to comply with a prior court-approved repayment plan. The availability of an efficacious alternative remedy under Section 17 barred the invocation of Article 226. The appeal was dismissed as an abuse of the judicial process.

## KEY QUOTE

A litigant cannot avoid the non-compliance of approaching the Tribunal, which requires the prescription of fees, and use the constitutional remedy as an alternative.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `challenges_auction` is TRUE — borrower challenges a sale notice under Rule 8(6)
2. `prayer_scope_covers_current_measure` is TRUE — borrower seeks to quash the current enforcement step
3. `previous_sa_filed` is TRUE — borrower had previously approached the DRT or court for relief
4. [PENDING FIELD] `borrower_invokes_article_226` is TRUE — borrower files a writ petition under Article 226 instead of pursuing Section 17 remedy
5. [PENDING FIELD] `extraordinary_circumstances_absent` is TRUE — no fraud, mala fide, or jurisdictional error shown

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the borrower has no alternative statutory remedy — e.g., DRT lacks jurisdiction due to IBC moratorium or procedural bar — in such cases, *Mardia Chemicals* allows Article 226 to be invoked.
   SLRAI ROUTING: if `drt_alternative_remedy_available` = FALSE → Mardia Chemicals applies.

2. When there is a clear procedural violation in the SARFAESI process (e.g., defective notice, non-receipt) — such cases are to be raised before the DRT under Section 17, not in writ.
   SLRAI ROUTING: if `service_defect` = TRUE → Kanaiyalal applies.

3. When the bank has acted mala fide or there is a jurisdictional error — such extraordinary circumstances allow High Court intervention.
   SLRAI ROUTING: if `bank_action_mala_fide` = TRUE → Mardia Chemicals applies.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002  
Primary provision: Section 17(1) — "Any person (including a borrower), aggrieved by any measure taken by the Authorised Officer under this Act, may make an application to the Debts Recovery Tribunal..."  
Instrument level: ACT  
Nature of provision: MANDATORY — the DRT is the exclusive forum for aggrieved persons, absent extraordinary circumstances.

Secondary: Article 226, Constitution of India — power of High Courts to issue writs.  
Court held: While wide, this power must not be used to circumvent statutory remedies.  
Nature: DIRECTORY — exercise only in extraordinary circumstances.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: *Naveen Mathew Philip* [(2023) SCC Online (SC) 435]  
  Reaffirmed that High Courts should not entertain writ petitions under Article 226 in SARFAESI matters when Section 17 provides an efficacious alternative remedy.  
  SLRAI ROUTING: if `statutory_remedy_available` = TRUE → Naveen Mathew Philip applies.

Follows: *Mardia Chemicals Ltd. v. Union of India* [(2004) 4 SCC 311]  
  Recognized that Article 226 can be invoked only in exceptional cases where the tribunal cannot provide relief.  
  SLRAI ROUTING: if `extraordinary_circumstances_present` = TRUE → Mardia Chemicals applies.

Distinguishes: *Kanaiyalal Lalchand Sachdev v. State of Maharashtra*  
  Kanaiyalal dealt with a procedural defect (non-reply to Section 13(3A) objection) that could be raised before DRT.  
  This case involves a direct writ challenge to enforcement without alleging such defects.  
  SLRAI ROUTING: if `objection_filed` = TRUE AND `bank_reply_given` = FALSE → Kanaiyalal applies; else → this judgment applies.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: borrower_invokes_article_226
Type: FactEntry[bool]
Description: True if borrower files a writ petition under Article 226 challenging SARFAESI action
Module: M1

Field name: extraordinary_circumstances_absent
Type: FactEntry[bool]
Description: True if no mala fide, fraud, jurisdictional error, or procedural illegality is alleged
Module: M1

Field name: drt_alternative_remedy_available
Type: FactEntry[bool]
Description: True if borrower has not approached DRT and no bar (like IBC) exists
Module: M1

**B. New YAML Rule Needed:**
Module: M1
Rule ID: M1_C8_writ_abuse
Conditions: borrower_invokes_article_226=True AND drt_alternative_remedy_available=True AND extraordinary_circumstances_absent=True
Severity: FATAL
Message: "Borrower invoking Article 226 despite availability of Section 17 remedy. Writ petition liable to be dismissed as abuse of process."
Judgment tag: ["Sanil_Kumar_V", "Naveen_Mathew_Philip"]
Statutory basis: ACT

**C. New Ground Code Needed:**
Suggested code: CIRCUMVENT_TRIBUNAL
Description: Borrower attempts to bypass DRT by filing writ under Article 226 without alleging extraordinary circumstances
Module: M1

**D. Existing Judgments to Update:**
File: naveen_mathew_philip.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Applied by: Sanil Kumar.V (2023) SCC Online Ker 435 — affirmed that writ petitions under Article 226 should not be entertained when Section 17 remedy is available."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: UNKNOWN
