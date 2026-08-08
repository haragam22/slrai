# Compliance Engine — Full Rule Review


## M1_DEMAND_NOTICE

### M1_C1 — 60 days must elapse between demand notice and enforcement action
- statutory_basis: `Section 13(2) SARFAESI Act 2002`
- preconditions: [{'field': 'demand_notice_date', 'operator': 'is_not_null'}]
- **M1_C1_a**
  - expression: `sixty_day_period_elapsed == False`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Enforcement action taken before 60-day period elapsed from demand notice dated {demand_notice_date}.
- pass_message: 60-day period from demand notice ({demand_notice_date}) satisfied.

### M1_C2 — Amount in demand notice must match account records within 5% tolerance
- preconditions: [{'field': 'demand_notice_amount', 'operator': 'is_not_null'}, {'field': 'actual_outstanding_amount', 'operator': 'is_not_null'}]
- **M1_C2_a**
  - expression: `abs(demand_notice_amount - actual_outstanding_amount) / actual_outstanding_amount * 100 > 5`
  - result_if_true: `FAIL`  severity: `CURABLE`  outcome_favors: **BORROWER**
  - message: Demand notice amount ({demand_notice_amount}) differs from records ({actual_outstanding_amount}) by more than 5%.

### M1_C3 — Service mode must be valid under SARFAESI Rules
- **M1_C3_a**
  - expression: `notice_service_mode not in ['registered_post_ad','personal_service','substituted_service','email_if_agreed']`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Notice service mode '{notice_service_mode}' is not a valid mode under SARFAESI Rules.

### M1_C4 — Proof of service must be present in bank file
- **M1_C4_a**
  - expression: `notice_dispatch_proof_present == False`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: No proof of service (POD/acknowledgment/affidavit) found. Cannot verify notice was served.

### M1_C5 — Service date must not predate notice issue date — catches data entry errors
- statutory_basis: `Section 13(2) SARFAESI Act 2002 — 60-day period runs from service, not issue`
- preconditions: [{'field': 'demand_notice_date', 'operator': 'is_not_null'}, {'field': 'notice_service_date', 'operator': 'is_not_null'}]
- **M1_C5_a**
  - expression: `notice_service_date < demand_notice_date`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Service date ({notice_service_date}) recorded before notice issue date ({demand_notice_date}). Data entry error — 60-day period computation will be wrong.
- pass_message: Service date ({notice_service_date}) on or after notice issue date ({demand_notice_date}). Correct date used for 60-day computation.

### M1_C6 — Demand notice must state: (1) outstanding amount, (2) secured asset details, (3) 60-day demand, (4) consequences of non-payment
- statutory_basis: `Section 13(2) SARFAESI Act 2002 — prescribed content of demand notice`
- preconditions: [{'field': 'demand_notice_date', 'operator': 'is_not_null'}]
- **M1_C6_a**
  - expression: `notice_content_complete == False`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Demand notice does not appear to contain all 4 prescribed content elements required under Section 13(2). Notice may be defective on format. Ground: NOTICE_FORMAT_DEFECT.
- pass_message: Demand notice content confirmed complete — all prescribed elements present.

### M1_C7 — Possession notice must not be issued before 60 days from service date
- statutory_basis: `Section 13(2) SARFAESI Act 2002 — 60-day moratorium before Section 13(4)`
- preconditions: [{'field': 'notice_service_date', 'operator': 'is_not_null'}, {'field': 'possession_notice_date', 'operator': 'is_not_null'}]
- **M1_C7_a**
  - expression: `(possession_notice_date - notice_service_date).days < 60`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Possession notice dated {possession_notice_date} issued before 60-day moratorium expired from service on {notice_service_date}. Premature enforcement under Section 13(4) is a fatal defect.
- pass_message: Possession notice issued after 60-day moratorium from service date ({notice_service_date}).

### M1_C8 — AO must have written authorization from principal officer
- statutory_basis: `Authorized Officer Authorization`
- preconditions: [{'field': 'authorized_officer_name', 'operator': 'is_not_null'}]
- **M1_C8_a**
  - expression: `ao_has_written_authorization == False`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Authorized Officer {authorized_officer_name} ({authorized_officer_designation}) lacks written authorization from the principal officer. Enforcement action is void.
- pass_message: Authorized Officer {authorized_officer_name} has verified written authorization.


## M2_REPLY_COMPLIANCE

