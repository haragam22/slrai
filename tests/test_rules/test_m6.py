"""M6 (valuation) rule tests — confirmed facts injected manually, no DB."""
from datetime import date

from app.services.compliance.engine import run_all_modules


def cf(value):
    return {"value": value, "human_confirmed": True}


def facts(**kwargs) -> dict:
    return {k: cf(v) for k, v in kwargs.items()}


def result_for(results, rule_id):
    return next(r for r in results if r.rule_id == rule_id)


# ── M6_C1 — valuer must be RBI-empanelled + RVA-registered ─────────────────

def test_m6_c1_fail_valuer_not_empanelled():
    f = facts(valuation_report_present=True, valuer_rbi_empanelled=False, valuer_registered_under_rvact=True)
    r = result_for(run_all_modules(f, modules_to_run=["M6"]), "M6_C1")
    assert r.status == "FAIL"
    assert r.severity == "FATAL"


def test_m6_c1_pass_valuer_properly_credentialed():
    f = facts(valuation_report_present=True, valuer_rbi_empanelled=True, valuer_registered_under_rvact=True)
    r = result_for(run_all_modules(f, modules_to_run=["M6"]), "M6_C1")
    assert r.status == "PASS"


# ── M6_C2 — valuation age ───────────────────────────────────────────────────

def test_m6_c2_fail_stale_valuation():
    f = facts(valuation_date=date(2024, 1, 1), auction_date=date(2024, 12, 1))
    r = result_for(run_all_modules(f, modules_to_run=["M6"]), "M6_C2")
    assert r.status == "FAIL"
    assert r.severity == "CURABLE"


def test_m6_c2_pass_fresh_valuation():
    f = facts(valuation_date=date(2024, 10, 1), auction_date=date(2024, 12, 1))
    r = result_for(run_all_modules(f, modules_to_run=["M6"]), "M6_C2")
    assert r.status == "PASS"


# ── M6_C3 — reserve price vs valuation ──────────────────────────────────────

def test_m6_c3_fail_undervalued():
    f = facts(reserve_price=500000, valuation_amount=1000000)
    r = result_for(run_all_modules(f, modules_to_run=["M6"]), "M6_C3")
    assert r.status == "FAIL"
    assert r.severity == "CURABLE"


def test_m6_c3_pass_adequate_reserve_price():
    f = facts(reserve_price=900000, valuation_amount=1000000)
    r = result_for(run_all_modules(f, modules_to_run=["M6"]), "M6_C3")
    assert r.status == "PASS"


# ── M6_C4 — valuation must predate sale notice ──────────────────────────────

def test_m6_c4_fail_sale_notice_before_valuation():
    f = facts(valuation_date=date(2025, 2, 1), sale_notice_date=date(2025, 1, 1))
    r = result_for(run_all_modules(f, modules_to_run=["M6"]), "M6_C4")
    assert r.status == "FAIL"
    assert r.severity == "FATAL"


def test_m6_c4_pass_valuation_before_sale_notice():
    f = facts(valuation_date=date(2025, 1, 1), sale_notice_date=date(2025, 2, 1))
    r = result_for(run_all_modules(f, modules_to_run=["M6"]), "M6_C4")
    assert r.status == "PASS"


def test_only_m6_rules_returned():
    f = facts()
    results = run_all_modules(f, modules_to_run=["M6"])
    assert all(r.module == "M6_VALUATION" for r in results)
    assert {r.rule_id for r in results} == {"M6_C1", "M6_C2", "M6_C3", "M6_C4"}
