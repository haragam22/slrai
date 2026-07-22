"""Builds docs/wiki/sarfaesi_law_wiki.md and docs/wiki/third_party_law_wiki.md
from full-text statute files in docs/statutes/.

TWO OUTPUT FILES:
  sarfaesi_law_wiki.md    — loaded into every Chain A and Chain B call.
                            SARFAESI Act and SI Rules: FULL TEXT (all sections).
                            RDB Act, RBI circulars: selective sections only.
  third_party_law_wiki.md — loaded conditionally into Chain B only when:
                            sa_applicant_type != BORROWER/GUARANTOR, OR
                            tenancy_claimed=True, OR ibc_moratorium_active=True,
                            OR sale_certificate_issued=True.
                            TPA, IBC, Registration Act, Stamp Act: selective.

SARFAESI Act and SI Enforcement Rules are FULL TEXT because every section
and sub-rule is potentially relevant to an SA ground. No section of these
two Acts is "safe to skip" — omitting a sub-clause that a borrower cites
means the LLM cannot correctly classify the ground or identify the rule.

All other Acts use section filtering via ActSource.filter_sections because
they are large general statutes where only 4-8 sections are SARFAESI-relevant.

SLRAI annotations are injected after specific section texts via SLRAI_ANNOTATIONS
dict. Annotations explain which module, field, and rule each provision feeds.
They are structured as [SLRAI MODULE: ...] blocks so the LLM parser during
extraction can identify the annotation vs the statutory text.

Output format matches the header convention nlp_layer.py's statutory wiki
loader and judgments/retrieval.py's retrieve_statute_text() regex expect:

    ## Section 13(2)
    <exact statutory text>
    [SLRAI MODULE: ... annotation, if registered]

    ## Rule 8
    <exact statutory text>

Input: one full-text .txt file per Act, registered in WIKI_1_SOURCES /
WIKI_2_SOURCES below. Use scripts/extract_statute_pdf.py first if you only
have a PDF — it produces cleaner text (via Document AI layout extraction)
than raw copy/paste, which matters because this script's clause-boundary
regex is typo-sensitive (see _check_for_gaps below). Drop raw PDFs in
docs/statutes_pdf/ and convert into docs/statutes/<name>.txt.

Handles, explicitly:
  - Preamble (everything before the first numbered clause) -> "## Preamble"
    entry, not silently dropped.
  - Schedules/Forms (headings like "THE FIRST SCHEDULE", "FORM IV") -> their
    own entries, not glued onto the last section's text. Detected because they
    don't match the numbered-clause pattern and appear after the last real
    clause.
  - Provisos / Explanations ("Provided that...", "Explanation.—") are left
    attached to the subclause they follow — this is correct for a legal RAG
    system; they're not a separate citable unit.
  - Typo-caused silent merges (e.g. "13 .Enforcement" missing the exact
    ". " pattern) can't be detected from text alone, so this script checks
    for gaps in the parsed clause number sequence and WARNS loudly — a skipped
    number is the signature of a merge. It does not attempt to fix the typo;
    fix the source .txt and re-run.

Run once, and again whenever docs/statutes/ changes:
    python scripts/build_law_wiki.py
"""
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

STATUTES_DIR = Path("docs/statutes")
WIKI_1_PATH = Path("docs/wiki/sarfaesi_law_wiki.md")     # always-loaded
WIKI_2_PATH = Path("docs/wiki/third_party_law_wiki.md")  # conditionally-loaded


@dataclass
class ActSource:
    filename: str       # file in docs/statutes/
    label: str           # "Section" or "Rule" — used in wiki entry headers
    act_name: str        # shown in each entry's provenance footer
    full_text: bool = True          # if True: include ALL parsed clauses
    filter_sections: set[str] = field(default_factory=set)
    # filter_sections is only used when full_text=False.
    # Values are top-level clause numbers as strings: {"13", "14", "17"}.
    # Sub-clauses (e.g. "13(2)") are included automatically when their parent
    # section is in filter_sections — you do not need to list sub-clauses here.


