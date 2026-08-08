"""Judgment summarizer — turns raw fetched text into what the pipeline loads.

    python scripts/summarize_judgments.py

Reads every docs/judgments_raw/<slug>.txt (+ its <slug>.meta.json sidecar,
written by fetch_from_ik.py) and writes docs/judgments/<slug>.md. This is the
file load_judgments.py reads; load_judgments.py's output (Postgres + Qdrant)
is what Chain B's applicability/retrieval step queries during a case run —
the raw .txt is never read at case-run time.

Two-stage per judgment, not one prompt-and-hope:
  1. REASON — the model (a thinking model, e.g. Qwen3-235B-thinking) is given
     JUDGMENT_SUMMARY_PROMPT_v2.md verbatim and free rein to work through the
     judgment and answer in that prompt's own markdown template. This is
     where the legal reasoning happens.
  2. LOCK — a second call takes stage 1's answer and re-emits it as JSON
     against a strict schema (OpenRouter response_format=json_schema). This
     call does no new reasoning, only extraction — its job is to guarantee
     every field OpenRouter/the model would have to hand-format correctly
     (YAML frontmatter, list syntax, exact enum values) is instead schema-
     validated. We render the final .md from that JSON ourselves, so a
     malformed YAML block from the model can never reach disk.

Claude/the model sets has_verified_conditions itself per the prompt's own
guardrail — treat any has_verified_conditions:true it produces as a draft,
not a verified Class A judgment, until a human actually checks the field
names against CaseFactSchema and the source text (project rule: Class A
needs a human sign-off, per CLAUDE_v51.md).

Skips (does not overwrite) any <slug>.md that already exists — re-run safe
after adding new raw files. Pass --force to regenerate everything.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

PROMPT_PATH = Path(__file__).parent.parent / "JUDGMENT_SUMMARY_PROMPT_v2.md"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

VALID_GROUND_CODES = [
    "SERVICE_DEFECT", "AMOUNT_DISPUTE", "REPLY_NOT_GIVEN", "AUCTION_GAP_DEFECT",
    "NEWSPAPER_PUB_DEFECT", "LIMITATION_EXPIRED", "TENANCY_CLAIM", "VALUATION_DISPUTE",
    "NOTICE_ALL_PARTIES", "NPA_PREMATURE", "NPA_DURING_RESTRUC", "MSME_RESTRUC_SKIPPED",
    "POSSESSION_DEFECT", "NOTICE_FORMAT_DEFECT", "AO_AUTHORIZATION",
    "AUCTION_NOTICE_AFFIXING", "AUCTION_DURING_STAY", "PENDING_SA_CONCEALED",
    "THIRD_PARTY_ATS", "AUCTION_PURCHASER", "RIGHT_OF_REDEMPTION",
    "SECOND_SA_FRESH_CAUSE", "UNKNOWN",
]

# Stage 2's schema — every field the .md template needs, typed and enum-
# constrained so the model can't hand us broken YAML/list syntax. Body
# sections stay free-text (that's prose, not structured data) but every
# frontmatter field that drives retrieval/routing is locked down.
LOCK_SCHEMA = {
    "name": "judgment_interpretation",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "citation": {"type": "string"},
            "title": {"type": "string"},
            "short_name": {"type": "string", "maxLength": 60},
            "court": {"type": "string", "enum": ["SUPREME_COURT", "HIGH_COURT", "DRAT", "DRT"]},
            "high_court_state": {"type": ["string", "null"]},
            "bench_strength": {"type": "integer", "minimum": 1},
            "judgment_date": {"type": ["string", "null"]},
            "overruled": {"type": "boolean"},
            "overruled_by": {"type": ["string", "null"]},
            "distinguished_by": {"type": "array", "items": {"type": "string"}},
            "favor": {"type": "string", "enum": ["BANK", "BORROWER", "NEUTRAL"]},
            "favor_verified": {"type": "boolean"},
            "ground_codes": {
                "type": "array", "minItems": 1,
                "items": {"type": "string", "enum": VALID_GROUND_CODES},
            },
            "statutory_basis": {"type": "string", "enum": ["ACT", "RULES", "BOTH", "RBI", "TPA", "IBC", "OTHER"]},
            "act_sections": {"type": "array", "items": {"type": "string"}},
            "rules_sections": {"type": "array", "items": {"type": "string"}},
            "slrai_modules": {"type": "array", "items": {"type": "string"}},
            "keywords": {"type": "array", "items": {"type": "string"}},
            "retrieval_condition": {"type": "string", "maxLength": 200},
            "source": {"type": "string", "enum": ["SC_FULL_TEXT", "HC_FULL_TEXT", "DRAT_FULL_TEXT", "IBC_LAW_SUMMARY", "IK_SUMMARY"]},
            "ik_doc_id": {"type": "string"},
            "ik_url": {"type": "string"},
            "has_verified_conditions": {"type": "boolean"},
            "borrower_claim": {"type": "string"},
            "holding_summary": {"type": "string"},
            "key_facts": {"type": "string"},
            "court_decision": {"type": "string"},
            "key_quote": {"type": "string"},
            "applicable_conditions_text": {"type": "string"},
            "exclusion_conditions_text": {"type": "string"},
            "statutory_context": {"type": "string"},
            "relationship_to_other_judgments": {"type": "string"},
            "new_requirements": {"type": "string"},
            "confident": {"type": "boolean"},
        },
        "required": [
            "citation", "title", "short_name", "court", "high_court_state", "bench_strength",
            "judgment_date", "overruled", "overruled_by", "distinguished_by", "favor",
            "favor_verified", "ground_codes", "statutory_basis", "act_sections", "rules_sections",
            "slrai_modules", "keywords", "retrieval_condition", "source", "ik_doc_id", "ik_url", "has_verified_conditions",
            "borrower_claim", "holding_summary", "key_facts", "court_decision", "key_quote",
            "applicable_conditions_text", "exclusion_conditions_text", "statutory_context",
            "relationship_to_other_judgments", "new_requirements", "confident",
        ],
    },
}

LOCK_SYSTEM_PROMPT = """You are given a completed SARFAESI judgment analysis (produced against a
markdown template) below. Re-emit its content as the JSON object described by the
response schema. Do not reason further, do not change any legal conclusion, do not
add or drop information — this is a format conversion only.

