"""Judgment applicability — wiki-based (v6), single Claude call per case.

The corpus is the ~69 curated judgment .md files in docs/judgments/ — small
enough to load in full into Chain B context every case, no vector retrieval
needed for the applicability check itself (Qdrant is still used upstream in
retrieval.py to pre-filter candidates by ground_code before this runs).
There is no Class B / unverified tier anymore — every judgment in the corpus
gets the same applicability evaluation.
"""
from __future__ import annotations

import json
import logging
import sys
import time
from pathlib import Path

from app.config import settings
from app.services import llm_client
from app.services.llm_client import client

logger = logging.getLogger(__name__)

_JUDGMENTS_DIR = Path(__file__).resolve().parents[3] / "docs" / "judgments"
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))

_wiki_cache: str | None = None
_judgment_count_cache: int = 0
_third_party_wiki_cache: str | None = None
_sarfaesi_law_wiki_cache: str | None = None


def _load_class_a_wiki() -> str:
    """Builds the judgment wiki live from docs/judgments/*.md, cached at
    module level (built once per worker process). Returns "" if the corpus
    directory is empty/missing — callers must treat "" as "no judgments
    available". Replaces the old compiled docs/wiki/class_a_judgments_wiki.md
    cache file, which silently went stale (last compiled at 47 judgments,
    corpus has since grown to 69) — the .md folder is the source of truth,
    no separate build step to forget."""
    global _wiki_cache, _judgment_count_cache
    if _wiki_cache is None:
        from _judgment_md import format_judgment_entry, load_all_judgment_files

        records = load_all_judgment_files(_JUDGMENTS_DIR)
        _judgment_count_cache = len(records)
        if not records:
            _wiki_cache = ""
        else:
            records.sort(key=lambda j: j["short_name"])
            header = f"{len(records)} verified judgments — loaded into Chain B context.\n\n"
            body = "\n---\n\n".join(format_judgment_entry(j) for j in records)
            _wiki_cache = header + body
    return _wiki_cache


def _load_sarfaesi_law_wiki() -> str:
    """Loads sarfaesi_law_wiki.md (full SARFAESI Act + Enforcement Rules
    digest) into memory, cached at module level. Every SA in this corpus
    operates on this statutory base — it's compulsory context for every
    applicability call, not retrieved, always injected (same pattern as
    third_party_wiki below). Previously this was only loaded in
    nlp_layer.py (fact extraction) — the applicability/reasoning step never
    saw it, which is why judgment relevance reasoning couldn't cite specific
    Act sections or Rule numbers."""
    global _sarfaesi_law_wiki_cache
    if _sarfaesi_law_wiki_cache is None:
        try:
            with open(settings.sarfaesi_law_wiki_path, "r", encoding="utf-8") as f:
                _sarfaesi_law_wiki_cache = f.read().strip()
        except FileNotFoundError:
            logger.warning("%s not found", settings.sarfaesi_law_wiki_path)
            _sarfaesi_law_wiki_cache = ""
    return _sarfaesi_law_wiki_cache


def _load_third_party_wiki() -> str:
    """Loads third_party_law_wiki.md (RDB Act, TPA, IBC, Registration Act,
    Stamp Act) into memory, cached at module level. Loaded unconditionally
    into every Chain B applicability call — RDB Act's DRT jurisdiction/interim
    relief provisions (Section 19(25) etc.) are needed for every analysis,
    not just third-party/tenancy/IBC/completed-auction cases. Returns "" if
    the wiki hasn't been built yet (build_law_wiki.py not run)."""
    global _third_party_wiki_cache
    if _third_party_wiki_cache is None:
        try:
            with open(settings.third_party_wiki_path, "r", encoding="utf-8") as f:
                _third_party_wiki_cache = f.read().strip()
        except FileNotFoundError:
            logger.warning("%s not found — run scripts/build_law_wiki.py", settings.third_party_wiki_path)
            _third_party_wiki_cache = ""
    return _third_party_wiki_cache