# ── WIKI FILE 1 — sarfaesi_law_wiki.md ───────────────────────────────────────
# Loaded into EVERY Chain A call (extraction) and every Chain B call.
# Contains: SARFAESI Act (full), SI Enforcement Rules (full),
#           RBI IRAC (full), RBI MSME Circular (full), RBI Fair Practices Code (selective)
# RDB Act moved to WIKI_2_SOURCES (see below) — was pushing Wiki 1 to ~79,500
# tokens against a 65,000 budget. RDB Act (DRT jurisdiction/interim relief) is
# most relevant during Chain B judgment analysis, not Chain A extraction.
WIKI_1_SOURCES: list[ActSource] = [
    ActSource(
        filename="sarfaesi_act.txt",
        label="Section",
        act_name="SARFAESI Act, 2002",
        full_text=True,           # ALL sections — every subsection is legally relevant
    ),
    ActSource(
        filename="sarfaesi_rules.txt",
        label="Rule",
        act_name="Security Interest (Enforcement) Rules, 2002",
        full_text=True,           # ALL rules — Rule 8 alone has 10+ sub-rules
    ),
    ActSource(
        filename="rbi_irac.txt",
        label="Para",
        act_name="RBI Master Direction — IRAC Prudential Norms, 2021",
        full_text=True,           # Short document — include fully for NPA rules
    ),
    ActSource(
        filename="rbi_msme.txt",
        label="Para",
        act_name="RBI MSME Restructuring Circular (DBR.No.BP.BC.18/21.04.048/2018-19)",
        full_text=True,           # Short circular — include fully for M9 module
    ),
    ActSource(
        filename="rbi_fpc.txt",
        label="Para",
        act_name="RBI Fair Practices Code for Lenders",
        full_text=False,
        filter_sections={"6", "7", "8"},
        # Only the paragraphs about written communication and reasons for rejection.
        # Para 6/7/8 typically cover borrower communication obligations.
        # If the document uses headings rather than numbered paragraphs,
        # include the sections titled: "Loan application and processing",
        # "Rejection of applications", "Borrower representations".
    ),
]

# ── WIKI FILE 2 — third_party_law_wiki.md ────────────────────────────────────
# Loaded into every Chain B call (applicability.py::_load_third_party_wiki),
# unconditionally — RDB Act's DRT jurisdiction/interim relief provisions
# (Section 19(25) etc.) are needed for every Chain B analysis, not just
# third-party/tenancy/IBC/completed-auction cases.
# Contains: RDB Act (selective), TPA, IBC, Registration Act, Stamp Act (selective)
WIKI_2_SOURCES: list[ActSource] = [
    ActSource(
        filename="rdb_act.txt",
        label="Section",
        act_name="Recovery of Debts and Bankruptcy Act, 1993",
        full_text=False,
        filter_sections={"2", "17", "18", "19", "20", "22", "26"},
        # Section 19 includes 19(25) and 19(26) — DRT interim relief powers.
        # Section 17/18/19: DRT jurisdiction + powers.
        # Section 26: limitation — DRT can condone delay.
    ),
    ActSource(
        filename="transfer_of_property_act.txt",
        label="Section",
        act_name="Transfer of Property Act, 1882",
        full_text=False,
        filter_sections={"52", "54", "58", "60", "65A", "105", "107", "108"},
        # 52: lis pendens, 54: sale/agreement for sale, 58: mortgage types,
        # 60: right of redemption, 65A: equitable mortgage,
        # 105: lease defined, 107: registration of leases, 108: rights of lessor/lessee
    ),
    ActSource(
        filename="ibc_2016.txt",
        label="Section",
        act_name="Insolvency and Bankruptcy Code, 2016",
        full_text=False,
        filter_sections={"3", "14", "33", "52", "60", "95", "96", "101", "238"},
        # 3: definitions, 14: corporate moratorium (THE KEY ONE for F4 filter),
        # 33: liquidation order, 52: secured creditor in liquidation,
        # 60: adjudicating authority (NCLT vs DRT conflict),
        # 95/96/101: personal insolvency for individual guarantors,
        # 238: IBC override clause (IBC beats SARFAESI)
    ),
    ActSource(
        filename="registration_act.txt",
        label="Section",
        act_name="Registration Act, 1908",
        full_text=False,
        filter_sections={"17", "49"},
        # 17: documents requiring compulsory registration (leases > 1 year)
        # 49: effect of non-registration — inadmissible as evidence
    ),
    ActSource(
        filename="stamp_act.txt",
        label="Section",
        act_name="Indian Stamp Act, 1899",
        full_text=False,
        filter_sections={"2", "17", "33", "35"},
        # 2: definitions, 17: instruments must be stamped at/before execution,
        # 33: impounding of unstamped instruments,
        # 35: unstamped instruments inadmissible in evidence
    ),
]