### M2_C1 — Bank must reply to objection — reply not given
- statutory_basis: `Section 13(3A) SARFAESI Act 2002`
- preconditions: [{'field': 'objection_filed', 'operator': 'eq', 'value': True}]
- **M2_C1_a**
  - expression: `bank_reply_given == False`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Borrower filed objection on {objection_date}. Bank has not replied. Fatal under Kanaiyalal (2011) 2 SCC 782.
- pass_message: Bank replied on {bank_reply_date}.

### M2_C2 — Bank reply must be within 15 days
- preconditions: [{'field': 'objection_filed', 'operator': 'eq', 'value': True}, {'field': 'bank_reply_given', 'operator': 'eq', 'value': True}]
- **M2_C2_a**
  - expression: `reply_days_elapsed > 15`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Bank replied {reply_days_elapsed} days after objection. Exceeds 15-day limit.

### M2_C3 — Bank reply must give reasons for rejecting the objection
- statutory_basis: `Reasoned Reply Requirement`
- preconditions: [{'field': 'bank_reply_given', 'operator': 'eq', 'value': True}]
- **M2_C3_a**
  - expression: `bank_reply_gives_reasons == False`
  - result_if_true: `FAIL`  severity: `CURABLE`  outcome_favors: **BORROWER**
  - message: Bank reply is not reasoned. DRT may set aside notice or require proper reply depending on forum.
- pass_message: Bank provided a reasoned reply.


## M3_AUCTION_GAP

### M3_C1 — 30-day gap required between sale notice and auction (immovable)
- statutory_basis: `Rule 8(6) Security Interest (Enforcement) Rules 2002`
- preconditions: [{'field': 'asset_type', 'operator': 'eq', 'value': 'immovable'}]
- **M3_C1_a**
  - expression: `auction_gap_days < 30`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Auction held {auction_gap_days} days after sale notice. Minimum required: 30 days.

### M3_C2 — Newspaper publication of sale notice required
- **M3_C2_a**
  - expression: `newspaper_publication_done == False`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Newspaper publication of sale notice not confirmed in bank records.

### M3_C3 — Sale notice must state the reserve price — which must be set from an approved valuer's report
- statutory_basis: `Rule 8(5) and 8(6) Security Interest (Enforcement) Rules 2002`
- preconditions: [{'field': 'sale_notice_date', 'operator': 'is_not_null'}]
- **M3_C3_a**
  - expression: `reserve_price == None`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Sale notice does not state a reserve price. Rule 8(5) requires the authorised officer to fix reserve price from an approved valuer's report before issuing the sale notice. Auction is procedurally defective.
- pass_message: Reserve price ({reserve_price}) stated in sale notice as required by Rule 8(5).

### M3_C4 — Sale notice must not be issued before possession notice — bank cannot auction before taking possession
- statutory_basis: `Rule 8 Security Interest (Enforcement) Rules 2002 — possession before sale`
- preconditions: [{'field': 'possession_notice_date', 'operator': 'is_not_null'}, {'field': 'sale_notice_date', 'operator': 'is_not_null'}]
- **M3_C4_a**
  - expression: `sale_notice_date < possession_notice_date`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Sale notice dated {sale_notice_date} predates possession notice dated {possession_notice_date}. Bank cannot issue a sale notice before taking possession of the secured asset. Fatal procedural defect under Rule 8.
- pass_message: Sale notice ({sale_notice_date}) correctly issued after possession notice ({possession_notice_date}).

### M3_C6 — Auction/sale notice must be affixed at a conspicuous part of the secured property
- statutory_basis: `Rule 8(6)(7) Security Interest (Enforcement) Rules 2002`
- preconditions: [{'field': 'auction_date', 'operator': 'is_not_null'}, {'field': 'auction_notice_affixed_on_property', 'operator': 'is_not_null'}]
- **M3_C6_a**
  - expression: `auction_notice_affixed_on_property == False`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - ground_codes: ['AUCTION_NOTICE_AFFIXING']
  - message: Rule 8(6)(7) of Security Interest (Enforcement) Rules 2002 violated. The bank did not affix the auction/sale notice at a conspicuous part of the secured property before conducting the auction on {auction_date}. The Supreme Court in Mathew Varghese v. M. Amritha Kumar (2014) 5 SCC 610 held that non-compliance with mandatory affixing requirement renders the sale null and void.