APPLICABILITY_SYSTEM_PROMPT = """You are a legal analyst matching Indian SARFAESI case precedents to the facts of a case.
You will receive a library of verified judgment summaries and the confirmed facts of a case.
For EACH judgment in the library whose ground_codes overlap with the grounds raised in this case,
decide whether the judgment's holding applies to these specific facts.

You will also receive the full text of the SARFAESI Act and Security Interest
(Enforcement) Rules 2002 — every case in this corpus operates on this statutory
base. Ground your reasoning in it: cite the actual Act section or Rule number
that governs the ground in question, not just the judgment's holding in the
abstract.

Return ONLY a valid JSON array — one object per judgment considered. No preamble, no markdown.
Each object must have this exact structure:
{
  "short_name":    "the judgment's short_name exactly as given",
  "citation":      "the judgment's citation exactly as given",
  "applicable":    true | false,
  "reason":        "2-4 sentences covering: (a) the specific Act section or Rule number governing this ground, (b) the confirmed case fact(s) that trigger or fail it, (c) the judgment's ratio applied to those specific facts, (d) net effect on this ground's strength. Cite section/rule numbers by name — do not just restate the judgment's holding_summary verbatim.",
  "favor":         "BANK" | "BORROWER" | "NEUTRAL",
  "relevant_fact":  "the single confirmed fact field name most relevant to this determination, or null"
}

Rules:
- Only include judgments whose ground_codes overlap with the grounds raised in this case.
- Each judgment entry in the library has an "Applies when:" section AND a
  "Does NOT apply when:" section. You MUST check BOTH before deciding. A judgment
  is "applicable": true only if the case facts affirmatively satisfy the "Applies when"
  conditions AND do NOT match any "Does NOT apply when" exclusion.
- A judgment's "Statutory basis" field tells you which body of law it actually
  belongs to (e.g. SARFAESI, IBC, RDB Act). If a judgment's own statutory basis
  doesn't match the enforcement measure actually being challenged in this case
  (e.g. an IBC Section 7 admission judgment when this case is a SARFAESI
  auction challenge), it is NOT applicable regardless of surface keyword overlap
  in the ground_code — say so explicitly in the reason.
- When two judgments in the library address the same type of dispute but reach
  opposite outcomes (their "Does NOT apply when" section names the other judgment
  as the alternative — an "SLRAI ROUTING" note), route strictly on the routing
  field/value given — never let both judgments come back applicable=true for the
  same fact pattern.
- If a required fact is not confirmed, applicable=false with reason explaining
  what is unconfirmed — do not guess.
- Never fabricate a judgment not present in the library."""


def _build_user_prompt(confirmed_facts: dict, sa_grounds: list[str]) -> str:
    """Dynamic part only — the static judgment library + statutory wiki live
    in the cached system prompt (_build_system_blocks) instead, so this
    prompt changes per-case without invalidating the cache. Tagged the same
    way as the system blocks (<case_facts>) so this case's specific facts
    stay clearly separated from the static law/judgment text above it —
    same delimiting discipline as _build_system_blocks, not just this one
    call site."""
    facts_json = json.dumps(confirmed_facts, default=str, ensure_ascii=False, indent=2)
    grounds_json = json.dumps(sorted(sa_grounds), ensure_ascii=False)
    return (
        "<case_facts>\n"
        f"Grounds raised in this case: {grounds_json}\n\n"
        f"Confirmed case facts:\n{facts_json}\n"
        "</case_facts>"
    )