# Maps (filename, clause_key) → annotation string appended after statutory text.
# clause_key must EXACTLY match the string produced by:
#   f"{source.label} {number}"  (e.g. "Section 13(2)", "Rule 8", "Para 4")
SLRAI_ANNOTATIONS: dict[tuple[str, str], str] = {

    # ── SARFAESI ACT ──────────────────────────────────────────────────────────

    ("sarfaesi_act.txt", "Section 13"): (
        "\n[SLRAI: M1 + M3 — Parent section for all enforcement actions. "
        "The bank's right to enforce security interest flows from this section. "
        "Sub-sections 13(2) through 13(13) are individually critical — see below.]"
    ),
    ("sarfaesi_act.txt", "Section 13(2)"): (
        "\n[SLRAI MODULE: M1 — DEMAND NOTICE. "
        "The 60-day period starts from the date the borrower RECEIVES the notice, "
        "not from the date of dispatch. "
        "Fields: demand_notice_date, notice_service_date, demand_notice_amount. "
        "Rule M1_C1: sixty_day_period_elapsed must be True before any 13(4) action. "
        "Rule M1_C2: demand_notice_amount must match actual_outstanding_amount. "
        "Service must comply with Rule 3 of SI Enforcement Rules.]"
    ),
    ("sarfaesi_act.txt", "Section 13(3)"): (
        "\n[SLRAI MODULE: M2 — BORROWER RIGHT TO OBJECT. "
        "The borrower's representation under 13(3) is what triggers the bank's "
        "mandatory duty under 13(3A). objection_filed field captures whether "
        "the borrower exercised this right. objection_date field captures when.]"
    ),
    ("sarfaesi_act.txt", "Section 13(3A)"): (
        "\n[SLRAI MODULE: M2 — BANK REPLY IS MANDATORY NOT DIRECTORY. "
        "[SLRAI NOTE: 'shall' = mandatory — SC in Kanaiyalal (2011) 2 SCC 782] "
        "The bank MUST: (a) consider the representation, (b) give REASONS for non-acceptance, "
        "(c) communicate within 15 DAYS. A reply saying only 'rejected' is NOT compliance. "
        "Fields: bank_reply_given, bank_reply_date, bank_reply_gives_reasons. "
        "Rule M2_C2: if objection_filed=True and bank_reply_given=False → FATAL. "
        "Rule M2_C3: if bank_reply_given=True and bank_reply_gives_reasons=False → CURABLE.]"
    ),
    ("sarfaesi_act.txt", "Section 13(4)"): (
        "\n[SLRAI MODULE: M1 + M3 — ACTIONS AFTER 60 DAYS. "
        "The four permitted actions: (a) take possession, (b) take over management, "
        "(c) appoint manager, (d) require payment from debtors of the borrower. "
        "The measure challenged in the SA (possession notice, sale notice, auction) "
        "must be one of these. measure_type field captures which action was taken. "
        "measure_date field captures when. All of Rule 8 and Rule 9 flow from 13(4)(a).]"
    ),
    ("sarfaesi_act.txt", "Section 13(8)"): (
        "\n[SLRAI MODULE: M3 — 30-DAY NOTICE BEFORE SALE. "
        "[AUTHORITY: Mathew Varghese v. M. Amritha Kumar (2014) 5 SCC 610 — "
        "Section 13(8) read with Rule 8(1): 30 clear days notice to borrower is mandatory. "
        "Auction failure not solely attributable to borrower = fresh notice required.] "
        "auction_gap_days field: auction_date minus sale_notice_date must be ≥30.]"
    ),
    ("sarfaesi_act.txt", "Section 14"): (
        "\n[SLRAI NOTE: CMM PETITION — MUST DISCLOSE PENDING SA. "
        "When bank files Section 14 petition for physical possession, the affidavit "
        "MUST disclose: (a) outstanding amount, (b) security description, "
        "(c) whether any SA is PENDING before DRT on this property. "
        "Concealing a pending SA from the CMM = fraud on the court. "
        "This is the basis for the PENDING_SA_CONCEALED ground code. "
        "bank_suppressed_sa_before_cmm field — ADVISORY severity in report.]"
    ),
    ("sarfaesi_act.txt", "Section 17"): (
        "\n[SLRAI MODULE: M4 — SA FILING AT DRT. "
        "Section 17(1): 45-day limitation from the date of the MEASURE, not from "
        "when borrower learned of it. M4_C1: sa_filing_date minus measure_date ≤45 days. "
        "Section 17(4): DRT CAN grant interim stay — drt_interim_stay_granted field. "
        "[AUTHORITY: A Section 17(4) stay is a court order. Auction conducted AFTER "
        "a Section 17(4) stay = ABSOLUTE_BAR. Rule M3_C7 captures this violation.] "
        "Section 17(2) mandatory pre-deposit: STRUCK DOWN by Mardia Chemicals (2004) 4 SCC 311.]"
    ),
    ("sarfaesi_act.txt", "Section 31"): (
        "\n[SLRAI PRE-INTAKE: Exemptions from SARFAESI. "
        "Section 31(i): agricultural land → F1 filter fires, INTAKE_REJECTED. "
        "Section 31(ii): amount ≤1 lakh → F2 filter fires, INTAKE_REJECTED. "
        "If borrower argues the secured asset falls under any Section 31 exemption, "
        "that is a threshold objection — SARFAESI does not apply at all.]"
    ),
    ("sarfaesi_act.txt", "Section 34"): (
        "\n[SLRAI NOTE: Civil courts have NO jurisdiction over SARFAESI enforcement. "
        "Third parties (ATS holders, tenants) seeking to stop SARFAESI must approach DRT. "
        "However: HC writ jurisdiction under Article 226 was allowed when DRTs were "
        "non-functional — as in Santosh Jain v. PNB (Delhi HC, November 2021).]"
    ),
    ("sarfaesi_act.txt", "Section 35"): (
        "\n[SLRAI CRITICAL — HIERARCHY NOTE: "
        "SARFAESI overrides other laws — BUT IBC Section 238 overrides SARFAESI. "
        "Correct hierarchy: IBC > SARFAESI > other laws. "
        "[AUTHORITY: Innoventive Industries v. ICICI Bank (2018) 1 SCC 407 — "
        "Section 238 IBC prevails over Section 35 SARFAESI.] "
        "F4 pre-intake filter implements this: ibc_moratorium_active=True → pipeline paused.]"
    ),

    # ── SI ENFORCEMENT RULES ──────────────────────────────────────────────────

    ("sarfaesi_rules.txt", "Rule 3"): (
        "\n[SLRAI MODULE: M1 — DEMAND NOTICE SERVICE. "
        "Rule 3 specifies valid modes of service: (a) registered post AD, (b) speed post, "
        "(c) affixing at last known address + newspaper publication, (d) email if agreed. "
        "notice_service_mode field captures which mode was used. "
        "notice_dispatch_proof_present field: if False → M1_C3 fires as CURABLE. "
        "Proof = POD acknowledgment or speed post receipt.]"
    ),
    ("sarfaesi_rules.txt", "Rule 4"): (
        "\n[SLRAI MODULE: M1 + M3 — POSSESSION NOTICE AFTER 13(4). "
        "After taking possession, bank must: (a) publish in two newspapers, "
        "(b) send intimation to CMM. Both are mandatory. "
        "possession_notice_date field. This notice is distinct from the sale notice under Rule 8.]"
    ),
    ("sarfaesi_rules.txt", "Rule 8"): (
        "\n[SLRAI MODULE: M3 — SALE OF IMMOVABLE SECURED ASSETS. "
        "This is the most litigated rule in SARFAESI auction challenges. "
        "Sub-rules 8(1) through 8(9) together form the complete mandatory procedure. "
        "Every sub-rule is individually enforceable. See annotations below for each.]"
    ),
    ("sarfaesi_rules.txt", "Rule 8(1)"): (
        "\n[SLRAI MODULE: M3 — 30 CLEAR DAYS NOTICE TO BORROWER. "
        "[SLRAI NOTE: 'shall' = mandatory per Mathew Varghese (2014) 5 SCC 610] "
        "M3_C1: auction_date minus sale_notice_date must be ≥30 days. "
        "If first auction failed and failure NOT solely due to borrower → fresh 30-day notice. "
        "auction_gap_days = computed field (auction_date - sale_notice_date).]"
    ),
    ("sarfaesi_rules.txt", "Rule 8(2)"): (
        "\n[SLRAI MODULE: M3 — NEWSPAPER PUBLICATION. "
        "Two newspapers required. At least one must have circulation in the area "
        "where the secured asset is located. "
        "newspaper_publication_done field. M3_C2: if False → FATAL.]"
    ),
    ("sarfaesi_rules.txt", "Rule 8(6)"): (
        "\n[SLRAI MODULE: M3 — CONTENT OF SALE NOTICE. "
        "The notice MUST contain: (a) description of property + known encumbrances, "
        "(b) the secured debt amount, (c) reserve price, (d) time and place of auction, "
        "(e) EMD amount and terms, (f) other terms the authorised officer considers necessary. "
        "'Known encumbrances' includes pending SA before DRT. "
        "Failure to disclose pending SA = M3_C8 (PENDING_SA_CONCEALED) fires. "
        "emd_stated_in_notice field. reserve_price field.]"
    ),
    ("sarfaesi_rules.txt", "Rule 8(6)(7)"): (
        "\n[SLRAI MODULE: M3 — RULE M3_C6 — AFFIXING NOTICE AT PROPERTY. "
        "[SLRAI NOTE: 'shall' = mandatory — affirmed in both Mathew Varghese (2014) and "
        "Vasu P. Shetty (2014) 6 SCC 660: non-compliance renders sale NULL AND VOID.] "
        "The auction notice MUST be physically affixed at a conspicuous part of the "
        "immovable property BEFORE the auction. The bank cannot argue impossibility "
        "because a third party was in possession — courts have rejected this defence. "
        "auction_notice_affixed_on_property field: if False → M3_C6 fires as FATAL.]"
    ),
    ("sarfaesi_rules.txt", "Rule 8(8)"): (
        "\n[SLRAI MODULE: M10 — SALE CERTIFICATE. "
        "Issued after full payment received from auction purchaser. "
        "sale_certificate_issued field. sale_certificate_date field. "
        "[AUTHORITY: Celir LLP v. Bafna Motors (2023) 13 SCC 561 — "
        "once sale certificate issued, right of redemption under TPA Section 60 "
        "is extinguished. Setting aside requires fundamental procedural error or fraud.] "
        "right_of_redemption_extinguished = computed True when sale_certificate_issued = True.]"
    ),
    ("sarfaesi_rules.txt", "Rule 8(9)"): (
        "\n[SLRAI MODULE: M10 — DELIVERY OF POSSESSION TO PURCHASER. "
        "possession_given_to_auction_purchaser field. "
        "After this point: Celir LLP (2023) applies fully — DRT must weigh "
        "auction purchaser's equities. M10_C4 rule fires when both sale_certificate_issued "
        "and possession_given_to_auction_purchaser are True.]"
    ),
    ("sarfaesi_rules.txt", "Rule 9"): (
        "\n[SLRAI MODULE: M3 — SALE OF MOVABLE SECURED ASSETS. "
        "asset_type = 'movable' triggers Rule 9 analysis. "
        "Same 30-day notice principle as Rule 8(1). "
        "Rule 9(4): extension of time for payment of balance — by agreement between "
        "secured creditor and purchaser. If purchaser defaults after extension → "
        "bank can forfeit EMD and re-auction.]"
    ),

    # ── RDB ACT ──────────────────────────────────────────────────────────────

    ("rdb_act.txt", "Section 19"): (
        "\n[SLRAI MODULE: M3 + M10 — DRT POWERS INCLUDING INTERIM RELIEF. "
        "Section 19(25) is the DRT's specific power to GRANT INTERIM RELIEF "
        "pending hearing of the SA. When exercised → drt_interim_stay_granted = True. "
        "A bank that conducts auction AFTER a Section 19(25) order = contempt of DRT. "
        "Rule M3_C7 (ABSOLUTE_BAR): auction_conducted_despite_stay + "
        "stay_was_operational_on_auction_date → sale is void.]"
    ),

    # ── RBI IRAC ─────────────────────────────────────────────────────────────

    ("rbi_irac.txt", "NPA Definition"): (
        "\n[SLRAI MODULE: M8 — NPA IS THE JURISDICTIONAL TRIGGER. "
        "The bank CANNOT issue Section 13(2) demand notice unless the account is NPA. "
        "Premature NPA classification = Section 13(2) notice has no legal basis. "
        "M8_C1: days_from_last_payment_to_npa must be ≥90 for term loans. "
        "For CC/OD: account must have been 'out of order' for ≥90 days.]"
    ),

    # ── IBC 2016 ─────────────────────────────────────────────────────────────

    ("ibc_2016.txt", "Section 14"): (
        "\n[SLRAI PRE-INTAKE: F4 FILTER — IBC MORATORIUM STOPS SARFAESI. "
        "[SLRAI NOTE: 'shall' = automatic and immediate upon NCLT admission order] "
        "Section 14(1)(d) specifically bars enforcement of any security interest. "
        "SARFAESI enforcement against a corporate debtor in CIRP is prohibited. "
        "ibc_moratorium_active field: if True → F4 fires → pipeline paused for legal review. "
        "Moratorium starts on NCLT ADMISSION (not filing) of the insolvency petition. "
        "ibc_moratorium_start_date = date of NCLT admission order.]"
    ),
    ("ibc_2016.txt", "Section 238"): (
        "\n[SLRAI CRITICAL — IBC OVERRIDES SARFAESI. "
        "[AUTHORITY: Innoventive Industries v. ICICI Bank (2018) 1 SCC 407] "
        "When IBC and SARFAESI conflict, IBC wins. "
        "This overrides SARFAESI Section 35 ('SARFAESI overrides other laws'). "
        "Hierarchy: IBC > SARFAESI > TPA and other general laws. "
        "F4 pre-intake filter is the system implementation of this principle.]"
    ),
    ("ibc_2016.txt", "Section 95"): (
        "\n[SLRAI MODULE: M7 — PERSONAL INSOLVENCY OF INDIVIDUAL GUARANTORS. "
        "Section 95 allows creditor to apply for insolvency of an individual guarantor. "
        "Section 96 creates INTERIM MORATORIUM on debt enforcement against the guarantor. "
        "This protects the guarantor's PERSONAL assets — not the borrower's secured assets. "
        "The bank can still enforce SARFAESI against the borrower's property. "
        "guarantor_ibc_moratorium field — add in V1.1 for guarantor-specific analysis.]"
    ),

    # ── TPA 1882 ─────────────────────────────────────────────────────────────

    ("transfer_of_property_act.txt", "Section 52"): (
        "\n[SLRAI MODULE: M10 — LIS PENDENS / PENDING SA PROTECTION. "
        "When SA is pending before DRT, any sale of the property is subject to outcome. "
        "The auction purchaser takes title subject to the SA proceeding. "
        "If DRT sets aside the enforcement → auction purchaser's title is affected. "
        "This is the doctrine that protects the SA applicant even after auction. "
        "pending_sa_existed_at_auction_date field.]"
    ),
    ("transfer_of_property_act.txt", "Section 54"): (
        "\n[SLRAI MODULE: M10 — ATS HOLDER RIGHTS. "
        "An Agreement to Sell gives CONTRACTUAL rights — NOT property rights. "
        "The ATS holder cannot assert their agreement against the bank's prior mortgage. "
        "Bank defence: registered security interest (mortgage) > mere contractual right (ATS). "
        "However: if ATS holder has possession + paid substantial consideration + paid bank EMIs "
        "→ courts may grant equitable relief. ats_payments_made_to_loan_account field captures this. "
        "M10_C3 handles the strong-bona-fide ATS holder scenario.]"
    ),
    ("transfer_of_property_act.txt", "Section 60"): (
        "\n[SLRAI MODULE: M10 — RIGHT OF REDEMPTION EXTINGUISHMENT. "
        "[AUTHORITY: Celir LLP v. Bafna Motors (2023) 13 SCC 561 — "
        "right of redemption extinguishes when sale is CONFIRMED (certificate issued), "
        "not when possession is given to purchaser.] "
        "right_of_redemption_extinguished = computed True when sale_certificate_issued = True. "
        "After extinguishment: borrower cannot get property back even by paying full dues. "
        "Only fraud or fundamental procedural error can set aside a confirmed sale.]"
    ),
    ("transfer_of_property_act.txt", "Section 107"): (
        "\n[SLRAI MODULE: M5 — LEASE REGISTRATION REQUIREMENT. "
        "Lease for more than ONE YEAR must be by registered instrument. "
        "lease_registered field: if False and lease_duration_months > 12 → "
        "tenancy claim is unenforceable against the bank. "
        "[Cross-reference: Registration Act Section 49 — unregistered documents "
        "that require registration are inadmissible as evidence.] "
        "Courts treat unregistered long leases as monthly tenancies terminable by notice.]"
    ),

    # ── REGISTRATION ACT ─────────────────────────────────────────────────────

    ("registration_act.txt", "Section 17"): (
        "\n[SLRAI MODULE: M5 + M10 — WHAT MUST BE REGISTERED. "
        "Key: leases from year to year or for term exceeding one year MUST be registered. "
        "ATS for immoveable property above Rs 100 value must also be registered. "
        "lease_registered field. ats_registered field.]"
    ),
    ("registration_act.txt", "Section 49"): (
        "\n[SLRAI MODULE: M5 + M10 — EFFECT OF NON-REGISTRATION. "
        "Unregistered document cannot: affect immoveable property, be received as evidence "
        "of any transaction affecting immoveable property. "
        "Exception: can be received as evidence of a COLLATERAL purpose. "
        "SLRAI APPLICATION: "
        "(1) Unregistered long lease → M5 tenancy claim cannot be proved before DRT → M5 PASS for bank. "
        "(2) Unstamped/unregistered ATS → may be inadmissible → weakens M10_C2 ATS holder claim.]"
    ),

    # ── STAMP ACT ────────────────────────────────────────────────────────────

    ("stamp_act.txt", "Section 35"): (
        "\n[SLRAI MODULE: M10 — UNSTAMPED INSTRUMENTS INADMISSIBLE. "
        "An unstamped or insufficiently stamped instrument CANNOT be admitted in evidence. "
        "CAN be admitted if party pays deficit duty + penalty (usually 10x deficit). "
        "ats_stamp_duty_paid field: if False → flag as ADVISORY in M10_C2. "
        "NOTE: In Santosh Jain v. PNB, bank alleged ATS was understamped "
        "(stamp paper dated 06.10.2015 but ATS claimed to be dated 30.06.2015 — "
        "stamp paper bought AFTER execution). Courts treat backdated stamping as fraud indicator.]"
    ),
}

