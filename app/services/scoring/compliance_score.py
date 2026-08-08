"""Bank procedural compliance score aggregation.

Only M1-M9 feed this score — those modules check whether the BANK followed
SARFAESI procedure correctly. M10 (third-party rights) scores the strength
of a third party's claim against the bank, which is a different question;
it feeds ground_strength.py / litigation exposure instead, not this score.
"""
from __future__ import annotations

DEDUCTIONS = {
    "ABSOLUTE_BAR":    50,
    "FATAL":           40,
    "HIGH":            25,
    "REVIEW_REQUIRED": 20,
    "CURABLE":         15,
    "UNKNOWN":         10,
    "MINOR":            5,
    "ADVISORY":         3,
}

PROCEDURAL_MODULES = {"M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9"}


def compute_compliance_score(compliance_results: list) -> int:
    """Deduct only for findings that (a) came from a check actually firing
    (severity is not None — the generic "nothing wrong" fallthrough has no
    severity) and (b) favor the borrower, i.e. are a genuine bank procedural
    defect. A rule author's PASS/FAIL/REVIEW status label is not a reliable
    signal of direction — outcome_favors, set explicitly per check in the
    YAML, is (see H14(c))."""
    total_deductions = sum(
        DEDUCTIONS.get(r.severity, 0)
        for r in compliance_results
        if r.severity is not None
        and r.outcome_favors == "BORROWER"
        and r.module.split("_")[0] in PROCEDURAL_MODULES
    )
    return max(0, 100 - total_deductions)
