"""Per-ground borrower strength score computation — corpus-informed judicial scoring.

FACTS OVERRIDE VECTORS: judicial_score only shifts the corpus base rate when an
applicable_judgments entry carries a verified court/favor pair (Class A only).
"""
from __future__ import annotations

COURT_RANK = {"SUPREME_COURT": 4, "HIGH_COURT": 3, "DRAT": 2, "DRT": 1}


def compute_judicial_score(
    ground_code: str,
    applicable_judgments: list[dict],
    corpus_stats: dict,
) -> float:
    if corpus_stats["data_confidence"] in ("HIGH", "MEDIUM"):
        borrower_win_pct = corpus_stats.get("verified", {}).get("borrower_win_pct")
        if borrower_win_pct is None:
            borrower_win_pct = corpus_stats.get("full", {}).get("borrower_win_pct") or 0
        base_score = borrower_win_pct / 100
    else:
        base_score = 0.40  # no data — neutral

    sc_borrower = [j for j in applicable_judgments if j["court"] == "SUPREME_COURT" and j["favor"] == "BORROWER"]
    sc_bank     = [j for j in applicable_judgments if j["court"] == "SUPREME_COURT" and j["favor"] == "BANK"]

    if sc_borrower:
        return max(base_score, 0.85)
    elif sc_bank:
        return min(base_score, 0.20)
    else:
        hc_borrower = [j for j in applicable_judgments if j["favor"] == "BORROWER"]
        if hc_borrower:
            return min(base_score + 0.10, 1.0)
        return base_score


def compute_ground_strength(
    ground_code: str,
    compliance_result_status: str,  # 'PASS' | 'FAIL' | 'UNKNOWN'
    applicable_judgments: list[dict],
    corpus_stats: dict,
) -> dict:
    if compliance_result_status == "FAIL":
        factual_score = 1.0   # bank's record confirms borrower's allegation
    elif compliance_result_status == "UNKNOWN":
        factual_score = 0.4   # conservative: unverified = some risk
    else:
        factual_score = 0.0   # bank's record contradicts allegation

    judicial_score = compute_judicial_score(ground_code, applicable_judgments, corpus_stats)

    ground_strength = (factual_score * 0.55) + (judicial_score * 0.45)

    return {
        "ground_code":     ground_code,
        "factual_score":   round(factual_score, 4),
        "judicial_score":  round(judicial_score, 4),
        "ground_strength": round(ground_strength, 4),
        "strength_label":  _strength_label(ground_strength),
    }


def _strength_label(score: float) -> str:
    if score < 0.25:
        return "WEAK"
    if score < 0.50:
        return "ARGUABLE"
    if score < 0.70:
        return "STRONG"
    return "VERY_STRONG"


def compute_litigation_exposure(ground_scores: list[dict]) -> float:
    if not ground_scores:
        return 0.0
    scores = [g["ground_strength"] for g in ground_scores]
    return round((max(scores) * 0.65) + (sum(scores) / len(scores) * 0.35), 4)
