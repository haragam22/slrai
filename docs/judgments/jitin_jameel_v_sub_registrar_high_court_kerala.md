---
citation: "2025:KER:34188"
title: "Jithin Jameel vs Sub Registrar on 19 May, 2025"
short_name: "Jithin Jameel"
court: HIGH_COURT
high_court_state: "Kerala"
bench_strength: 1
judgment_date: "2025-05-19"
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
keywords: ["Section 89(4)", "filing in Book No.1", "no stamp duty", "sale certificate", "not compulsorily registrable", "Section 17(2)(xii)", "Kerala Stamp Act", "Sub-Registrar", "copy of sale certificate", "statutory finality"]
retrieval_condition: "Applies when the Sub-Registrar refuses to file a copy of the SARFAESI auction sale certificate in Book No.1 under Section 89(4) of the Registration Act, 1908, citing stamp duty requirements."
source: IK_SUMMARY
ik_doc_id: "72307797"
ik_url: "https://indiankanoon.org/doc/72307797/"
has_verified_conditions: true
chunk_type: null
applicable_conditions: []
exclusion_conditions: []
---

## BORROWER'S CLAIM

The borrowers (auction purchasers) alleged that the respective Sub-Registrars wrongfully refused to file copies of their sale certificates in Book No.1 as mandated under Section 89(4) of the Registration Act, 1908, by insisting on payment of stamp duty under the Kerala Stamp Act, 1959. They contended that a sale certificate issued under SARFAESI is not a compulsorily registrable instrument under Section 17(1) of the Registration Act and is specifically exempted under Section 17(2)(xii). They further argued that the act of filing a copy in Book No.1 under Section 89(4) is a ministerial act of record-keeping and does not constitute registration that attracts stamp duty. The prayer was for a direction to the Sub-Registrars to file the sale certificates without insisting on stamp duty.

## HOLDING SUMMARY

Section 89(4) of the Registration Act, 1908 mandates that a copy of a sale certificate issued by a Civil or Revenue Officer (including a SARFAESI Authorised Officer) to an auction purchaser must be filed in Book No.1 by the Sub-Registrar. This filing is a ministerial act of record-keeping and does not constitute registration under Section 17(1) of the Act. Consequently, it does not attract stamp duty under the Kerala Stamp Act, 1959. A sale certificate issued under SARFAESI is not a conveyance and is specifically exempted from compulsory registration under Section 17(2)(xii) of the Registration Act. The mere act of filing a copy under Section 89(4) does not create or extinguish title and therefore cannot be subjected to stamp duty. The Sub-Registrar has no discretion to refuse filing based on stamp duty grounds. This applies when: the Sub-Registrar refuses to file a copy of a SARFAESI sale certificate in Book No.1, citing non-payment of stamp duty.

## KEY FACTS OF THIS CASE

This is a batch of writ petitions filed by successful auction purchasers who had acquired immovable properties through SARFAESI enforcement actions conducted by banks and financial institutions. The auction purchasers obtained valid sale certificates from the Authorised Officers of the respective banks. When they or the banks forwarded copies of these certificates to the concerned Sub-Registrars for filing in Book No.1 as per Section 89(4) of the Registration Act, the Sub-Registrars refused, demanding payment of stamp duty under the Kerala Stamp Act, 1959. The petitioners challenged this refusal, relying on precedents from the Supreme Court and other High Courts. The lower authorities had not entertained the filing, prompting the writ petitions before the Kerala High Court.

## WHAT THE COURT DECIDED

The Kerala High Court allowed the writ petitions and directed the respective Sub-Registrars to file the copies of the sale certificates in Book No.1 as required under Section 89(4) of the Registration Act, 1908, without insisting on the payment of any stamp duty. The court declared that the filing of a copy of a SARFAESI sale certificate under Section 89(4) does not attract stamp duty. The court also permitted the petitioners to approach the banks for revalidation of the sale certificates if required, and the Sub-Registrars were directed to file the revalidated copies within one month of receipt.

## KEY QUOTE

the mere act of filing a copy of the sale certificate in Book No. 1, as mandated under Section 89(4) of the Registration Act, does not attract stamp duty.

## CONDITION: WHEN THIS JUDGMENT APPLIES

This judgment applies when:
1. `sale_certificate_issued` is TRUE — a sale certificate has been issued to the auction purchaser under SARFAESI
2. `auction_notice_discloses_pending_sa` is FALSE — the auction has concluded and the sale is confirmed
3. `challenges_auction` is FALSE — the challenge is not to the auction itself but to the post-auction filing
4. `prayer_scope_covers_current_measure` is TRUE — the relief sought includes the filing of the sale certificate
5. `sub_registrar_refuses_filing` is TRUE — the Sub-Registrar has refused to file the copy of the sale certificate in Book No.1
6. `refusal_reason` contains "stamp duty" — the refusal is based on the demand for stamp duty under the Kerala Stamp Act or similar state legislation

## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY

