"""M9 (MSME) rule tests — confirmed facts injected manually, no DB."""
from app.services.compliance.engine import run_all_modules


def cf(value):
    return {"value": value, "human_confirmed": True}


def facts(**kwargs) -> dict:
    return {k: cf(v) for k, v in kwargs.items()}


def result_for(results, rule_id):
    return next(r for r in results if r.rule_id == rule_id)


# ── M9_C1 — MSME status must be confirmed ───────────────────────────────────

def test_m9_c1_unknown_no_udyam_cert():
    f = facts(msme_claimed_by_borrower=True, udyam_cert_in_bank_file=False)
    r = result_for(run_all_modules(f, modules_to_run=["M9"]), "M9_C1")
    assert r.status == "UNKNOWN"
    assert r.severity == "REVIEW_REQUIRED"


def test_m9_c1_pass_udyam_cert_present():
    f = facts(msme_claimed_by_borrower=True, udyam_cert_in_bank_file=True)
    r = result_for(run_all_modules(f, modules_to_run=["M9"]), "M9_C1")
    assert r.status == "PASS"


def test_m9_c1_not_applicable_no_msme_claim():
    f = facts(msme_claimed_by_borrower=False)
    r = result_for(run_all_modules(f, modules_to_run=["M9"]), "M9_C1")
    assert r.status == "PASS"


# ── M9_C2 — restructuring offered pre-NPA ───────────────────────────────────

def test_m9_c2_fail_restructuring_not_offered():
    f = facts(udyam_cert_in_bank_file=True, restructuring_offered_pre_npa=False)
    r = result_for(run_all_modules(f, modules_to_run=["M9"]), "M9_C2")
    assert r.status == "FAIL"
    assert r.severity == "CURABLE"


def test_m9_c2_pass_restructuring_offered():
    f = facts(udyam_cert_in_bank_file=True, restructuring_offered_pre_npa=True)
    r = result_for(run_all_modules(f, modules_to_run=["M9"]), "M9_C2")
    assert r.status == "PASS"


def test_only_m9_rules_returned():
    f = facts()
    results = run_all_modules(f, modules_to_run=["M9"])
    assert all(r.module == "M9_MSME" for r in results)
    assert {r.rule_id for r in results} == {"M9_C1", "M9_C2"}