- pass_message: Auction notice was affixed at the secured property prior to auction on {auction_date}, as required by Rule 8(6)(7).

### M3_C7 — Auction must not be conducted while a DRT/court interim stay is operational
- statutory_basis: `Section 17(4) SARFAESI Act 2002`
- preconditions: [{'field': 'auction_conducted_despite_stay', 'operator': 'is_not_null'}, {'field': 'stay_was_operational_on_auction_date', 'operator': 'is_not_null'}]
- **M3_C7_a**
  - expression: `auction_conducted_despite_stay == True and stay_was_operational_on_auction_date == True`
  - result_if_true: `FAIL`  severity: `ABSOLUTE_BAR`  outcome_favors: **BORROWER**
  - ground_codes: ['AUCTION_DURING_STAY']
  - message: Auction was conducted on {auction_date} in express defiance of a DRT/court interim stay order passed on {drt_stay_order_date} under Section 17(4) of the SARFAESI Act. Conducting an auction in contempt of a court order is not a procedural defect — it is a jurisdictional violation that cannot be cured. The sale certificate dated {sale_certificate_date} is prima facie void. Celir LLP v. Bafna Motors (2023) 13 SCC 561 affirms that fundamental procedural errors and fraud ground setting aside of a confirmed sale.
- pass_message: No evidence that the auction on {auction_date} was conducted during an operational stay.

### M3_C8 — Bank must disclose pending litigation known to it in the auction notice
- statutory_basis: `Rule 8(6)(7)(a) Security Interest (Enforcement) Rules 2002`
- preconditions: [{'field': 'pending_sa_existed_at_auction_date', 'operator': 'is_not_null'}, {'field': 'auction_notice_discloses_pending_sa', 'operator': 'is_not_null'}]
- **M3_C8_a**
  - expression: `pending_sa_existed_at_auction_date == True and auction_notice_discloses_pending_sa == False`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - ground_codes: ['PENDING_SA_CONCEALED', 'AUCTION_NOTICE_AFFIXING']
  - message: Securitisation Application {previous_sa_number} was pending before DRT-I on the date of auction ({auction_date}). Rule 8(6)(7)(a) requires the bank to disclose all encumbrances KNOWN to it in the auction notice, which includes pending litigation. The bank failed to disclose the pending SA and any interim orders — material concealment that vitiates the auction process.
- pass_message: Auction notice disclosed pending litigation ({previous_sa_number}) as required by Rule 8(6)(7)(a).


## M4_LIMITATION

### M4_C1 — SA must be filed within 45 days of challenged measure
- statutory_basis: `Section 17(1) SARFAESI Act 2002`
- **M4_C1_a**
  - expression: `days_from_measure_to_sa > 45`
  - result_if_true: `FAIL`  severity: `ABSOLUTE_BAR`  outcome_favors: **BANK**
  - message: SA filed {days_from_measure_to_sa} days after measure dated {measure_date}. 45-day limit exceeded. Application is time-barred.

### M4_C2 — Measure type must be identified to calculate limitation
- **M4_C2_a**
  - expression: `measure_type == None`
  - result_if_true: `UNKNOWN`  severity: `REVIEW_REQUIRED`  outcome_favors: **NEUTRAL**
  - message: The specific measure challenged by the SA cannot be determined. Review SA paragraph 1.

### M4_C3 — Where the SA challenges the auction itself, 45-day limitation runs from auction date independently of challenge to earlier measures
- statutory_basis: `Section 17(1) SARFAESI Act 2002 — each measure has independent 45-day window`
- preconditions: [{'field': 'auction_date', 'operator': 'is_not_null'}, {'field': 'sa_filing_date', 'operator': 'is_not_null'}]
- **M4_C3_a**
  - expression: `(sa_filing_date - auction_date).days > 45`
  - result_if_true: `FAIL`  severity: `ABSOLUTE_BAR`  outcome_favors: **BANK**
  - message: SA filed after auction on {auction_date}. Any challenge specifically to the auction is time-barred even if challenge to earlier measures (possession) is within time.
- pass_message: SA filed within 45 days of auction date ({auction_date}). Challenge to auction is within time.