# Matches a numbered clause start at the beginning of a line, bare-act style:
#   "13. Enforcement of security interest.—"
#   "13A. Registration by asset reconstruction companies.—"
#   "8. Sale of immovable secured assets.—"
# Group 1 = the clause number, including any letter suffix (13, 13A, 17A ...).
# NOTE: strict on purpose (exact "N. " with no stray space before the dot).
# A source typo like "13 .Enforcement" or "13 Enforcement" (missing dot) will
# NOT match and that section's text silently merges into the previous one.
# _check_for_gaps() below is the safety net that surfaces this.
CLAUSE_START_RE = re.compile(
    r"^\s*(\d+[A-Za-z]?)\.\s+(?=\S)",
    re.MULTILINE,
)

# Matches a sub-clause marker at the start of a line within a section, e.g.
#   "(1) Where any borrower..."
#   "(3A) If the borrower makes any representation..."
SUBCLAUSE_START_RE = re.compile(
    r"^\s*\((\d+[A-Za-z]?)\)\s+(?=\S)",
    re.MULTILINE,
)

# Marks the start of a Schedule/Form/Appendix block — these don't follow
# section numbering and must not be glued onto the last matched section.
# Matches lines like "THE FIRST SCHEDULE", "SCHEDULE I", "FORM IV", "APPENDIX A".
SCHEDULE_START_RE = re.compile(
    r"^\s*(?:THE\s+)?((?:FIRST|SECOND|THIRD|FOURTH|FIFTH)?\s*SCHEDULE(?:\s+[IVXLC]+)?|"
    r"FORM(?:\s*NO\.?)?\s*[-–]?\s*[A-Z0-9IVXLC]+|APPENDIX(?:\s+[A-Z0-9]+)?)\s*$",
    re.MULTILINE,
)


