"""Judgment corpus win-rate statistics — Qdrant payload filtering, no vector search.

Returns BOTH counts:
  verified — favor_verified=True only (the manually-verified Class A judgments)
  full     — across all judgments (Class A + Class B)
Verified is the primary signal; both are shown in the report.
"""
from __future__ import annotations

import logging

from qdrant_client.models import FieldCondition, Filter, MatchAny, MatchValue

from app.config import settings

logger = logging.getLogger(__name__)


def _count_favor(client, collection: str, ground_code: str, favor_value: str, verified_only: bool) -> int:
    must_conditions = [
        FieldCondition(key="ground_codes", match=MatchAny(any=[ground_code])),
        FieldCondition(key="favor", match=MatchValue(value=favor_value)),
        FieldCondition(key="overruled", match=MatchValue(value=False)),
    ]
    if verified_only:
        must_conditions.append(FieldCondition(key="favor_verified", match=MatchValue(value=True)))

    result = client.count(
        collection_name=collection,
        count_filter=Filter(must=must_conditions),
        exact=True,
    )
    return result.count


def get_ground_statistics(ground_code: str) -> dict:
    """
    Counts judgments in the corpus by outcome for a specific ground code.
    Returns zeros (data_confidence=NO_DATA) on an empty/unreachable corpus —
    never raises, so Chain B can run before the judgment corpus is loaded.
    """
    from qdrant_client import QdrantClient

    empty = {
        "verified": {"total": 0, "borrower_wins": 0, "bank_wins": 0, "neutral": 0,
                      "borrower_win_pct": None, "bank_win_pct": None},
        "full": {"total": 0, "borrower_wins": 0, "bank_wins": 0, "neutral": 0,
                 "borrower_win_pct": None, "bank_win_pct": None},
        "data_confidence": "NO_DATA",
    }

    try:
        client = QdrantClient(url=settings.qdrant_url)
        collection = settings.qdrant_judgments_collection

        v_borrower = _count_favor(client, collection, ground_code, "BORROWER", verified_only=True)
        v_bank     = _count_favor(client, collection, ground_code, "BANK", verified_only=True)
        v_neutral  = _count_favor(client, collection, ground_code, "NEUTRAL", verified_only=True)
        v_total    = v_borrower + v_bank + v_neutral

        f_borrower = _count_favor(client, collection, ground_code, "BORROWER", verified_only=False)
        f_bank     = _count_favor(client, collection, ground_code, "BANK", verified_only=False)
        f_neutral  = _count_favor(client, collection, ground_code, "NEUTRAL", verified_only=False)
        f_total    = f_borrower + f_bank + f_neutral
    except Exception:
        logger.exception("Qdrant statistics query failed for ground_code=%s — returning NO_DATA", ground_code)
        return empty

    return {
        "verified": {
            "total":            v_total,
            "borrower_wins":    v_borrower,
            "bank_wins":        v_bank,
            "neutral":          v_neutral,
            "borrower_win_pct": round(v_borrower / v_total * 100, 1) if v_total > 0 else None,
            "bank_win_pct":     round(v_bank / v_total * 100, 1) if v_total > 0 else None,
        },
        "full": {
            "total":            f_total,
            "borrower_wins":    f_borrower,
            "bank_wins":        f_bank,
            "neutral":          f_neutral,
            "borrower_win_pct": round(f_borrower / f_total * 100, 1) if f_total > 0 else None,
            "bank_win_pct":     round(f_bank / f_total * 100, 1) if f_total > 0 else None,
        },
        "data_confidence": (
            "HIGH" if v_total >= 10 else
            "MEDIUM" if v_total >= 5 else
            "LOW" if f_total > 0 else
            "NO_DATA"
        ),
    }
