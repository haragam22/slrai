---
citation: "2024 INSC 890"
title: "The State Of Punjab vs M/S Ferrous Alloy Forgings P Ltd"
short_name: "Ferrous Alloy Forgings"
court: SUPREME_COURT
high_court_state: null
bench_strength: 2
judgment_date: "2024-11-19"
overruled: false
overruled_by: null
distinguished_by: []
favor: BORROWER
favor_verified: true
ground_codes: ["AUCTION_PURCHASER", "UNKNOWN"]
statutory_basis: OTHER
act_sections: []
rules_sections: []
slrai_modules: ["M10"]
keywords: ["sale certificate", "stamp duty on sale certificate", "Section 17(2)(xii)", "Order XXI Rule 94 CPC", "Section 89(4) Registration Act", "no stamp duty", "evidence of title", "not a conveyance", "finality of auction sale"]
retrieval_condition: "Applies when the auction purchaser is being asked to pay stamp duty on the sale certificate issued by the court or authorized officer."
source: SC_FULL_TEXT
ik_doc_id: "191767744"
ik_url: "https://indiankanoon.org/doc/191767744/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower (M/s Ferrous Alloy Forgings P Ltd) contended that the Registrar of the High Court erred in directing it to pay stamp duty on the sale certificate issued in its favour following a court-confirmed auction sale. It argued that a sale certificate is not a conveyance and does not transfer title, but merely serves as evidence of a completed sale, and therefore cannot attract stamp duty under the Stamp Act. The borrower further relied on Section 17(2)(xii) of the Registration Act, which excludes sale certificates from compulsory registration, to assert that such documents are not instruments of transfer. The prayer was to direct the issuance of the original sale certificate without payment of stamp duty and to refund the stamp duty already deposited.

## HOLDING SUMMARY

A sale certificate issued to an auction purchaser upon confirmation of a court-supervised sale does not transfer title and is merely formal evidence of the already completed transfer of ownership. The vesting of title occurs upon confirmation of the sale under Order XXI Rule 92 of the CPC, not upon issuance of the certificate under Rule 94. Consequently, the sale certificate is not a conveyance and does not attract stamp duty under the Stamp Act. While Articles 18 and 23 of the First Schedule to the Stamp Act may impose duty if the certificate is presented for registration, the mere issuance of the certificate by the court or authorized officer does not trigger such liability. Section 17(2)(xii) of the Registration Act explicitly excludes sale certificates from compulsory registration, reinforcing their non-transfer nature. Section 89(4) of the Registration Act mandates only the forwarding of a copy to the Sub-Registrar for filing in Book I, which suffices for public record. This applies when: the auction purchaser is being required to pay stamp duty on a sale certificate issued by a court or authorized officer in confirmation of a completed auction sale.

## KEY FACTS OF THIS CASE

M/s Punjab United Forge Limited was wound up under the Companies Act, 1956, and its secured assets were auctioned by IFCI with court permission. M/s Ferrous Alloy Forgings Pvt. Ltd., a sister concern of the respondent, emerged as the highest bidder. The sale was confirmed by the official liquidator and later by the High Court. The respondent applied for a sale certificate under Order XXI Rule 94 of the CPC, but the Registrar directed it to pay stamp duty on the immovable property valuation of Rs. 2.25 crore. The respondent challenged this before the High Court, which ruled in its favour, directing issuance of the certificate and refund of stamp duty. The State of Punjab appealed to the Supreme Court, arguing that stamp duty was mandatory.

## WHAT THE COURT DECIDED

The Supreme Court dismissed the appeal, affirming the High Court’s order. It held that no stamp duty is payable on a sale certificate issued by a court or authorized officer confirming an auction sale. The original sale certificate was to be handed over to the respondent, and a copy was to be sent to the Sub-Registrar under Section 89(4) of the Registration Act. The stamp duty already deposited by the respondent was to be refunded within one month.

## KEY QUOTE