def _split_schedules(tail_text: str) -> list[tuple[str, str]]:
    """Splits trailing Schedules/Forms/Appendices into their own entries."""
    matches = list(SCHEDULE_START_RE.finditer(tail_text))
    if not matches:
        return []
    result = []
    for i, match in enumerate(matches):
        label = " ".join(match.group(1).split())
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(tail_text)
        result.append((label, tail_text[start:end].strip()))
    return result


def _split_into_clauses(full_text: str) -> tuple[str | None, list[tuple[str, str]], list[tuple[str, str]]]:
    """Splits a full Act/Rules text into (preamble, clauses, schedules).

    clauses: two levels of entries are produced —
      - "13"     — the whole section, full text, for general context
      - "13(2)"  — each sub-clause individually, since retrieve_statute_text()
                   and the rule engine cite exact sub-clause numbers like
                   "13(2)" / "13(3A)", not just the parent section.
    schedules: (label, text) pairs for anything after the last numbered
      clause that looks like a Schedule/Form/Appendix, split out instead of
      being appended to the last section's text.
    """
    matches = list(CLAUSE_START_RE.finditer(full_text))
    if not matches:
        return None, [], []

    preamble = full_text[:matches[0].start()].strip()

    clauses = []
    schedules = []
    for i, match in enumerate(matches):
        number = match.group(1)
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        section_text = full_text[start:end]

        if i + 1 == len(matches):
            # Last clause — check if a Schedule/Form/Appendix is glued onto its tail.
            schedule_matches = list(SCHEDULE_START_RE.finditer(section_text))
            if schedule_matches:
                section_text = section_text[:schedule_matches[0].start()]
                schedules = _split_schedules(
                    full_text[start + schedule_matches[0].start():end]
                )

        section_text = section_text.strip()
        clauses.append((number, section_text))

        for sub_number, sub_text in _split_subclauses(section_text):
            clauses.append((f"{number}({sub_number})", sub_text))

    return (preamble or None), clauses, schedules


