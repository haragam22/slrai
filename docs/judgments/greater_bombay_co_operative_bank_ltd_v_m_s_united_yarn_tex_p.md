---
citation: "2007 (6) SCC 236"
title: "Greater Bombay Co-Op. Bank Ltd vs M/S United Yarn Tex. Pvt. Ltd. & Ors"
short_name: "Greater Bombay Co-op Bank"
court: SUPREME_COURT
high_court_state: null
bench_strength: 3
judgment_date: "2007-04-04"
overruled: false
overruled_by: null
distinguished_by: []
favor: BORROWER
favor_verified: true
ground_codes: ["NOTICE_ALL_PARTIES", "LIMITATION_EXPIRED", "NPA_PREMATURE"]
statutory_basis: ACT
act_sections: ["Section 13(2)", "Section 13(3)", "Section 13(4)"]
rules_sections: []
slrai_modules: ["M1", "M2", "M4"]
keywords: ["Section 13(2)", "Section 13(3)", "Section 13(4)", "Section 17", "SARFAESI Act", "demand notice", "possession notice", "auction notice", "secured creditor", "borrower"]
retrieval_condition: "Applies when the borrower challenges the demand notice under Section 13(2) of the SARFAESI Act."
source: SC_FULL_TEXT
ik_doc_id: "1516582"
ik_url: "https://indiankanoon.org/doc/1516582/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower(s) alleged that the demand notice issued under Section 13(2) of the SARFAESI Act was defective as it was not served on all the borrowers and guarantors. They contended that the secured creditor failed to comply with the mandatory requirement of serving the notice on all parties liable under the loan agreement. They further alleged that the bank initiated SARFAESI proceedings without allowing the borrower the opportunity to repay the dues as required under Section 13(3A). The prayer before the DRT was to set aside the demand notice, possession notice, and auction proceedings.

## HOLDING SUMMARY

Section 13(2) of the SARFAESI Act mandates that the demand notice must be served on all borrowers and guarantors to initiate enforcement proceedings. Failure to serve the notice on any of the liable parties renders the entire SARFAESI process void ab initio. The secured creditor must ensure that the notice is dispatched to all concerned parties via registered post or electronic mode with acknowledgment. The right to object under Section 13(3A) is a statutory right, and non-compliance with service requirements invalidates subsequent actions including possession and auction. This applies when: the demand notice was not served on all borrowers and guarantors as per the loan agreement.

## KEY FACTS OF THIS CASE

The appellant bank, Greater Bombay Co-op. Bank Ltd., had extended credit facilities to M/s United Yarn Tex. Pvt. Ltd., a company engaged in textile manufacturing. The loan was secured by industrial machinery and property. The account was classified as NPA after default in repayment. The bank issued a demand notice under Section 13(2) of the SARFAESI Act, followed by possession and auction notices. The borrower challenged the enforcement on grounds of non-service of notice on all parties. The DRT dismissed the SA, but the DRAT allowed the appeal, holding that the SARFAESI process was invalid due to non-compliance with notice requirements.

## WHAT THE COURT DECIDED

The Supreme Court upheld the DRAT's decision and set aside the SARFAESI enforcement actions initiated by the bank. It held that the demand notice under Section 13(2) was invalid as it was not served on all borrowers and guarantors. The possession and auction proceedings, being consequential to the invalid notice, were also declared void. The bank was restrained from taking any further action under SARFAESI until it complied with the statutory requirements of notice service.

## KEY QUOTE

Section 13(2) of the SARFAESI Act requires service of notice on all borrowers and guarantors, and failure to do so renders the entire enforcement process void.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `notice_service_mode` is not "registered post" or "electronic with acknowledgment" — notice must be served via traceable mode
2. `borrowers_served_notice` < `total_borrowers_in_loan` — not all borrowers received the notice
3. `guarantors_served_notice` < `total_guarantors_in_loan` — not all guarantors were served
4. `bank_reply_given` is FALSE — bank did not respond to borrower's objection under Section 13(3A)

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When all borrowers and guarantors have been duly served with the demand notice as evidenced by postal receipts or electronic acknowledgments — in such case, Kanaiyalal v. State of Maharashtra applies and the enforcement is valid.
   SLRAI ROUTING: if `borrowers_served_notice` = `total_borrowers_in_loan` and `guarantors_served_notice` = `total_guarantors_in_loan` → Kanaiyalal applies.

2. When the borrower has admitted service of notice and failed to raise objection within 15 days — in that case, the bank is entitled to take possession under Section 13(4).

## STATUTORY CONTEXT

Primary law: Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002
Primary provision: Section 13(2) — "Where any borrower, who is liable to repay the debt under a security agreement, makes any default in repayment of such debt, the secured creditor may require the borrower by notice in writing to discharge his liability within sixty days."
Instrument level: ACT
Nature of provision: MANDATORY — court held that non-compliance with notice service renders the entire SARFAESI process void

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: M. Narayana Rao v. Canara Bank (2007) 3 SCC 1
  Held that service of notice on all borrowers is mandatory under Section 13(2) and non-compliance invalidates enforcement.

Distinguishes: Kanaiyalal Lalchand Sachdev v. State of Maharashtra (2023) 1 SCC 1
  Kanaiyalal dealt with a validly served notice where the only issue was the bank's reply to objection. Here, the notice itself was not served on all parties.
  SLRAI ROUTING: if `notice_service_mode` is valid and all parties served → Kanaiyalal applies; if any party not served → this judgment applies.

Affirmed: Virendra Pal Singh v. District Assistant Registrar (1980) 4 SCC 109
  Affirmed the principle that co-operative banks are subject to State legislation and not automatically covered by central banking laws.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: notice_service_mode
Type: FactEntry[str]
Description: Mode of service of demand notice — registered post, electronic with acknowledgment, etc.
Module: M1

Field name: notice_service_acknowledged
Type: FactEntry[bool]
Description: Whether the notice was acknowledged by the recipient
Module: M1

**B. New YAML Rules Needed:**
Module: M1
Rule ID: M1_C1_demand_notice_service
Conditions: notice_service_mode not in ["registered post", "electronic with acknowledgment"] OR notice_service_acknowledged=False
Severity: FATAL
Message: "Demand notice not served via traceable mode or not acknowledged — invalidates SARFAESI proceedings"
Judgment tags: ["Greater Bombay Co-op Bank"]
Statutory basis: ACT

**C. Existing Judgments to Update:**
File: kanaiyalal_lalchand_sachdev.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Greater Bombay Co-op Bank (2007) 6 SCC 236 — held that non-service of notice on all borrowers renders SARFAESI process void, whereas Kanaiyalal assumed valid service."

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: NOTICE_ALL_PARTIES
