---
citation: "2022 SCC OnLine SC 2196"
title: "Punjab National Bank v. Union of India Thr. Its Secretary"
short_name: "Punjab National Bank"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2022-02-24"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["SERVICE_DEFECT", "NOTICE_ALL_PARTIES"]
statutory_basis: ACT
act_sections: ["Section 13(2)", "Section 13(4)", "Section 35"]
rules_sections: []
slrai_modules: ["M1", "M10"]
keywords: ["Section 35 SARFAESI", "overriding effect", "confiscation proceedings", "excise duty priority", "Rule 173Q(2)", "vesting in Central Government", "first charge secured creditor", "Section 11E Central Excise Act", "Section 38A Central Excise Act", "proceedings without jurisdiction"]
retrieval_condition: "Applies when the confiscation order was passed under a repealed rule and the secured creditor claims priority under Section 35 of SARFAESI Act."
source: SC_FULL_TEXT
ik_doc_id: "122842801"
ik_url: "https://indiankanoon.org/doc/122842801/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower, Punjab National Bank, alleged that the Commissioner of Customs and Central Excise lacked jurisdiction to pass confiscation orders dated 26.03.2007 and 29.03.2007 under Rule 173Q(2) of the Central Excise Rules, 1944, because the said rule had been omitted from the statute book with effect from 12.05.2000. They contended that the proceedings could not be continued under a repealed rule and that Section 38A of the Central Excise Act, 1944, did not save such proceedings in the absence of a contrary legislative intent. They further argued that as a secured creditor under SARFAESI Act, 2002, they had first charge over the secured assets, and their rights could not be defeated by a confiscation order passed without statutory authority.

## HOLDING SUMMARY

Section 35 of the SARFAESI Act, 2002, gives the Act overriding effect over any inconsistent provisions in other laws, including the Central Excise Act, 1944. A confiscation order passed under Rule 173Q(2) of the Central Excise Rules, 1944, after its omission on 12.05.2000, is without jurisdiction and nullity in law, as Section 38A of the Central Excise Act does not save such proceedings in the absence of a contrary legislative intent. The secured creditor’s right under SARFAESI prevails over excise dues where no specific provision grants first charge to the government, and the confiscation order is rooted in a non-existent rule. This applies when: a confiscation order is passed under a repealed rule and the secured creditor asserts priority under Section 35 of the SARFAESI Act.

## KEY FACTS OF THIS CASE

Punjab National Bank, as lead bank in a consortium, provided credit facilities to M/s Rathi Ispat Ltd. (RIL) in 2005, against mortgage of all movable and immovable properties. RIL defaulted, and the bank issued a Section 13(2) SARFAESI notice on 02.08.2007. Earlier, in 1996, excise authorities had initiated confiscation proceedings under Rule 173Q(2) of the Central Excise Rules, 1944, which were set aside by CESTAT and remanded. The Commissioner passed fresh confiscation orders on 26.03.2007 and 29.03.2007 under the same rule, which had been omitted in 2000. The bank challenged these orders, asserting its SARFAESI rights. The Allahabad High Court dismissed the writ petition, holding that confiscated property vests in the Central Government. The Supreme Court allowed the appeal.

## WHAT THE COURT DECIDED

The Supreme Court allowed the appeal, holding that the confiscation orders dated 26.03.2007 and 29.03.2007 were passed without jurisdiction as Rule 173Q(2) had been omitted in 2000 and was not revived. The Court further held that the secured creditor’s rights under SARFAESI Act, 2002, have overriding effect over excise dues, and the bank was entitled to enforce its security interest. The impugned orders of the Commissioner were quashed.

## KEY QUOTE

