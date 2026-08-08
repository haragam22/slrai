---
citation: "2023 INSC 30"
title: "Kotak Mahindra Bank Limited vs Girnar Corrugators Pvt. Ltd. & Ors."
short_name: "Kotak Mahindra Bank v. Girnar Corrugators"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2023-01-05"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["PENDING_SA_CONCEALED"]
statutory_basis: ACT
act_sections: ["Section 14", "Section 17", "Section 26E"]
rules_sections: []
slrai_modules: ["M3"]
keywords: ["Section 26E", "MSMED Act", "priority of recovery", "Section 14 SARFAESI", "Facilitation Council award", "non-obstante clause", "overriding effect", "recovery as arrears of land revenue"]
retrieval_condition: "Applies when the bank's SARFAESI recovery is challenged by a prior MSMED Act Facilitation Council award claiming priority of recovery."
source: SC_FULL_TEXT
ik_doc_id: "34834631"
ik_url: "https://indiankanoon.org/doc/34834631/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers, including respondent No.1 (a micro or small enterprise), alleged that the recovery proceedings initiated by the bank under Section 14 of the SARFAESI Act should not prevail over the recovery certificates issued in their favour under the MSMED Act. They contended that Section 24 of the MSMED Act, being a later enactment with a non-obstante clause, gives overriding effect to the recovery mechanism under Sections 15 to 23 of the MSMED Act, including the award of the Facilitation Council. They further argued that such awards are executable as arrears of land revenue under state rules and thus have first charge on the secured assets. The prayer was to uphold the High Court’s decision that the MSMED Act recoveries take precedence over SARFAESI enforcement.

## HOLDING SUMMARY

Section 26E of the SARFAESI Act, inserted by amendment in 2016, establishes a statutory priority for secured creditors by providing that debts due to them shall be paid in priority over all other debts, including revenue taxes and cesses, after registration of the security interest. This provision contains a non-obstante clause and is a later enactment than the MSMED Act (2006), thereby prevailing over any conflicting recovery mechanism. The Court held that the MSMED Act does not contain an express provision granting priority over secured creditors akin to Section 26E, and thus its recovery mechanism under Sections 15–23 cannot override SARFAESI enforcement. The order of the Naib Tehsildar refusing possession under Section 14 on grounds of a pending MSMED recovery was without jurisdiction, as disputes must be adjudicated only by the DRT under Section 17. This applies when: a Facilitation Council award under the MSMED Act is claimed to have priority over a SARFAESI recovery, but Section 26E of the SARFAESI Act applies and no express priority is granted under the MSMED Act.

## KEY FACTS OF THIS CASE

Kotak Mahindra Bank had extended credit facilities to Mission Vivacare, secured by immovable properties in Dhar, Madhya Pradesh. Upon default, the bank initiated SARFAESI proceedings and filed an application under Section 14 on 17.06.2014, which was allowed by the District Magistrate on 24.09.2014 for possession of the secured assets. However, the Naib Tehsildar refused to act, citing a pending recovery certificate in favour of Girnar Corrugators Pvt. Ltd. (a respondent) issued under the MSMED Act after an award by the Facilitation Council on 11.09.2014. The bank challenged this refusal in the High Court, which initially ruled in its favour. The Division Bench reversed, holding that the MSMED Act prevails. The Supreme Court restored the Single Judge’s order, affirming SARFAESI’s primacy.

## WHAT THE COURT DECIDED

The Supreme Court allowed the appeal, set aside the Division Bench’s judgment, and restored the Single Judge’s order. It held that the Naib Tehsildar had no jurisdiction to refuse possession under Section 14 of the SARFAESI Act based on a pending MSMED Act recovery. The Court declared that recoveries under the SARFAESI Act, particularly under Section 26E, prevail over those under the MSMED Act. It clarified that any party aggrieved by SARFAESI measures must approach the DRT under Section 17, not obstruct enforcement through parallel recovery mechanisms.

## KEY QUOTE

