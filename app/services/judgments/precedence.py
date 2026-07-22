"""Conflict resolver for competing judgments; raises LegalUncertaintyException."""
from __future__ import annotations

COURT_RANK = {
    "SUPREME_COURT": 4,
    "HIGH_COURT":    3,
    "DRAT":          2,
    "DRT":           1,
}


class LegalUncertaintyException(Exception):
    pass


def resolve_conflict(j1: dict, j2: dict) -> dict:
    """Returns the judgment that takes precedence. Raises LegalUncertaintyException
    on genuine ambiguity (same court rank, same bench strength, same date) —
    that case must be flagged for human lawyer review, never auto-resolved."""
    r1, r2 = COURT_RANK[j1["court"]], COURT_RANK[j2["court"]]
    if r1 != r2:
        return j1 if r1 > r2 else j2
    if j1["bench_strength"] != j2["bench_strength"]:
        return j1 if j1["bench_strength"] > j2["bench_strength"] else j2
    if j1["judgment_date"] != j2["judgment_date"]:
        return j1 if j1["judgment_date"] > j2["judgment_date"] else j2
    raise LegalUncertaintyException(
        f"Unresolvable conflict between {j1['citation']} and {j2['citation']}. "
        f"Flag as LEGAL_UNCERTAINTY. Human lawyer review required."
    )


def resolve_conflicts_for_ground(judgments: list[dict]) -> dict:
    """Reduces a list of applicable judgments for one ground code to a single
    controlling precedent. Returns {"controlling": dict} or
    {"controlling": None, "uncertainty_reason": str} if unresolvable."""
    if not judgments:
        return {"controlling": None}
    controlling = judgments[0]
    for candidate in judgments[1:]:
        try:
            controlling = resolve_conflict(controlling, candidate)
        except LegalUncertaintyException as exc:
            return {"controlling": None, "uncertainty_reason": str(exc)}
    return {"controlling": controlling}
