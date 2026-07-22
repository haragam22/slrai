"""Shared parser for docs/judgments/*.md files — used by compile_class_a_wiki.py
and load_judgments.py.

Format v2.0 (see JUDGMENT_SUMMARY_PROMPT_v2.md for the full authoring spec):

    ---
    citation: "..."
    title: "..."
    short_name: "..."
    court: SUPREME_COURT
    high_court_state: null
    bench_strength: 2
    judgment_date: "2026-04-01"
    overruled: false
    overruled_by: null
    distinguished_by: []
    favor: BORROWER
    favor_verified: true
    ground_codes: [RIGHT_OF_REDEMPTION, AUCTION_PURCHASER]
    statutory_basis: RULES
    act_sections: ["Section 13(8)"]
    rules_sections: ["Rule 9(4)"]
    slrai_modules: [M3, M10]
    keywords: ["Rule 9(4)", "balance consideration", ...]
    source: SC_FULL_TEXT
    ik_doc_id: ""
    ik_url: "https://..."
    has_verified_conditions: true
    ---

    ## BORROWER'S CLAIM
    ...
    ## HOLDING SUMMARY
    ...
    ## KEY FACTS OF THIS CASE
    ...
    ## WHAT THE COURT DECIDED
    ...
    ## KEY QUOTE
    ...
    ## CONDITION: WHEN THIS JUDGMENT APPLIES
    ...
    ## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY
    ...
    ## STATUTORY CONTEXT
    ...
    ## RELATIONSHIP TO OTHER JUDGMENTS
    ...
    ## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES
    ...
    ## WIN-RATE CONTRIBUTION
    ...

The body is split into named sections by "## HEADING" — every section is
optional at parse time (missing sections default to ""), but HOLDING SUMMARY
is what drives the Qdrant embedding, so a judgment without it is barely
useful. compile_class_a_wiki.py is what enforces "must have holding_summary"
for inclusion, not this parser.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

REQUIRED_FIELDS = {"citation", "title", "short_name", "court", "favor", "ground_codes", "has_verified_conditions"}

# Maps "## SECTION HEADING" (case-insensitive, apostrophes/colons stripped for
# matching) -> the dict key it's stored under.
SECTION_KEY_MAP = {
    "BORROWER'S CLAIM":                                "borrower_claim",
    "HOLDING SUMMARY":                                 "holding_summary",
    "KEY FACTS OF THIS CASE":                          "key_facts",
    "WHAT THE COURT DECIDED":                          "court_decision",
    "KEY QUOTE":                                       "key_quote",
    "CONDITION: WHEN THIS JUDGMENT APPLIES":           "applicable_conditions_text",
    "CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY":    "exclusion_conditions_text",
    "STATUTORY CONTEXT":                               "statutory_context",
    "RELATIONSHIP TO OTHER JUDGMENTS":                 "relationship_to_other_judgments",
    "NEW REQUIREMENTS THIS JUDGMENT INTRODUCES":       "new_requirements",
    "WIN-RATE CONTRIBUTION":                           "win_rate_contribution",
}

_SECTION_HEADER_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


class JudgmentFileError(ValueError):
    pass


def _parse_body_sections(body: str) -> dict[str, str]:
    """Splits the markdown body on '## HEADING' lines into a dict keyed by
    SECTION_KEY_MAP's normalized names. Unknown headings are ignored (forward
    compatible with template additions); missing sections default to ""."""
    sections: dict[str, str] = {v: "" for v in SECTION_KEY_MAP.values()}

    matches = list(_SECTION_HEADER_RE.finditer(body))
    for i, m in enumerate(matches):
        heading = m.group(1).strip()
        key = SECTION_KEY_MAP.get(heading.upper())
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        if key:
            sections[key] = content

    return sections


def parse_judgment_md(path: Path) -> dict[str, Any]:
    """Parses one judgment .md file (v2.0 format) into a flat dict: all
    frontmatter fields + all body sections (see SECTION_KEY_MAP), with
    'holding_summary' also duplicated as the canonical embedding text."""
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        raise JudgmentFileError(f"{path}: missing YAML frontmatter (must start with '---')")

    parts = raw.split("---", 2)
    if len(parts) < 3:
        raise JudgmentFileError(f"{path}: malformed frontmatter block")

    frontmatter = yaml.safe_load(parts[1]) or {}
    body = parts[2].strip()

    missing = REQUIRED_FIELDS - frontmatter.keys()
    if missing:
        raise JudgmentFileError(f"{path}: missing required frontmatter fields: {sorted(missing)}")

    # Frontmatter defaults — v2.0 additions and legacy v1 fields both optional.
    frontmatter.setdefault("bench_strength", 1)
    frontmatter.setdefault("overruled", False)
    frontmatter.setdefault("overruled_by", None)
    frontmatter.setdefault("distinguished_by", [])
    frontmatter.setdefault("favor_verified", False)
    frontmatter.setdefault("statutory_basis", None)
    frontmatter.setdefault("act_sections", [])
    frontmatter.setdefault("rules_sections", [])
    frontmatter.setdefault("slrai_modules", [])
    frontmatter.setdefault("keywords", [])
    frontmatter.setdefault("source", "SC_FULL_TEXT")
    frontmatter.setdefault("ik_doc_id", "")
    frontmatter.setdefault("ik_url", "")
    frontmatter.setdefault("chunk_type", None)
    frontmatter.setdefault("high_court_state", None)
    frontmatter.setdefault("judgment_date", None)
    # Legacy v1 structured-condition fields — unused by the wiki-based
    # applicability engine (H7), kept for backward compatibility only.
    frontmatter.setdefault("applicable_conditions", [])
    frontmatter.setdefault("exclusion_conditions", [])

    sections = _parse_body_sections(body)
    frontmatter.update(sections)

    return frontmatter


def load_all_judgment_files(judgments_dir: Path) -> list[dict[str, Any]]:
    """Loads and parses every .md file in judgments_dir. Returns [] for an
    empty/missing directory — never raises for "no corpus yet"."""
    if not judgments_dir.exists():
        return []
    records = []
    for md_file in sorted(judgments_dir.glob("*.md")):
        records.append(parse_judgment_md(md_file))
    return records