### M4_C5 — DRT cannot set aside a measure not prayed against — auction completed but prayer does not cover it
- statutory_basis: `ACT`
- preconditions: [{'field': 'auction_date', 'operator': 'is_not_null'}, {'field': 'challenges_auction', 'operator': 'is_not_null'}]
- **M4_C5_a**
  - expression: `challenges_auction == False and challenges_demand_notice == True`
  - result_if_true: `FAIL`  severity: `ADVISORY`  outcome_favors: **BANK**
  - ground_codes: ['SECOND_SA_FRESH_CAUSE']
  - message: Prayer scope mismatch: auction already conducted on {auction_date} but SA prayer does not include SET_ASIDE_AUCTION or SET_ASIDE_SALE_CERTIFICATE. DRT cannot set aside a measure not prayed against. Applicant may need to amend prayer or file fresh SA under Oasis Dealcom principle (2016 SC).
- pass_message: Prayer scope covers the current enforcement measure ({auction_date}).


## M5_TENANCY

### M5_C1 — Lease after mortgage cannot defeat enforcement
- statutory_basis: `Section 17(1)(d) SARFAESI + Transfer of Property Act`
- preconditions: [{'field': 'tenancy_claimed', 'operator': 'eq', 'value': True}]
- **M5_C1_a**
  - expression: `lease_predates_mortgage == False`
  - result_if_true: `PASS`  severity: `ADVISORY`  outcome_favors: **BANK**
  - message: Lease ({lease_date}) is after mortgage ({mortgage_date}). Cannot defeat bank under ITC v. Blue Coast (2018) 15 SCC 99.

### M5_C2 — Lease after demand notice is expressly excluded
- preconditions: [{'field': 'tenancy_claimed', 'operator': 'eq', 'value': True}]
- **M5_C2_a**
  - expression: `lease_post_default_notice == True`
  - result_if_true: `PASS`  severity: `ADVISORY`  outcome_favors: **BANK**
  - message: Lease ({lease_date}) was created after demand notice ({demand_notice_date}). Section 17(1)(d) expressly excludes such leases.

### M5_C3 — Unregistered lease > 1 year is invalid
- preconditions: [{'field': 'tenancy_claimed', 'operator': 'eq', 'value': True}]
- **M5_C3_a**
  - expression: `lease_registered == False and lease_duration_months > 12`
  - result_if_true: `PASS`  severity: `ADVISORY`  outcome_favors: **BANK**
  - message: BANK FAVORABLE: Claimed lease of {lease_duration_months} months is unregistered. Unregistered leases > 1 year have no validity under Section 107 Transfer of Property Act.

### M5_C4 — Registered lease predating mortgage — this is the strongest tenancy defence; requires full legal review before proceeding
- statutory_basis: `Transfer of Property Act Sections 105-111 + Section 17(1) SARFAESI`
- preconditions: [{'field': 'tenancy_claimed', 'operator': 'eq', 'value': True}]
- **M5_C4_a**
  - expression: `lease_predates_mortgage == True and lease_registered == True`
  - result_if_true: `FAIL`  severity: `REVIEW_REQUIRED`  outcome_favors: **BORROWER**
  - message: BORROWER STRONG GROUND: Registered lease dated {lease_date} predates mortgage dated {mortgage_date}. This is the strongest tenancy defence available under TPA. DRT will likely scrutinise enforcement. Do not proceed without full legal review.
- pass_message: No registered pre-mortgage lease detected. Tenancy claim assessed.


## M6_VALUATION

### M6_C1 — Valuer must be RBI-empanelled and registered under Registered Valuers Act 2017
- statutory_basis: `Rule 8(6) Security Interest (Enforcement) Rules 2002`
- preconditions: [{'field': 'valuation_report_present', 'operator': 'eq', 'value': True}]
- **M6_C1_a**
  - expression: `valuer_rbi_empanelled == False or valuer_registered_under_rvact == False`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Valuer '{valuer_name}' does not appear to be RBI-empanelled or registered under RVA 2017. Valuation legally defective.

### M6_C2 — Valuation report must not be more than 6 months old at auction
- **M6_C2_a**
  - expression: `valuation_age_at_auction_days > 180`
  - result_if_true: `FAIL`  severity: `CURABLE`  outcome_favors: **BORROWER**
  - message: Valuation report ({valuation_date}) is {valuation_age_at_auction_days} days old at auction. Exceeds 180-day guideline.

### M6_C3 — Reserve price not to fall below 75% of valuation without second valuation
- **M6_C3_a**
  - expression: `reserve_price_vs_valuation_pct < 75`
  - result_if_true: `FAIL`  severity: `CURABLE`  outcome_favors: **BORROWER**
  - message: Reserve price is {reserve_price_vs_valuation_pct}% of valuation. Significantly below valuation. Borrower may allege undervaluation.

