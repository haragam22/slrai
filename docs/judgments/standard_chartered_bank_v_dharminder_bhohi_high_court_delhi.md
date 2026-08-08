---
citation: "(2014) 1 SCC 341"
title: "Standard Chartered Bank v. Dharminder Bhohi and others"
short_name: "Standard Chartered Bank v. Dharminder Bhohi"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2013-09-13"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["AUCTION_PURCHASER"]
statutory_basis: ACT
act_sections: ["Section 17", "Section 19", "Section 34"]
rules_sections: []
slrai_modules: ["M10"]
keywords: ["liberty to file action", "DRAT jurisdiction", "compensation vs damages", "inherent powers of tribunal", "Section 19 SARFAESI", "no civil court jurisdiction", "abuse of process", "ends of justice", "tribunal cannot grant liberty", "settlement between borrower and purchaser"]
retrieval_condition: "Applies when the DRAT granted liberty to an auction purchaser to file a separate action against the bank for omission, despite the bank not being party to the compromise."
source: SC_FULL_TEXT
ik_doc_id: "147299938"
ik_url: "https://indiankanoon.org/doc/147299938/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower did not directly challenge the enforcement action on procedural grounds but instead entered into a settlement with the auction purchaser before the DRAT. The auction purchaser, impleaded in the appeal, claimed that the bank had failed to disclose the pendency of litigation before the DRT at the time of auction, which influenced her decision to participate. She contended that she was entitled to damages for this omission and sought liberty from the DRAT to initiate a separate legal action against the bank. The High Court upheld the DRAT’s grant of such liberty, effectively allowing a collateral remedy outside the SARFAESI framework.

## HOLDING SUMMARY

The Supreme Court held that the Debt Recovery Appellate Tribunal (DRAT), being a statutory tribunal created under the SARFAESI Act and RDB Act, does not possess inherent powers to grant liberty to a party to initiate a separate legal action against the bank for alleged omissions. The jurisdiction of the DRAT is strictly confined to adjudicating disputes arising under Sections 17 and 18 of the SARFAESI Act, including granting compensation under Section 19 where possession is found to be illegal. Granting liberty to file a separate suit exceeds the tribunal’s statutory authority, especially when the bank was not a party to the compromise between the borrower and the auction purchaser. Such an order undermines the exclusivity of remedies under SARFAESI and violates Section 34, which bars civil court jurisdiction. This applies when: the DRAT grants liberty to an auction purchaser to sue the bank for omission, despite the absence of a finding of illegality in the enforcement action.

## KEY FACTS OF THIS CASE

Standard Chartered Bank sanctioned a home loan of Rs. 12 lakhs to Dharminder Bhohi in 1999, secured by a mortgage on a property. The account turned into an NPA, and the bank issued a Section 13(2) notice on 28.12.2002. After non-payment, the bank took possession in 2004 and conducted a public auction in March 2005. The auction purchaser, respondent No. 3, deposited Rs. 25.60 lakhs. The borrower challenged the action under Section 17 before the DRT, which gave him 15 days to repay. The DRAT, after a delay of nearly five years, passed an order in May 2010 approving a settlement between the borrower and the auction purchaser, and granted liberty to the purchaser to file an action against the bank for not disclosing the pendency of the DRT application. The bank challenged this liberty clause in the High Court, which refused to interfere. The bank appealed to the Supreme Court.

## WHAT THE COURT DECIDED

The Supreme Court allowed the appeal and deleted the portion of the DRAT’s order granting liberty to the auction purchaser to file a separate action against the bank. It held that such a direction was beyond the statutory jurisdiction of the DRAT. The High Court’s refusal to interfere was set aside. However, the Court declined to remit the matter to the DRAT for fresh adjudication, noting that the auction purchaser had not challenged the order and that the bank had already realized its dues and the property had changed hands.

## KEY QUOTE