1. When the auction purchaser is seeking registration of the original sale certificate as a conveyance — in that case, stamp duty would be applicable under the relevant Stamp Act, and this judgment does not apply.
   SLRAI ROUTING: if `registration_of_original_certificate_sought` = TRUE → standard stamp duty rules apply.

2. When the sale certificate itself is challenged for non-compliance with SARFAESI procedures (e.g., Rule 9(4) delay, no reply to 13(3A)) — this judgment only applies to the post-sale filing issue, not the validity of the sale.
   SLRAI ROUTING: if `challenges_auction` = TRUE → apply SARFAESI-specific precedents like E. Muthurathinasabathy or Celir LLP.

3. When the refusal by the Sub-Registrar is based on grounds other than stamp duty (e.g., defective certificate, lack of jurisdiction) — this judgment only addresses the stamp duty objection.

## STATUTORY CONTEXT

Primary law: Registration Act, 1908
Primary provision: Section 89(4) — "Every Revenue Officer granting a certificate of sale to the purchaser of immovable property sold by public auction shall send a copy of the certificate to the Registering Officer within the local limits of whose jurisdiction the whole or any part of the immovable property comprised in the certificate is situate, and such officer shall file the copy in his Book No. 1."
Instrument level: OTHER (Registration Act)
Nature of provision: MANDATORY — the Sub-Registrar "shall file" the copy, leaving no discretion.

Secondary: Section 17(2)(xii) Registration Act, 1908 — "any certificate of sale granted to the purchaser of any property sold by public auction by a Civil or Revenue Officer" is exempt from compulsory registration.
Nature: MANDATORY exemption.

Tertiary: Kerala Stamp Act, 1959, Entry 16 — treats "certificate of sale" as chargeable with duty. The court held this is overridden by the specific mandate of the Registration Act in this context.

## RELATIONSHIP TO OTHER JUDGMENTS

Follows: Shanti Devi L. Singh v. Tax Recovery Officer (1990) 3 SCC 605
  Held that filing under Section 89(4) is not registration attracting stamp duty and the term "Revenue Officer" includes TROs.

Follows: Esjaypee Impex Pvt. Ltd. v. Canara Bank (2021) 11 SCC 537
  Affirmed that Section 17(2)(xii) and Section 89(4) mandate only filing of a copy, not registration, and this does not attract stamp duty.

Follows: G. Madhurambal v. Inspector General of Registration (2022 LiveLaw (SC) 969)
  Supreme Court dismissed SLPs challenging Madras HC's view that SARFAESI sale certificates need only be filed under Section 89(4) without stamp duty.

Follows: State of Punjab v. Ferrous Alloy Forgings (P) Ltd. (2024 SCC OnLine SC 3372)
  Supreme Court explicitly held that a SARFAESI sale certificate is not compulsorily registrable and mere filing under Section 89(4) is sufficient and does not attract stamp duty.

Distinguishes: Sub-Registrar v. Nadirshah (2009 (1) KLT 630)
  A previous Kerala HC decision that upheld stamp duty demand. This judgment overrules its applicability in light of subsequent binding Supreme Court decisions.

## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES

**A. New CaseFactSchema Fields Needed:**
Field name: sub_registrar_refuses_filing
Type: FactEntry[bool]
Description: True if the Sub-Registrar has refused to file the copy of the sale certificate in Book No.1
Module: M10

Field name: refusal_reason
Type: FactEntry[str]
Description: The stated reason for the Sub-Registrar's refusal (e.g., "stamp duty", "defective certificate")
Module: M10

Field name: registration_of_original_certificate_sought
Type: FactEntry[bool]
Description: True if the applicant is seeking registration of the original sale certificate as a conveyance
Module: M10

**B. New YAML Rules Needed:**
Module: M10
Rule ID: M10_C8_section89_filing_no_stamp_duty
Conditions: sale_certificate_issued=True AND sub_registrar_refuses_filing=True AND refusal_reason="stamp duty"
Severity: FATAL
Message: "Sub-Registrar cannot refuse to file a copy of the SARFAESI sale certificate in Book No.1 under Section 89(4) of the Registration Act, 1908, on grounds of stamp duty. Such filing is mandatory and does not attract stamp duty."
Judgment tags: ["JITHIN_JAMEEL", "ESJAYPEE_IMPEX", "FERROUS_ALLOY"]
Statutory basis: OTHER

**C. Existing Judgments to Update:**
File: nadirshah_kerala_sub_registrar.md
Section: ## RELATIONSHIP TO OTHER JUDGMENTS
Add: "Distinguished by: Jithin Jameel (2025:KER:34188) — held that refusal to file under Section 89(4) on stamp duty grounds is impermissible in light of subsequent Supreme Court decisions in Esjaypee Impex, G. Madhurambal, and Ferrous Alloy Forgings."

## WIN-RATE CONTRIBUTION
favor: BORROWER
counted_in_ground: AUCTION_PURCHASER
