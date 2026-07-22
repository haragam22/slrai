"""Parses Document AI layout output into paragraph dicts and persists them.

text_original is written once, at insert time, and never modified afterward
(app-layer immutability rule — see CLAUDE_v51.md database section).
"""
import logging

from langdetect import LangDetectException, detect

from app.models.db import Paragraph, SyncSessionLocal

logger = logging.getLogger(__name__)

HEADING_MAX_LEN = 80
NUMBERED_PREFIXES = ("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "(i)", "(a)", "(1)")


def detect_paragraph_language(text: str) -> str:
    """Returns 'en', 'hi', or 'mixed'."""
    try:
        lang = detect(text)
    except LangDetectException:
        return "en"

    hindi_chars = sum(1 for c in text if "ऀ" <= c <= "ॿ")
    if lang == "hi":
        return "hi"
    if hindi_chars > 5:
        return "mixed"
    return "en"


def _looks_like_heading(text: str) -> bool:
    stripped = text.strip()
    return bool(stripped) and len(stripped) <= HEADING_MAX_LEN and stripped.isupper()


def _looks_numbered(text: str) -> bool:
    stripped = text.strip()
    return stripped.startswith(NUMBERED_PREFIXES)


def parse_ocr_result(ocr_result: dict) -> list[dict]:
    """
    Converts docai_ocr.extract_layout() output into paragraph dicts ready
    for save_paragraphs_to_db(). Assigns language per paragraph.
    """
    parsed = []
    for para in ocr_result["paragraphs"]:
        text = para["text"]
        parsed.append({
            "page_number":     para["page_number"],
            "para_sequence":   para["para_sequence"],
            "text_original":   text,
            "language":        detect_paragraph_language(text),
            "is_heading":      _looks_like_heading(text),
            "is_numbered":     _looks_numbered(text),
            "is_handwritten":  False,
            "bbox":            para.get("bbox"),
            "ocr_confidence":  para.get("ocr_confidence"),
        })
    return parsed


def save_paragraphs_to_db(document_id: str, paragraphs: list[dict]) -> int:
    """Bulk inserts parsed paragraphs for a document. Returns count inserted."""
    if not paragraphs:
        return 0

    rows = [
        Paragraph(
            document_id=document_id,
            page_number=p["page_number"],
            para_sequence=p["para_sequence"],
            text_original=p["text_original"],
            language=p["language"],
            is_heading=p["is_heading"],
            is_numbered=p["is_numbered"],
            is_handwritten=p["is_handwritten"],
            bbox=p.get("bbox"),
            ocr_confidence=p.get("ocr_confidence"),
        )
        for p in paragraphs
    ]

    with SyncSessionLocal() as db:
        db.bulk_save_objects(rows)
        db.commit()

    logger.info("saved %d paragraphs for document=%s", len(rows), document_id)
    return len(rows)
