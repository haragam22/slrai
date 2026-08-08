---
citation: "2022 INSC 303"
title: "NKGSB Cooperative Bank Limited vs Subir Chakravarty & Ors."
short_name: "Subir Chakravarty"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2022-02-25"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["POSSESSION_DEFECT"]
statutory_basis: ACT
act_sections: ["Section 14(1A)"]
rules_sections: []
slrai_modules: ["M3"]
keywords: ["Section 14(1A)", "officer subordinate", "Advocate Commissioner", "CMM", "DM", "functional subordination", "officer of the court", "ministerial act", "statutory subordination", "administrative subordination"]
retrieval_condition: "Applies when the District Magistrate or Chief Metropolitan Magistrate appoints an advocate as commissioner to take possession under Section 14(1A) of the SARFAESI Act."
source: SC_FULL_TEXT
ik_doc_id: "129557920"
ik_url: "https://indiankanoon.org/doc/129557920/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers alleged that the District Magistrate (DM) or Chief Metropolitan Magistrate (CMM) lacked the power under Section 14(1A) of the SARFAESI Act to appoint an advocate as commissioner to take possession of secured assets. They contended that the phrase "any officer subordinate to him" must be interpreted strictly to mean only those officers who are administratively or statutorily subordinate to the DM/CMM, and not advocates. They further argued that advocates, being officers of the court but not part of the executive hierarchy, cannot be delegated such statutory authority. The prayer before the DRT/High Court was to set aside the order appointing the advocate commissioner and declare the possession invalid.

## HOLDING SUMMARY

Section 14(1A) of the SARFAESI Act, which permits the District Magistrate or Chief Metropolitan Magistrate to authorize "any officer subordinate to him" to take possession of secured assets, must be interpreted to include advocates appointed as commissioners, as they are officers of the court and functionally subordinate to the Magistrate. The Supreme Court held that the legislative intent behind the 2013 amendment was to facilitate efficient enforcement of security interests, and a narrow interpretation excluding advocates would defeat this purpose. The Court rejected the Bombay High Court's strict statutory interpretation and affirmed the views of the Madras, Kerala, and Delhi High Courts, recognizing the functional subordination of advocates to the court. This applies when: the DM or CMM appoints an advocate commissioner to take possession under Section 14(1A), and the borrower challenges the validity of such appointment.

## KEY FACTS OF THIS CASE

The NKGSB Cooperative Bank had advanced a loan of Rs. 4.44 crore to borrowers secured by a flat in Mumbai. The account was declared NPA after default in 2017, and a Section 13(2) notice was served. The bank later applied under Section 14 of the SARFAESI Act for the CMM to take possession. The CMM appointed an advocate as commissioner to take possession of the property. The borrowers challenged this appointment in the Bombay High Court, arguing that an advocate is not an "officer subordinate" under Section 14(1A). The Bombay High Court agreed and set aside the order. This led to a conflict with other High Courts (Madras, Kerala, Delhi) which had upheld such appointments. The matter was appealed to the Supreme Court to resolve the conflict.

## WHAT THE COURT DECIDED

The Supreme Court allowed the appeals filed by the secured creditors, set aside the Bombay High Court judgment, and upheld the power of the DM/CMM to appoint an advocate commissioner under Section 14(1A) of the SARFAESI Act. The Court declared the Bombay High Court's view as "not a good law" and affirmed that advocates, being officers of the court, are functionally subordinate and can be validly appointed to take possession. The special leave petition challenging the Madras High Court's decision was delinked and listed separately for admission on a different issue.

## KEY QUOTE

An advocate is an officer of the court and, thus, subordinate to the CMM/DM for the purposes of Section 14(1A) of the 2002 Act.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `possession_taken_date` is not null — possession of secured asset was taken
2. `possession_mode` is "CMM/DM appointed commissioner" — possession was taken through a commissioner
3. `challenges_sale_notice` is TRUE — borrower challenges the possession process
4. `sa_applicant_type` is "borrower" — the applicant in the SA is the borrower
5. `prayer_scope_covers_current_measure` is TRUE — the prayer includes setting aside possession

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the appointment is made by an authority other than the DM or CMM — in that case, the statutory basis of Section 14 does not apply.
2. When the challenge is not to the appointment of an advocate but to the procedural compliance of the Section 13(2) notice — in that case, Kanaiyalal v. State of Maharashtra applies.
3. When the possession was taken directly by the bank's authorized officer under Section 13(4), without invoking Section 14 — in that case, the issue of DM/CMM appointment does not arise.

## STATUTORY CONTEXT

Primary law: Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002  
Primary provision: Section 14(1A) — "The District Magistrate or the Chief Metropolitan Magistrate may authorise any officer subordinate to him,— (i) to take possession of such assets and documents relating thereto; and (ii) to forward such assets and documents to the secured creditor."  
Instrument level: ACT  
Nature of provision: MANDATORY — the word "may" is directory, not mandatory, but the power conferred is substantive and must be interpreted purposively.

## RELATIONSHIP TO OTHER JUDGMENTS

Distinguishes: NKGSB Cooperative Bank Ltd. v. Subir Chakravarty (Bombay High Court)  
  The Bombay High Court held that an advocate is not an "officer subordinate" under Section 14(1A).  
  SLRAI ROUTING: if `court` = "HIGH_COURT" AND `high_court_state` = "Maharashtra" → Bombay HC view applies (narrow interpretation); if `court` = "SUPREME_COURT" → this judgment applies (broad functional subordination).

Follows: Muhammed Ashraf v. Union of India (Kerala HC)  
  Affirmed the Kerala High Court's view that advocates can be appointed as commissioners under Section 14(1A).

Follows: S. Chandramohan v. CMM, Egmore (Madras HC)  
  Upheld the Madras High Court's reasoning that advocates, as officers of the court, are competent to be appointed commissioners.

Follows: Rahul Chaudhary v. Andhra Bank (Delhi HC)  
  Endorsed the Delhi High Court's conclusion that Section 14(1A) does not bar appointment of advocates as receivers.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: possession_mode
Type: FactEntry[str]
Description: How possession was taken — e.g., "bank AO", "CMM/DM", "CMM/DM appointed commissioner"
Module: M3
Extraction: From DRT order or SA petition describing the mode of possession

**B. New YAML Rule Needed:**
Module: M3
Rule ID: M3_C1_section14_1A_validity
Conditions: possession_mode="CMM/DM appointed commissioner" AND court="SUPREME_COURT"
Severity: INFO
Message: "Appointment of advocate commissioner under Section 14(1A) is valid per Subir Chakravarty (2022 INSC 303)."
Judgment tag: [this judgment's short_name]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: nkgsb_cooperative_bank_v_subir_chakravarty_bombay_hc.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Subir Chakravarty (2022 INSC 303) — held that appointment of advocate commissioner under Section 14(1A) is valid as advocates are officers of the court and functionally subordinate."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: POSSESSION_DEFECT