def _split_subclauses(section_text: str) -> list[tuple[str, str]]:
    sub_matches = list(SUBCLAUSE_START_RE.finditer(section_text))
    if not sub_matches:
        return []

    result = []
    for i, match in enumerate(sub_matches):
        sub_number = match.group(1)
        start = match.start()
        end = sub_matches[i + 1].start() if i + 1 < len(sub_matches) else len(section_text)
        result.append((sub_number, section_text[start:end].strip()))
    return result


def _check_for_gaps(filename: str, clauses: list[tuple[str, str]]) -> None:
    """Warns if top-level clause numbers skip — the signature of a typo-caused
    silent merge (see CLAUSE_START_RE note). Only checks purely numeric
    top-level clauses (skips lettered ones like '13A' and sub-clauses).
    """
    top_level_numbers = sorted({
        int(number) for number, _ in clauses
        if "(" not in number and number.isdigit()
    })
    if len(top_level_numbers) < 2:
        return
    gaps = [
        n for n in range(top_level_numbers[0], top_level_numbers[-1] + 1)
        if n not in top_level_numbers
    ]
    if gaps:
        print(
            f"WARNING: {filename}: gap in section numbering at {gaps} — "
            f"likely a source typo (missing '. ' after a number) caused that "
            f"section to silently merge into the previous one. Check the raw "
            f"text around section {gaps[0] - 1}."
        )


