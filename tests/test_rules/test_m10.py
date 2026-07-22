"""M10 (third-party rights) rule tests — confirmed facts injected manually, no DB.

M10 only runs when explicitly passed in modules_to_run (never in the M1-M9 default).
"""
from datetime import date

from app.services.compliance.engine import run_all_modules


def cf(value):
    return {"value": value, "human_confirmed": True}


def facts(**kwargs) -> dict:
    return {k: cf(v) for k, v in kwargs.items()}


def result_for(results, rule_id):
    return next(r for r in results if r.rule_id == rule_id)


def test_m10_not_run_by_default():
    f = facts(sa_applicant_type="THIRD_PARTY_ATS")
    results = run_all_modules(f)  # modules_to_run=None -> M1-M9 only
    assert not any(r.module == "M10_THIRD_PARTY" for r in results)


# (a) sa_applicant_type = THIRD_PARTY_ATS -> M10_C1 fires ADVISORY

def test_m10_c1_fires_for_third_party_ats():
    f = facts(sa_applicant_type="THIRD_PARTY_ATS")
    r = result_for(run_all_modules(f, modules_to_run=["M1", "M10"]), "M10_C1")
    assert r.status == "REVIEW"
    assert r.severity == "ADVISORY"


def test_m10_c1_not_applicable_for_borrower():
    f = facts(sa_applicant_type="BORROWER")
    r = result_for(run_all_modules(f, modules_to_run=["M10"]), "M10_C1")
    assert r.status == "PASS"  # precondition not met = not applicable


# (b) ats_simultaneous_mortgage = True -> M10_C2 fires HIGH

def test_m10_c2_fires_for_simultaneous_ats_mortgage():
    f = facts(
        sa_applicant_type="THIRD_PARTY_ATS",
        ats_simultaneous_mortgage=True,
        ats_date=date(2024, 6, 1),
        mortgage_date=date(2024, 6, 1),
    )
    r = result_for(run_all_modules(f, modules_to_run=["M10"]), "M10_C2")
    assert r.status == "FAIL"
    assert r.severity == "HIGH"


def test_m10_c2_pass_ats_predates_mortgage():
    # ats_simultaneous_mortgage is a computed field (never stored raw) —
    # derive it from ats_date/mortgage_date, not injected directly.
    f = facts(
        sa_applicant_type="THIRD_PARTY_ATS",
        ats_date=date(2024, 1, 1),
        mortgage_date=date(2024, 6, 1),
    )
    r = result_for(run_all_modules(f, modules_to_run=["M10"]), "M10_C2")
    assert r.status == "PASS"


# (c) sale_certificate_issued = True AND possession_given_to_auction_purchaser = True
#     -> M10_C4 fires HIGH, right_of_redemption_extinguished = True

def test_m10_c4_fires_for_confirmed_sale_with_possession():
    f = facts(
        sale_certificate_issued=True,
        possession_given_to_auction_purchaser=True,
        sale_certificate_date=date(2025, 4, 1),
    )
    results = run_all_modules(f, modules_to_run=["M10"])
    r = result_for(results, "M10_C4")
    assert r.status == "REVIEW"
    assert r.severity == "HIGH"

    from app.services.compliance.engine import COMPUTED_FIELD_RESOLVERS, _flatten_confirmed_facts
    flat = _flatten_confirmed_facts(f)
    assert COMPUTED_FIELD_RESOLVERS["right_of_redemption_extinguished"](flat) is True


def test_m10_c5_fires_for_confirmed_sale_pre_possession():
    f = facts(sale_certificate_issued=True, possession_given_to_auction_purchaser=False)
    r = result_for(run_all_modules(f, modules_to_run=["M10"]), "M10_C5")
    assert r.status == "REVIEW"
    assert r.severity == "CURABLE"


# (d) auction_conducted_despite_stay = True AND stay_was_operational_on_auction_date = True
#     -> M3_C7 fires ABSOLUTE_BAR

def test_m3_c7_fires_alongside_m10():
    f = facts(
        auction_date=date(2025, 3, 1),
        drt_interim_stay_granted=True,
        drt_stay_order_date=date(2025, 2, 1),
        auction_conducted_despite_stay=True,
    )
    results = run_all_modules(f, modules_to_run=["M3", "M10"])
    r = result_for(results, "M3_C7")
    assert r.status == "FAIL"
    assert r.severity == "ABSOLUTE_BAR"


# (e) auction_notice_affixed_on_property = False -> M3_C6 fires FATAL

def test_m3_c6_fires_alongside_m10():
    f = facts(auction_date=date(2025, 3, 1), auction_notice_affixed_on_property=False)
    results = run_all_modules(f, modules_to_run=["M3", "M10"])
    r = result_for(results, "M3_C6")
    assert r.status == "FAIL"
    assert r.severity == "FATAL"


# ── M10_C3 — mitigating factor ──────────────────────────────────────────────

def test_m10_c3_pass_bona_fide_payments():
    f = facts(sa_applicant_type="THIRD_PARTY_ATS", ats_payments_made_to_loan_account=True)
    r = result_for(run_all_modules(f, modules_to_run=["M10"]), "M10_C3")
    assert r.status == "PASS"
    assert r.severity == "ADVISORY"


# ── M10_C6 — second SA fresh cause (Oasis Dealcom) ──────────────────────────

def test_m10_c6_pass_fresh_cause_of_action():
    f = facts(previous_sa_filed=True, challenges_auction=True, challenges_demand_notice=False)
    r = result_for(run_all_modules(f, modules_to_run=["M10"]), "M10_C6")
    assert r.status == "PASS"
    assert r.severity == "ADVISORY"


def test_only_m10_rules_returned():
    f = facts()
    results = run_all_modules(f, modules_to_run=["M10"])
    assert all(r.module == "M10_THIRD_PARTY" for r in results)
    assert {r.rule_id for r in results} == {
        "M10_C1", "M10_C2", "M10_C3", "M10_C4", "M10_C5", "M10_C6", "M10_C7",
    }


def test_m10_c7_fail_balance_paid_late():
    f = facts(
        sale_certificate_issued=True,
        balance_payment_date=date(2025, 6, 1),
        auction_date=date(2025, 1, 1),
    )
    r = result_for(run_all_modules(f, modules_to_run=["M10"]), "M10_C7")
    assert r.status == "FAIL"
    assert r.severity == "FATAL"


def test_m10_c7_pass_balance_paid_within_90_days():
    f = facts(
        sale_certificate_issued=True,
        balance_payment_date=date(2025, 2, 1),
        auction_date=date(2025, 1, 1),
    )
    r = result_for(run_all_modules(f, modules_to_run=["M10"]), "M10_C7")
    assert r.status == "PASS"
