"""Final recommendation via compliance_score × ground_strength matrix lookup."""
from __future__ import annotations

MATRIX = [
    # (compliance_min, compliance_max, exposure_max, label, text)
    (90, 100, 0.25, "PROCEED",
     "Bank followed procedure correctly. Borrower's case is weak."),
    (90, 100, 0.45, "PROCEED_WITH_AWARENESS",
     "Procedure clean. Some arguable grounds. Monitor DRT hearings."),
    (90, 100, 1.00, "HIGH_RISK",
     "Procedure clean but borrower has strong legal grounds."),
    (70,  89, 0.25, "PROCEED_WITH_CONDITIONS",
     "Minor procedural gaps. Borrower case weak. Get legal affidavit on curable defects."),
    (70,  89, 0.45, "ELEVATED_RISK",
     "Both sides have exposure. Detailed legal review recommended."),
    (70,  89, 1.00, "HIGH_RISK",
     "Do not proceed without detailed legal review."),
    ( 0,  69, 1.00, "DO_NOT_PROCEED",
     "Significant procedural defects. Auction highly vulnerable."),
]


def get_recommendation(compliance_score: int, litigation_exposure: float,
                        absolute_bar_triggered: bool) -> dict:
    if absolute_bar_triggered and litigation_exposure < 0.30:
        return {
            "label": "PROCEED_FAVOURABLE",
            "text": "SA appears to be time-barred under Section 17. Dismissal likely.",
        }

    for comp_min, comp_max, exp_max, label, text in MATRIX:
        if comp_min <= compliance_score <= comp_max and litigation_exposure <= exp_max:
            return {"label": label, "text": text}

    if litigation_exposure >= 0.65:
        return {
            "label": "DO_NOT_PROCEED_CRITICAL",
            "text": "Borrower has very strong grounds regardless of bank procedure.",
        }

    return {"label": "MANUAL_REVIEW_REQUIRED",
            "text": "Score combination not in matrix. Legal review required."}
