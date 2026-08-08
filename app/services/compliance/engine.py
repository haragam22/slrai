"""YAML rule interpreter using simpleeval — never eval().

See SLRAI_Blueprint_v5.md Section 13 (interpreter contract) and Section 14
(module rule definitions).
"""
from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional

import yaml
from simpleeval import EvalWithCompoundTypes

from app.models.schemas import RuleResult

RULES_DIR = Path(__file__).parent / "rules"

_DATE_FORMATS = ("%d.%m.%Y", "%Y-%m-%d")


def _coerce_stored_value(raw: str) -> Any:
    """CaseFact.field_value is always stored as text. Convert to the typed
    value rule expressions expect: bool, float, date, or leave as string."""
    if raw in ("True", "true"):
        return True
    if raw in ("False", "false"):
        return False
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    try:
        return float(raw) if "." in raw or "e" in raw.lower() else int(raw)
    except ValueError:
        pass
    return raw


def load_confirmed_facts(case_id: str, db) -> dict:
    """Load human_confirmed=True case_facts for a case, in the shape
    run_all_modules()/evaluate_rule() expect: {field_name: {"value": ..., "human_confirmed": True}}.
    """
    from app.models.db import CaseFact

    rows = db.query(CaseFact).filter_by(case_id=case_id, human_confirmed=True).all()
    confirmed_facts = {}
    for row in rows:
        if row.field_value is None:
            continue
        confirmed_facts[row.field_name] = {
            "value": _coerce_stored_value(row.field_value),
            "human_confirmed": True,
        }
    return confirmed_facts


