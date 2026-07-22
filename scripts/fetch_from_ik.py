"""Indian Kanoon API fetcher + Class B summary generator.

    python scripts/fetch_from_ik.py --citations-file docs/judgments_manifest.txt

Fetches judgment full text from the Indian Kanoon API for each citation/query
in the manifest, drafts a Class B holding summary via Claude with a safety
gate (SUMMARY_UNCERTAIN -> skip), and writes docs/judgments/<slug>.md.

No-ops (exit 0) if IK_API_TOKEN is not set — the H7 pipeline must run without
the judgment corpus present; this script only matters once real citations and
an API token are supplied.

Manifest format: one citation or search query per line, '#' comments allowed.
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

IK_BASE_URL = "https://api.indiankanoon.org"

SUMMARY_DRAFT_PROMPT = """You are summarising an Indian court judgment for a legal database.
Write a 120-180 word summary with this exact structure:
Sentence 1: What procedural ground was raised and by which party
Sentence 2: Specific facts relevant to that ground
Sentence 3-4: What the court held and the statutory basis cited
Sentence 5: The specific condition required for this holding to apply

Rules:
- Write only what the COURT decided — not what was argued
- Include the exact SARFAESI section or Rule number mentioned
- State explicitly whether the outcome favoured the bank or the borrower
- If the ratio is unclear or the judgment is purely procedural with no holding,
  write exactly: SUMMARY_UNCERTAIN: [one-sentence reason]
- Return only the summary text — nothing else"""


def generate_class_b_summary(judgment_text: str, max_retries: int = 2) -> str | None:
    """Generates a holding summary for a Class B judgment. Returns None if
    uncertain or generation failed — None means skip, never load with a
    wrong/guessed summary (better a smaller honest corpus than a larger
    uncertain one)."""
    import anthropic

    from app.config import settings

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    for attempt in range(max_retries + 1):
        try:
            response = client.messages.create(
                model=settings.claude_model,
                max_tokens=400,
                temperature=0.0,
                system=SUMMARY_DRAFT_PROMPT,
                messages=[{"role": "user", "content": judgment_text[:8000]}],
            )
            summary = response.content[0].text.strip()

            if "SUMMARY_UNCERTAIN" in summary:
                return None
            words = summary.split()
            if len(words) < 80:
                return None
            if len(words) > 250:
                summary = " ".join(words[:200])
            return summary

        except anthropic.AuthenticationError:
            raise  # fatal — wrong/unset key, do not silently report as SUMMARY_UNCERTAIN
        except anthropic.RateLimitError:
            if attempt == max_retries:
                raise
            time.sleep(5)
        except Exception:
            if attempt == max_retries:
                return None
            time.sleep(2)
    return None


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return slug[:60]


def _ik_search(client, query: str) -> dict | None:
    resp = client.post(f"{IK_BASE_URL}/search/", params={"formInput": query})
    resp.raise_for_status()
    data = resp.json()
    docs = data.get("docs") or []
    return docs[0] if docs else None


def _ik_fetch_doc(client, doc_id: str) -> dict:
    resp = client.post(f"{IK_BASE_URL}/doc/{doc_id}/")
    resp.raise_for_status()
    return resp.json()


def fetch_and_summarize(query: str, output_dir: Path) -> bool:
    import httpx

    from app.config import settings

    headers = {"Authorization": f"Token {settings.ik_api_token}"}
    with httpx.Client(headers=headers, timeout=30.0) as client:
        hit = _ik_search(client, query)
        if hit is None:
            print(f"SKIP (no result): {query}")
            return False

        doc = _ik_fetch_doc(client, hit["tid"])
        judgment_text = re.sub(r"<[^>]+>", " ", doc.get("doc", ""))

    summary = generate_class_b_summary(judgment_text)
    if summary is None:
        print(f"SKIP (SUMMARY_UNCERTAIN): {query}")
        return False

    slug = _slugify(hit.get("title", query))
    md_path = output_dir / f"{slug}.md"
    frontmatter = (
        "---\n"
        f"citation: \"{hit.get('title', query)}\"\n"
        f"title: \"{hit.get('title', query)}\"\n"
        f"short_name: {slug}\n"
        "court: HIGH_COURT\n"
        "high_court_state: null\n"
        "bench_strength: 1\n"
        "judgment_date: null\n"
        "overruled: false\n"
        "overruled_by: null\n"
        "favor: NEUTRAL\n"
        "favor_verified: false\n"
        "ground_codes: [UNKNOWN]\n"
        "has_verified_conditions: false\n"
        "source: IBC_LAW_SUMMARY\n"
        "chunk_type: null\n"
        "applicable_conditions: []\n"
        "exclusion_conditions: []\n"
        "---\n\n"
    )
    md_path.write_text(frontmatter + summary + "\n", encoding="utf-8")
    print(f"WROTE: {md_path}")
    return True


def main() -> int:
    from app.config import settings

    parser = argparse.ArgumentParser()
    parser.add_argument("--citations-file", default="docs/judgments_manifest.txt")
    parser.add_argument("--out-dir", default="docs/judgments")
    args = parser.parse_args()

    if not settings.ik_api_token:
        print("IK_API_TOKEN not set — skipping Indian Kanoon fetch.")
        return 0

    manifest = Path(args.citations_file)
    if not manifest.exists():
        print(f"Manifest not found: {manifest} — nothing to fetch.")
        return 0

    queries = [
        line.strip() for line in manifest.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not queries:
        print(f"Manifest {manifest} is empty — nothing to fetch.")
        return 0

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    import anthropic

    try:
        fetched = sum(fetch_and_summarize(q, out_dir) for q in queries)
    except anthropic.AuthenticationError:
        print("ANTHROPIC_API_KEY is invalid or not set — cannot generate Class B "
              "summaries. IK search/fetch works independently of this; set a "
              "real key in .env and re-run.")
        return -1

    print(f"{fetched}/{len(queries)} judgments fetched and summarized.")
    return fetched


if __name__ == "__main__":
    main()
