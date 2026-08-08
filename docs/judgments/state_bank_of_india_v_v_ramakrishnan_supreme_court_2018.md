---
citation: "AIR 2018 SC 3876"
title: "State Bank Of India vs V. Ramakrishnan"
short_name: "V. Ramakrishnan"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2018-08-14"
overruled: false
overruled_by: null
distinguished_by: []
favor: BANK
favor_verified: true
ground_codes: ["PENDING_SA_CONCEALED"]
statutory_basis: IBC
act_sections: []
rules_sections: []
slrai_modules: ["M3"]
keywords: ["Section 14 IBC", "moratorium", "personal guarantor", "CIRP", "Section 60 IBC", "Section 31 IBC", "Section 101 IBC", "stay proceedings"]
retrieval_condition: "Applies when a bank proceeds against a personal guarantor under SARFAESI while a CIRP is ongoing against the corporate debtor and the bank did not conceal a pending SA."
source: SC_FULL_TEXT
ik_doc_id: "163084985"
ik_url: "https://indiankanoon.org/doc/163084985/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers alleged that the moratorium imposed under Section 14 of the Insolvency and Bankruptcy Code, 2016, which applies upon admission of a corporate insolvency resolution process (CIRP), also extends to personal guarantors of the corporate debtor. They contended that proceedings under SARFAESI against the personal guarantor and his property must be stayed during the pendency of the CIRP. They further argued that Section 60(2) and Section 31 of the IBC support this interpretation, as personal guarantors are bound by the resolution plan and are part of the insolvency process. The prayer before the NCLT and NCLAT was to restrain the bank from enforcing security interests against the personal guarantor during the moratorium.

## HOLDING SUMMARY

Section 14 of the Insolvency and Bankruptcy Code, 2016, which imposes a moratorium upon the initiation of a corporate insolvency resolution process, applies only to the corporate debtor and not to personal guarantors. The Supreme Court held that the language of Section 14 is unambiguous—it refers exclusively to the corporate debtor and does not extend to individual sureties. The Court distinguished between the corporate entity and the personal guarantor, affirming that the liability of a guarantor is co-extensive but independent, and enforcement proceedings under SARFAESI can proceed against the guarantor’s assets even during the moratorium. The amendment to Section 14(3) by the IBC (Amendment) Act, 2018, which explicitly excludes sureties from the moratorium, was deemed clarificatory and retrospective, reinforcing the legislative intent. This applies when: a personal guarantor is proceeded against under SARFAESI while a CIRP is ongoing against the corporate debtor and the bank has not concealed a pending SA.

## KEY FACTS OF THIS CASE

The respondent was the Managing Director and personal guarantor of a corporate debtor that had availed credit facilities from the State Bank of India. The loan account was classified as NPA on 26.07.2015, and a SARFAESI demand notice was issued on 04.08.2015. A possession notice followed on 18.11.2016. The corporate debtor filed for CIRP under Section 10 of the IBC on 20.05.2017, which was admitted on 19.06.2017, triggering the Section 14 moratorium. The personal guarantor then moved the NCLT seeking a stay on SARFAESI proceedings, arguing that the moratorium extended to him. The NCLT and NCLAT allowed the interim application, but the Supreme Court reversed the decision, holding that SARFAESI enforcement against the guarantor could proceed.

## WHAT THE COURT DECIDED

The Supreme Court allowed the appeals filed by the State Bank of India and set aside the orders of the NCLAT and NCLT. It held that Section 14 of the IBC does not impose a moratorium on proceedings against personal guarantors. The bank was permitted to continue SARFAESI enforcement actions against the personal guarantor’s properties. The Court clarified that the liability of a personal guarantor remains enforceable independently of the corporate debtor’s insolvency process.

## KEY QUOTE

