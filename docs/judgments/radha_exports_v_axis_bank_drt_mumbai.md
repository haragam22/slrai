---
citation: "(2023) ibclaw.in 123 DRAT"
title: "State Bank Of India vs M/S Bharath Infra Exports And Imports ... on 28 November, 2022"
short_name: "State Bank of India v. Bharath Infra"
court: DRAT
high_court_state: null
bench_strength: 2
judgment_date: "2022-11-28"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["AMOUNT_DISPUTE"]
statutory_basis: IBC
act_sections: []
rules_sections: []
slrai_modules: ["M4"]
keywords: ["IBC Section 7", "financial debt", "default", "adjudicating authority discretion", "reconciliation of accounts"]
retrieval_condition: "Applies when the adjudicating authority refuses to admit a Section 7 IBC application by directing reconciliation of accounts instead of deciding on existence of default."
source: IBC_LAW_SUMMARY
ik_doc_id: "192594834"
ik_url: "https://indiankanoon.org/doc/192594834/"
has_verified_conditions: false
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower (M/s. Bharath Infra Exports and Imports Ltd.) alleged that there was no financial debt or default as it had fully cleared all cash credit and letter of credit (LC) facilities by 07.10.2016, including payment of Rs.10.63 crore and adjustment of fixed deposits. They contended that the bank unilaterally increased LC margins from 10% to 15% and illegally debited amounts, including penal interest, without justification. The borrower further claimed that the bank forged LC documents, as the purported LCs were not signed by its authorised signatory, and that a forensic audit report relied upon by the bank was biased. They argued that the existence of multiple disputes and pending proceedings before other forums warranted rejection of the Section 7 application under the IBC, and that the NCLT erred in directing a joint reconciliation of accounts instead of adjudicating the default.

## HOLDING SUMMARY

The National Company Law Appellate Tribunal (NCLAT) held that the Adjudicating Authority (NCLT) under the Insolvency and Bankruptcy Code, 2016, lacks the jurisdiction to direct a forensic audit or reconciliation of accounts at the pre-admission stage of a Section 7 application. The sole function of the NCLT is to ascertain the existence of a default based on records of the information utility or other evidence produced by the financial creditor, within 14 days. The Tribunal reaffirmed that the pendency of disputes or the borrower's solvency are not valid grounds to refuse admission of a Section 7 application when a default is evident from the creditor's records. The NCLT's direction for reconciliation was held to be beyond its statutory powers and contrary to the summary nature of IBC proceedings. This applies when: the adjudicating authority refuses to admit a Section 7 application by directing reconciliation of accounts instead of deciding on the existence of default.

## KEY FACTS OF THIS CASE

M/s. Bharath Infra Exports and Imports Ltd. had availed credit facilities from State Bank of India, including a cash credit limit and letter of credit (LC) facilities, with a total sanctioned limit of Rs.157.22 crores as of 2015. The account became irregular on 20.10.2016 due to the devolvement of LCs, and the loan was classified as NPA on 17.01.2017. The bank filed a Section 7 application before the NCLT, Bengaluru, seeking initiation of the Corporate Insolvency Resolution Process (CIRP) for a claimed default of Rs.146.93 crores. The NCLT, instead of admitting or rejecting the application, directed the bank to reconcile the accounts with the corporate debtor. The bank appealed this order to the NCLAT, arguing that the NCLT had exceeded its jurisdiction.

## WHAT THE COURT DECIDED

The NCLAT set aside the impugned order of the NCLT, Bengaluru, which had refused to admit the Section 7 application and instead directed a joint reconciliation of accounts. The NCLAT held that the NCLT had acted beyond its jurisdiction and failed to apply the law correctly. It directed the NCLT to restore the Section 7 application and admit it for the initiation of the Corporate Insolvency Resolution Process (CIRP) against the corporate debtor within 10 days of the judgment.

## KEY QUOTE

