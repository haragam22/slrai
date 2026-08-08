---
citation: "AIR 2011 Delhi 174"
title: "M/s. Sterling Agro Industries Ltd. vs Union Of India & Ors."
short_name: "Sterling Agro"
court: HIGH_COURT
high_court_state: "Delhi"
bench_strength: 5
judgment_date: "2011-08-01"
overruled: false
overruled_by: null
distinguished_by: []
favor: NEUTRAL
favor_verified: true
ground_codes: ["UNKNOWN"]
statutory_basis: OTHER
act_sections: []
rules_sections: []
slrai_modules: []
keywords: []
retrieval_condition: ""
source: HC_FULL_TEXT
ik_doc_id: "115567041"
ik_url: "https://indiankanoon.org/doc/115567041/"
has_verified_conditions: false
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The petitioner, M/s. Sterling Agro Industries Ltd., challenged the order passed by the Revisionary Authority located in Delhi, which dismissed its revision application against a customs duty determination. It contended that since the impugned order was passed by an authority situated within the territorial jurisdiction of the Delhi High Court, the Court had the jurisdiction to entertain the writ petition under Article 226 of the Constitution of India. The petitioner relied on the Full Bench decision in New India Assurance Co. Ltd. v. Union of India, which held that the location of the appellate or revisional authority constitutes a part of the cause of action, thereby conferring jurisdiction on the High Court where such authority is located.

## HOLDING SUMMARY

Article 226(2) of the Constitution of India allows a High Court to exercise writ jurisdiction if the cause of action, wholly or in part, arises within its territorial jurisdiction, even if the seat of the authority is outside. However, the mere presence of an appellate or revisional authority in a particular High Court’s jurisdiction does not automatically make that Court the appropriate forum. The doctrine of forum conveniens remains applicable, and the High Court retains discretion to decline jurisdiction if another forum is more appropriate, considering the convenience of parties, witnesses, and the nature of the dispute. The decision in New India Assurance Co. Ltd. is clarified to the extent that it treated the location of the appellate authority as determinative of jurisdiction. This applies when: a writ petition is filed in a High Court solely because an appellate or revisional authority is located there, but the substantial cause of action and relevant facts lie elsewhere.

## KEY FACTS OF THIS CASE

This case arose from a challenge by M/s. Sterling Agro Industries Ltd. to an order dated 9.7.2010 passed by the Revisionary Authority of the Ministry of Finance in Delhi, which dismissed its revision application concerning denial of drawback benefits under customs law. The original order was passed in Malanpur, Madhya Pradesh, and the appellate order was passed in Indore, Madhya Pradesh. The petitioner approached the Delhi High Court solely because the revisional authority was located in Delhi. The case was part of a batch of connected matters raising the same jurisdictional issue. The Division Bench referred the matter to a larger Bench to reconsider the Full Bench decision in New India Assurance Co. Ltd. v. Union of India, which had held that the location of the appellate authority alone was sufficient to confer jurisdiction.

## WHAT THE COURT DECIDED

The Constitution Bench of the Delhi High Court partially overruled and clarified the Full Bench decision in New India Assurance Co. Ltd. v. Union of India. It held that while the location of an appellate or revisional authority may constitute a part of the cause of action, it is not determinative of jurisdiction. The High Court may still decline to exercise jurisdiction under the doctrine of forum conveniens if the substantial cause of action and relevant facts lie elsewhere. The matter was remanded to the appropriate Division Bench for further consideration on merits.

## KEY QUOTE

Even if a miniscule part of cause of action arises within the jurisdiction of this court, a writ petition would be maintainable before this Court, however, the cause of action has to be understood as per the ratio laid down in the case of Alchemist Ltd.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `drt_interim_stay_granted` is FALSE — no stay order is in force affecting jurisdiction
2. `challenges_auction` is FALSE — the dispute is not related to SARFAESI auction or enforcement
3. [PENDING FIELD] `writ_petition_filed_in_high_court` is TRUE — a writ petition is filed under Article 226
4. [PENDING FIELD] `impugned_order_by_appellate_authority_in_delhi` is TRUE — the challenged order is passed by an appellate/revisional authority located in Delhi
5. [PENDING FIELD] `substantial_cause_of_action_outside_delhi` is TRUE — the core facts and original order are located outside Delhi

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the dispute involves SARFAESI Act enforcement actions such as demand notice, possession, or auction — in that case, jurisdictional rules under SARFAESI and DRT Act apply, not general Article 226 principles.
   SLRAI ROUTING: if `challenges_auction` = TRUE → SARFAESI-specific precedents apply.