### M6_C4 — Valuation must be obtained before the sale notice is issued — reserve price derives from valuation
- statutory_basis: `Rule 8(5) Security Interest (Enforcement) Rules 2002 — reserve price set from pre-existing valuation`
- preconditions: [{'field': 'valuation_date', 'operator': 'is_not_null'}, {'field': 'sale_notice_date', 'operator': 'is_not_null'}]
- **M6_C4_a**
  - expression: `sale_notice_date <= valuation_date`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Sale notice dated {sale_notice_date} issued on or before valuation report dated {valuation_date}. Reserve price cannot be derived from a valuation that did not yet exist. Sequence of steps under Rule 8(5) violated.
- pass_message: Valuation report ({valuation_date}) correctly obtained before sale notice ({sale_notice_date}).


## M7_MULTIPARTY_NOTICE

### M7_C1 — All co-borrowers must be individually served
- statutory_basis: `Section 13(2) SARFAESI — notice to all borrowers`
- **M7_C1_a**
  - expression: `borrowers_served_notice < total_borrowers_in_loan`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Loan has {total_borrowers_in_loan} borrowers. Notice served on only {borrowers_served_notice}. Each unserved borrower is a separate fatal defect.

### M7_C2 — All guarantors/mortgagors must be individually served
- **M7_C2_a**
  - expression: `guarantors_served_notice < total_guarantors_in_loan`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Loan has {total_guarantors_in_loan} guarantors. Notice served on only {guarantors_served_notice}.


## M8_NPA_CLASSIFICATION

### M8_C1 — Account can only be NPA after 90 days of default
- statutory_basis: `RBI Master Circular on Prudential Norms — Income Recognition, Asset Classification`
- **M8_C1_a**
  - expression: `days_from_last_payment_to_npa < 90`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Account classified NPA on {npa_classification_date}, only {days_from_last_payment_to_npa} days after last payment. RBI requires 90-day window.

### M8_C2 — Cannot classify NPA when approved restructuring is active
- preconditions: [{'field': 'restructuring_proposal_pending', 'operator': 'eq', 'value': True}]
- **M8_C2_a**
  - expression: `restructuring_approval_date == None or npa_classification_date <= restructuring_approval_date`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - message: Account classified NPA while restructuring proposal was pending/active. Impermissible.

### M8_C3 — Borrower should be notified of NPA classification
- **M8_C3_a**
  - expression: `classification_notice_given == False`
  - result_if_true: `FAIL`  severity: `ADVISORY`  outcome_favors: **BORROWER**
  - message: No record of NPA classification notice to borrower. Advisory — not statutory, but some HCs have held it as fair procedure.

### M8_C4 — Interest charged post-NPA must be simple interest only — compound interest (interest on interest) is not permitted and inflates the demand notice amount
- statutory_basis: `RBI IRAC Master Circular 2025-26 — income recognition on NPA accounts`
- **M8_C4_a**
  - expression: `interest_application_correct == False`
  - result_if_true: `FAIL`  severity: `CURABLE`  outcome_favors: **BORROWER**
  - message: Interest application post-NPA classification appears incorrect. RBI IRAC norms prohibit compound interest on NPA accounts. If compound interest was charged, demand notice amount is overstated — notice may be defective on amount. Ground: AMOUNT_DISPUTE.
- pass_message: Interest application on NPA account confirmed correct (simple interest only).

### M8_C6 — Account no longer NPA at auction date — jurisdictional fact under Section 13(2) not satisfied
- statutory_basis: `RBI IRAC Master Circular Clause 4.2.5`
- preconditions: [{'field': 'account_standard_at_auction_date', 'operator': 'is_not_null'}, {'field': 'auction_date', 'operator': 'is_not_null'}]
- **M8_C6_a**
  - expression: `account_standard_at_auction_date == True`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - ground_codes: ['NPA_PREMATURE']
  - message: Payments made after NPA classification (total Rs. {payments_post_npa_total}) were sufficient to cover the overdue amount of Rs. {overdue_amount_at_auction_date} as of the auction date {auction_date}. Under RBI IRAC Master Circular clause 4.2.5, when arrears of interest and principal are paid, the account should be reclassified as Standard. A bank cannot auction a property when the loan account is no longer NPA — the jurisdictional fact under Section 13(2) (the account being NPA) is no longer satisfied at the time of the sale.
