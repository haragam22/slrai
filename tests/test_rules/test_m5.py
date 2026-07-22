"""M5 (tenancy) rule tests — confirmed facts injected manually, no DB.

CRITICAL: statuses are PASS or FAIL only — never PASS_FAVORABLE (not a valid
DB status). "Bank favorable" outcomes are still status=PASS.
"""
from datetime import date

from app.services.compliance.engine import run_all_modules

VALID_STATUSES = {"PASS", "FAIL", "UNKNOWN"}


def cf(value):
    return {"value": value, "human_confirmed": True}


def facts(**kwargs) -> dict:
    return {k: cf(v) for k, v in kwargs.items()}


def result_for(results, rule_id):
    return next(r for r in results if r.rule_id == rule_id)


# ── M5_C1 — lease after mortgage (bank favorable) ───────────────────────────

def test_m5_c1_pass_lease_after_mortgage():
    f = facts(tenancy_claimed=True, lease_date=date(2025, 2, 1), mortgage_date=date(2025, 1, 1))
    r = result_for(run_all_modules(f, modules_to_run=["M5"]), "M5_C1")
    assert r.status == "PASS"
    assert r.status in VALID_STATUSES  # never PASS_FAVORABLE


def test_m5_c1_not_applicable_no_tenancy_claim():
    f = facts(tenancy_claimed=False)
    r = result_for(run_all_modules(f, modules_to_run=["M5"]), "M5_C1")
    assert r.status == "PASS"


# ── M5_C2 — lease after demand notice ───────────────────────────────────────

def test_m5_c2_pass_lease_after_notice():
    f = facts(tenancy_claimed=True, lease_date=date(2025, 3, 1), demand_notice_date=date(2025, 1, 1))
    r = result_for(run_all_modules(f, modules_to_run=["M5"]), "M5_C2")
    assert r.status == "PASS"
    assert r.status in VALID_STATUSES


# ── M5_C3 — unregistered lease > 1 year ─────────────────────────────────────

def test_m5_c3_pass_unregistered_long_lease():
    f = facts(tenancy_claimed=True, lease_registered=False, lease_duration_months=24)
    r = result_for(run_all_modules(f, modules_to_run=["M5"]), "M5_C3")
    assert r.status == "PASS"
    assert r.status in VALID_STATUSES


# ── M5_C4 — registered pre-mortgage lease (borrower strong ground) ─────────

def test_m5_c4_fail_registered_pre_mortgage_lease():
    f = facts(
        tenancy_claimed=True,
        lease_date=date(2024, 1, 1),
        mortgage_date=date(2024, 6, 1),
        lease_registered=True,
    )
    r = result_for(run_all_modules(f, modules_to_run=["M5"]), "M5_C4")
    assert r.status == "FAIL"
    assert r.severity == "REVIEW_REQUIRED"


def test_m5_c4_pass_no_pre_mortgage_lease():
    f = facts(
        tenancy_claimed=True,
        lease_date=date(2024, 8, 1),
        mortgage_date=date(2024, 6, 1),
        lease_registered=True,
    )
    r = result_for(run_all_modules(f, modules_to_run=["M5"]), "M5_C4")
    assert r.status == "PASS"


def test_only_m5_rules_returned():
    f = facts()
    results = run_all_modules(f, modules_to_run=["M5"])
    assert all(r.module == "M5_TENANCY" for r in results)
    assert {r.rule_id for r in results} == {"M5_C1", "M5_C2", "M5_C3", "M5_C4"}
    assert all(r.status in VALID_STATUSES for r in results)
