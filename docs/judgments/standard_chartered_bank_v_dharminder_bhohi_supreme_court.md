---
citation: "(2014) 1 SCC 341"
title: "Standard Chartered Bank v. Dharminder Bhohi and others"
short_name: "Dharminder Bhohi"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2013-09-13"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["AUCTION_DURING_STAY", "PENDING_SA_CONCEALED"]
statutory_basis: ACT
act_sections: ["Section 17", "Section 19", "Section 34"]
rules_sections: []
slrai_modules: ["M3", "M10"]
keywords: ["liberty to file action", "pending SA concealed", "abuse of process", "DRAT jurisdiction", "Section 19 SARFAESI", "no inherent powers", "compromise not binding on bank", "auction during stay", "statutory finality"]
retrieval_condition: "Applies when the DRAT granted liberty to an auction purchaser to file a civil suit against the bank for conducting auction without disclosing a pending Section 17 application."
source: SC_FULL_TEXT
ik_doc_id: "147299938"
ik_url: "https://indiankanoon.org/doc/147299938/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower(s) alleged that the bank conducted the auction of the mortgaged property despite a pending Section 17 application before the DRT, thereby rendering the sale infructuous. They contended that the bank failed to disclose the existence of the ongoing litigation to the auction purchaser, who participated in the auction without knowledge of the dispute. The auction purchaser further claimed that she was entitled to damages from the bank for being misled, and the DRAT granted her liberty to initiate a civil action against the bank for such omission. The prayer before the High Court and Supreme Court included enforcement of this liberty to sue.

## HOLDING SUMMARY

The Supreme Court held that the Debt Recovery Appellate Tribunal (DRAT) lacks inherent jurisdiction to grant liberty to an auction purchaser to initiate a civil suit against a secured creditor for conducting an auction while a Section 17 application was pending. The tribunal’s powers are strictly statutory and confined to the SARFAESI Act and RDB Act, and it cannot assume the role of a civil court by authorizing collateral litigation. While Section 19 of the SARFAESI Act allows for compensation to borrowers when enforcement actions are found illegal, no such remedy is extended to auction purchasers. Granting liberty to file a civil suit constitutes an abuse of process and exceeds the tribunal’s limited jurisdiction. This applies when: the DRAT grants liberty to an auction purchaser to sue the bank for conducting an auction without disclosing a pending Section 17 application.

## KEY FACTS OF THIS CASE

Standard Chartered Bank sanctioned a home loan of Rs. 12 lakhs to Dharminder Bhohi in 1999, secured by a mortgaged property. The account turned NPA, and the bank issued a Section 13(2) notice on 28.12.2002. The borrower filed a Section 17 application before the DRT on 15.3.2005 challenging the enforcement, but the bank proceeded to auction the property on 10.3.2005. The auction purchaser, M/s. Unitech, deposited Rs. 25.60 lakhs and sought confirmation of sale. The DRT granted the borrower 15 days to repay and compensate the auction purchaser. The borrower appealed to the DRAT, which remained pending for over four and a half years. During this time, the DRAT allowed a compromise between the borrower and auction purchaser and granted the latter liberty to sue the bank for not disclosing the pending litigation. The bank challenged this direction in the High Court and then the Supreme Court.

## WHAT THE COURT DECIDED

The Supreme Court allowed the bank’s appeal, deleting the DRAT’s observation granting liberty to the auction purchaser to file a civil suit against the bank. It held that the DRAT had no jurisdiction to authorize such litigation, as its powers are strictly circumscribed by the SARFAESI and RDB Acts. The Court declined to remit the matter to the DRAT for fresh adjudication, noting that the bank had already recovered its dues and the property had changed hands. No costs were awarded.

## KEY QUOTE

Taking note of a submission made at the behest of the auction purchaser and then proceed to say that he is at liberty to file any action against the bank for any omission committed by it has no sanction of law.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `pending_sa_existed_at_auction_date` is TRUE — a Section 17 application was pending before the DRT on the date of auction
2. `auction_notice_discloses_pending_sa` is FALSE — the auction notice did not disclose the existence of the pending SA
3. `auction_purchaser_granted_liberty_to_sue` is TRUE — the DRAT or DRT granted the auction purchaser liberty to initiate a civil suit against the bank
4. `sa_applicant_type` is "AUCTION_PURCHASER" — the applicant before the tribunal is the auction purchaser, not the borrower
5. `tribunal_granted_compensation_to_purchaser` is FALSE — the tribunal did not award compensation under Section 19, but only granted procedural liberty

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the auction purchaser is seeking compensation under Section 19 of the SARFAESI Act for illegal sale — in that case, the tribunal may have jurisdiction to consider such a claim if framed properly.
   SLRAI ROUTING: if `prayer_scope_covers_compensation_under_s19` = TRUE → Section 19 applies; if FALSE → this judgment applies.