- pass_message: Account remained NPA as of the auction date ({auction_date}).


## M9_MSME

### M9_C1 — MSME status must be confirmed from bank file before M9 runs
- statutory_basis: `RBI MSME Restructuring Circular (Feb 2018 + Aug 2020)`
- preconditions: [{'field': 'msme_claimed_by_borrower', 'operator': 'eq', 'value': True}]
- **M9_C1_a**
  - expression: `udyam_cert_in_bank_file == False`
  - result_if_true: `UNKNOWN`  severity: `REVIEW_REQUIRED`  outcome_favors: **NEUTRAL**
  - message: Borrower claims MSME status. No Udyam Certificate in bank file. Human confirmation required: check original credit file.

### M9_C2 — Restructuring must have been offered to MSME before NPA classification
- preconditions: [{'field': 'udyam_cert_in_bank_file', 'operator': 'eq', 'value': True}]
- **M9_C2_a**
  - expression: `restructuring_offered_pre_npa == False`
  - result_if_true: `FAIL`  severity: `CURABLE`  outcome_favors: **BORROWER**
  - message: Borrower is MSME (Udyam: {udyam_registration_number}). Restructuring not offered before NPA classification. Applicable circular: {applicable_rbi_circular}.


## M10_THIRD_PARTY

### M10_C1 — SA applicant is a third party ATS holder — standing under Section 17 is contested
- statutory_basis: `ACT`
- preconditions: [{'field': 'sa_applicant_type', 'operator': 'eq', 'value': 'THIRD_PARTY_ATS'}]
- **M10_C1_a**
  - expression: `sa_applicant_type == 'THIRD_PARTY_ATS'`
  - result_if_true: `REVIEW`  severity: `ADVISORY`  outcome_favors: **NEUTRAL**
  - ground_codes: ['THIRD_PARTY_ATS']
  - message: SA applicant is a third party holding an Agreement to Sell — not the borrower or guarantor. Standing under Section 17 of the SARFAESI Act is contested for ATS holders. Some High Courts have allowed such SAs (Delhi HC, Madras HC) on the basis that the applicant is a person aggrieved by the measures. Other benches have denied standing. DRT will determine standing as a preliminary issue. Bank should prepare to contest maintainability.

### M10_C2 — ATS and mortgage executed same date — strong bank fraud defense
- statutory_basis: `BOTH`
- preconditions: [{'field': 'sa_applicant_type', 'operator': 'eq', 'value': 'THIRD_PARTY_ATS'}, {'field': 'ats_simultaneous_mortgage', 'operator': 'eq', 'value': True}]
- **M10_C2_a**
  - expression: `ats_simultaneous_mortgage == True`
  - result_if_true: `FAIL`  severity: `HIGH`  outcome_favors: **BANK**
  - ground_codes: ['THIRD_PARTY_ATS']
  - message: Agreement to Sell (ATS) and mortgage deed executed on the same date ({ats_date} = {mortgage_date}). Bank will allege that the ATS was executed with knowledge of the mortgage and in collusion with the borrower to defeat the bank's security interest. The ATS holder cannot claim ignorance of the mortgage when both were executed simultaneously. This significantly weakens the third party's claim.

### M10_C3 — ATS holder paid substantial consideration directly to loan account — mitigates fraud allegation
- statutory_basis: `BOTH`
- preconditions: [{'field': 'sa_applicant_type', 'operator': 'eq', 'value': 'THIRD_PARTY_ATS'}, {'field': 'ats_payments_made_to_loan_account', 'operator': 'eq', 'value': True}]
- **M10_C3_a**
  - expression: `ats_payments_made_to_loan_account == True`
  - result_if_true: `PASS`  severity: `ADVISORY`  outcome_favors: **BORROWER**
  - ground_codes: ['THIRD_PARTY_ATS']
  - message: ATS holder has made payments directly to the bank's loan account (total paid: Rs. {ats_advance_paid}). This demonstrates bona fide conduct and good faith. Courts have treated payment by the ATS holder into the loan account as evidence that the bank had knowledge of the arrangement and implicitly accepted the ATS holder as a de facto party to the loan servicing. This substantially mitigates the bank's fraud allegation under M10_C2.

