"""Ingests docs/judgments/*.md into Postgres (judgments table) + Qdrant
(sarfaesi_judgments collection).

    python scripts/load_judgments.py --dir docs/judgments/
    python scripts/load_judgments.py --dir docs/judgments/ --file e_muthurathinasabathy.md

Upserts by citation — safe to re-run after editing/adding .md files. A no-op
on an empty directory (0 processed, exit 0) so this can run before the
judgment corpus is ready without breaking anything downstream.
"""
from __future__ import annotations

import argparse
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from _judgment_md import parse_judgment_md, load_all_judgment_files  # noqa: E402


def _upsert_postgres(records: list[dict]) -> dict[str, uuid.UUID]:
    """Upserts each record into the judgments table by citation. Returns
    {citation: judgment_id} for the Qdrant payload step below."""
    from app.models.db import Judgment, SyncSessionLocal

    citation_to_id: dict[str, uuid.UUID] = {}
    with SyncSessionLocal() as db:
        for r in records:
            existing = db.query(Judgment).filter_by(citation=r["citation"]).first()
            if existing is None:
                existing = Judgment(id=uuid.uuid4(), citation=r["citation"])
                db.add(existing)

            existing.title = r["title"]
            existing.short_name = r["short_name"]
            existing.court = r["court"]
            existing.high_court_state = r.get("high_court_state")
            existing.bench_strength = r.get("bench_strength", 1)
            existing.judgment_date = r.get("judgment_date")
            existing.overruled = r.get("overruled", False)
            existing.distinguished_by = r.get("distinguished_by") or []
            existing.favor = r["favor"]
            existing.favor_verified = r.get("favor_verified", False)
            existing.ground_codes = r["ground_codes"]
            existing.statutory_basis = r.get("statutory_basis")
            existing.act_sections = r.get("act_sections") or []
            existing.rules_sections = r.get("rules_sections") or []
            existing.slrai_modules = r.get("slrai_modules") or []
            existing.keywords = r.get("keywords") or []
            existing.holding_summary = r["holding_summary"]
            existing.borrower_claim = r.get("borrower_claim", "")
            existing.applicable_conditions_text = r.get("applicable_conditions_text", "")
            existing.exclusion_conditions_text = r.get("exclusion_conditions_text", "")
            existing.has_verified_conditions = r["has_verified_conditions"]
            existing.source = r.get("source", "SC_FULL_TEXT")
            existing.ik_doc_id = r.get("ik_doc_id", "")
            existing.ik_url = r.get("ik_url", "")
            existing.chunk_type = r.get("chunk_type")
            existing.applicable_conditions = r.get("applicable_conditions") or []
            existing.exclusion_conditions = r.get("exclusion_conditions") or []

            db.flush()
            citation_to_id[r["citation"]] = existing.id

        # Second pass: resolve overruled_by citation -> UUID FK now that all
        # judgments in this batch have ids.
        for r in records:
            overruled_by_citation = r.get("overruled_by")
            if not overruled_by_citation:
                continue
            existing = db.query(Judgment).filter_by(citation=r["citation"]).first()
            target_id = citation_to_id.get(overruled_by_citation)
            if target_id is None:
                target = db.query(Judgment).filter_by(citation=overruled_by_citation).first()
                target_id = target.id if target else None
            existing.overruled_by = target_id

        db.commit()
    return citation_to_id


def _upsert_qdrant(records: list[dict], citation_to_id: dict[str, uuid.UUID]) -> int:
    from qdrant_client import QdrantClient
    from qdrant_client.models import PointStruct

    from app.config import settings
    from app.services.judgments.retrieval import _get_embedder

    client = QdrantClient(url=settings.qdrant_url)
    embedder = _get_embedder()

    points = []
    for r in records:
        judgment_id = citation_to_id[r["citation"]]
        vector = embedder.encode(r["holding_summary"]).tolist()
        points.append(PointStruct(
            id=str(judgment_id),
            vector=vector,
            payload={
                "id": str(judgment_id),
                "citation": r["citation"],
                "title": r["title"],
                "short_name": r["short_name"],
                "court": r["court"],
                "favor": r["favor"],
                "favor_verified": r.get("favor_verified", False),
                "ground_codes": r["ground_codes"],
                "keywords": r.get("keywords") or [],
                "slrai_modules": r.get("slrai_modules") or [],
                "overruled": r.get("overruled", False),
                "has_verified_conditions": r["has_verified_conditions"],
                "source": r.get("source", "SC_FULL_TEXT"),
                "holding_summary": r["holding_summary"],
                "borrower_claim": r.get("borrower_claim", ""),
            },
        ))

    if points:
        client.upsert(collection_name=settings.qdrant_judgments_collection, points=points)
    return len(points)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="docs/judgments", help="Directory of judgment .md files")
    parser.add_argument("--file", default=None, help="Ingest a single file within --dir instead of the whole directory")
    args = parser.parse_args()

    judgments_dir = Path(args.dir)

    if args.file:
        target = judgments_dir / args.file
        if not target.exists():
            print(f"File not found: {target}")
            return 0
        records = [parse_judgment_md(target)]
    else:
        records = load_all_judgment_files(judgments_dir)

    if not records:
        print(f"0 judgment files found in {judgments_dir} — nothing to load.")
        return 0

    citation_to_id = _upsert_postgres(records)
    print(f"{len(records)} judgments upserted into Postgres.")

    from app.config import settings
    n = _upsert_qdrant(records, citation_to_id)
    print(f"{n} judgments upserted into Qdrant ('{settings.qdrant_judgments_collection}').")

    return len(records)


if __name__ == "__main__":
    main()