2. When the borrower, not the auction purchaser, is granted compensation by the tribunal — Section 19 explicitly allows compensation to borrowers, and such orders are valid.
   SLRAI ROUTING: if `sa_applicant_type` = "BORROWER" and `relief_granted` = "compensation" → Section 19 applies; if `sa_applicant_type` = "AUCTION_PURCHASER" → this judgment applies.

3. When the civil court, not the DRAT, grants such liberty — this judgment only restricts tribunals, not civil courts exercising independent jurisdiction.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002  
Primary provision: Section 19 — "If the Debts Recovery Tribunal or the Court of District Judge, on an application made under section 17 or section 17A or the Appellate Tribunal or the High Court on an appeal preferred under section 18 or section 18A, holds that the possession of secured assets by the secured creditor is not in accordance with the provisions of this Act and rules made thereunder and directs the secured creditors to return such secured assets to the concerned borrowers, such borrower shall be entitled to the payment of such compensation and costs as may be determined by such Tribunal or Court of District Judge or Appellate Tribunal or the High Court referred to in section 18B."  
Instrument level: ACT  
Nature of provision: MANDATORY — compensation is only available to borrowers, not third-party purchasers, and only upon a finding of illegality.

Secondary: Section 34 — "No civil court shall have jurisdiction to entertain any suit or proceeding in respect of any matter which a Debts Recovery Tribunal or the Appellate Tribunal is empowered by or under this Act to determine..."  
Nature: MANDATORY — reinforces the exclusive jurisdiction of tribunals and bars parallel civil proceedings.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Mardia Chemicals Ltd. v. Union of India (2004) 4 SCC 311  
  Affirmed that public interest in speedy recovery outweighs individual procedural grievances, and tribunals must act expeditiously to serve this purpose.

Follows: United Bank of India v. Satyawati Tondon (2006) 4 SCC 1  
  Reinforced that DRT/DRAT jurisdiction is strictly defined by statute and limited to adjudicating on enforcement measures under Section 13(4).

Distinguishes: Transcore v. Union of India (2009) 8 SCC 366  
  While Transcore emphasized time-value of assets, this case clarifies that tribunals cannot create new remedies beyond statutory grant.  
  SLRAI ROUTING: if `tribunal_creates_new_remedy` = TRUE → Dharminder Bhohi applies; if `tribunal_interprets_existing_power` = TRUE → Transcore applies.

Affirmed: Union of India v. R. Gandhi, Madras Bar Association (2010) 1 SCC 125  
  Tribunals are creatures of statute and lack inherent powers; they must function within the four corners of the enabling law.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: auction_purchaser_granted_liberty_to_sue
Type: FactEntry[bool]
Description: True if the DRT/DRAT granted the auction purchaser liberty to initiate a civil suit against the bank
Module: M10
Extraction: From tribunal order — look for phrases like "liberty to file action", "right to sue", "remedy against the bank"

Field name: sa_applicant_type
Type: FactEntry[str]
Description: Type of applicant — "BORROWER", "AUCTION_PURCHASER", "GUARANTOR", "TENANT"
Module: M10
Extraction: From SA filing — identify the party category based on role in SARFAESI process

**B. New YAML Rule Needed:**
Module: M10
Rule ID: M10_C8_liberty_to_sue_invalid
Conditions: sa_applicant_type="AUCTION_PURCHASER" AND auction_purchaser_granted_liberty_to_sue=True
Severity: FATAL
Message: "DRAT/DRT cannot grant liberty to auction purchaser to file civil suit. Such direction is without jurisdiction and invalid under SARFAESI Act."
Judgment tag: ["Dharminder_Bhohi"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: satyawati_tondon_united_bank.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Dharminder Bhohi (2014) 1 SCC 341 — held that Section 19 compensation is only for borrowers, not auction purchasers, and tribunals cannot grant liberty to sue beyond statutory powers."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: AUCTION_DURING_STAY
