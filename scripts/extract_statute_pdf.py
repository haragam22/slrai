"""Converts a statute PDF into clean bare-act-numbered .txt for build_law_wiki.py.

Raw copy/paste or generic pdftotext output is prone to exactly the kind of
typo that silently breaks build_law_wiki.py's clause regex (extra space
before a period, missing period after a section number, e.g. "13 .Enforcement"
or "13 Enforcement"). Rather than adding a second PDF library for text
extraction, this reuses the Document AI layout extractor already built for
SA documents (app/services/ocr/docai_ocr.py) — its paragraph-level output is
far less prone to that class of error than raw text-layer extraction,
because it reconstructs paragraphs from layout geometry, not
character-stream order.

Document AI's synchronous process_document API caps input at 15 pages in
non-imageless mode for this processor (see
google.api_core.exceptions.InvalidArgument: PAGE_LIMIT_EXCEEDED). Statute
PDFs routinely exceed that (SARFAESI Rules alone ran 38+ pages), so this
script splits the source PDF into <=15-page chunks with pypdf, calls
Document AI once per chunk, and concatenates the paragraphs in order —
same page-break blank-line behavior as a single call.

This does NOT fix every possible OCR error — it produces a best-effort .txt
that you should spot-check, especially around section boundaries and chunk
seams. If build_law_wiki.py's gap warning fires after this, check the
flagged section by hand.

Usage:
    python scripts/extract_statute_pdf.py path/to/sarfaesi_act.pdf docs/statutes/sarfaesi_act.txt
"""
import sys
from pathlib import Path

# Normalizes the exact patterns known to break CLAUSE_START_RE in build_law_wiki.py:
#   "13 .Enforcement"  -> "13. Enforcement"   (stray space before the dot)
#   "13 Enforcement"   -> "13. Enforcement"   (missing dot) — only applied when
#                                               the word after the number is
#                                               capitalized, to avoid mangling
#                                               ordinary sentences like "13 days".
import re

_STRAY_SPACE_BEFORE_DOT = re.compile(r"^(\s*\d+[A-Za-z]?)\s+\.\s*(?=\S)", re.MULTILINE)
_MISSING_DOT_AFTER_NUMBER = re.compile(r"^(\s*\d+[A-Za-z]?)\s+(?=[A-Z][a-z])", re.MULTILINE)


def normalize_clause_numbering(text: str) -> str:
    text = _STRAY_SPACE_BEFORE_DOT.sub(r"\1. ", text)
    text = _MISSING_DOT_AFTER_NUMBER.sub(r"\1. ", text)
    return text


def extract_pdf_to_text(pdf_path: Path) -> str:
    # extract_layout() in app/services/ocr/docai_ocr.py already handles
    # <=15-page chunking + Document AI calls + page renumbering — same
    # splitter this script used to duplicate locally.
    from app.services.ocr.docai_ocr import extract_layout

    file_bytes = pdf_path.read_bytes()
    result = extract_layout(file_bytes)

    lines = []
    last_page = None
    for para in result["paragraphs"]:
        if last_page is not None and para["page_number"] != last_page:
            lines.append("")  # blank line at page breaks — helps eyeball review
        lines.append(para["text"])
        last_page = para["page_number"]

    return "\n\n".join(lines)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python scripts/extract_statute_pdf.py <input.pdf> <output.txt>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    if not pdf_path.exists():
        print(f"ERROR: {pdf_path} not found.")
        sys.exit(1)

    raw_text = extract_pdf_to_text(pdf_path)
    normalized_text = normalize_clause_numbering(raw_text)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(normalized_text, encoding="utf-8")

    changed = raw_text != normalized_text
    print(f"Wrote {out_path} ({len(normalized_text)} chars).")
    if changed:
        print("Applied clause-numbering normalization (stray space / missing dot fixes).")
    print("Spot-check section boundaries before running build_law_wiki.py — "
          "OCR layout extraction is best-effort, not guaranteed typo-free.")


if __name__ == "__main__":
    main()
