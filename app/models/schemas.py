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
    detail: dict[str, Any] = field(default_factory=dict)
    judgment_tags: list[str] = field(default_factory=list)
    ground_codes: list[str] = field(default_factory=list)
