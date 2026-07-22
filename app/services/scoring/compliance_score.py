"""Bank procedural compliance score aggregation."""
from __future__ import annotations

DEDUCTIONS = {
    "FATAL":        40,
    "ABSOLUTE_BAR": 50,
    "CURABLE":      15,
    "MINOR":         5,
    "ADVISORY":      3,
    "UNKNOWN":      10,
}


def compute_compliance_score(compliance_results: list) -> int:
    total_deductions = sum(
        DEDUCTIONS.get(r.severity, 0)
        for r in compliance_results
        if r.status == "FAIL"
    )
    return max(0, 100 - total_deductions)