A confiscation order passed under a provision which stood omitted from the statute book is without jurisdiction and is a nullity in the eye of law.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `notice_all_parties` is TRUE — the secured creditor has created a valid security interest over the property
2. `challenges_demand_notice` is FALSE — the challenge is not to the SARFAESI demand notice but to a prior confiscation order
3. `property_classification` is "immovable" OR "movable" — the property sought to be confiscated includes land, building, plant, machinery, etc.
4. `statutory_basis` is "ACT" — the dispute involves interpretation of SARFAESI Act, particularly Section 35
5. `pending_sa_existed_at_auction_date` is FALSE — the issue is not about pending SARFAESI proceedings but about validity of confiscation under a repealed rule

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the confiscation order was passed under a currently valid rule and the challenge is only on grounds of natural justice or quantum — in that case, *Kolhapur Canesugar Works* applies.
   SLRAI ROUTING: if `rule_under_which_confiscation_passed` is valid → *Kolhapur Canesugar Works* applies; if rule was omitted → this judgment applies.

2. When the SARFAESI enforcement is challenged on grounds of service, amount, or reply — in that case, *Kanaiyalal* or *Celir LLP* applies depending on the ground.
   SLRAI ROUTING: if `objection_filed` = TRUE and `bank_reply_given` = FALSE → *Kanaiyalal* applies; if auction defect → *Celir LLP* applies.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002  
Primary provision: Section 35 — "The provisions of this Act shall have effect, notwithstanding anything inconsistent therewith contained in any other law for the time being in force or any instrument having effect by virtue of any such law."  
Instrument level: ACT  
Nature of provision: MANDATORY — court held that Section 35 gives SARFAESI Act overriding effect, and no other law can prevail if inconsistent.

Secondary law: Central Excise Act, 1944  
Provision: Section 38A(c) and (e) — saves rights, liabilities, investigations despite repeal, unless contrary intention appears.  
Nature: DIRECTORY — court held that contrary legislative intent is evident from non-reintroduction of Rule 173Q(2) and change in Rule 28 to vest only "goods", not immovable property.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Kolhapur Canesugar Works Ltd. v. Union of India (2000) 2 SCC 536  
  Held that Section 6 of General Clauses Act, 1897 does not apply to omission of a Rule; omission without saving clause ends pending proceedings. This judgment applies the same principle to Rule 173Q(2).

Follows: UTI Bank Ltd. v. Dy. Commissioner Central Excise (2006 SCC Online Madras 1182)  
  Held that in absence of specific "first charge" provision in Central Excise Act, secured creditor’s claim prevails. This judgment affirms that principle and extends it with Section 35 override.

Distinguishes: Union of India v. SICOM Ltd. (2009) 2 SCC 121  
  SICOM held that SARFAESI does not give statutory first charge, but this judgment clarifies that Section 35’s overriding effect ensures secured creditor’s priority even without a "first charge" clause.  
  SLRAI ROUTING: if `section_11E_applies` = TRUE and `rule_repealed` = FALSE → SICOM applies; if `rule_repealed` = TRUE → this judgment applies.

Affirmed: Dena Bank v. Bhikhabhai Prabhu Dass Parikh (2000) 5 SCC 694  
  Reaffirmed that Crown debts do not have priority over secured creditors. This judgment applies that principle in the SARFAESI context.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: rule_under_which_confiscation_passed
Type: FactEntry[str]
Description: Name of the rule under which confiscation order was passed (e.g., "Rule 173Q(2)")
Module: M10
Extraction: From confiscation order or department communication

Field name: rule_omitted_before_order_date
Type: FactEntry[bool]
Description: True if the rule under which confiscation was passed was omitted before the order date
Computed from: rule_under_which_confiscation_passed, rule_omission_date, confiscation_order_date
Module: M10

**B. New YAML Rule Needed:**
Module: M10
Rule ID: M10_C8_confiscation_under_repealed_rule
Conditions: rule_omitted_before_order_date = True
Severity: FATAL
Message: "Confiscation order passed under a repealed rule is without jurisdiction and cannot defeat SARFAESI rights of secured creditor."
Judgment tag: ["PUNJAB_NATIONAL_BANK"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: union_of_india_v_sicom_ltd.md
Section: ## HOLDING SUMMARY
Add: "However, where the confiscation order is passed under a repealed rule, *Punjab National Bank v. Union of India* (2022) holds that such order is a nullity and SARFAESI rights prevail."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: SERVICE_DEFECT
