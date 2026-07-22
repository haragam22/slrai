"""M2 (bank reply compliance) rule tests — confirmed facts injected manually, no DB."""
from datetime import date

from app.services.compliance.engine import run_all_modules


def cf(value):
    return {"value": value, "human_confirmed": True}


def facts(**kwargs) -> dict:
    return {k: cf(v) for k, v in kwargs.items()}


def result_for(results, rule_id):
    return next(r for r in results if r.rule_id == rule_id)


# ── M2_C1 — reply not given ─────────────────────────────────────────────────

def test_m2_c1_fail_no_reply():
    f = facts(objection_filed=True, objection_date=date(2025, 1, 1), bank_reply_given=False)
    results = run_all_modules(f, modules_to_run=["M2"])
    r = result_for(results, "M2_C1")
    assert r.status == "FAIL"
    assert r.severity == "FATAL"


def test_m2_c1_not_applicable_no_objection():
    f = facts(objection_filed=False)
    results = run_all_modules(f, modules_to_run=["M2"])
    r = result_for(results, "M2_C1")
    assert r.status == "PASS"  # precondition unmet = not applicable


def test_m2_c1_unknown_objection_not_confirmed():
    f = facts()
    results = run_all_modules(f, modules_to_run=["M2"])
    r = result_for(results, "M2_C1")
    assert r.status == "UNKNOWN"


# ── M2_C2 — reply within 15 days ────────────────────────────────────────────

def test_m2_c2_fail_late_reply():
    f = facts(
        objection_filed=True,
        bank_reply_given=True,
        objection_date=date(2025, 1, 1),
        bank_reply_date=date(2025, 1, 25),  # 24 days
    )
    results = run_all_modules(f, modules_to_run=["M2"])
    r = result_for(results, "M2_C2")
    assert r.status == "FAIL"
    assert r.severity == "FATAL"


def test_m2_c2_pass_timely_reply():
    f = facts(
        objection_filed=True,
        bank_reply_given=True,
        objection_date=date(2025, 1, 1),
        bank_reply_date=date(2025, 1, 10),  # 9 days
    )
    results = run_all_modules(f, modules_to_run=["M2"])
    r = result_for(results, "M2_C2")
    assert r.status == "PASS"


# ── M2_C3 — reasoned reply ──────────────────────────────────────────────────

def test_m2_c3_fail_unreasoned_reply():
    f = facts(bank_reply_given=True, bank_reply_gives_reasons=False)
    results = run_all_modules(f, modules_to_run=["M2"])
    r = result_for(results, "M2_C3")
    assert r.status == "FAIL"
    assert r.severity == "CURABLE"


def test_m2_c3_pass_reasoned_reply():
    f = facts(bank_reply_given=True, bank_reply_gives_reasons=True)
    results = run_all_modules(f, modules_to_run=["M2"])
    r = result_for(results, "M2_C3")
    assert r.status == "PASS"


def test_m2_c3_not_applicable_no_reply():
    f = facts(bank_reply_given=False)
    results = run_all_modules(f, modules_to_run=["M2"])
    r = result_for(results, "M2_C3")
    assert r.status == "PASS"


# ── module scoping ──────────────────────────────────────────────────────────

def test_only_m2_rules_returned():
    f = facts()
    results = run_all_modules(f, modules_to_run=["M2"])
    assert all(r.module == "M2_REPLY_COMPLIANCE" for r in results)
    assert {r.rule_id for r in results} == {"M2_C1", "M2_C2", "M2_C3"}