2. When the petitioner is challenging a central legislation’s constitutional validity — in such cases, multiple High Courts may have jurisdiction regardless of cause of action location.
   SLRAI ROUTING: if `challenges_legislation_validity` = TRUE → constitutional precedents apply.

3. When the appellate authority’s order is the only operative order and all parties are within the jurisdiction — in such cases, the Full Bench in New India Assurance may still be applicable.

## STATUTORY CONTEXT

Primary law: Constitution of India
Primary provision: Article 226(2) — "The power conferred by clause (1) to issue directions, orders or writs to any Government, authority or person may also be exercised by any High Court exercising jurisdiction in relation to the territories within which the cause of action, wholly or in part, arises for the exercise of such power, notwithstanding that the seat of such Government or authority or the residence of such person is not within those territories."
Instrument level: OTHER
Nature of provision: DIRECTORY — court held that jurisdiction is discretionary and subject to forum conveniens

## RELATIONSHIP TO OTHER JUDGMENTS

Overruled: New India Assurance Company Limited v. Union of India, AIR 2010 Delhi 43 (FB)
  The Full Bench had held that the location of the appellate authority alone confers jurisdiction and that the Delhi High Court cannot decline to entertain such petitions.
  This judgment modifies that view, holding that forum conveniens allows discretion to decline jurisdiction.
  SLRAI ROUTING: if `impugned_order_by_appellate_authority_in_delhi` = TRUE AND `substantial_cause_of_action_outside_delhi` = TRUE → Sterling Agro applies; if both in Delhi → New India Assurance may still apply.

Follows: Alchemist Ltd. v. State Bank of Sikkim, (2007) 11 SCC 335
  Reaffirmed that only facts forming an integral part of the cause of action confer jurisdiction, not incidental or peripheral facts.

Follows: Kusum Ingots & Alloys Ltd. v. Union of India, (2004) 6 SCC 254
  Confirmed that a part of cause of action arising in a jurisdiction is sufficient, but not all facts are material to jurisdiction.

Distinguishes: M. Rajendran v. KPK Oils (2025 SCC OnLine SC 2036)
  M. Rajendran dealt with curtailed redemption rights under SARFAESI; this case deals with constitutional jurisdiction — different legal domains.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: writ_petition_filed_in_high_court
Type: FactEntry[bool]
Description: True if the borrower has filed a writ petition under Article 226 in a High Court
Module: M10

Field name: impugned_order_by_appellate_authority_in_delhi
Type: FactEntry[bool]
Description: True if the challenged order was passed by an appellate or revisional authority located in Delhi
Module: M10

Field name: substantial_cause_of_action_outside_delhi
Type: FactEntry[bool]
Description: True if the core facts, original order, and relevant evidence are located outside Delhi
Module: M10

**B. New YAML Rules Needed:**
Module: M10
Rule ID: M10_J1_forum_conveniens_delhi
Conditions: writ_petition_filed_in_high_court=True AND impugned_order_by_appellate_authority_in_delhi=True AND substantial_cause_of_action_outside_delhi=True
Severity: WARNING
Message: "Writ petition filed in Delhi HC based on appellate authority location, but substantial cause of action lies elsewhere. Jurisdiction may be declined under forum conveniens per Sterling Agro."
Judgment tags: ["Sterling_Agro"]
Statutory basis: OTHER

**C. New Ground Codes Needed:**
Suggested code: FORUM_CONVENIENS_JURISDICTION
Description: Challenge to jurisdiction based on forum conveniens despite partial cause of action in the High Court's territory
Module: M10

**D. Existing Judgments to Update:**
File: new_india_assurance_co_ltd.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Overruled by: Sterling Agro Industries Ltd. v. Union of India (AIR 2011 Delhi 174) — held that location of appellate authority alone does not confer jurisdiction; forum conveniens remains applicable."

## WIN-RATE CONTRIBUTION
favor: NEUTRAL
counted_in_ground: UNKNOWN
