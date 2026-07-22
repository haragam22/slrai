"""M4 (limitation) rule tests — confirmed facts injected manually, no DB."""
from datetime import date

from app.services.compliance.engine import run_all_modules


def cf(value):
    return {"value": value, "human_confirmed": True}


def facts(**kwargs) -> dict:
    return {k: cf(v) for k, v in kwargs.items()}


def result_for(results, rule_id):
    return next(r for r in results if r.rule_id == rule_id)


# ── M4_C1 — 45-day limitation ───────────────────────────────────────────────

def test_m4_c1_fail_time_barred():
    f = facts(measure_date=date(2025, 1, 1), sa_filing_date=date(2025, 3, 1))
    r = result_for(run_all_modules(f, modules_to_run=["M4"]), "M4_C1")
    assert r.status == "FAIL"
    assert r.severity == "ABSOLUTE_BAR"


def test_m4_c1_pass_within_time():
    f = facts(measure_date=date(2025, 1, 1), sa_filing_date=date(2025, 1, 20))
    r = result_for(run_all_modules(f, modules_to_run=["M4"]), "M4_C1")
    assert r.status == "PASS"


# ── M4_C2 — measure type identified ─────────────────────────────────────────

def test_m4_c2_unknown_measure_type():
    f = facts(measure_type=None)
    r = result_for(run_all_modules(f, modules_to_run=["M4"]), "M4_C2")
    assert r.status == "UNKNOWN"


def test_m4_c2_pass_measure_type_identified():
    f = facts(measure_type="possession_notice")
    r = result_for(run_all_modules(f, modules_to_run=["M4"]), "M4_C2")
    assert r.status == "PASS"


# ── M4_C3 — auction-specific limitation ─────────────────────────────────────

def test_m4_c3_fail_auction_challenge_time_barred():
    f = facts(auction_date=date(2025, 1, 1), sa_filing_date=date(2025, 3, 1))
    r = result_for(run_all_modules(f, modules_to_run=["M4"]), "M4_C3")
    assert r.status == "FAIL"
    assert r.severity == "ABSOLUTE_BAR"


def test_m4_c3_pass_auction_challenge_within_time():
    f = facts(auction_date=date(2025, 1, 1), sa_filing_date=date(2025, 1, 20))
    r = result_for(run_all_modules(f, modules_to_run=["M4"]), "M4_C3")
    assert r.status == "PASS"


# ── M4_C5 — prayer scope mismatch (Oasis Dealcom) ───────────────────────────

def test_m4_c5_fail_prayer_scope_mismatch():
    f = facts(auction_date=date(2025, 1, 1), challenges_auction=False, challenges_demand_notice=True)
    r = result_for(run_all_modules(f, modules_to_run=["M4"]), "M4_C5")
    assert r.status == "FAIL"
    assert r.severity == "ADVISORY"


def test_m4_c5_pass_prayer_scope_covers_auction():
    f = facts(auction_date=date(2025, 1, 1), challenges_auction=True, challenges_demand_notice=False)
    r = result_for(run_all_modules(f, modules_to_run=["M4"]), "M4_C5")
    assert r.status == "PASS"


def test_only_m4_rules_returned():
    f = facts()
    results = run_all_modules(f, modules_to_run=["M4"])
    assert all(r.module == "M4_LIMITATION" for r in results)
    assert {r.rule_id for r in results} == {"M4_C1", "M4_C2", "M4_C3", "M4_C5"}
