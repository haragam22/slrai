"""M3 (auction gap) rule tests — confirmed facts injected manually, no DB."""
from datetime import date

from app.services.compliance.engine import run_all_modules


def cf(value):
    return {"value": value, "human_confirmed": True}


def facts(**kwargs) -> dict:
    return {k: cf(v) for k, v in kwargs.items()}


def result_for(results, rule_id):
    return next(r for r in results if r.rule_id == rule_id)


# ── M3_C1 — 30-day auction gap ──────────────────────────────────────────────

def test_m3_c1_fail_short_gap():
    f = facts(asset_type="immovable", sale_notice_date=date(2025, 1, 1), auction_date=date(2025, 1, 15))
    r = result_for(run_all_modules(f, modules_to_run=["M3"]), "M3_C1")
    assert r.status == "FAIL"
    assert r.severity == "FATAL"


def test_m3_c1_pass_sufficient_gap():
    f = facts(asset_type="immovable", sale_notice_date=date(2025, 1, 1), auction_date=date(2025, 2, 15))
    r = result_for(run_all_modules(f, modules_to_run=["M3"]), "M3_C1")
    assert r.status == "PASS"


def test_m3_c1_not_applicable_movable():
    f = facts(asset_type="movable")
    r = result_for(run_all_modules(f, modules_to_run=["M3"]), "M3_C1")
    assert r.status == "PASS"


# ── M3_C2 — newspaper publication ───────────────────────────────────────────

def test_m3_c2_fail_no_publication():
    f = facts(newspaper_publication_done=False)
    r = result_for(run_all_modules(f, modules_to_run=["M3"]), "M3_C2")
    assert r.status == "FAIL"


def test_m3_c2_pass_publication_done():
    f = facts(newspaper_publication_done=True)
    r = result_for(run_all_modules(f, modules_to_run=["M3"]), "M3_C2")
    assert r.status == "PASS"


# ── M3_C3 — reserve price stated ────────────────────────────────────────────

def test_m3_c3_fail_no_reserve_price():
    f = facts(sale_notice_date=date(2025, 1, 1), reserve_price=None)
    r = result_for(run_all_modules(f, modules_to_run=["M3"]), "M3_C3")
    assert r.status == "FAIL"


def test_m3_c3_pass_reserve_price_stated():
    f = facts(sale_notice_date=date(2025, 1, 1), reserve_price=500000)
    r = result_for(run_all_modules(f, modules_to_run=["M3"]), "M3_C3")
    assert r.status == "PASS"


# ── M3_C4 — possession before sale notice ───────────────────────────────────

def test_m3_c4_fail_sale_before_possession():
    f = facts(possession_notice_date=date(2025, 2, 1), sale_notice_date=date(2025, 1, 15))
    r = result_for(run_all_modules(f, modules_to_run=["M3"]), "M3_C4")
    assert r.status == "FAIL"


def test_m3_c4_pass_correct_order():
    f = facts(possession_notice_date=date(2025, 1, 1), sale_notice_date=date(2025, 2, 1))
    r = result_for(run_all_modules(f, modules_to_run=["M3"]), "M3_C4")
    assert r.status == "PASS"


# ── M3_C6 — notice not affixed at property ──────────────────────────────────

def test_m3_c6_fail_not_affixed():
    f = facts(auction_date=date(2025, 3, 1), auction_notice_affixed_on_property=False)
    r = result_for(run_all_modules(f, modules_to_run=["M3"]), "M3_C6")
    assert r.status == "FAIL"
    assert r.severity == "FATAL"


def test_m3_c6_pass_affixed():
    f = facts(auction_date=date(2025, 3, 1), auction_notice_affixed_on_property=True)
    r = result_for(run_all_modules(f, modules_to_run=["M3"]), "M3_C6")
    assert r.status == "PASS"


# ── M3_C7 — auction during operational stay (ABSOLUTE_BAR) ─────────────────

def test_m3_c7_fail_auction_during_stay():
    f = facts(
        auction_date=date(2025, 3, 1),
        drt_interim_stay_granted=True,
        drt_stay_order_date=date(2025, 2, 1),
        auction_conducted_despite_stay=True,
    )
    r = result_for(run_all_modules(f, modules_to_run=["M3"]), "M3_C7")
    assert r.status == "FAIL"
    assert r.severity == "ABSOLUTE_BAR"


def test_m3_c7_pass_stay_operational_but_auction_not_despite_it():
    # stay_was_operational_on_auction_date only ever resolves True or None
    # (never False) — a genuine PASS needs both preconditions confirmed
    # non-null with the check condition false.
    f = facts(
        auction_date=date(2025, 3, 1),
        drt_interim_stay_granted=True,
        drt_stay_order_date=date(2025, 2, 1),
        auction_conducted_despite_stay=False,
    )
    r = result_for(run_all_modules(f, modules_to_run=["M3"]), "M3_C7")
    assert r.status == "PASS"


def test_m3_c7_unknown_no_stay_confirmed():
    f = facts(auction_date=date(2025, 3, 1), auction_conducted_despite_stay=False)
    r = result_for(run_all_modules(f, modules_to_run=["M3"]), "M3_C7")
    assert r.status == "UNKNOWN"


# ── M3_C8 — pending SA concealed ────────────────────────────────────────────

def test_m3_c8_fail_concealed():
    f = facts(pending_sa_existed_at_auction_date=True, auction_notice_discloses_pending_sa=False)
    r = result_for(run_all_modules(f, modules_to_run=["M3"]), "M3_C8")
    assert r.status == "FAIL"
    assert r.severity == "FATAL"


def test_m3_c8_pass_disclosed():
    f = facts(pending_sa_existed_at_auction_date=True, auction_notice_discloses_pending_sa=True)
    r = result_for(run_all_modules(f, modules_to_run=["M3"]), "M3_C8")
    assert r.status == "PASS"


def test_only_m3_rules_returned():
    f = facts()
    results = run_all_modules(f, modules_to_run=["M3"])
    assert all(r.module == "M3_AUCTION_GAP" for r in results)
    assert {r.rule_id for r in results} == {
        "M3_C1", "M3_C2", "M3_C3", "M3_C4", "M3_C6", "M3_C7", "M3_C8",
    }