A sale certificate is merely the evidence of such title. It is well settled that when an auction-purchaser derives title on confirmation of sale in his favour, and a sale certificate is issued evidencing such sale and title, no further deed of transfer from the court is contemplated or required.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when: the auction purchaser is being required to pay stamp duty on a sale certificate issued by a court or authorized officer in confirmation of a completed auction sale.

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the document in question is a registered sale deed or conveyance executed by the secured creditor — in that case, standard stamp duty rules apply under the Stamp Act.
   SLRAI ROUTING: if `sale_deed_executed` = TRUE → standard stamp duty rules apply; if `sale_certificate_issued` = TRUE and no deed executed → this judgment applies.

2. When the sale certificate is being used as a substitute for a conveyance in private transactions — this judgment protects only court-confirmed or SARFAESI-compliant auction sales.
   SLRAI ROUTING: if `auction_type` = "PRIVATE_SALE" → this judgment does not apply.

3. When the challenge is to the validity of the auction itself on grounds like service defect or amount dispute — this judgment addresses only the stamp duty aspect of the sale certificate.
   SLRAI ROUTING: if `ground_codes` includes "SERVICE_DEFECT" or "AMOUNT_DISPUTE" → other precedents apply.

## STATUTORY CONTEXT

Primary law: Indian Registration Act, 1908  
Primary provision: Section 17(2)(xii) — "A certificate of sale granted to any purchaser of any property sold by public auction by a Civil or Revenue Officer."  
Instrument level: OTHER  
Nature: MANDATORY — the exclusion from compulsory registration is absolute.

Secondary law: Code of Civil Procedure, 1908  
Provision: Order XXI Rule 94 — "The Court may, on the application of the purchaser, issue to him a certificate of sale."  
Nature: DIRECTORY — but the issuance is a mandatory consequence of confirmed sale.

Tertiary law: Stamp Act  
Articles 18 & 23 — impose duty on instruments of conveyance and sale; court held these do not apply to sale certificates as they are not conveyances.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Municipal Corporation of Delhi v. Pramod Kumar Gupta (AIR 1991 SC 401)  
  Held that title passes upon confirmation of sale under Order XXI Rule 92 CPC, and the sale certificate under Rule 94 is merely a formal declaration.

Follows: B. Arvind Kumar v. Govt. Of India (2007) 5 SCC 745  
  Confirmed that a sale certificate issued by a court or authorized officer does not require registration under Section 17(1) of the Registration Act.

Follows: M/s Esjaypee Impex Private Limited v. Canara Bank (2021) 11 SCC 537  
  Reiterated that the auction purchaser is entitled to the original sale certificate and a copy must be sent to the Sub-Registrar under Section 89(4).

Follows: Inspector General of Registration v. G. Madhurambal (2022 SCC Online SC 2079)  
  Held that a certificate of sale cannot be regarded as a conveyance subject to stamp duty.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: auction_conducted_by_authorized_officer
Type: FactEntry[bool]
Description: True if the auction was conducted by a court, liquidator, or authorized officer under SARFAESI or winding-up proceedings
Module: M10
Extraction: Determined from the nature of the enforcement proceeding (SARFAESI, IBC, winding-up, etc.)

**B. New YAML Rule Needed:**
Module: M10
Rule ID: M10_C8_no_stamp_duty_on_sale_certificate
Conditions: sale_certificate_issued=True AND sa_applicant_type="AUCTION_PURCHASER"
Severity: INFO
Message: "No stamp duty is payable on a sale certificate issued by a court or authorized officer. The certificate is merely evidence of title and not a conveyance. Any demand for stamp duty on such certificate is legally unsustainable."
Judgment tag: ["Ferrous_Alloy_Forgings"]
Statutory basis: OTHER

**C. New Ground Codes Needed:**
Suggested code: STAMP_DUTY_ON_CERTIFICATE
Description: Challenge to demand of stamp duty on sale certificate issued post-auction
Module: M10

**D. Existing Judgments to Update:**
File: esjaypee_impex_canara_bank.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Reinforced by: Ferrous Alloy Forgings (2024 INSC 890) — clarified that no stamp duty is payable on sale certificate issued under Section 89(4), which is merely evidence of title."

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: AUCTION_PURCHASER
