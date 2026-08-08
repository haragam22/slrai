---
citation: "CBI vs. M/s Gondwana Ispat Ltd & Ors, 27 April 2018"
title: "CBI vs. M/s Gondwana Ispat Ltd & Ors"
short_name: "Gondwana Ispat"
court: DRAT
high_court_state: null
bench_strength: 1
judgment_date: "2018-04-27"
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
retrieval_condition: "Applies when the borrower challenges the allocation of a coal block based on false representations about company registration and project status."
source: DRAT_FULL_TEXT
ik_doc_id: "181543286"
ik_url: "https://indiankanoon.org/doc/181543286/"
has_verified_conditions: false
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers alleged that the Central Bureau of Investigation (CBI) filed a false case against them, claiming that the applications for coal block allocation were submitted by a non-existent company and that false representations were made about financial tie-ups and land acquisition. They contended that the company was in the process of registration and that the actions were legitimate pre-incorporation activities. The borrowers further argued that the prosecution failed to prove any mens rea or guilty intention on their part. The prayer before the Special Judge was to acquit them of all charges.

## HOLDING SUMMARY

The court held that the accused, Ashok Daga and M/s Gondwana Ispat Ltd., were guilty of the offence of cheating under Section 420 of the Indian Penal Code (IPC) for making false representations to various government authorities to obtain the allocation of a coal block. The court found that the accused misrepresented the status of the company's registration and made false claims about financial tie-ups and land acquisition. The court also held that the accused were guilty of criminal conspiracy under Section 120-B of the IPC for the common object of procuring the allocation of a coal block through fraudulent means. This applies when: the accused made false representations to government authorities to obtain the allocation of a coal block.

## KEY FACTS OF THIS CASE

M/s Gondwana Ispat Ltd. (GIL) was a company promoted by Ashok Daga, who applied for the allocation of a coal block for a sponge iron plant. The company was not registered at the time of the initial applications, and false representations were made about the company's registration and financial preparedness. The Screening Committee meetings were influenced by these false representations, leading to the reservation of the Majra coal block for GIL. The company failed to develop the coal mine or set up the end-use plant, and Ashok Daga sold his equity in the company for a significant financial gain. The CBI investigated and found evidence of fraud, leading to the filing of charges.

## WHAT THE COURT DECIDED

The court convicted Ashok Daga and M/s Gondwana Ispat Ltd. for the offences of cheating under Section 420 of the IPC and criminal conspiracy under Section 120-B of the IPC. The court found that the accused had made false representations to government authorities to obtain the allocation of a coal block. The court also acquitted Ashok Daga of the charge of cheating for the sale of his equity, as there was no bar on the transfer of equity in the allocatee company.

## KEY QUOTE

A-2 Ashok Daga, who was the main promoter of M/s GIL transferred 25,000 shares of the company as were held by his two companies i.e. M/s Auric Commercial Pvt. Ltd and M/s Caspack Finvest (I) Pvt. Ltd. in favour of Mrs. Sudha Devi Daga W/o Sh. Govind Dass Daga.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `company_registration_status` is FALSE — the company was not registered at the time of application.
2. `false_representations_made` is TRUE — false representations were made about the company's registration and financial preparedness.
3. `coal_block_allocated` is TRUE — the coal block was allocated based on these false representations.
4. `equity_sold` is TRUE — the promoter sold their equity in the company for a significant financial gain.

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the company was registered at the time of application — in that scenario, the case of M/s Gondwana Ispat Ltd. does not apply.
2. When no false representations were made about financial preparedness or land acquisition — in that scenario, the case of M/s Gondwana Ispat Ltd. does not apply.
3. When the coal block was not allocated — in that scenario, the case of M/s Gondwana Ispat Ltd. does not apply.

## STATUTORY CONTEXT

Primary law: Indian Penal Code, 1860
Primary provision: Section 420 — "Whoever, by deceiving any person, fraudulently or dishonestly induces the person so deceived to deliver any property to any person, or to consent that any person shall retain any property, or intentionally induces the person so deceived to do or omit to do anything which he would not do or omit if he were not so deceived, and which act or omission causes or is likely to cause damage or harm to that person in body, mind, reputation or property, is said to "cheat"."
Level: IPC
Nature: MANDATORY

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Iridium India Telecom Limited vs Motorola Incorporated and Others (2011) 1 SCC 74 — Established that willful concealment of facts can constitute fraud.
Distinguishes: None — This judgment does not distinguish any other judgment.
Overruled: None — This judgment does not overrule any other judgment.
Affirmed: None — This judgment does not affirm any other judgment.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed**
Field name: company_registration_status
Type: FactEntry[bool]
Description: True if the company was registered at the time of application, False otherwise.
Module: M1

Field name: false_representations_made
Type: FactEntry[bool]
Description: True if false representations were made about the company's registration and financial preparedness, False otherwise.
Module: M1

Field name: coal_block_allocated
Type: FactEntry[bool]
Description: True if the coal block was allocated based on the false representations, False otherwise.
Module: M1

Field name: equity_sold
Type: FactEntry[bool]
Description: True if the promoter sold their equity in the company for a significant financial gain, False otherwise.
Module: M1

**B. New YAML Rules Needed**
Module: M1
Rule ID: M1_C1_false_representations
Conditions: company_registration_status=False AND false_representations_made=True
Severity: FATAL
Message: "The company was not registered at the time of application, and false representations were made about the company's registration and financial preparedness."
Judgment tags: ["Gondwana Ispat"]
Statutory basis: IPC

**C. New Ground Codes Needed**
Suggested code: FALSE_REPRESENTATIONS
Description: The borrower made false representations to government authorities to obtain the allocation of a coal block.
Module: M1

**D. Existing Judgments to Update**
File: iridium_india_telecom.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add line: "Distinguished by: Gondwana Ispat — held that false representations about company registration and financial preparedness can constitute fraud."

**E. No New Requirements**
No new fields, rules, or ground codes required. Fits within existing schema.

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: UNKNOWN
