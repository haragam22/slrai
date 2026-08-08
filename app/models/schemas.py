"""Pydantic v2 request/response schemas + CaseFactSchema."""
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class RuleResult:
    """Result of evaluating one compliance rule against confirmed case facts.

    ground_codes carries the SA ground(s) this rule's failure supports —
    consumed by scoring (H6) to link compliance failures to ground strength.
    Not persisted to compliance_results (no matching column); judgment_tags is.
    """
    rule_id: str
    module: str
    status: str  # PASS | FAIL | UNKNOWN
    severity: Optional[str]
    message: str
    outcome_favors: str = "BANK"  # BANK | BORROWER | NEUTRAL — who this finding favors,
    # independent of the status label (a rule author can call a bank-favorable
    # finding "PASS" or "FAIL" depending on how the check reads; this is the
    # actual direction scoring needs). Defaults BANK only for the "no check
    # fired, record is clean" fallthrough — every check-driven result must
    # set this explicitly in its YAML (see engine.py).
    detail: dict[str, Any] = field(default_factory=dict)
    judgment_tags: list[str] = field(default_factory=list)
    ground_codes: list[str] = field(default_factory=list)