Section 26E of the SARFAESI Act which is inserted in 2016 is also having a non-obstante clause. Even as per the submission on behalf of respondent No.1, two enactments have competing non-obstante provision and nothing repugnant, then the non-obstante clause of the subsequent statute would prevail over the earlier enactments.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `pending_sa_existed_at_auction_date` is TRUE — a recovery proceeding under MSMED Act or similar law was pending at the time of SARFAESI enforcement
2. `auction_conducted_despite_stay` is FALSE — no formal stay was granted by DRT or court
3. `statutory_basis` is "ACT" — the dispute involves interpretation of SARFAESI Act provisions
4. `act_sections` contains "Section 26E" — the bank relies on Section 26E for priority of recovery
5. `challenges_auction` is TRUE — the borrower or third party challenges the auction on grounds of prior recovery rights under a special statute like MSMED Act

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the recovery under the MSMED Act is protected by a valid interim or final stay order from the DRT or High Court — in that case, *Celco Trading v. Union of India* (2022) applies, and enforcement must cease during the stay.
   SLRAI ROUTING: if `drt_interim_stay_granted` = TRUE → *Celco Trading* applies; if FALSE → this judgment applies.

2. When the dispute involves dues under a statute that explicitly grants priority over secured creditors (e.g., certain tax or labour laws with charge provisions) — in such cases, the specific statute may override SARFAESI.
   SLRAI ROUTING: if `statutory_basis` includes "OTHER" and `act_sections` contains a provision with express priority (e.g., "Section 137 MP Land Revenue Code") → case-specific analysis required.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002  
Primary provision: Section 26E — "Notwithstanding anything inconsistent therewith contained in any other law for the time being in force, after the registration of security interest, the debts due to any secured creditor shall be paid in priority over all other debts and all revenue taxes and cesses and other rates payable to the Central Government or State Government or Local Authority."  
Instrument level: ACT  
Nature of provision: MANDATORY — court held that the non-obstante clause and later enactment status make this a binding priority rule.

Secondary: Section 14 SARFAESI Act — empowers District Magistrate to assist secured creditor in taking possession.  
Nature: MANDATORY — DM has no jurisdiction to adjudicate disputes or refuse possession based on third-party claims.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Bank of India v. Ketan Praekh & Ors. [(2008) 8 SCC 148]  
  Applied the principle that a later non-obstante clause prevails over an earlier one in case of conflict.

Distinguishes: Celir LLP v. Bafna Motors (2024) 2 SCC 1  
  While Celir LLP dealt with auction finality, this case addresses priority between enforcement mechanisms.  
  SLRAI ROUTING: if `challenges_auction` is based on procedural delay → *Celir LLP*; if based on competing recovery statute → *Kotak Mahindra Bank v. Girnar Corrugators* applies.

Affirmed: M. Rajendran v. KPK Oils (2025 SCC OnLine SC 2036)  
  Reaffirmed that DRT is the exclusive forum for challenging SARFAESI measures under Section 17.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**  
Field name: msmed_recovery_pending  
Type: FactEntry[bool]  
Description: True if a recovery certificate or award under MSMED Act is pending against the secured asset  
Module: M3  
Extraction: From borrower’s SA or bank’s rejoinder; often cited in objections

**B. New YAML Rule Needed:**  
Module: M3  
Rule ID: M3_C8_msmed_vs_sarfaesi_priority  
Conditions: msmed_recovery_pending=True AND act_sections contains "Section 26E"  
Severity: FATAL  
Message: "MSMED Act recovery does not override SARFAESI enforcement under Section 26E. Bank has statutory priority unless stay is in place."  
Judgment tag: ["Kotak_Mahindra_Bank_v_Girnar_Corrugators"]  
Statutory basis: ACT

**C. Existing Judgments to Update:**  
File: celir_llp_bafna_motors.md  
Section: ## RELATIONSHIP TO OTHER JUDGMENTS  
Add: "Distinguished by: Kotak Mahindra Bank v. Girnar Corrugators (2023 INSC 30) — held that Section 26E of SARFAESI Act gives secured creditors priority over MSMED Act recovery claims, even with non-obstante clause."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: PENDING_SA_CONCEALED