The Adjudicating Authority cannot travel beyond the letter of law and the dictum of the Hon'ble Apex Court. The satisfaction in regard to occurrence of default has to be drawn by the Adjudicating Authority either from the records of the information utility or other evidence provided by the 'Financial Creditor'.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `challenges_auction` is FALSE — the dispute is not related to SARFAESI auction but to IBC admission
2. `measure_type` is "IBC Section 7 Application" — the measure is an application under Section 7 of the IBC
3. `drt_interim_stay_granted` is FALSE — no stay from a DRT is in force
4. `prayer_scope_covers_current_measure` is TRUE — the borrower's prayer includes challenging the admission of the IBC application
5. `measure_date` is not null — the date of the Section 7 application is known
6. `sa_filing_date` is not null — the date of the appeal against the NCLT order is known
7. [PENDING FIELD] `nclt_directed_reconciliation` is TRUE — the NCLT has directed a reconciliation of accounts instead of deciding on the default

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the dispute involves a challenge to a SARFAESI auction or possession — in that case, SARFAESI-specific judgments like Kanaiyalal or Celir LLP apply.
2. When the financial creditor is an operational creditor filing under Section 9 of the IBC — Section 9 has a mandatory admission process, unlike the discretionary nature of Section 7 for financial creditors.
3. When the NCLT has admitted or rejected the application on merits, without directing reconciliation — this judgment only applies when the NCLT has erroneously directed a reconciliation.

## STATUTORY CONTEXT

Primary law: Insolvency and Bankruptcy Code, 2016
Primary provision: Section 7(4) — "The Adjudicating Authority shall, within fourteen days of the receipt of the application, ascertain the existence of a default from the records of an information utility or on the basis of other evidence which the financial creditor may produce."
Level: IBC
Nature: MANDATORY — the provision is directory in time (14 days) but mandatory in function; the Adjudicating Authority must decide on the existence of default based on available evidence, not conduct an audit.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Innoventive Industries v. ICICI Bank (2018) 1 SCC 407
  Reaffirmed that the Adjudicating Authority's role under Section 7 is limited to verifying the existence of a default from the creditor's evidence, not resolving disputes.

Follows: E.S. Krishnamurthy v. Bharath Hi-Tech Builders (2022) 3 SCC 161
  Confirmed that the Adjudicating Authority has only two choices under Section 7(5): admit or reject the application. Any other action, such as directing reconciliation, is outside its jurisdiction.

Distinguishes: Vidarbha Industries Power Ltd. v. Axis Bank Ltd. (2022)
  While Vidarbha acknowledged the NCLT's discretion under Section 7(5)(a), it did not permit the NCLT to abdicate its duty by directing a reconciliation. This judgment clarifies that discretion does not include refusing to decide.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: nclt_directed_reconciliation
Type: FactEntry[bool]
Description: True if the NCLT, in its order on a Section 7 application, directed the parties to reconcile accounts instead of admitting or rejecting the application
Module: M4
Extraction: From the text of the NCLT's impugned order in the appeal

**B. New YAML Rule Needed:**
Module: M4
Rule ID: M4_C1_nclt_reconciliation_directed
Conditions: measure_type="IBC Section 7 Application" AND nclt_directed_reconciliation=True
Severity: FATAL
Message: "The Adjudicating Authority (NCLT) has directed reconciliation of accounts, which is beyond its jurisdiction under Section 7 of the IBC. The application must be admitted or rejected based on evidence of default."
Judgment tag: ["State Bank of India v. Bharath Infra"]
Statutory basis: IBC

**C. No New Ground Codes Required:**
The borrower's argument about disputed debt and reconciliation is covered under the existing "AMOUNT_DISPUTE" ground code, as it challenges the quantum and validity of the claimed debt.

**D. Existing Judgments to Update:**
File: innoventive_industries_icici_bank.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add line: "Applied by: State Bank of India v. Bharath Infra (2022) — reaffirmed that NCLT cannot direct reconciliation and must decide on existence of default under Section 7."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: AMOUNT_DISPUTE