Section 14 refers only to debts due by corporate debtors, who are limited liability companies, and it is clear that in the vast majority of cases, personal guarantees are given by Directors who are in management of the companies.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `ibc_moratorium_active` is TRUE — a moratorium under Section 14 of the IBC is in force against the corporate debtor
2. `sa_applicant_type` is "personal_guarantor" — the applicant in the SA is a personal guarantor of the corporate debtor
3. `challenges_auction` is TRUE OR `challenges_demand_notice` is TRUE — the SA challenges SARFAESI enforcement actions
4. `prayer_scope_covers_current_measure` is TRUE — the prayer includes a request to stay SARFAESI proceedings during CIRP
5. `pending_sa_existed_at_auction_date` is FALSE — the bank did not conceal a pending SA in its Section 14 petition

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the applicant is the corporate debtor itself — in that case, the moratorium under Section 14 applies directly, and the enforcement is automatically stayed.
   SLRAI ROUTING: if `sa_applicant_type` = "corporate_debtor" → Section 14 stays apply; if `sa_applicant_type` = "personal_guarantor" → this judgment applies.

2. When the bank concealed a pending SARFAESI application while seeking relief under Section 14 — in such cases, the principle from *Celina Agarwal v. PRK Enterprises* applies, and the bank may be estopped from enforcing.
   SLRAI ROUTING: if `pending_sa_existed_at_auction_date` = TRUE AND `auction_notice_discloses_pending_sa` = FALSE → *Celina Agarwal* applies.

## STATUTORY CONTEXT

Primary law: Insolvency and Bankruptcy Code, 2016  
Primary provision: Section 14(1) — "On the insolvency commencement date, the Adjudicating Authority shall by order declare moratorium for prohibiting... (a) the institution of suits or continuation of pending suits or proceedings against the corporate debtor..."  
Instrument level: IBC  
Nature of provision: MANDATORY — court held the moratorium applies only to the corporate debtor, not third parties like guarantors. The word "corporate debtor" is used repeatedly and exclusively, indicating a deliberate legislative choice.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: *Madras Petrochem Ltd. v. BIFR* (2016) 4 SCC 1  
  Affirmed that Parliament deliberately omitted a moratorium on guarantors, learning from the overbroad stay under Section 22 of the Sick Industrial Companies Act.

Distinguishes: *Sanjeev Shriya v. State Bank of India* (2018) 2 All LJ 769  
  Allahabad High Court held that moratorium extends to personal guarantors. This judgment overrules that view.
  SLRAI ROUTING: if `court` = "HIGH_COURT" AND `favor` = "BORROWER" → check for SC override; if `court` = "SUPREME_COURT" → *V. Ramakrishnan* applies.

Follows: *Sicom Investments v. Rajesh Kumar Drolia* (2017) SCC Online Bom 9725  
  Bombay High Court held that Section 14 does not apply to personal guarantors — reasoning adopted by the Supreme Court.

Affirmed: *National Project Construction Corp. v. Sandhu & Co.* (AIR 1990 P&H 300)  
  Reaffirmed that a creditor may proceed against the surety independently of the principal debtor.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: ibc_moratorium_active
Type: FactEntry[bool]
Description: True if a moratorium under Section 14 of the IBC is in force against the corporate debtor
Module: M3
Computed from: CIRP admission date and resolution/liquidation order date

Field name: sa_applicant_type
Type: FactEntry[str]
Description: Type of applicant in the SA — values: "corporate_debtor", "personal_guarantor", "auction_purchaser", "tenant"
Module: Cross-cutting
Extraction: From SA filing details and prayer clause

**B. New YAML Rule Needed:**
Module: M3
Rule ID: M3_C8_moratorium_vs_sarfaesi
Conditions: ibc_moratorium_active=True AND sa_applicant_type="personal_guarantor"
Severity: WARNING
Message: "SARFAESI enforcement against personal guarantor is permissible during CIRP moratorium per V. Ramakrishnan (2018). No automatic stay applies."
Judgment tag: ["V_Ramakrishnan"]
Statutory basis: IBC

**C. Existing Judgments to Update:**
File: sanjeev_shriya_sbi.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Overruled by: V. Ramakrishnan (AIR 2018 SC 3876) — SC held that Section 14 moratorium does not extend to personal guarantors."

## WIN-RATE CONTRIBUTION
favor: BANK
counted_in_ground: PENDING_SA_CONCEALED
