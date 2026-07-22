"""Compiles Class A judgment .md files → docs/wiki/class_a_judgments_wiki.md.

Run offline, rebuild whenever a judgment .md file is added/updated:
    python scripts/compile_class_a_wiki.py

Safe on an empty docs/judgments/ dir — writes a wiki with a header only, so
Chain B's applicability.py can run (and correctly short-circuit to []) before
the corpus is loaded.

Entry headers use "### " (3 hashes) — applicability.py and callers count
Class A judgments in the wiki via `len(re.findall(r"^### ", wiki, re.MULTILINE))`.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _judgment_md import load_all_judgment_files  # noqa: E402

JUDGMENTS_DIR = Path("docs/judgments")
OUTPUT_PATH = Path("docs/wiki/class_a_judgments_wiki.md")


def _format_entry(j: dict) -> str:
    ground_codes = ", ".join(j.get("ground_codes") or [])
    modules = ", ".join(j.get("slrai_modules") or [])
    statutory_basis = j.get("statutory_basis") or "N/A"
    borrower_claim = j.get("borrower_claim") or "(not provided)"
    holding = j.get("holding_summary") or "(not provided)"
    applies_when = j.get("applicable_conditions_text") or "(not specified)"
    does_not_apply_when = j.get("exclusion_conditions_text") or "None"

    return (
        f"### [{j['court']}] {j['short_name']}\n"
        f"**Citation:** {j['citation']}\n"
        f"**Favor:** {j['favor']} | **Statutory basis:** {statutory_basis}\n"
        f"**Ground codes:** {ground_codes}\n"
        f"**Modules:** {modules}\n\n"
        f"**Borrower's claim:**\n{borrower_claim}\n\n"
        f"**Holding:**\n{holding}\n\n"
        f"**Applies when:**\n{applies_when}\n\n"
        f"**Does NOT apply when:**\n{does_not_apply_when}\n"
    )


def compile_wiki() -> int:
    records = load_all_judgment_files(JUDGMENTS_DIR)
    class_a = [j for j in records if j.get("has_verified_conditions") is True]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not class_a:
        OUTPUT_PATH.write_text(
            "# Class A Judgment Wiki\n\n"
            "No Class A judgments loaded yet. Run `python scripts/compile_class_a_wiki.py` "
            "again after adding .md files to docs/judgments/.\n",
            encoding="utf-8",
        )
        print(f"0 Class A judgments found in {JUDGMENTS_DIR} — wrote empty wiki.")
        return 0

    class_a.sort(key=lambda j: j["short_name"])
    header = f"# Class A Judgment Wiki\n\n{len(class_a)} verified judgments — loaded into Chain B context.\n\n"
    body = "\n---\n\n".join(_format_entry(j) for j in class_a)
    OUTPUT_PATH.write_text(header + body + "\n", encoding="utf-8")
    print(f"{len(class_a)} Class A judgments compiled into {OUTPUT_PATH}")
    return len(class_a)


if __name__ == "__main__":
    compile_wiki()