Taking note of a submission made at the behest of the auction purchaser and then proceed to say that he is at liberty to file any action against the bank for any omission committed by it has no sanction of law.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `sa_applicant_type` is "auction_purchaser" — the applicant in the SA is the auction purchaser
2. `drat_granted_liberty_to_sue` is TRUE — the DRAT granted liberty to initiate a separate legal action against the bank
3. `bank_was_party_to_compromise` is FALSE — the bank was not a party to the settlement or compromise between borrower and purchaser
4. `no_illegality_in_enforcement` is TRUE — the enforcement action (possession, auction) was not found to be illegal or non-compliant
5. `section_19_compensation_not_awarded` is TRUE — the tribunal did not award compensation under Section 19 for illegal possession

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the DRAT or DRT finds that the bank’s enforcement action was illegal or non-compliant with SARFAESI provisions — in that case, Section 19 allows for compensation, and the auction purchaser may be entitled to relief under the SARFAESI framework.
   SLRAI ROUTING: if `enforcement_action_illegal` = TRUE → Section 19 applies → compensation may be awarded.

2. When the auction purchaser is challenging the validity of the auction or possession itself under Section 17 — this judgment does not bar such a challenge; it only restricts the grant of liberty to file a separate civil suit.
   SLRAI ROUTING: if `challenges_auction` = TRUE → other precedents like Kanaiyalal or Celir LLP apply.

3. When the bank consented to the compromise or was a party to the settlement — in such a case, the tribunal’s observation may be treated as part of the agreed terms.
   SLRAI ROUTING: if `bank_was_party_to_compromise` = TRUE → this judgment does not apply.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002  
Primary provision: Section 19 — "If the Debts Recovery Tribunal or the Court of District Judge, on an application made under section 17 or section 17A or the Appellate Tribunal or the High Court on an appeal preferred under section 18 or section 18A, holds that the possession of secured assets by the secured creditor is not in accordance with the provisions of this Act and rules made thereunder and directs the secured creditors to return such secured assets to the concerned borrowers, such borrower shall be entitled to the payment of such compensation and costs as may be determined by such Tribunal or Court of District Judge or Appellate Tribunal or the High Court referred to in section 18B."  
Instrument level: ACT  
Nature: MANDATORY — compensation is only available if illegal possession is established.

Secondary: Section 34 — "No civil court shall have jurisdiction to entertain any suit or proceeding in respect of any matter which a Debts Recovery Tribunal or the Appellate Tribunal is empowered by or under this Act to determine..."  
Nature: MANDATORY — establishes exclusivity of SARFAESI remedies.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Mardia Chemicals Ltd. v. Union of India — reaffirms that SARFAESI is a complete code for enforcement and remedies, and public interest in recovery outweighs individual procedural claims.

Follows: United Bank of India v. Satyawati Tondon — confirms that DRT/DRAT jurisdiction is limited to adjudicating on enforcement measures under Section 17 and cannot extend to creating new remedies.

Distinguishes: Ashok Saw Mill (2004) 4 SCC 311 — while that case recognized DRAT’s power to set aside transactions, it did not authorize the creation of collateral remedies outside the Act.  
SLRAI ROUTING: if `transaction_set_aside` = TRUE → Ashok Saw Mill applies; if `liberty_to_sue_granted` = TRUE → this judgment applies.

Affirmed: Union of India v. R. Gandhi, Madras Bar Association — reiterates that tribunals are creatures of statute and lack inherent powers like civil courts.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: drat_granted_liberty_to_sue
Type: FactEntry[bool]
Description: True if the DRAT granted liberty to the auction purchaser (or any party) to file a separate legal action against the bank
Module: M10
Extraction: From DRAT order text — look for phrases like "liberty to file action", "right to sue", "remedy against the bank"

Field name: bank_was_party_to_compromise
Type: FactEntry[bool]
Description: True if the bank was a signatory or consenting party to the settlement between borrower and third party
Module: M10
Extraction: Check if bank is listed as a party to the compromise or if its consent is recorded in the order

**B. New YAML Rule Needed:**
Module: M10
Rule ID: M10_C8_drat_liberty_beyond_jurisdiction
Conditions: drat_granted_liberty_to_sue=True AND enforcement_action_illegal=False
Severity: FATAL
Message: "DRAT granted liberty to auction purchaser to file separate action against bank despite no illegality in enforcement. Such liberty is beyond tribunal's jurisdiction under SARFAESI Act. Remedy, if any, lies under Section 19 only."
Judgment tag: ["Standard_Chartered_Bank_v_Dharminder_Bhohi"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: ashok_saw_mill.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Standard Chartered Bank v. Dharminder Bhohi (2014) 1 SCC 341 — held that grant of liberty to file separate action against bank is beyond DRAT's jurisdiction, even if Ashok Saw Mill recognized power to set aside transactions."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: AUCTION_PURCHASER
