"""Indian Kanoon API fetcher — raw judgment text only.

    python scripts/fetch_from_ik.py --citations-file docs/judgments_manifest.txt

For each title/citation/query in the manifest: searches Indian Kanoon, fetches
the full judgment text, and writes it verbatim to
docs/judgments_raw/<slug>.txt plus a sidecar docs/judgments_raw/<slug>.meta.json
(ik_doc_id, ik_url, the manifest line that found it) — the info
scripts/summarize_judgments.py needs but that isn't in the judgment text
itself.

This script does not call Claude and does not write interpretations.
scripts/summarize_judgments.py is the separate step that turns these raw
files into docs/judgments/*.md (what load_judgments.py actually loads into
Postgres/Qdrant for retrieval during a case run) — run that after this one.

No-ops (exit 0) if IK_API_TOKEN is not set — the H7 pipeline must run without
the judgment corpus present; this script only matters once real citations and
an API token are supplied.

Manifest format: one citation, case title, or search query per line, '#'
comments allowed. Optionally end a line with a court hint in parentheses —
e.g. "Celir LLP v. Bafna Motors (DRAT Chennai)" — when the same case title
was decided by more than one court/bench (common: same dispute litigated at
DRT, then DRAT, then HC) and you need to disambiguate which one to fetch.
The hint is folded into the IK search query and into the output slug, so
"Foo v. Bar (DRAT Chennai)" and "Foo v. Bar (High Court Bombay)" land as two
separate files instead of one overwriting the other.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

IK_BASE_URL = "https://api.indiankanoon.org"


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return slug[:60]


_COURT_HINT_RE = re.compile(r"^(.*\S)\s*\(([^()]+)\)\s*(?:\[[^\[\]]*\])?\s*$")
_YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


def _split_court_hint(line: str) -> tuple[str, str | None]:
    """'Foo v. Bar (DRAT Chennai)' -> ('Foo v. Bar', 'DRAT Chennai').

    Trailing bracket asides like '[Basa Chandramouli]' (see manifest line 15)
    are stripped along with the hint — they're editorial notes, not court info.
    """
    m = _COURT_HINT_RE.match(line)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return line, None


def _parse_hint(hint: str | None) -> tuple[str | None, str | None]:
    """'DRAT Mumbai 2025' -> ('DRAT Mumbai', '2025'); year is optional."""
    if not hint:
        return None, None
    ym = _YEAR_RE.search(hint)
    if not ym:
        return hint, None
    year = ym.group(0)
    court = (hint[:ym.start()] + hint[ym.end():]).strip()
    return court or None, year


def _ik_search(client, query: str) -> list[dict]:
    resp = client.post(f"{IK_BASE_URL}/search/", params={"formInput": query})
    resp.raise_for_status()
    data = resp.json()
    return data.get("docs") or []


_TITLE_STOPWORDS = {
    "v", "vs", "and", "or", "ors", "anr", "others", "the", "of", "in", "on", "by",
    "ltd", "ltd.", "pvt", "pvt.", "private", "limited", "co", "co.", "company",
    "bank", "india", "state", "union", "national", "authorized", "authorised",
    "officer", "corporation", "m", "s", "m/s", "mr", "mrs", "smt", "dr", "rep",
    "its", "chief", "for", "no", "vide", "under", "sri", "shri",
}


def _significant_tokens(title: str) -> set[str]:
    return {
        w for w in re.findall(r"[a-z0-9]+", title.lower())
        if len(w) > 2 and w not in _TITLE_STOPWORDS
    }


def _title_matches(manifest_title: str, doc_title: str) -> bool:
    """Reject a hit that shares no distinct party-name token with the manifest
    title — without this, a hint-less generic title (no court/year to score
    against) blindly takes IK's docs[0], which for common titles can be a
    wholly unrelated case (seen in practice: 3 of 111 manifest lines pulled
    the wrong judgment this way)."""
    wanted = _significant_tokens(manifest_title)
    if not wanted:
        return True  # nothing distinctive to check against — don't false-reject
    got = _significant_tokens(doc_title)
    return bool(wanted & got)


def _pick_best(docs: list[dict], manifest_title: str, court: str | None, year: str | None) -> dict | None:
    """Prefer the search hit whose title/court/date matches the manifest's
    court name and year hint over blindly taking the top result — IK's
    ranking often surfaces the wrong bench/instance for common case titles."""
    docs = [d for d in docs if _title_matches(manifest_title, d.get("title") or "")]
    if not docs:
        return None
    if not court and not year:
        return docs[0]

    def score(doc: dict) -> int:
        s = 0
        title = (doc.get("title") or "").lower()
        doc_court = (doc.get("docsource") or "").lower()
        if court and (court.lower() in title or court.lower() in doc_court):
            s += 2
        if year:
            if year in title:
                s += 2
            elif year in str(doc.get("publishdate") or ""):
                s += 1
        return s

    return max(docs, key=score)


def _ik_fetch_doc(client, doc_id: str) -> dict:
    resp = client.post(f"{IK_BASE_URL}/doc/{doc_id}/")
    resp.raise_for_status()
    return resp.json()


def _with_retry(fn, *args, retries: int = 1, backoff: float = 5.0):
    """Retry once on 403 — IK returns 403 for both bad auth and (per support)
    transient throttling of accounts whose non-commercial token is still
    under review. The API docs specify no rate limit, so this is a guess,
    not a documented contract."""
    import httpx
    import time

    for attempt in range(retries + 1):
        try:
            return fn(*args)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403 and attempt < retries:
                print(f"  403 from IK, retrying in {backoff}s (token still under review?)")
                time.sleep(backoff)
                continue
            raise


def fetch_one(client, line: str, raw_dir: Path) -> str | None:
    title, court_hint = _split_court_hint(line)
    court, year = _parse_hint(court_hint)
    query = f"{title} {court_hint}" if court_hint else title

    docs = _with_retry(_ik_search, client, query)
    hit = _pick_best(docs, title, court, year)
    if hit is None:
        print(f"SKIP (no result): {line}")
        return None

    doc = _with_retry(_ik_fetch_doc, client, hit["tid"])
    judgment_text = re.sub(r"<[^>]+>", " ", doc.get("doc", ""))

    slug_base = f"{title} {court_hint}" if court_hint else hit.get("title", title)
    slug = _slugify(slug_base)
    raw_path = raw_dir / f"{slug}.txt"
    raw_path.write_text(judgment_text, encoding="utf-8")

    meta_path = raw_dir / f"{slug}.meta.json"
    meta_path.write_text(json.dumps({
        "manifest_line": line,
        "court_hint": court_hint,
        "court": court,
        "year": year,
        "ik_doc_id": str(hit["tid"]),
        "ik_url": f"https://indiankanoon.org/doc/{hit['tid']}/",
        "ik_title": hit.get("title", title),
    }, indent=2), encoding="utf-8")

    print(f"WROTE: {raw_path}")
    return slug


def main() -> int:
    from app.config import settings

    parser = argparse.ArgumentParser()
    parser.add_argument("--citations-file", default="docs/judgments_manifest.txt")
    parser.add_argument("--raw-dir", default="docs/judgments_raw")
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

    raw_dir = Path(args.raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)

    import time

    import httpx

    not_found: list[str] = []
    headers = {"Authorization": f"Token {settings.ik_api_token}"}
    with httpx.Client(headers=headers, timeout=30.0) as client:
        for i, q in enumerate(queries):
            if i:
                time.sleep(1.0)  # ponytail: fixed pace, no doc-stated limit to tune to
            if fetch_one(client, q, raw_dir) is None:
                not_found.append(q)

    fetched = len(queries) - len(not_found)
    not_found_path = raw_dir / "_not_found.txt"
    if not_found:
        not_found_path.write_text("\n".join(not_found) + "\n", encoding="utf-8")
        print(f"\n{len(not_found)} not found on Indian Kanoon (see {not_found_path}):")
        for q in not_found:
            print(f"  - {q}")
    elif not_found_path.exists():
        not_found_path.unlink()  # all resolved this run — stale list would be misleading

    print(f"\n{fetched}/{len(queries)} judgments fetched to {raw_dir}/")
    return fetched


if __name__ == "__main__":
    main()
