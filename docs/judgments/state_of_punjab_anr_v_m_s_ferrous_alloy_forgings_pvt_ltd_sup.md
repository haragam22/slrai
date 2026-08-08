---
citation: "2024 INSC 890"
title: "The State of Punjab vs M/S Ferrous Alloy Forgings P Ltd"
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
ground_codes: ["AUCTION_PURCHASER"]
statutory_basis: OTHER
act_sections: []
rules_sections: []
slrai_modules: ["M10"]
keywords: ["sale certificate", "stamp duty on sale certificate", "Section 89(4) Registration Act", "Order XXI Rule 94 CPC", "certificate of sale", "non-Registrable document", "evidence of title", "no stamp duty"]
retrieval_condition: "Applies when the auction purchaser challenges the requirement to pay stamp duty on a sale certificate issued by a court or authorized officer."
source: SC_FULL_TEXT
ik_doc_id: "191767744"
ik_url: "https://indiankanoon.org/doc/191767744/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrower (M/s Ferrous Alloy Forgings P Ltd) challenged the requirement imposed by the Registrar to pay stamp duty on the sale certificate issued in its favour as the successful auction purchaser in a court-confirmed winding-up sale. It contended that a sale certificate issued under Order XXI Rule 94 of the CPC is not a conveyance and does not transfer title, and therefore cannot attract stamp duty. The borrower further argued that Section 17(2)(xii) of the Registration Act, 1908, explicitly excludes such certificates from compulsory registration, and thus, no stamp duty can be levied merely for issuance of the certificate. The prayer was to direct the issuance of the original sale certificate and refund of the stamp duty already deposited.

## HOLDING SUMMARY

A sale certificate issued to an auction purchaser under Order XXI Rule 94 of the CPC is not an instrument of conveyance and does not transfer title; it is merely formal evidence of a title that already vested upon confirmation of sale under Rule 92. Since such a certificate is not compulsorily registrable under Section 17(2)(xii) of the Registration Act, 1908, it cannot attract stamp duty at the time of issuance. The obligation to pay stamp duty arises only if the purchaser chooses to present the certificate for registration or use it for another purpose that triggers liability under the Stamp Act. The issuance of the sale certificate and forwarding of a copy to the Sub-Registrar under Section 89(4) of the Registration Act is a ministerial act and does not depend on payment of stamp duty. This applies when: the borrower is a court-auction purchaser challenging stamp duty liability on the sale certificate itself.

## KEY FACTS OF THIS CASE

M/s Ferrous Alloy Forgings Pvt. Ltd., a sister concern of the respondent, emerged as the highest bidder in a court-ordered auction of assets of M/s Punjab United Forge Limited, which was being wound up under the Companies Act, 1956. The sale was confirmed by the High Court. The purchaser applied for a sale certificate under Order XXI Rule 94 of the CPC. The Company Judge directed payment of stamp duty on immovable properties valued at Rs. 2.25 crore. The purchaser challenged this before the High Court, which ruled in its favour. The State of Punjab appealed to the Supreme Court, arguing that stamp duty was mandatory. The core dispute was whether stamp duty could be levied on the sale certificate itself.

## WHAT THE COURT DECIDED

The Supreme Court dismissed the appeal, affirming the High Court’s order. It held that no stamp duty is payable on the issuance of a sale certificate under a court auction. The original sale certificate was to be handed over to the purchaser, and a copy sent to the Sub-Registrar under Section 89(4) of the Registration Act. The stamp duty previously deposited by the purchaser was to be refunded. The Court clarified that stamp duty liability, if any, arises only upon subsequent use of the certificate, not at the time of issuance.

## KEY QUOTE

