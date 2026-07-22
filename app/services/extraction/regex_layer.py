"""Layer A — deterministic regex extraction of case facts. Runs first, always.

All regex hits get confidence=1.0 and extraction_method="regex" — they never
go to the workbench (see confidence_router.py routing rules).
"""
import re
from datetime import date
from decimal import Decimal, InvalidOperation

REGEX_PATTERNS = {
    "date_dmy_dot":   re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b"),
    "date_dmy_slash": re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b"),
    "date_written":   re.compile(
        r"\b(\d{1,2})(?:st|nd|rd|th)?\s+"
        r"(January|February|March|April|May|June|July|August|September|October|November|December)"
        r"\s+(\d{4})\b",
        re.IGNORECASE,
    ),
    "amount_inr": re.compile(
        r"(?:Rs\.?|INR|Rupees?)\s*"
        r"([\d,]+(?:\.\d{2})?)"
        r"(?:\s*(?:lakhs?|lacs?|crores?|thousands?|/-))?"
    ),
    "section_ref": re.compile(
        r"(?:[Ss]ection|[Ss]ec\.?|[Ss]\.)\s*"
        r"(\d+(?:\([A-Za-z0-9]+\))*)",
        re.IGNORECASE,
    ),
    "rule_ref": re.compile(r"[Rr]ule\s+(\d+[A-Za-z]?(?:\([A-Za-z0-9]+\))*)"),
}

MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}


def extract_dates(text: str) -> list[dict]:
    """Returns list of {date, raw_text, confidence: 1.0, extraction_method: 'regex'}"""
    results = []
    for pattern_name, pattern in {
        k: v for k, v in REGEX_PATTERNS.items() if k.startswith("date_")
    }.items():
        for match in pattern.finditer(text):
            try:
                if pattern_name == "date_written":
                    d = date(
                        int(match.group(3)),
                        MONTH_MAP[match.group(2).lower()],
                        int(match.group(1)),
                    )
                else:
                    d = date(
                        int(match.group(3)),
                        int(match.group(2)),
                        int(match.group(1)),
                    )
                results.append({
                    "date": d.isoformat(),
                    "raw_text": match.group(0),
                    "confidence": 1.0,
                    "extraction_method": "regex",
                })
            except ValueError:
                continue  # invalid date (e.g. 31/02/2023) — skip
    return results


def extract_amounts(text: str) -> list[dict]:
    """Returns list of {amount, raw_text, confidence: 1.0, extraction_method: 'regex'}"""
    results = []
    for match in REGEX_PATTERNS["amount_inr"].finditer(text):
        amount_str = match.group(1).replace(",", "")
        try:
            results.append({
                "amount": str(Decimal(amount_str)),
                "raw_text": match.group(0),
                "confidence": 1.0,
                "extraction_method": "regex",
            })
        except InvalidOperation:
            continue
    return results


def extract_section_refs(text: str) -> list[dict]:
    """Returns list of {ref_type, section_number, raw_text, confidence: 1.0, extraction_method: 'regex'}"""
    results = []
    for match in REGEX_PATTERNS["section_ref"].finditer(text):
        results.append({
            "ref_type": "section",
            "section_number": match.group(1),
            "raw_text": match.group(0),
            "confidence": 1.0,
            "extraction_method": "regex",
        })
    for match in REGEX_PATTERNS["rule_ref"].finditer(text):
        results.append({
            "ref_type": "rule",
            "section_number": match.group(1),
            "raw_text": match.group(0),
            "confidence": 1.0,
            "extraction_method": "regex",
        })
    return results


def extract_all(text: str) -> dict:
    """Convenience entry point — runs all Layer A extractors on one paragraph."""
    return {
        "dates": extract_dates(text),
        "amounts": extract_amounts(text),
        "section_refs": extract_section_refs(text),
    }
