"""
Pre-intake filters.

Filter schedule:
  F2 — runs at case creation (cases.py POST /cases)
  F1, F3, F4 — run during Chain A after document extraction
  F5, F6 — run during Chain A alongside F1/F3/F4; non-terminating routing flags (v5.4)

PASS / action mapping:
  F1 → INTAKE_REJECTED  (agricultural land — statutory bar)
  F2 → INTAKE_REJECTED  (below minimum loan threshold — below Rs 1 lakh)
  F3 → INTAKE_REJECTED  (>80% of loan repaid — enforcement unnecessary)
  F4 → DO_NOT_PROCEED_CRITICAL  (IBC moratorium active — stay enforcement)
  F5 → ROUTE_TO_M10  (non-terminating — third party applicant, not borrower/guarantor)
  F6 → HIGH_THRESHOLD_CHALLENGE  (non-terminating — sale certificate already issued)

run_f2_filter returns None when the filter does NOT fire (principal is OK).
run_pre_intake_filters_chain_a returns None when no filter fires.
run_route_flags returns [] when neither F5 nor F6 fires — unlike F1/F3/F4 these
do not terminate the pipeline, so they are collected as a list rather than
short-circuiting on first match.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


SARFAESI_MIN_LOAN_AMOUNT = Decimal("100000")


class IntakeFilterResult(BaseModel):
    passed: bool
    filter_id: str
    result_label: str
    reason: str
    action: str


# ─── F2 ──────────────────────────────────────────────────────────────────────

def run_f2_filter(
    principal_amount: Optional[Decimal],
) -> Optional[IntakeFilterResult]:
    """Runs at case creation. Returns None if filter did not fire (amount is OK)."""
    if principal_amount is None:
        return None
    if principal_amount < SARFAESI_MIN_LOAN_AMOUNT:
        return IntakeFilterResult(
            passed=False,
            filter_id="F2",
            result_label="BELOW_MINIMUM_THRESHOLD",
            reason=(
                f"Principal amount ₹{principal_amount:,.2f} is below the SARFAESI minimum "
                f"threshold of ₹{SARFAESI_MIN_LOAN_AMOUNT:,.2f} (Section 2(1)(o))."
            ),
            action="INTAKE_REJECTED",
        )
    return None


# ─── F1, F3, F4 (Chain A) ─────────────────────────────────────────────────────

def _run_f1(facts: dict) -> Optional[IntakeFilterResult]:
    secured_asset_type = facts.get("secured_asset_type")
    if secured_asset_type and str(secured_asset_type).lower() == "agricultural_land":
        return IntakeFilterResult(
            passed=False,
            filter_id="F1",
            result_label="AGRICULTURAL_LAND_STATUTORY_BAR",
            reason=(
                "SARFAESI Act does not apply to agricultural land "
                "(Section 31(i)). Enforcement action cannot proceed."
            ),
            action="INTAKE_REJECTED",
        )
    return None


def _run_f3(facts: dict) -> Optional[IntakeFilterResult]:
    try:
        amount_repaid = Decimal(str(facts.get("amount_repaid") or "0"))
        principal = Decimal(str(facts.get("principal_loan_amount") or "0"))
    except Exception:
        return None

    if principal > 0 and (amount_repaid / principal) > Decimal("0.80"):
        repaid_pct = int((amount_repaid / principal) * 100)
        return IntakeFilterResult(
            passed=False,
            filter_id="F3",
            result_label="SUBSTANTIAL_REPAYMENT",
            reason=(
                f"Borrower has repaid {repaid_pct}% of principal (>80%). "
                "SARFAESI enforcement at this stage is disproportionate and "
                "may not survive judicial scrutiny."
            ),
            action="INTAKE_REJECTED",
        )
    return None


def _run_f4(facts: dict) -> Optional[IntakeFilterResult]:
    ibc_moratorium_active = str(facts.get("ibc_moratorium_active") or "").lower()
    if ibc_moratorium_active in ("true", "yes", "1"):
        return IntakeFilterResult(
            passed=False,
            filter_id="F4",
            result_label="IBC_MORATORIUM_ACTIVE",
            reason=(
                "IBC moratorium is active (Section 14, Insolvency and Bankruptcy Code 2016). "
                "SARFAESI enforcement is stayed during the moratorium period."
            ),
            action="DO_NOT_PROCEED_CRITICAL",
        )
    return None


def run_pre_intake_filters_chain_a(
    case_facts: dict,
) -> Optional[IntakeFilterResult]:
    """Runs F1, F3, F4 in sequence during Chain A. Returns first triggered filter or None."""
    for fn in (_run_f1, _run_f3, _run_f4):
        result = fn(case_facts)
        if result is not None:
            return result
    return None


# ─── F5, F6 (Chain A — non-terminating routing flags, v5.4) ─────────────────

def _run_f5(facts: dict) -> Optional[dict]:
    """F5 — third party applicant (non-borrower / non-guarantor). Routes to M10."""
    applicant_type = facts.get("sa_applicant_type")
    if applicant_type not in (None, "BORROWER", "GUARANTOR"):
        return {
            "filter_id": "F5",
            "result_label": "ROUTE_TO_M10",
            "reason": (
                f"SA applicant is {applicant_type} — not the borrower or guarantor. "
                "Module M10 (Third Party Rights) will be the primary analysis "
                "framework. M1-M9 still run for procedural compliance. DRT may "
                "raise preliminary maintainability objection."
            ),
        }
    return None


def _run_f6(facts: dict) -> Optional[dict]:
    """F6 — auction already completed (sale certificate issued)."""
    if str(facts.get("sale_certificate_issued") or "").lower() in ("true", "yes", "1"):
        return {
            "filter_id": "F6",
            "result_label": "HIGH_THRESHOLD_CHALLENGE",
            "reason": (
                f"Sale certificate issued on "
                f"{facts.get('sale_certificate_date', 'unknown date')}. The auction "
                "has been completed and sale confirmed. Setting aside the sale now "
                "requires fundamental procedural error or fraud per Celir LLP v. "
                "Bafna Motors (2023) 13 SCC 561. M3 rules will assess whether "
                "M3_C6/M3_C7/M3_C8 apply — these are the grounds that can clear "
                "the Celir LLP threshold."
            ),
        }
    return None


def run_route_flags(case_facts: dict) -> list[dict]:
    """Runs F5, F6 during Chain A. Non-terminating — returns every flag that fires."""
    flags = []
    for fn in (_run_f5, _run_f6):
        result = fn(case_facts)
        if result is not None:
            flags.append(result)
    return flags
