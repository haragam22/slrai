"""M8 (NPA classification) rule tests — confirmed facts injected manually, no DB."""
from datetime import date

from app.services.compliance.engine import run_all_modules


def cf(value):
    return {"value": value, "human_confirmed": True}


def facts(**kwargs) -> dict:
    return {k: cf(v) for k, v in kwargs.items()}


def result_for(results, rule_id):
    return next(r for r in results if r.rule_id == rule_id)


# ── M8_C1 — 90-day NPA window ────────────────────────────────────────────────

def test_m8_c1_fail_premature_npa():
    f = facts(date_of_last_payment=date(2025, 1, 1), npa_classification_date=date(2025, 2, 1))
    r = result_for(run_all_modules(f, modules_to_run=["M8"]), "M8_C1")
    assert r.status == "FAIL"
    assert r.severity == "FATAL"


def test_m8_c1_pass_valid_npa_timing():
    f = facts(date_of_last_payment=date(2025, 1, 1), npa_classification_date=date(2025, 5, 1))
    r = result_for(run_all_modules(f, modules_to_run=["M8"]), "M8_C1")
    assert r.status == "PASS"


# ── M8_C2 — no NPA during active restructuring ──────────────────────────────

def test_m8_c2_fail_npa_during_restructuring():
    f = facts(
        restructuring_proposal_pending=True,
        restructuring_approval_date=date(2025, 3, 1),
        npa_classification_date=date(2025, 2, 1),
    )
    r = result_for(run_all_modules(f, modules_to_run=["M8"]), "M8_C2")
    assert r.status == "FAIL"
    assert r.severity == "FATAL"


def test_m8_c2_pass_npa_after_restructuring_approval():
    f = facts(
        restructuring_proposal_pending=True,
        restructuring_approval_date=date(2025, 1, 1),
        npa_classification_date=date(2025, 2, 1),
    )
    r = result_for(run_all_modules(f, modules_to_run=["M8"]), "M8_C2")
    assert r.status == "PASS"


# ── M8_C3 — classification notice given (advisory) ──────────────────────────

def test_m8_c3_fail_no_notice():
    f = facts(classification_notice_given=False)
    r = result_for(run_all_modules(f, modules_to_run=["M8"]), "M8_C3")
    assert r.status == "FAIL"
    assert r.severity == "ADVISORY"


def test_m8_c3_pass_notice_given():
    f = facts(classification_notice_given=True)
    r = result_for(run_all_modules(f, modules_to_run=["M8"]), "M8_C3")
    assert r.status == "PASS"


# ── M8_C4 — no compound interest on NPA ─────────────────────────────────────

def test_m8_c4_fail_compound_interest():
    f = facts(interest_application_correct=False)
    r = result_for(run_all_modules(f, modules_to_run=["M8"]), "M8_C4")
    assert r.status == "FAIL"
    assert r.severity == "CURABLE"


def test_m8_c4_pass_simple_interest():
    f = facts(interest_application_correct=True)
    r = result_for(run_all_modules(f, modules_to_run=["M8"]), "M8_C4")
    assert r.status == "PASS"


# ── M8_C6 — NPA upgradation before auction ──────────────────────────────────

def test_m8_c6_fail_account_upgraded_before_auction():
    f = facts(
        payments_post_npa_total=500000,
        overdue_amount_at_auction_date=400000,
        auction_date=date(2025, 6, 1),
    )
    r = result_for(run_all_modules(f, modules_to_run=["M8"]), "M8_C6")
    assert r.status == "FAIL"
    assert r.severity == "FATAL"


def test_m8_c6_pass_still_npa_at_auction():
    f = facts(
        payments_post_npa_total=100000,
        overdue_amount_at_auction_date=400000,
        auction_date=date(2025, 6, 1),
    )
    r = result_for(run_all_modules(f, modules_to_run=["M8"]), "M8_C6")
    assert r.status == "PASS"


def test_only_m8_rules_returned():
    f = facts()
    results = run_all_modules(f, modules_to_run=["M8"])
    assert all(r.module == "M8_NPA_CLASSIFICATION" for r in results)
    assert {r.rule_id for r in results} == {"M8_C1", "M8_C2", "M8_C3", "M8_C4", "M8_C6"}