def _should_include_clause(source: ActSource, number: str) -> bool:
    """Returns True if this clause should be written to the wiki.

    For full-text acts: always True.
    For filtered acts: True if the TOP-LEVEL number is in filter_sections.
    Sub-clauses (e.g. "13(2)") are included when their parent ("13") is in
    filter_sections — checked by stripping the sub-clause suffix.
    """
    if source.full_text:
        return True
    top_level = number.split("(")[0].strip()
    return top_level in source.filter_sections


def _get_annotation(filename: str, clause_header: str) -> str:
    """Returns the SLRAI annotation for a given (filename, clause_header) pair.
    clause_header is the full header string, e.g. 'Section 13(2)', 'Rule 8(6)(7)'.
    Returns empty string if no annotation registered.
    """
    return SLRAI_ANNOTATIONS.get((filename, clause_header), "")


def _build_one_wiki(
    output_path: Path,
    sources: list[ActSource],
    wiki_label: str,
) -> None:
    """Builds one wiki file from the given sources.
    Called twice: once for sarfaesi_law_wiki.md, once for third_party_law_wiki.md.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    found_sources = [s for s in sources if (STATUTES_DIR / s.filename).exists()]

    if not found_sources:
        expected = ", ".join(s.filename for s in sources)
        output_path.write_text(
            f"<!-- PLACEHOLDER: no source files found for {wiki_label}. "
            f"Expected: {expected}. "
            f"Extraction runs WITHOUT this statutory context until files are added. -->\n",
            encoding="utf-8",
        )
        print(
            f"WARNING [{wiki_label}]: no source files found. "
            f"Wrote placeholder to {output_path}."
        )
        return

    entries = []
    total_clauses = 0

    for source in found_sources:
        path = STATUTES_DIR / source.filename
        full_text = path.read_text(encoding="utf-8")
        preamble, clauses, schedules = _split_into_clauses(full_text)

        if not clauses:
            print(
                f"WARNING: no clause boundaries detected in {source.filename} — "
                f"skipped. Check it uses bare-act numbering (e.g. '13. Section title.—')."
            )
            continue

        _check_for_gaps(source.filename, clauses)

        # ── Act-level header ────────────────────────────────────────────────
        mode_note = "FULL TEXT" if source.full_text else (
            "SELECTIVE: sections " + ", ".join(sorted(source.filter_sections, key=lambda x: (len(x), x)))
        )
        entries.append(
            f"# {source.act_name}\n"
            f"<!-- {mode_note} -->\n"
        )

        # ── Preamble ────────────────────────────────────────────────────────
        if preamble:
            header = "Preamble"
            annotation = _get_annotation(source.filename, header)
            entries.append(
                f"## Preamble\n\n{preamble}{annotation}\n\n"
                f"_Source: {source.act_name}_\n"
            )

        # ── Clauses ─────────────────────────────────────────────────────────
        included = 0
        for number, text in clauses:
            if not _should_include_clause(source, number):
                continue

            clause_header = f"{source.label} {number}"
            annotation = _get_annotation(source.filename, clause_header)
            entries.append(
                f"## {clause_header}\n\n{text}{annotation}\n\n"
                f"_Source: {source.act_name}_\n"
            )
            included += 1

        # ── Schedules (only for full-text acts) ─────────────────────────────
        if source.full_text:
            for label, sched_text in schedules:
                entries.append(
                    f"## {label}\n\n{sched_text}\n\n"
                    f"_Source: {source.act_name}_\n"
                )
                print(
                    f"{source.filename}: schedule '{label}' → split into own entry."
                )

        total_clauses += included
        print(
            f"{source.filename}: {included} clause(s) written"
            f"{' (full text)' if source.full_text else f' (filtered from {len(clauses)} parsed)'}"
            f"{', preamble included' if preamble else ''}"
        )

    if not entries:
        print(f"ERROR [{wiki_label}]: no clauses written. {output_path} not created.")
        return

    output_path.write_text("\n".join(entries) + "\n", encoding="utf-8")

    # Token estimate
    char_count = output_path.stat().st_size
    est_tokens = char_count // 4
    print(
        f"\n[OK] {wiki_label}: {total_clauses} clause(s) -> {output_path}\n"
        f"   Estimated size: {est_tokens:,} tokens\n"
    )
    if est_tokens > 95_000:
        print(
            f"   WARNING: approaching context window limit (100K). "
            f"Consider trimming lower-priority acts."
        )


def build_wiki() -> None:
    """Entry point — builds both wiki files."""
    _build_one_wiki(
        output_path=WIKI_1_PATH,
        sources=WIKI_1_SOURCES,
        wiki_label="sarfaesi_law_wiki (always-loaded)",
    )
    _build_one_wiki(
        output_path=WIKI_2_PATH,
        sources=WIKI_2_SOURCES,
        wiki_label="third_party_law_wiki (conditionally-loaded)",
    )
    print(
        "\nRun token check:\n"
        "  python -c \""
        "f1=open('docs/wiki/sarfaesi_law_wiki.md').read(); "
        "f2=open('docs/wiki/third_party_law_wiki.md').read(); "
        "print(f'Wiki 1: ~{len(f1)//4:,} tokens'); "
        "print(f'Wiki 2: ~{len(f2)//4:,} tokens')"
        "\""
    )


if __name__ == "__main__":
    build_wiki()
