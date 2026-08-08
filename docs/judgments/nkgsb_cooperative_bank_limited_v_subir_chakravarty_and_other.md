---
citation: "2022 SCC OnLine SC 234"
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
act_sections: ["Section 14(1A)", "Section 14(1)", "Section 14(2)", "Section 14(3)"]
rules_sections: []
slrai_modules: ["M3"]
keywords: ["Section 14(1A)", "officer subordinate", "Advocate Commissioner", "CMM", "DM", "functional subordination", "administrative subordination", "statutory subordination", "possession notice", "Rule 8(3)"]
retrieval_condition: "Applies when the CMM or DM appoints an advocate as commissioner to take possession under Section 14(1A) of the SARFAESI Act."
source: SC_FULL_TEXT
ik_doc_id: "129557920"
ik_url: "https://indiankanoon.org/doc/129557920/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers alleged that the Chief Metropolitan Magistrate (CMM) or District Magistrate (DM) cannot appoint an advocate as a commissioner to take possession of secured assets under Section 14(1A) of the SARFAESI Act, as an advocate is not an "officer subordinate" to the CMM/DM in the administrative or service sense. They contended that the statutory language "any officer subordinate to him" must be interpreted strictly to mean only those officers who are part of the official administrative hierarchy. They further argued that allowing advocates to act as commissioners would undermine the accountability and procedural safeguards intended by the Act. The prayer before the DRT/HC was to set aside the order appointing the advocate commissioner and quash the possession proceedings.

## HOLDING SUMMARY

Section 14(1A) of the SARFAESI Act permits the Chief Metropolitan Magistrate or District Magistrate to authorize any officer subordinate to take possession of secured assets and forward them to the secured creditor. The term "officer subordinate" is interpreted functionally, not merely administratively or statutorily, and includes advocates appointed as commissioners because they are officers of the court and functionally subordinate to the Magistrate. The appointment of an advocate commissioner to execute possession orders is valid and consistent with the legislative intent of ensuring timely enforcement of security interests. This interpretation upholds the efficacy of SARFAESI proceedings and prevents logistical bottlenecks. This applies when: the CMM or DM appoints an advocate commissioner to take possession under Section 14(1A).

## KEY FACTS OF THIS CASE

NKGSB Cooperative Bank Limited had sanctioned a loan of Rs. 4.44 crore to borrowers secured by a flat in Mumbai. The account was declared NPA after default on 30.10.2017. A Section 13(2) demand notice was issued and later published due to non-receipt. The bank applied to the ACMM under Section 14 for possession, which was granted on 26.7.2019, appointing an advocate to take possession. The borrowers challenged this before the Bombay High Court, arguing that an advocate cannot be an "officer subordinate" under Section 14(1A). The High Court agreed and quashed the order. The bank appealed to the Supreme Court. Parallel proceedings in Madras and Delhi High Courts had upheld such appointments, creating a conflict.

## WHAT THE COURT DECIDED

The Supreme Court allowed the appeals filed by the secured creditors, set aside the Bombay High Court judgment, and upheld the validity of appointing an advocate commissioner under Section 14(1A) of the SARFAESI Act. It declared that advocates, being officers of the court, are functionally subordinate to the CMM/DM and thus eligible for appointment. The Court distinguished between statutory, administrative, and functional subordination, adopting the latter as the correct test. The special leave petition against the Madras High Court was delinked for separate hearing on a different issue.

## KEY QUOTE

An advocate is an officer of the court and, thus, subordinate to the concerned CMM/DM within their jurisdiction.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `possession_taken_date` is not null — possession was taken under Section 14
2. `possession_mode` is "CMM/DM-appointed officer" — possession executed by an officer authorized by the Magistrate
3. `possession_mode` includes "Advocate Commissioner" — the officer appointed is an advocate
4. `section_14_application_filed` is TRUE — application made under Section 14(1)
5. `section_14_1a_invoked` is TRUE — Section 14(1A) was relied upon for authorization

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When possession is taken directly by the secured creditor's "authorised officer" under Section 13(4) without invoking Section 14 — in that case, Rule 8(1) of the SARFAESI Rules applies, and the issue of CMM/DM appointment does not arise.
   SLRAI ROUTING: if `possession_mode` = "Authorised Officer under Section 13(4)" → Rule 8(1) applies; if `possession_mode` = "CMM/DM-appointed officer" → this judgment applies.

2. When the appointed person is a peon, clerk, or other non-officer of the court — this judgment does not extend to unqualified personnel.
   SLRAI ROUTING: if `appointed_officer_type` = "non-officer" → distinction applies; if `appointed_officer_type` = "Advocate" → this judgment applies.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002
Primary provision: Section 14(1A) — "The District Magistrate or the Chief Metropolitan Magistrate may authorise any officer subordinate to him,— (i) to take possession of such assets and documents relating thereto; and (ii) to forward such assets and documents to the secured creditor."
Instrument level: ACT
Nature of provision: PERMISSIVE — use of "may" makes it discretionary, not mandatory

Secondary provision: Section 14(1) — obligates CMM/DM to act on application; Section 14(2) — enables use of force; Section 14(3) — grants immunity to authorized officers.
Level: ACT
Nature: MANDATORY (for 14(1)), DIRECTORY (for 14(1A))

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: M/s. J. Marks Exim (India) Pvt. Ltd. vs. Punjab National Bank (2017 SCC OnLine Bom 2246)
  Affirmed that CMM can appoint officers for possession, though not specifically advocate commissioners.

Distinguishes: Muhammed Ashraf & Anr. vs. Union of India & Ors. (AIR 2009 Kerala 14)
  That case allowed advocate commissioners but predated Section 14(1A); this judgment confirms such practice remains valid post-amendment.
  SLRAI ROUTING: if `section_14_1a_invoked` = TRUE → this judgment applies; if pre-2013 case → Muhammed Ashraf applies.

Distinguishes: NKGSB Cooperative Bank Ltd. v. Subir Chakravarty (Bombay HC)
  The Bombay High Court took a strict statutory view, which this SC judgment overrules.
  SLRAI ROUTING: if `court` = "SUPREME_COURT" → this judgment applies; if `court` = "HIGH_COURT" and state = "Maharashtra" → prior Bombay HC view was applied but is now overruled.

Affirmed: The Federal Bank Ltd., Ernakulam vs. A.V. Punnus (AIR 2014 Kerala 7)
  Upheld the principle that advocates can be appointed as commissioners under functional subordination.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: section_14_application_filed
Type: FactEntry[bool]
Description: True if secured creditor filed written application under Section 14(1) to CMM/DM
Module: M3

Field name: section_14_1a_invoked
Type: FactEntry[bool]
Description: True if order under Section 14(1) invokes Section 14(1A) for authorization
Module: M3

Field name: appointed_officer_type
Type: FactEntry[str]
Description: Type of officer appointed — e.g., "Advocate", "Peon", "Subordinate Officer"
Module: M3

**B. New YAML Rule Needed:**
Module: M3
Rule ID: M3_C1_section14_1a_validity
Conditions: section_14_1a_invoked=True AND appointed_officer_type="Advocate"
Severity: INFO
Message: "Appointment of advocate as commissioner under Section 14(1A) is valid per Subir Chakravarty (2022) SCC OnLine SC 234."
Judgment tag: ["Subir_Chakravarty"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: muhammed_ashraf_union_of_india.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Subir Chakravarty (2022 SCC OnLine SC 234) — while both allow advocate commissioners, this case confirms validity post-insertion of Section 14(1A)."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: POSSESSION_DEFECT