A sale certificate is merely the evidence of such title. It is well settled that when an auction-purchaser derives title on confirmation of sale in his favour, and a sale certificate is issued evidencing such sale and title, no further deed of transfer from the court is contemplated or required.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `sa_applicant_type` is "AUCTION_PURCHASER" — the applicant is the successful bidder in a court-confirmed auction
2. `challenges_auction` is TRUE — the challenge pertains to the auction process or its aftermath
3. `prayer_scope_covers_current_measure` is TRUE — the prayer includes issuance of sale certificate or refund of stamp duty
4. `sale_certificate_issued` is TRUE — a sale certificate has been or is to be issued under court process
5. `challenges_demand_notice` is FALSE — the challenge is not against a SARFAESI demand notice
6. `ibc_moratorium_active` is FALSE — the case does not fall under IBC moratorium

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the instrument in question is a registered sale deed and not a sale certificate — in that case, standard stamp duty rules under the relevant State Stamp Act apply.
2. When the auction is conducted under SARFAESI Act, 2002 by a bank/AO and not under court supervision — this judgment applies only to court-confirmed sales under CPC/Companies Act; SARFAESI sales are governed by different principles (e.g., Celir LLP).
3. When the purchaser seeks to register the sale certificate — in such case, Article 18 or 23 of the Stamp Act may apply depending on jurisdiction.

## STATUTORY CONTEXT

Primary law: Indian Registration Act, 1908  
Primary provision: Section 17(2)(xii) — "A certificate of sale granted to any purchaser of any property sold by a public auction by a civil or revenue officer."  
Instrument level: OTHER  
Nature of provision: DIRECTORY — interpreted as excluding such certificates from compulsory registration.

Secondary law: Stamp Act, Articles 18 and 23  
Article 18: Applies to "Conveyance" including sale of immovable property.  
Article 23: Applies to "Certificate of sale in execution of a decree."  
Court held: A sale certificate under court auction is not a conveyance per se; stamp duty arises only upon presentation for registration, not at issuance.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Municipal Corporation of Delhi v. Pramod Kumar Gupta (AIR 1991 SC 401)  
  Held that title passes upon confirmation of sale under CPC Rule 92; the sale certificate under Rule 94 is a formal declaration, not a title-creating instrument.

Follows: B. Arvind Kumar v. Govt. of India (2007) 5 SCC 745  
  Reaffirmed that a sale certificate is merely evidence of title, not a conveyance, and does not require registration.

Follows: M/s Esjaypee Impex Pvt. Ltd. v. Canara Bank (2021) 11 SCC 537  
  Confirmed that Section 89(4) of the Registration Act mandates forwarding of sale certificate copy to Sub-Registrar, which suffices for filing in Book I.

Distinguishes: Celir LLP v. Bafna Motors (2024) 2 SCC 1  
  Celir LLP governs SARFAESI auctions and finality of sale upon timely payment. This case applies only to court-supervised auctions under CPC/Companies Act.  
  SLRAI ROUTING: if `auction_type` = "COURT_AUCTION" → Ferrous Alloy Forgings applies; if `auction_type` = "SARFAESI_AUCTION" → Celir LLP applies.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Field Needed:**
Field name: auction_type
Type: FactEntry[str]
Description: Distinguishes between "SARFAESI_AUCTION", "COURT_AUCTION", "IBC_AUCTION"
Module: M10
Extraction: Determined from the enforcing authority and legal basis (e.g., SARFAESI Act, CPC, IBC)

**B. New YAML Rule Needed:**
Module: M10
Rule ID: M10_C8_stamp_duty_on_sale_cert
Conditions: auction_type="COURT_AUCTION" AND challenges_auction=True AND sale_certificate_issued=True
Severity: INFO
Message: "Sale certificate in court auctions is not a conveyance and does not attract stamp duty at issuance. Liability, if any, arises only upon registration or use."
Judgment tag: ["Ferrous_Alloy_Forgings"]
Statutory basis: OTHER

**C. No New Requirements**
No new ground codes or major schema changes required. The distinction is adequately captured by `auction_type`.

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: AUCTION_PURCHASER
