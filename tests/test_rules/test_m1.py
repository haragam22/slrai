"""M1 (demand notice) rule tests — confirmed facts injected manually, no DB."""
from datetime import date

from app.services.compliance.engine import run_all_modules


def cf(value):
    return {"value": value, "human_confirmed": True}


def facts(**kwargs) -> dict:
    return {k: cf(v) for k, v in kwargs.items()}


def result_for(results, rule_id):
    return next(r for r in results if r.rule_id == rule_id)


# ── M1_C1 — 60-day period ───────────────────────────────────────────────────

def test_m1_c1_fail_period_not_elapsed():
    f = facts(
        demand_notice_date=date(2025, 1, 1),
        possession_notice_date=date(2025, 1, 30),  # only 29 days
    )
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C1")
    assert r.status == "FAIL"
    assert r.severity == "FATAL"


def test_m1_c1_pass_period_elapsed():
    f = facts(
        demand_notice_date=date(2025, 1, 1),
        possession_notice_date=date(2025, 3, 15),  # 73 days
    )
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C1")
    assert r.status == "PASS"


def test_m1_c1_unknown_precondition_missing():
    f = facts()
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C1")
    assert r.status == "UNKNOWN"


# ── M1_C2 — amount tolerance ────────────────────────────────────────────────

def test_m1_c2_fail_amount_discrepancy():
    f = facts(demand_notice_amount=1_000_000, actual_outstanding_amount=800_000)
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C2")
    assert r.status == "FAIL"
    assert r.severity == "CURABLE"


def test_m1_c2_pass_within_tolerance():
    f = facts(demand_notice_amount=1_000_000, actual_outstanding_amount=980_000)
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C2")
    assert r.status == "PASS"


# ── M1_C3 — service mode ────────────────────────────────────────────────────

def test_m1_c3_fail_invalid_service_mode():
    f = facts(notice_service_mode="whatsapp")
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C3")
    assert r.status == "FAIL"
    assert r.severity == "FATAL"


def test_m1_c3_pass_valid_service_mode():
    f = facts(notice_service_mode="registered_post_ad")
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C3")
    assert r.status == "PASS"


# ── M1_C4 — proof of service ────────────────────────────────────────────────

def test_m1_c4_fail_no_proof():
    f = facts(notice_dispatch_proof_present=False)
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C4")
    assert r.status == "FAIL"


def test_m1_c4_pass_proof_present():
    f = facts(notice_dispatch_proof_present=True)
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C4")
    assert r.status == "PASS"


# ── M1_C5 — service date consistency ────────────────────────────────────────

def test_m1_c5_fail_service_predates_notice():
    f = facts(
        demand_notice_date=date(2025, 2, 1),
        notice_service_date=date(2025, 1, 25),
    )
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C5")
    assert r.status == "FAIL"


def test_m1_c5_pass_service_after_notice():
    f = facts(
        demand_notice_date=date(2025, 2, 1),
        notice_service_date=date(2025, 2, 3),
    )
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C5")
    assert r.status == "PASS"


# ── M1_C6 — notice content complete ─────────────────────────────────────────

def test_m1_c6_fail_content_incomplete():
    f = facts(demand_notice_date=date(2025, 1, 1), notice_content_complete=False)
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C6")
    assert r.status == "FAIL"


def test_m1_c6_pass_content_complete():
    f = facts(demand_notice_date=date(2025, 1, 1), notice_content_complete=True)
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C6")
    assert r.status == "PASS"


# ── M1_C7 — moratorium before possession notice ─────────────────────────────

def test_m1_c7_fail_premature_possession_notice():
    f = facts(
        notice_service_date=date(2025, 1, 1),
        possession_notice_date=date(2025, 1, 20),  # only 19 days
    )
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C7")
    assert r.status == "FAIL"


def test_m1_c7_pass_after_moratorium():
    f = facts(
        notice_service_date=date(2025, 1, 1),
        possession_notice_date=date(2025, 3, 15),
    )
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C7")
    assert r.status == "PASS"


# ── M1_C8 — AO authorization ────────────────────────────────────────────────

def test_m1_c8_fail_no_authorization():
    f = facts(
        authorized_officer_name="R. Sharma",
        authorized_officer_designation="Chief Manager",
        ao_has_written_authorization=False,
    )
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C8")
    assert r.status == "FAIL"


def test_m1_c8_pass_has_authorization():
    f = facts(
        authorized_officer_name="R. Sharma",
        authorized_officer_designation="Chief Manager",
        ao_has_written_authorization=True,
    )
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C8")
    assert r.status == "PASS"


def test_m1_c8_unknown_no_ao_named():
    f = facts()
    results = run_all_modules(f, modules_to_run=["M1"])
    r = result_for(results, "M1_C8")
    assert r.status == "UNKNOWN"


# ── module scoping ──────────────────────────────────────────────────────────

def test_only_m1_rules_returned():
    f = facts()
    results = run_all_modules(f, modules_to_run=["M1"])
    assert all(r.module == "M1_DEMAND_NOTICE" for r in results)
    assert {r.rule_id for r in results} == {
        "M1_C1", "M1_C2", "M1_C3", "M1_C4", "M1_C5", "M1_C6", "M1_C7", "M1_C8",
    }
