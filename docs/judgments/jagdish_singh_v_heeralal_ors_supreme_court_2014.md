---
citation: "2014 (1) SCC 479"
title: "Jagdish Singh vs Heeralal & Ors"
short_name: "Jagdish Singh"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2013-10-30"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["AUCTION_PURCHASER", "TENANCY_CLAIM"]
statutory_basis: ACT
act_sections: ["Section 13(4)", "Section 17", "Section 34"]
rules_sections: []
slrai_modules: ["M3", "M5"]
keywords: ["Section 34", "civil court jurisdiction", "HUF property", "ancestral property", "aggrieved person", "Section 17 DRT", "right to appeal", "no civil suit", "jurisdiction bar"]
retrieval_condition: "Applies when a civil suit is filed challenging the SARFAESI auction on grounds of title or HUF status after the auction has been confirmed."
source: SC_FULL_TEXT
ik_doc_id: "128032254"
ik_url: "https://indiankanoon.org/doc/128032254/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers (Respondent Nos.1 to 5) alleged that the property auctioned under SARFAESI was joint family property of a Hindu Undivided Family (HUF), acquired from joint family funds, and not the individual property of the borrowers who had mortgaged it. They contended that the civil court had jurisdiction to decide questions of title and familial ownership, and that the DRT could not adjudicate upon such rights. They further argued that the auction purchaser had no right to object to a suit seeking declaration of title and partition, and that the civil court was the proper forum to determine their proprietary rights. The prayer before the civil court was for declaration of title, partition, and permanent injunction against the auction and transfer of the property.

## HOLDING SUMMARY

Section 34 of the SARFAESI Act, 2002 completely bars the jurisdiction of civil courts in any matter that can be determined by the DRT or DRAT under the Act, including challenges to enforcement measures under Section 13(4) such as auction and sale. Even if a party claims that the secured asset is HUF or ancestral property, such a dispute must be raised before the DRT under Section 17, not in a civil suit. The expression "any person" in Section 17 includes third parties with an interest in the property, but their remedy is limited to the DRT. A civil suit challenging the validity of a SARFAESI auction on grounds of title or ownership is not maintainable. This applies when: a civil suit is filed to challenge the auction on grounds of HUF or ancestral title after the secured creditor has initiated enforcement under Section 13(4).

## KEY FACTS OF THIS CASE

The Bank of India had advanced a loan of Rs. 25 lakhs to M/s Guru Om Automobiles, secured by an equitable mortgage on one acre of land and three houses held in the names of individual borrowers. Upon default, the bank issued a Section 13(2) notice and conducted an auction on 08.11.2005, which was confirmed in favor of Jagdish Singh, the appellant and auction purchaser. After the auction, Respondent Nos.1 to 5 filed a civil suit in the District Court of Barwani claiming the land was HUF property and seeking declaration, partition, and injunction. The bank and auction purchaser objected, citing lack of civil court jurisdiction under Section 34. The DRT had already dismissed a prior challenge to the auction. The civil court initially dismissed the suit, but the Madhya Pradesh High Court reversed, holding the civil court had jurisdiction. The Supreme Court reversed the High Court.

## WHAT THE COURT DECIDED

The Supreme Court allowed the appeal, set aside the judgment of the Madhya Pradesh High Court, and restored the order of the civil court dismissing the suit. It held that the civil court lacked jurisdiction under Section 34 of the SARFAESI Act to entertain a suit challenging the auction of secured assets. The proper remedy for the respondents was to file an application under Section 17 before the DRT, not a civil suit. The auction purchaser’s rights were protected, and no costs were awarded.

## KEY QUOTE

A civil court has no jurisdiction to entertain any suit or proceeding in respect of any matter which a Debts Recovery Tribunal or the Appellate Tribunal is empowered by or under this Act to determine.

## CONDITION: WHEN THIS JUDGMENT APPLIES

Applies when a civil suit is filed challenging the SARFAESI auction on grounds of title or HUF status after the auction has been confirmed.

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the challenge is to the classification of the account as NPA or the service of the demand notice — in that case, Kanaiyalal v. State of Maharashtra applies.
2. When the borrower themselves files an application under Section 17 before the DRT — then the DRT has jurisdiction and this case does not bar the proceeding, it confirms it.
3. When the property is not claimed to be HUF or ancestral but is subject to a tenancy or lease — then M. Rajendran or other tenancy-specific judgments apply.
   SLRAI ROUTING: if `tenancy_claimed` = TRUE → M_RAJENDRAN applies; if `property_classification` = "HUF" → Jagdish Singh applies.

## STATUTORY CONTEXT

Primary law: SARFAESI Act, 2002  
Primary provision: Section 34 — "No civil court shall have jurisdiction to entertain any suit or proceeding in respect of any matter which a Debts Recovery Tribunal or the Appellate Tribunal is empowered by or under this Act to determine and no injunction shall be granted by any court or other authority in respect of any action taken or to be taken in pursuance of any power conferred by or under this Act..."  
Instrument level: ACT  
Nature of provision: MANDATORY — the bar on civil court jurisdiction is absolute and applies even to claims of title or HUF status.

Secondary: Section 17 — provides the exclusive remedy for any aggrieved person, including third parties, to challenge enforcement measures before the DRT.  
Nature: MANDATORY — the DRT is the only forum for such disputes.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Mardia Chemicals Ltd. v. Union of India (2004) 4 SCC 311  
  Confirmed that Section 34 bars civil court jurisdiction even before enforcement measures are taken, as long as the matter falls within DRT’s purview.

Follows: Central Bank of India v. State of Kerala (2009) 4 SCC 94  
  Reiterated that DRT has exclusive jurisdiction over SARFAESI enforcement, and civil courts cannot interfere.

Distinguishes: Nahar Industrial Enterprises Ltd. v. HSBC (2009) 8 SCC 646  
  Nahar dealt with pre-SARFAESI rights and third-party claims in winding-up; here, the enforcement is post-SARFAESI and the remedy is clearly under Section 17.  
  SLRAI ROUTING: if `measure_type` = "SARFAESI enforcement" → Jagdish Singh applies; if `measure_type` = "winding-up" → Nahar applies.

Affirmed: Satyavati Tondon v. United Bank of India (2010) 8 SCC 110  
  Affirmed that "any person" under Section 17 includes third parties with interest, but their remedy is confined to DRT.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: property_classification
Type: FactEntry[str]
Description: Classification of the property as "Individual", "HUF", "Ancestral", "Joint Family", "Tenanted", etc.
Module: M5
Extraction: From borrower’s pleadings or SA content

**B. New YAML Rule Needed:**
Module: M5
Rule ID: M5_C1_huf_claim_in_civil_court
Conditions: challenges_auction=True AND sa_applicant_type="Third Party" AND property_classification="HUF" AND challenges_demand_notice=False
Severity: FATAL
Message: "Civil suit challenging SARFAESI auction on HUF grounds is not maintainable. Exclusive remedy is under Section 17 before DRT."
Judgment tag: ["JAGDISH_SINGH"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: nahar_industrial_enterprises.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Jagdish Singh (2014) 1 SCC 479 — held that civil suit challenging SARFAESI auction on HUF grounds is barred by Section 34; exclusive remedy is Section 17 before DRT."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: AUCTION_PURCHASER
