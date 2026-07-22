"""Qdrant lazy retrieval — ONE collection (sarfaesi_judgments), ground-code filtered.

Lazy retrieval rule: Chain B retrieves judgments ONLY for ground codes raised
in THIS case (sa_grounds) OR failed in THIS case's compliance results.
Never retrieve for all ground codes on every case.

FACTS OVERRIDE VECTORS: always metadata-filtered first, then vector
similarity — never pure vector search.
"""
from __future__ import annotations

import logging

from qdrant_client import models
from qdrant_client.models import FieldCondition, Filter, MatchAny, MatchValue
from sentence_transformers import SentenceTransformer

from app.config import settings

logger = logging.getLogger(__name__)

_embedder: SentenceTransformer | None = None
_embedder_model_name: str | None = None

FALLBACK_EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"

# Payload indexes required on the sarfaesi_judgments collection.
PAYLOAD_INDEXES: dict[str, str] = {
    "ground_codes":            "keyword",
    "court":                   "keyword",
    "favor":                   "keyword",
    "overruled":               "bool",
    "has_verified_conditions": "bool",
    "favor_verified":          "bool",
    "source":                  "keyword",
    "keywords":                "keyword",
    "slrai_modules":           "keyword",
}


def _get_embedder() -> SentenceTransformer:
    """Cached InLegalBERT embedder. Falls back to all-mpnet-base-v2 (also
    768-dim) if the primary model fails to load — e.g. no network access or
    a numpy/torch ABI mismatch in the current environment."""
    global _embedder, _embedder_model_name
    if _embedder is None:
        try:
            _embedder = SentenceTransformer(settings.embedding_model)
            _embedder_model_name = settings.embedding_model
        except Exception:
            logger.exception(
                "Failed to load embedding model '%s' — falling back to %s",
                settings.embedding_model, FALLBACK_EMBEDDING_MODEL,
            )
            _embedder = SentenceTransformer(FALLBACK_EMBEDDING_MODEL)
            _embedder_model_name = FALLBACK_EMBEDDING_MODEL
    return _embedder


async def setup_qdrant_collections() -> None:
    """Ensure the ONE sarfaesi_judgments collection + its payload indexes
    exist. Called from main.py FastAPI lifespan on startup. Idempotent —
    safe to call every startup."""
    from qdrant_client import AsyncQdrantClient

    client = AsyncQdrantClient(url=settings.qdrant_url)
    collection = settings.qdrant_judgments_collection

    existing = await client.get_collections()
    existing_names = {c.name for c in existing.collections}

    if collection not in existing_names:
        client_embedder = _get_embedder()
        vector_size = client_embedder.get_sentence_embedding_dimension()
        await client.create_collection(
            collection_name=collection,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        )
        logger.info("Created Qdrant collection '%s' (dim=%d)", collection, vector_size)

    for field_name, field_schema in PAYLOAD_INDEXES.items():
        try:
            await client.create_payload_index(
                collection_name=collection,
                field_name=field_name,
                field_schema=field_schema,
            )
        except Exception as exc:
            # Already exists — Qdrant raises on duplicate index creation.
            logger.debug("Payload index '%s' setup skipped: %s", field_name, exc)

    await client.close()


def is_qdrant_reachable() -> bool:
    """Contract §18.3 — cheap up-front check so a downed Qdrant fails fast
    once per Chain B run instead of once per ground_code retrieval call."""
    from qdrant_client import QdrantClient

    try:
        QdrantClient(url=settings.qdrant_url).get_collections()
        return True
    except Exception:
        logger.exception("Qdrant unreachable at %s", settings.qdrant_url)
        return False


def get_relevant_ground_codes(case_id: str, db) -> set[str]:
    """
    Returns the set of ground codes to retrieve judgments for: only ground
    codes raised in THIS SA or failed in THIS case's compliance results.
    """
    from app.models.db import ComplianceResult, SAGround
    from app.tasks.chain_b import RULE_TO_GROUND_MAP

    sa_grounds = db.query(SAGround.ground_code).filter_by(case_id=case_id).all()
    sa_codes = {row.ground_code for row in sa_grounds}

    failed = db.query(ComplianceResult.rule_id).filter_by(case_id=case_id, status="FAIL").all()
    failed_codes = {RULE_TO_GROUND_MAP.get(row.rule_id) for row in failed} - {None}

    return sa_codes | failed_codes


