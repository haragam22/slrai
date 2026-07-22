"""Class A applicability — wiki-based (v5.3), single Claude call per case.

Class A (75 manually-verified judgments) is small enough to load in full into
Chain B context — no per-judgment condition matching. Class B (~7,400 Qdrant
judgments) never gets an applicability check: it is returned as-is with
status SIMILARITY_RETRIEVED (see 15.3b / report Section B honesty distinction).
"""
from __future__ import annotations

import json
import logging
import time

import anthropic

from app.config import settings

logger = logging.getLogger(__name__)

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

_wiki_cache: str | None = None
_third_party_wiki_cache: str | None = None


def _load_class_a_wiki() -> str:
    """Loads class_a_judgments_wiki.md into memory, cached at module level.
    Returns "" if the wiki hasn't been compiled yet (empty/no-corpus state) —
    callers must treat "" as "no Class A judgments available"."""
    global _wiki_cache
    if _wiki_cache is None:
        try:
            with open(settings.class_a_judgments_wiki_path, "r", encoding="utf-8") as f:
                _wiki_cache = f.read().strip()
        except FileNotFoundError:
            _wiki_cache = ""
    return _wiki_cache


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

Return ONLY a valid JSON array — one object per judgment considered. No preamble, no markdown.
Each object must have this exact structure:
{
  "short_name":    "the judgment's short_name exactly as given",
  "citation":      "the judgment's citation exactly as given",
  "applicable":    true | false,
  "reason":        "one sentence — which specific confirmed fact(s) support or rule out applicability",
  "favor":         "BANK" | "BORROWER" | "NEUTRAL",
  "relevant_fact":  "the single confirmed fact field name most relevant to this determination, or null"
}

Rules:
- Only include judgments whose ground_codes overlap with the grounds raised in this case.
- Each judgment entry in the library has an "Applies when:" section AND a
  "Does NOT apply when:" section. You MUST check BOTH before deciding. A judgment
  is "applicable": true only if the case facts affirmatively satisfy the "Applies when"
  conditions AND do NOT match any "Does NOT apply when" exclusion.
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
    prompt changes per-case without invalidating the cache."""
    facts_json = json.dumps(confirmed_facts, default=str, ensure_ascii=False, indent=2)
    grounds_json = json.dumps(sorted(sa_grounds), ensure_ascii=False)
    return (
        f"Grounds raised in this case: {grounds_json}\n\n"
        f"Confirmed case facts:\n{facts_json}"
    )


def _build_system_blocks() -> list[dict]:
    """System prompt as content blocks with a cache_control breakpoint after
    the static judgment library + statutory wiki — both are byte-identical
    across every Chain B call until the wiki files are rebuilt, so this
    turns the previous "resend ~65k+ tokens every case" cost into one
    full-price write + cheap cache reads. See plan at
    .claude/plans/starry-orbiting-kite.md finding #1."""
    third_party_wiki = _load_third_party_wiki()
    statutory_context = (
        f"\n\nSupporting statutory context (RDB Act, TPA, IBC):\n{third_party_wiki}"
        if third_party_wiki else ""
    )
    blocks = [{"type": "text", "text": APPLICABILITY_SYSTEM_PROMPT}]
    blocks.append({
        "type": "text",
        "text": f"\n\nJudgment library:\n{_load_class_a_wiki()}{statutory_context}",
        "cache_control": {"type": "ephemeral"},
    })
    return blocks


def evaluate_class_a_applicability(
    confirmed_facts: dict,
    sa_grounds: list[str],
    judgment_count: int,
    max_retries: int = 2,
) -> list[dict]:
    """
    Single Claude call evaluating every Class A judgment relevant to the
    grounds raised in this case against confirmed facts.
    Returns [] immediately (no API call) if the Class A wiki is empty —
    lets Chain B run end-to-end before the judgment corpus is loaded.
    Returns [{short_name, citation, applicable, reason, favor, relevant_fact}, ...].
    """
    wiki = _load_class_a_wiki()
    if not wiki or judgment_count == 0:
        logger.info("Class A wiki empty or judgment_count=0 — skipping applicability call")
        return []

    if not sa_grounds:
        return []

    prompt = _build_user_prompt(confirmed_facts, sa_grounds)
    system_blocks = _build_system_blocks()

    for attempt in range(max_retries + 1):
        try:
            response = client.messages.create(
                model=settings.claude_model,
                max_tokens=4000,
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

        except anthropic.APITimeoutError as exc:
            logger.warning("applicability: Claude API timeout (attempt %d/%d): %s", attempt + 1, max_retries + 1, exc)
            if attempt == max_retries:
                return []
            time.sleep(5)

        except anthropic.RateLimitError:
            raise  # re-raise to Celery for exponential backoff retry

        except anthropic.AuthenticationError:
            raise  # fatal — wrong key, Celery sets case FAILED

        except Exception:
            logger.exception("applicability: unexpected error evaluating %d judgments", judgment_count)
            return []


def process_class_b_candidates(class_b_candidates: list[dict]) -> list[dict]:
    """Class B gets no applicability check — flagged as-is with
    status=SIMILARITY_RETRIEVED (see report Section B honesty distinction)."""
    return [
        {
            "judgment": judgment,
            "status": "SIMILARITY_RETRIEVED",
            "reason": "No verified conditions. Included as potentially relevant.",
        }
        for judgment in class_b_candidates
    ]
