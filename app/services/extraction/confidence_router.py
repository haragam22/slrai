"""Routes extracted fields to workbench or auto-accept based on confidence thresholds."""

from app.models.db import ALWAYS_HUMAN_CONFIRM_FIELDS as ALWAYS_HUMAN_CONFIRM

CONFIDENCE_THRESHOLD = 0.80


def route_fact(field_name: str, extraction_result: dict) -> dict:
    """Determines if a fact goes to workbench or is auto-accepted.
    Returns enriched fact dict with routing decision.
    """
    is_implied = extraction_result.get("implied", False)
    confidence = extraction_result.get("confidence", 0.0)

    if extraction_result.get("extraction_method") == "regex":
        return {**extraction_result, "confidence": 1.0, "requires_workbench": False}

    # Implied facts are ALWAYS capped and routed to workbench
    if is_implied:
        confidence = min(confidence, 0.75)
        return {
            **extraction_result,
            "confidence": confidence,
            "extraction_method": "nlp_implied",
            "requires_workbench": True,
        }

    if field_name in ALWAYS_HUMAN_CONFIRM:
        return {
            **extraction_result,
            "extraction_method": "nlp_explicit",
            "requires_workbench": True,
        }

    if confidence < CONFIDENCE_THRESHOLD:
        return {
            **extraction_result,
            "requires_workbench": True,
            "extraction_method": "nlp_explicit",
        }

    return {**extraction_result, "requires_workbench": False, "extraction_method": "nlp_explicit"}