### M10_C4 — Sale confirmed and possession given — Celir LLP high threshold to set aside applies
- statutory_basis: `BOTH`
- preconditions: [{'field': 'sale_certificate_issued', 'operator': 'eq', 'value': True}, {'field': 'possession_given_to_auction_purchaser', 'operator': 'eq', 'value': True}]
- **M10_C4_a**
  - expression: `sale_certificate_issued == True and possession_given_to_auction_purchaser == True`
  - result_if_true: `REVIEW`  severity: `HIGH`  outcome_favors: **BANK**
  - ground_codes: ['AUCTION_PURCHASER', 'RIGHT_OF_REDEMPTION']
  - message: Sale certificate issued on {sale_certificate_date} and physical possession given to auction purchaser. The Supreme Court in Celir LLP v. Bafna Motors (2023) 13 SCC 561 held that once a sale is confirmed and possession given, the borrower's right of redemption under TPA Section 60 is extinguished. To set aside the sale at this stage requires: (1) fundamental procedural error in the auction itself, OR (2) the sale was obtained by fraud or misrepresentation. The standard for setting aside rises significantly after physical possession. Check rules M3_C6 (notice affixing), M3_C7 (auction during stay), and M3_C8 (concealment) — if any of these fire, the fundamental procedural error threshold may be met.

### M10_C5 — Sale certificate issued but possession not yet given — right of redemption window may remain open
- statutory_basis: `BOTH`
- preconditions: [{'field': 'sale_certificate_issued', 'operator': 'eq', 'value': True}, {'field': 'possession_given_to_auction_purchaser', 'operator': 'eq', 'value': False}]
- **M10_C5_a**
  - expression: `sale_certificate_issued == True and possession_given_to_auction_purchaser == False`
  - result_if_true: `REVIEW`  severity: `CURABLE`  outcome_favors: **BORROWER**
  - ground_codes: ['RIGHT_OF_REDEMPTION', 'AUCTION_PURCHASER']
  - message: Sale certificate issued but physical possession not yet given to auction purchaser. The right of redemption under TPA Section 60 may not yet be fully extinguished at this stage. The borrower/applicant has a window to challenge the sale through DRT before possession is handed over. Procedural defects (M3_C6, M3_C7, M3_C8) if present are more readily actionable at this stage than post-possession.

### M10_C6 — Second SA maintainable where cause of action differs from first SA
- statutory_basis: `ACT`
- preconditions: [{'field': 'previous_sa_filed', 'operator': 'eq', 'value': True}, {'field': 'challenges_auction', 'operator': 'eq', 'value': True}]
- **M10_C6_a**
  - expression: `previous_sa_filed == True and challenges_auction == True and challenges_demand_notice == False`
  - result_if_true: `PASS`  severity: `ADVISORY`  outcome_favors: **BORROWER**
  - ground_codes: ['SECOND_SA_FRESH_CAUSE']
  - message: A previous SA ({previous_sa_number}) was filed by the same applicant. The present SA challenges the auction and/or sale certificate — a distinct cause of action from the original SA's challenge. The Supreme Court in Oasis Dealcom Pvt. Ltd. v. Khazana Dealcomm (2016) 10 SCC 214 held that a second SA is maintainable under Section 17 where the cause of action is different. The fresh auction constitutes a fresh cause of action. Bank may contest maintainability but the Oasis Dealcom principle should be cited in rebuttal.

### M10_C7 — Auction purchaser must pay balance consideration within 90 days of sale — sale does not attain statutory finality otherwise
- statutory_basis: `RULES`
- preconditions: [{'field': 'sale_certificate_issued', 'operator': 'eq', 'value': True}, {'field': 'balance_consideration_paid_within_90_days', 'operator': 'is_not_null'}]
- **M10_C7_a**
  - expression: `balance_consideration_paid_within_90_days == False`
  - result_if_true: `FAIL`  severity: `FATAL`  outcome_favors: **BORROWER**
  - ground_codes: ['AUCTION_PURCHASER', 'RIGHT_OF_REDEMPTION']
  - message: Auction purchaser paid balance consideration on {balance_payment_date}, after the 90-day outer limit prescribed by Rule 9(4) of the Security Interest (Enforcement) Rules 2002 (auction date: {auction_date}). The sale did not attain statutory finality within the mandatory timeline. The borrower's right of redemption was not extinguished because the statutory conditions for vesting of title were never fulfilled.
- pass_message: Balance consideration paid within the 90-day limit prescribed by Rule 9(4).