def _build_system_blocks() -> list[dict]:
    """System prompt + three clearly-delimited context blocks: statutory law,
    then the judgment library, in that order — law is the foundation the
    judgments interpret, so it's presented first, not buried after the
    precedents. Each block is its own tagged section (not one flat
    concatenated string) so the model doesn't blend a judgment's holding
    with a Rule's text or a different Act's provisions — this is what was
    missing before (Gemini's "semantic crowding" claim didn't apply to
    retrieval, since these were never in a shared vector store, but a flat
    untagged text blob at the *prompt* level was still a real legibility
    risk worth closing off explicitly).

    All three are byte-identical across every Chain B call until the wiki/
    corpus files change, so a single cache_control breakpoint at the end
    covers the whole assembled block — one full-price write, cheap cache
    reads on every subsequent case. See plan at
    .claude/plans/starry-orbiting-kite.md finding #1."""
    sarfaesi_wiki = _load_sarfaesi_law_wiki()
    third_party_wiki = _load_third_party_wiki()
    judgment_wiki = _load_class_a_wiki()

    sections = [APPLICABILITY_SYSTEM_PROMPT]

    if sarfaesi_wiki:
        sections.append(
            "\n\n<statutory_law jurisdiction=\"primary\">\n"
            "The following is the SARFAESI Act, 2002 + Security Interest "
            "(Enforcement) Rules, 2002 — the compulsory statutory base every "
            "case in this corpus operates on. Ground every applicability "
            "decision in this text: cite the actual section/rule number.\n\n"
            f"{sarfaesi_wiki}\n"
            "</statutory_law>"
        )
    if third_party_wiki:
        sections.append(
            "\n\n<statutory_law jurisdiction=\"supporting\">\n"
            "Supporting statutory context — RDB Act, Transfer of Property Act, "
            "IBC. Only relevant when a judgment's own statutory_basis is one "
            "of these, not SARFAESI itself. Do not let this override or blend "
            "with the primary SARFAESI text above — they govern different "
            "measures.\n\n"
            f"{third_party_wiki}\n"
            "</statutory_law>"
        )
    if judgment_wiki:
        sections.append(
            "\n\n<judgment_library>\n"
            "The following are the verified judgments in this case's corpus. "
            "Each entry states its own statutory_basis, ground_codes, "
            "\"Applies when\", and \"Does NOT apply when\" — treat each entry "
            "as self-contained; do not merge one judgment's holding with "
            "another's or with the statutory text above.\n\n"
            f"{judgment_wiki}\n"
            "</judgment_library>"
        )

    blocks = [{"type": "text", "text": sections[0]}]
    if len(sections) > 1:
        blocks.append({
            "type": "text",
            "text": "".join(sections[1:]),
            "cache_control": {"type": "ephemeral"},
        })
    return blocks


def evaluate_class_a_applicability(
    confirmed_facts: dict,
    sa_grounds: list[str],
    judgment_count: int | None = None,
    max_retries: int = 2,
) -> list[dict]:
    """
    Single Claude call evaluating every judgment in the corpus relevant to
    the grounds raised in this case against confirmed facts.
    Returns [] immediately (no API call) if the corpus is empty — lets
    Chain B run end-to-end before docs/judgments/ has any files.
    judgment_count is accepted for backward-compat with existing callers but
    ignored — the live loader's own count (_judgment_count_cache) is what's
    checked, since the corpus is read straight from docs/judgments/ now.
    Returns [{short_name, citation, applicable, reason, favor, relevant_fact}, ...].
    """
    wiki = _load_class_a_wiki()
    if not wiki or _judgment_count_cache == 0:
        logger.info("Judgment corpus empty — skipping applicability call")
        return []

    if not sa_grounds:
        return []

    prompt = _build_user_prompt(confirmed_facts, sa_grounds)
    system_blocks = _build_system_blocks()

    for attempt in range(max_retries + 1):
        try:
            response = client.messages.create(
                model=llm_client.MODEL,
                max_tokens=64000,  # Claude Sonnet's max output — no artificial cap
                temperature=settings.llm_temperature,
                system=system_blocks,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = response.content[0].text.strip()
            raw = raw.replace("```json", "").replace("```", "").strip()
            result = json.loads(raw)
            if not isinstance(result, list):
                raise ValueError(f"Expected JSON array, got {type(result).__name__}")
            return result

        except (json.JSONDecodeError, ValueError) as exc:
            logger.warning("applicability: bad response (attempt %d/%d): %s", attempt + 1, max_retries + 1, exc)
            if attempt == max_retries:
                return []
            time.sleep(1)

        except llm_client.APITimeoutError as exc:
            logger.warning("applicability: Claude API timeout (attempt %d/%d): %s", attempt + 1, max_retries + 1, exc)
            if attempt == max_retries:
                return []
            time.sleep(5)

        except llm_client.RateLimitError:
            raise  # re-raise to Celery for exponential backoff retry

        except llm_client.AuthenticationError:
            raise  # fatal — wrong key, Celery sets case FAILED

        except Exception:
            logger.exception("applicability: unexpected error evaluating judgments for grounds=%s", sa_grounds)
            return []