# Maps a confirmed fact (field, expected_value) to legal keywords the
# judgment corpus's `keywords` payload field uses — feeds the Stage 2
# keyword-fallback path in retrieve_candidate_judgments() when the primary
# ground_code + vector search returns sparse (<5) results.
CASE_KEYWORD_RULES: list[tuple[str, object, list[str]]] = [
    ("right_of_redemption_extinguished", False, ["right of redemption", "Rule 9(4)", "inchoate sale"]),
    ("sale_certificate_issued", True, ["sale certificate", "statutory finality", "auction purchaser"]),
    ("auction_conducted_despite_stay", True, ["AUCTION_DURING_STAY", "contempt of court", "stay in operation"]),
    ("auction_notice_affixed_on_property", False, ["Rule 8(6)(7)", "affixing notice", "Mathew Varghese"]),
    ("auction_notice_discloses_pending_sa", False, ["pending SA", "concealment", "encumbrance"]),
    ("sa_applicant_type", "THIRD_PARTY_ATS", ["Agreement to Sell", "ATS", "third party"]),
    ("sa_applicant_type", "AUCTION_PURCHASER", ["auction purchaser", "right of redemption", "sale certificate"]),
    ("bank_reply_gives_reasons", False, ["Section 13(3A)", "reasoned reply", "Kanaiyalal"]),
    ("account_standard_at_auction_date", True, ["NPA upgradation", "RBI IRAC 4.2.5", "account standard"]),
]


def build_case_keywords(confirmed_facts: dict) -> list[str]:
    """Derives Stage-2 keyword-fallback terms from confirmed case facts.
    confirmed_facts is the flat {field_name: value} shape (already unwrapped
    from the {"value":..., "human_confirmed":...} DB row shape)."""
    keywords: list[str] = []
    for field, expected_val, terms in CASE_KEYWORD_RULES:
        if confirmed_facts.get(field) == expected_val:
            keywords.extend(terms)
    return keywords


def retrieve_by_keywords(keywords: list[str], top_k: int = 5) -> list[dict]:
    """
    Fallback retrieval path — matches judgments whose 'keywords' payload
    field overlaps the given keywords. Used when ground_code + vector search
    returns sparse results (<5 hits): a judgment can be relevant on its
    specific fact pattern (e.g. "second_sa", "ats_holder") even when its
    primary ground_codes tag doesn't cover the case's exact ground.
    Returns [] on an empty/unreachable corpus — never raises.
    """
    from qdrant_client import QdrantClient

    if not keywords:
        return []

    try:
        client = QdrantClient(url=settings.qdrant_url)
        hits, _ = client.scroll(
            collection_name=settings.qdrant_judgments_collection,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="overruled", match=MatchValue(value=False)),
                    FieldCondition(key="keywords", match=MatchAny(any=keywords)),
                ]
            ),
            limit=top_k,
            with_payload=True,
        )
    except Exception:
        logger.exception("Qdrant keyword retrieval failed for keywords=%s — returning no candidates", keywords)
        return []

    return [point.payload for point in hits]


def retrieve_candidate_judgments(
    ground_code: str,
    case_keywords: list[str] | None = None,
    top_k: int = 20,
) -> tuple[list[dict], list[dict]]:
    """
    Returns (class_a_candidates, class_b_candidates) for a single ground code.

    Stage 1: ground_code filter + vector similarity (overruled=False).
    Stage 2: if stage 1 returns <5 hits and case_keywords is given, supplement
    with retrieve_by_keywords() — deduped by judgment id. Then split by
    has_verified_conditions. Returns ([], []) on an empty/unreachable corpus
    — never raises, so Chain B can run before the judgment corpus is loaded.
    """
    from qdrant_client import QdrantClient

    try:
        client = QdrantClient(url=settings.qdrant_url)
        embedder = _get_embedder()
        query_vector = embedder.encode(ground_code).tolist()

        results = client.search(
            collection_name=settings.qdrant_judgments_collection,
            query_vector=query_vector,
            query_filter=Filter(
                must=[
                    FieldCondition(key="ground_codes", match=MatchAny(any=[ground_code])),
                    FieldCondition(key="overruled", match=MatchValue(value=False)),
                ]
            ),
            limit=top_k,
            with_payload=True,
        )
        all_hits = [hit.payload for hit in results]
    except Exception:
        logger.exception("Qdrant retrieval failed for ground_code=%s — returning no candidates", ground_code)
        return [], []

    if len(all_hits) < 5 and case_keywords:
        existing_ids = {h.get("id") for h in all_hits}
        keyword_hits = retrieve_by_keywords(case_keywords, top_k=10)
        all_hits += [h for h in keyword_hits if h.get("id") not in existing_ids]

    class_a = [j for j in all_hits if j.get("has_verified_conditions") is True]
    class_b = [j for j in all_hits if j.get("has_verified_conditions") is False]
    return class_a, class_b
