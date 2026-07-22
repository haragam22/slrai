"""M7 (multi-party notice) rule tests — confirmed facts injected manually, no DB."""
from app.services.compliance.engine import run_all_modules


def cf(value):
    return {"value": value, "human_confirmed": True}


def facts(**kwargs) -> dict:
    return {k: cf(v) for k, v in kwargs.items()}


def result_for(results, rule_id):
    return next(r for r in results if r.rule_id == rule_id)


# ── M7_C1 — all co-borrowers served ─────────────────────────────────────────

def test_m7_c1_fail_unserved_borrower():
    f = facts(total_borrowers_in_loan=3, borrowers_served_notice=2)
    r = result_for(run_all_modules(f, modules_to_run=["M7"]), "M7_C1")
    assert r.status == "FAIL"
    assert r.severity == "FATAL"


def test_m7_c1_pass_all_served():
    f = facts(total_borrowers_in_loan=3, borrowers_served_notice=3)
    r = result_for(run_all_modules(f, modules_to_run=["M7"]), "M7_C1")
    assert r.status == "PASS"


# ── M7_C2 — all guarantors served ───────────────────────────────────────────

def test_m7_c2_fail_unserved_guarantor():
    f = facts(total_guarantors_in_loan=2, guarantors_served_notice=1)
    r = result_for(run_all_modules(f, modules_to_run=["M7"]), "M7_C2")
    assert r.status == "FAIL"
    assert r.severity == "FATAL"


def test_m7_c2_pass_all_served():
    f = facts(total_guarantors_in_loan=2, guarantors_served_notice=2)
    r = result_for(run_all_modules(f, modules_to_run=["M7"]), "M7_C2")
    assert r.status == "PASS"


def test_only_m7_rules_returned():
    f = facts()
    results = run_all_modules(f, modules_to_run=["M7"])
    assert all(r.module == "M7_MULTIPARTY_NOTICE" for r in results)
    assert {r.rule_id for r in results} == {"M7_C1", "M7_C2"}