def load_all_rules() -> list[dict]:
    """Load all YAML rule files. Called once per run_all_modules() call."""
    rules = []
    for yaml_file in sorted(RULES_DIR.glob("*.yaml")):
        with open(yaml_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            rules.extend((data or {}).get("rules", []))
    return rules


# Fields that are NEVER stored in case_facts — always computed from raw
# confirmed facts at rule-evaluation time. See CLAUDE_v51.md.
COMPUTED_FIELD_RESOLVERS: dict = {
    # ── EXISTING (v5.3) ──────────────────────────────────────────────────
    "sixty_day_period_elapsed": lambda f: (
        ((f.get("possession_notice_date") or f.get("sale_notice_date")) -
         max(f.get("demand_notice_date"), f.get("notice_service_date") or f.get("demand_notice_date"))).days >= 60
        if all(v for v in [
            f.get("demand_notice_date"),
            f.get("possession_notice_date") or f.get("sale_notice_date"),
        ]) else None
    ),
    "reply_days_elapsed": lambda f: (
        (f["bank_reply_date"] - f["objection_date"]).days
        if f.get("bank_reply_date") and f.get("objection_date") else None
    ),
    "auction_gap_days": lambda f: (
        (f["auction_date"] - f["sale_notice_date"]).days
        if f.get("auction_date") and f.get("sale_notice_date") else None
    ),
    "days_from_measure_to_sa": lambda f: (
        (f["sa_filing_date"] - f["measure_date"]).days
        if f.get("sa_filing_date") and f.get("measure_date") else None
    ),
    "lease_predates_mortgage": lambda f: (
        f["lease_date"] < f["mortgage_date"]
        if f.get("lease_date") and f.get("mortgage_date") else None
    ),
    "lease_post_default_notice": lambda f: (
        f["lease_date"] > f["demand_notice_date"]
        if f.get("lease_date") and f.get("demand_notice_date") else None
    ),
    "reserve_price_vs_valuation_pct": lambda f: (
        float(f["reserve_price"] / f["valuation_amount"] * 100)
        if f.get("reserve_price") and f.get("valuation_amount") else None
    ),
    "valuation_age_at_auction_days": lambda f: (
        (f["auction_date"] - f["valuation_date"]).days
        if f.get("auction_date") and f.get("valuation_date") else None
    ),
    "all_borrowers_served": lambda f: (
        f["borrowers_served_notice"] >= f["total_borrowers_in_loan"]
        if f.get("borrowers_served_notice") is not None and f.get("total_borrowers_in_loan") else None
    ),
    "all_guarantors_served": lambda f: (
        f["guarantors_served_notice"] >= f["total_guarantors_in_loan"]
        if f.get("guarantors_served_notice") is not None and f.get("total_guarantors_in_loan") else None
    ),
    "days_from_last_payment_to_npa": lambda f: (
        (f["npa_classification_date"] - f["date_of_last_payment"]).days
        if f.get("npa_classification_date") and f.get("date_of_last_payment") else None
    ),

    # ── NEW (v5.4) ───────────────────────────────────────────────────────
    "stay_was_operational_on_auction_date": lambda f: (
        True if (f.get("drt_interim_stay_granted") is True
                 and f.get("drt_stay_order_date") is not None
                 and f.get("auction_date") is not None
                 and f["drt_stay_order_date"] <= f["auction_date"])
        else None
    ),
    "right_of_redemption_extinguished": lambda f: (
        True if f.get("sale_certificate_issued") is True else None
    ),
    "ats_predates_mortgage": lambda f: (
        f["ats_date"] < f["mortgage_date"]
        if f.get("ats_date") and f.get("mortgage_date") else None
    ),
    "ats_simultaneous_mortgage": lambda f: (
        f["ats_date"] == f["mortgage_date"]
        if f.get("ats_date") and f.get("mortgage_date") else None
    ),
    "account_standard_at_auction_date": lambda f: (
        f.get("payments_post_npa_total", 0) >= f.get("overdue_amount_at_auction_date", float("inf"))
        if f.get("payments_post_npa_total") and f.get("overdue_amount_at_auction_date") else None
    ),
    "prayer_scope_covers_current_measure": lambda f: (
        # True if the borrower's SA prayer challenges the enforcement measure
        # currently at issue (Oasis Dealcom fresh-cause-of-action reasoning —
        # see v5.4 Block 1 / M4_C5). Only computable once challenges_auction
        # (or an equivalent per-measure prayer flag) has been confirmed.
        f.get("challenges_auction")
        if f.get("challenges_auction") is not None else None
    ),

    # Rule 9(4) SI Enforcement Rules — auction purchaser must pay the
    # balance 75% consideration within 90 days of the sale/auction, or the
    # sale never attains statutory finality (M10_C7).
    "balance_consideration_paid_within_90_days": lambda f: (
        (f["balance_payment_date"] - f["auction_date"]).days <= 90
        if f.get("balance_payment_date") and f.get("auction_date") else None
    ),
}


def _flatten_confirmed_facts(confirmed_facts: dict) -> dict:
    """confirmed_facts is {field_name: {"value": ..., "human_confirmed": bool}}.
    COMPUTED_FIELD_RESOLVERS lambdas expect flat {field_name: value} — only
    confirmed raw fields are exposed to them."""
    return {
        k: v.get("value")
        for k, v in confirmed_facts.items()
        if isinstance(v, dict) and v.get("human_confirmed") and v.get("value") is not None
    }


def _get_fact_value(field_name: str, confirmed_facts: dict) -> Any:
    """
    Returns confirmed value for a field, or None.
    For computed fields: calculates from raw confirmed facts inline.
    Raw facts are never overridden by stale computed values in DB.
    """
    if field_name in COMPUTED_FIELD_RESOLVERS:
        try:
            return COMPUTED_FIELD_RESOLVERS[field_name](_flatten_confirmed_facts(confirmed_facts))
        except Exception:
            return None

    fact = confirmed_facts.get(field_name)
    if fact is None or not fact.get("human_confirmed", False):
        return None
    return fact.get("value")


def safe_format(template: str, names: dict) -> str:
    """Format template, replacing missing vars with [UNKNOWN].
    Factory must take zero args — defaultdict(lambda k=None: ...) is wrong.
    """
    safe_names = defaultdict(lambda: "[UNKNOWN]", names)
    try:
        return template.format_map(safe_names)
    except Exception:
        return template


def evaluate_rule(rule: dict, confirmed_facts: dict) -> RuleResult:
    """
    Evaluates a single rule against confirmed facts.
    Returns RuleResult with status PASS / FAIL / UNKNOWN.
    """
    rule_id = rule["rule_id"]
    module = rule["module"]

    # Step 1: Check preconditions
    for pre in rule.get("preconditions", []):
        field_val = _get_fact_value(pre["field"], confirmed_facts)
        if field_val is None:
            return RuleResult(
                rule_id=rule_id, module=module,
                status="UNKNOWN", severity="UNKNOWN", outcome_favors="NEUTRAL",
                message=f"Precondition field '{pre['field']}' not confirmed. "
                        f"Cannot evaluate {rule_id}.",
                detail={},
                judgment_tags=[],
            )
        expected = pre.get("value")
        op = pre.get("operator", "eq")
        if op == "is_not_null":
            continue  # already confirmed non-null above
        if op == "eq" and field_val != expected:
            return RuleResult(
                rule_id=rule_id, module=module,
                status="PASS",  # not applicable = not a problem
                severity=None, outcome_favors="BANK",
                message=f"Rule {rule_id} not applicable: precondition '{pre['field']}' is {field_val}.",
                detail={}, judgment_tags=[],
            )

    # Step 2: Build names dict for simpleeval — only confirmed facts included.
    # A raw field that was confirmed as explicitly null (officer confirmed
    # "not present") must still appear as None so `field == None` checks can
    # fire — distinct from a field that was never confirmed at all, which
    # must stay absent so the expression raises NameNotDefined -> UNKNOWN.
    names = {}
    for field_name, fact in confirmed_facts.items():
        if field_name in COMPUTED_FIELD_RESOLVERS:
            continue  # computed fields are never stored raw — always derived below
        if isinstance(fact, dict) and fact.get("human_confirmed"):
            names[field_name] = fact.get("value")
    # also expose any computed field whose raw inputs are confirmed
    for computed_name in COMPUTED_FIELD_RESOLVERS:
        val = _get_fact_value(computed_name, confirmed_facts)
        if val is not None:
            names[computed_name] = val

    # Step 3: Evaluate each check
    for check in rule.get("checks", []):
        expression = check["expression"]
        try:
            evaluator = EvalWithCompoundTypes(names=names, functions={"abs": abs})
            result = evaluator.eval(expression)
        except Exception as e:
            return RuleResult(
                rule_id=rule_id, module=module,
                status="UNKNOWN", severity="UNKNOWN", outcome_favors="NEUTRAL",
                message=f"Cannot evaluate {rule_id}: required fact not confirmed. ({e})",
                detail={"expression": expression},
                judgment_tags=check.get("judgment_tags", []),
            )

        if result:
            message = safe_format(check["message_template"], names)
            # outcome_favors is mandatory per check — a rule author must say
            # who this specific finding favors; the status label (PASS/FAIL/
            # REVIEW) is not a reliable proxy for that (see compliance_score.py).
            if "outcome_favors" not in check:
                raise KeyError(
                    f"{rule_id}/{check.get('check_id', '?')}: missing required "
                    f"'outcome_favors' field (BANK/BORROWER/NEUTRAL)"
                )
            return RuleResult(
                rule_id=rule_id, module=module,
                status=check["result_if_true"],
                severity=check["severity"],
                outcome_favors=check["outcome_favors"],
                message=message,
                detail={"expression": expression, "evaluated_names": {
                    k: str(v) for k, v in names.items()
                }},
                judgment_tags=check.get("judgment_tags", []),
            )

    # Step 4: All checks passed — no defect found, a clean record is bank-favorable.
    pass_message = safe_format(rule.get("pass_message_template", "Rule passed."), names)

    return RuleResult(
        rule_id=rule_id, module=module,
        status="PASS", severity=None, outcome_favors="BANK",
        message=pass_message,
        detail={}, judgment_tags=[],
    )


def run_all_modules(
    confirmed_facts: dict,
    modules_to_run: Optional[list[str]] = None,
) -> list[RuleResult]:
    """
    Run specified compliance modules against confirmed case facts.
    If modules_to_run is None, runs M1-M9. M10 only runs when explicitly
    passed (see H8 — third-party applicant routing).
    """
    if modules_to_run is None:
        modules_to_run = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9"]

    all_rules = load_all_rules()
    results = []
    for rule in all_rules:
        module_prefix = rule["module"].split("_")[0]
        if module_prefix not in modules_to_run:
            continue
        result = evaluate_rule(rule, confirmed_facts)
        if result:
            results.append(result)
    return results