Rules:
- Emit ONE FLAT JSON object — every field (citation, title, court, favor,
  ground_codes, holding_summary, etc.) is a TOP-LEVEL key. The source template
  groups fields under comments like "# IDENTITY" / "# CLASSIFICATION" /
  "# SLRAI ROUTING" / "# SOURCE" for human readability only — do NOT reproduce
  those as nested JSON objects (e.g. {"identity": {"citation": ...}} is wrong;
  {"citation": ...} at the top level is correct).
- If the source analysis is missing a field, use your best reading of the analysis
  text to fill it; never leave a required field empty.
- ground_codes/court/favor/statutory_basis/source must be one of the schema's enum
  values — pick the closest valid one, never invent a new value.
- Set "confident": false if the source analysis itself expressed uncertainty about
  the ratio, ground code, or court — never guess past what the source already said."""


class OpenRouterAuthError(RuntimeError):
    pass


def _call_openrouter(
    system_prompt: str, user_content: str, response_format: dict | None = None, model: str | None = None,
) -> str:
    import httpx

    from app.config import settings

    if not settings.openrouter_api_key:
        raise OpenRouterAuthError("OPENROUTER_API_KEY not set")

    payload = {
        "model": model or settings.openrouter_model,
        "temperature": 0.0,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    }
    if response_format:
        payload["response_format"] = response_format

    resp = httpx.post(
        OPENROUTER_URL,
        headers={"Authorization": f"Bearer {settings.openrouter_api_key}"},
        json=payload,
        timeout=300.0,
    )
    if resp.status_code == 401:
        raise OpenRouterAuthError(resp.text)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


def _yaml_str(value) -> str:
    return json.dumps(value) if value is not None else "null"


def _yaml_list(values: list[str]) -> str:
    return "[" + ", ".join(json.dumps(v) for v in values) + "]"


def render_judgment_md(data: dict) -> str:
    """Deterministic renderer — the only thing that ever writes YAML
    frontmatter to disk, so a model's formatting mistakes can't reach it."""
    ground_codes = data["ground_codes"]
    return (
        "---\n"
        f"citation: {_yaml_str(data['citation'])}\n"
        f"title: {_yaml_str(data['title'])}\n"
        f"short_name: {_yaml_str(data['short_name'])}\n"
        f"court: {data['court']}\n"
        f"high_court_state: {_yaml_str(data['high_court_state'])}\n"
        f"bench_strength: {data['bench_strength']}\n"
        f"judgment_date: {_yaml_str(data['judgment_date'])}\n"
        f"overruled: {str(data['overruled']).lower()}\n"
        f"overruled_by: {_yaml_str(data['overruled_by'])}\n"
        f"distinguished_by: {_yaml_list(data['distinguished_by'])}\n"
        f"favor: {data['favor']}\n"
        f"favor_verified: {str(data['favor_verified']).lower()}\n"
        f"ground_codes: {_yaml_list(ground_codes)}\n"
        f"statutory_basis: {data['statutory_basis']}\n"
        f"act_sections: {_yaml_list(data['act_sections'])}\n"
        f"rules_sections: {_yaml_list(data['rules_sections'])}\n"
        f"slrai_modules: {_yaml_list(data['slrai_modules'])}\n"
        f"keywords: {_yaml_list(data['keywords'])}\n"
        f"retrieval_condition: {_yaml_str(data['retrieval_condition'])}\n"
        f"source: {data['source']}\n"
        f"ik_doc_id: {_yaml_str(data['ik_doc_id'])}\n"
        f"ik_url: {_yaml_str(data['ik_url'])}\n"
        f"has_verified_conditions: {str(data['has_verified_conditions']).lower()}\n"
        "chunk_type: null\n"
        "applicable_conditions: []\n"
        "exclusion_conditions: []\n"
        "---\n\n"
        f"## BORROWER'S CLAIM\n\n{data['borrower_claim']}\n\n"
        f"## HOLDING SUMMARY\n\n{data['holding_summary']}\n\n"
        f"## KEY FACTS OF THIS CASE\n\n{data['key_facts']}\n\n"
        f"## WHAT THE COURT DECIDED\n\n{data['court_decision']}\n\n"
        f"## KEY QUOTE\n\n{data['key_quote']}\n\n"
        f"## CONDITION: WHEN THIS JUDGMENT APPLIES\n\n{data['applicable_conditions_text']}\n\n"
        f"## CONDITION: WHEN THIS JUDGMENT DOES NOT APPLY\n\n{data['exclusion_conditions_text']}\n\n"
        f"## STATUTORY CONTEXT\n\n{data['statutory_context']}\n\n"
        f"## RELATIONSHIP TO OTHER JUDGMENTS\n\n{data['relationship_to_other_judgments']}\n\n"
        f"## NEW REQUIREMENTS THIS JUDGMENT INTRODUCES\n\n{data['new_requirements']}\n\n"
        f"## WIN-RATE CONTRIBUTION\n"
        f"favor: {data['favor']}\n"
        f"counted_in_ground: {ground_codes[0]}\n"
    )


def _flatten_locked_data(data: dict) -> dict:
    """Some providers (observed: Alibaba/qwen3-235b-thinking via OpenRouter)
    don't actually enforce json_schema 'strict' mode — the model mirrors the
    source prompt's human-readable grouping comments (# IDENTITY,
    # CLASSIFICATION, # SLRAI ROUTING, # SOURCE) as nested JSON objects
    instead of emitting the flat schema, and the nesting depth/shape isn't even
    consistent call-to-call (observed: different attempts against the same
    judgment nested different fields). Recursively un-nest every dict-valued
    field so any nesting shape still surfaces every leaf key at the top level."""
    flat: dict = {}

    def _walk(d: dict) -> None:
        # Claim this level's scalar keys before recursing, so a shallower
        # (more likely correct) value always wins over a same-named leaf
        # found deeper in the nesting.
        for key, value in d.items():
            if not isinstance(value, dict):
                flat.setdefault(key, value)
        for value in d.values():
            if isinstance(value, dict):
                _walk(value)

    _walk(data)
    return flat


def summarize_one(slug: str, judgment_text: str, meta: dict, max_retries: int = 2) -> str | None:
    """Returns the rendered .md content, or None if the model was uncertain
    or repeatedly failed to produce a valid, schema-locked interpretation."""
    from _judgment_md import JudgmentFileError, parse_judgment_md

    # No char cap — pass the full judgment. 12000 chars cut off mid-judgment
    # for most SC/HC full texts (long factual recitals, multi-round DRT/DRAT/HC
    # history), risking wrong overruled/distinguished_by/relationship answers
    # with no signal anything was cut. If a judgment ever exceeds the model's
    # context window, the OpenRouter call raises and the existing retry/skip
    # handling in the except blocks below catches it — no separate cap needed.
    reason_system = PROMPT_PATH.read_text(encoding="utf-8")
    reason_user = (
        f"Known metadata for this judgment (use for ik_doc_id / ik_url — verify "
        f"citation/title/court yourself from the text below, do not just copy 'ik_title'):\n"
        f"ik_doc_id: {meta.get('ik_doc_id', '')}\n"
        f"ik_url: {meta.get('ik_url', '')}\n\n"
        f"--- JUDGMENT TEXT ---\n{judgment_text}"
    )

    for attempt in range(max_retries + 1):
        try:
            # Stage 1 — reason, in the model's own words, against the full spec.
            reasoned_output = _call_openrouter(reason_system, reason_user)

            # Stage 2 — lock that answer into the strict schema, no new
            # reasoning. Runs on a non-thinking model (settings.openrouter_lock_model)
            # — measured the thinking model burning ~100s/file of hidden
            # reasoning tokens here for a task that's pure format conversion.
            from app.config import settings
            locked_raw = _call_openrouter(
                LOCK_SYSTEM_PROMPT, reasoned_output,
                response_format={"type": "json_schema", "json_schema": LOCK_SCHEMA},
                model=settings.openrouter_lock_model or None,
            )
            data = json.loads(locked_raw)
            data = _flatten_locked_data(data)

            if not data.get("confident", False):
                print(f"  SKIP (model uncertain): {slug}")
                return None
            word_count = len(data["holding_summary"].split())
            if word_count < 80:
                print(f"  SKIP (holding_summary too short, {word_count} words): {slug}")
                return None

            md_content = render_judgment_md(data)

            # Belt-and-suspenders: validate against the same parser
            # load_judgments.py uses, even though we rendered it ourselves.
            tmp_path = Path.cwd() / f"_slrai_validate_{slug}.md.tmp"
            tmp_path.write_text(md_content, encoding="utf-8")
            try:
                parse_judgment_md(tmp_path)
            finally:
                tmp_path.unlink(missing_ok=True)

            return md_content

        except OpenRouterAuthError:
            raise  # fatal — wrong/unset key
        except (JudgmentFileError, json.JSONDecodeError, KeyError) as e:
            print(f"  malformed output for {slug} (attempt {attempt + 1}): {e}")
            if attempt == max_retries:
                return None
            time.sleep(2)
        except Exception as e:
            print(f"  error for {slug} (attempt {attempt + 1}): {e}")
            if attempt == max_retries:
                return None
            time.sleep(2)
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", default="docs/judgments_raw")
    parser.add_argument("--out-dir", default="docs/judgments")
    parser.add_argument("--force", action="store_true", help="Regenerate even if the .md already exists")
    args = parser.parse_args()

    if not PROMPT_PATH.exists():
        print(f"{PROMPT_PATH} not found — cannot summarize without the spec.")
        return -1

    raw_dir = Path(args.raw_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # "_not_found.txt" (fetch_from_ik.py's SKIP log) matches *.txt and sorts
    # before real judgment slugs — without this filter it gets fed to the
    # model as if it were a judgment, and its list of case titles can't
    # satisfy the schema, burning the full retry budget on garbage input.
    raw_files = sorted(p for p in raw_dir.glob("*.txt") if not p.name.startswith("_"))
    if not raw_files:
        print(f"No raw judgments in {raw_dir}/ — run fetch_from_ik.py first.")
        return 0

    done = 0
    for raw_path in raw_files:
        slug = raw_path.stem
        out_path = out_dir / f"{slug}.md"
        if out_path.exists() and not args.force:
            print(f"SKIP (already summarized): {slug}")
            continue

        meta_path = raw_dir / f"{slug}.meta.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
        judgment_text = raw_path.read_text(encoding="utf-8")

        try:
            md_content = summarize_one(slug, judgment_text, meta)
        except OpenRouterAuthError:
            print("OPENROUTER_API_KEY invalid or not set — fix it in .env and re-run.")
            return -1

        if md_content is None:
            print(f"SKIP (could not produce valid summary): {slug}")
            continue

        out_path.write_text(md_content, encoding="utf-8")
        print(f"WROTE: {out_path}")
        done += 1

    print(f"{done}/{len(raw_files)} judgments summarized.")
    return done


if __name__ == "__main__":
    main()
