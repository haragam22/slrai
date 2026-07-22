"""Layer B — Claude API structured JSON extraction of case facts.

Never call Claude once per paragraph. process_paragraphs_for_extraction()
is the only entry point. temperature is always 0.0 (deterministic).
"""
import json
import logging
import time

import anthropic

from app.config import settings

logger = logging.getLogger(__name__)

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

BATCH_SIZE = 7  # paragraphs per Claude call — never exceed 8
OVERSIZED_CHARS = 2400  # sent solo to avoid max_tokens overflow

_wiki_cache: str | None = None


def _load_statutory_wiki() -> str:
    global _wiki_cache
    if _wiki_cache is None:
        try:
            with open(settings.sarfaesi_law_wiki_path, "r", encoding="utf-8") as f:
                _wiki_cache = f.read()
        except FileNotFoundError:
            _wiki_cache = ""
    return _wiki_cache


def get_batch_system_prompt() -> list[dict]:
    """Pre-load and return the system prompt for Claude extraction calls, as
    content blocks with a cache_control breakpoint on the wiki.

    The statutory wiki is injected directly into context (never retrieved) —
    see CLAUDE_v51.md Hybrid Wiki + Qdrant Architecture. It's identical on
    every call within a process (and across calls until the wiki file is
    rebuilt), so Anthropic prompt caching turns the previous "resend 77k
    tokens per batch" cost into one full-price write + cheap cache reads —
    see plan at .claude/plans/starry-orbiting-kite.md finding #1.
    """
    wiki = _load_statutory_wiki()
    blocks = [{"type": "text", "text": BATCH_SYSTEM_PROMPT}]
    if wiki:
        blocks.append({
            "type": "text",
            "text": f"\n\nSTATUTORY REFERENCE (SARFAESI Act, Rules, RDDBFI, RBI IRAC):\n{wiki}",
            "cache_control": {"type": "ephemeral"},
        })
    return blocks


BATCH_SYSTEM_PROMPT = """You are a legal document parser for Indian SARFAESI Act proceedings.
You will receive multiple paragraphs from the same legal document.
Extract structured facts from each paragraph.
Return ONLY a valid JSON array — one extraction object per paragraph, same order.
No preamble. No markdown. No explanation. First character must be [
Do not infer beyond what is stated. For implied facts set implied: true.
Missing facts: null. Never fabricate a value.

CRITICAL DISTINCTION: ACT vs RULES
When classifying ground_codes, you must identify if the borrower is challenging the ACT (the bank's fundamental right or interpretation of law) or the RULES (specific procedural or timing defects).
- ACT challenges route to the judgment corpus (Class A/B precedent matching).
- RULES challenges route to the deterministic YAML Rule Engine.
Assign statutory_basis correctly.

THIRD PARTY AND POST-AUCTION GROUND DETECTION (v5.4):

When extracting ground_codes, also check for:

1. THIRD_PARTY_ATS — present when applicant:
   - States they are "neither borrower nor guarantor"
   - Mentions an "Agreement to Sell" or "Agreement for Sale" or "ATS"
   - Claims they are in physical possession under a private sale agreement
   - Has paid substantial consideration directly to the borrower
   -> Set sa_applicant_type: "THIRD_PARTY_ATS"

2. AUCTION_DURING_STAY — present when applicant:
   - Mentions a DRT order / High Court order restraining possession or auction
   - States the bank conducted the auction DESPITE a pending court order
   - References any interim stay, injunction, or "court receiver" restraint
   -> Set auction_conducted_despite_stay: true

3. AUCTION_NOTICE_AFFIXING — present when applicant:
   - States the auction notice was never put up / affixed / pasted on the property
   - Mentions they were in possession and no notice was given at the property
   - Cites Rule 8(6)(7) or Mathew Varghese or Vasu Shetty
   -> Set auction_notice_affixed_on_property: false

4. RIGHT_OF_REDEMPTION — present when applicant:
   - Argues they have paid all outstanding dues
   - Claims the account is no longer NPA
   - Cites RBI IRAC clause 4.2.5 (NPA upgradation)
   - States they tendered payment before auction / after auction but before possession
   -> Extract payments_post_npa_total from stated payment amounts

5. SECOND_SA_FRESH_CAUSE — present when:
   - Applicant mentions they previously filed an SA
   - Present SA challenges a different SARFAESI measure (e.g. previous challenged
     demand notice, present challenges the auction)
   - Applicant cites "Oasis Dealcom" or "fresh cause of action"
   -> Set previous_sa_filed: true, challenges_auction: true

PRAYER DETECTION RULES:
- Look for paragraph headings: "PRAYER", "PRAYER CLAUSE", "RELIEF SOUGHT",
  "IT IS THEREFORE PRAYED", "PRAYERS", "IT IS RESPECTFULLY PRAYED"
- After finding the prayer paragraph, extract EACH sub-prayer as a separate item
- Mark prayers with "(ad-interim)" or "(interim)" or "(ex-parte)" as is_interim: true
- Mark prayers asking to "set aside" the auction/certificate as
  prayer_type: "SET_ASIDE_AUCTION" or "SET_ASIDE_SALE_CERTIFICATE"
- Mark prayers asking to "restrain" the bank as prayer_type: "RESTRAIN_*"
- The prayer clause is the most important paragraph in any SA — extract it completely"""

BATCH_USER_TEMPLATE = """Document type: {doc_type}

Extract from these {count} paragraphs. Return array of exactly {count} objects.

{paragraphs_json}

Each object must have this exact structure:
{{
  "metadata": {{
    "drt_jurisdiction": "DRT bench city/name if mentioned, else null",
    "sa_number":        "SA/application number if mentioned, else null",
    "primary_borrower": "borrower name if mentioned, else null"
  }},
  "dates": [
    {{"date": "DD.MM.YYYY", "context": "what event this date refers to", "implied": false}}
  ],
  "amounts": [
    {{"amount": 0.00, "currency": "INR", "context": "what this amount refers to"}}
  ],
  "dispatch_proof_methods": [],
  "ground_codes": [
    {{"code": "CODE_NAME", "statutory_basis": "ACT | RULES | BOTH | RBI | OTHER"}}
  ],
  "prayers": [
    {{
      "prayer_type": "SET_ASIDE_DEMAND_NOTICE|SET_ASIDE_POSSESSION_NOTICE|SET_ASIDE_SALE_NOTICE|SET_ASIDE_AUCTION|SET_ASIDE_SALE_CERTIFICATE|RESTRAIN_POSSESSION|RESTRAIN_SALE_DEED_EXECUTION|RESTRAIN_AUCTION|GRANT_TIME_TO_PAY|CONSIDER_OTS|ADJUDICATE_AMOUNT|STAY_ALL_PROCEEDINGS|OTHER",
      "is_interim": true,
      "measure_date": "DD.MM.YYYY or null",
      "prayer_text_verbatim": "exact prayer language from this paragraph",
      "granted": null
    }}
  ],
  "sa_prayer_text": "full verbatim prayer clause if this paragraph contains it",
  "date_facts": {{
    "balance_payment_date": "DD.MM.YYYY or null — date the auction purchaser deposited the balance 75% of the sale consideration to the bank (different from the auction date, when only 25% was deposited). Look for: 'balance amount deposited on', 'remaining 75% was paid on', 'balance sale consideration was deposited on'. Critical for Rule 9(4) — determines whether the balance was paid within the mandatory 90-day outer limit."
  }},
  "boolean_facts": {{
    "notice_served":                    null,
    "objection_filed":                  null,
    "bank_reply_given":                 null,
    "lease_claimed":                    null,
    "lease_registered":                 null,
    "valuation_disputed":               null,
    "valuation_challenged_by_borrower": null,
    "valuer_section_247_registered":    null,
    "valuer_rbi_empanelled":            null,
    "all_parties_served":               null,
    "npa_premature_alleged":            null,
    "msme_status_claimed":              null
  }},
  "confidence":              0.0,
  "implied_facts_present":   false,
  "ambiguous_elements":      []
}}

Valid dispatch_proof_methods: "registered_post_ad", "personal_service",
"substituted_service", "courier", "email", "affidavit_of_service", "unknown"

Valid ground_codes: SERVICE_DEFECT, AMOUNT_DISPUTE, REPLY_NOT_GIVEN,
AUCTION_GAP_DEFECT, NEWSPAPER_PUB_DEFECT, LIMITATION_EXPIRED, TENANCY_CLAIM,
VALUATION_DISPUTE, NOTICE_ALL_PARTIES, NPA_PREMATURE, NPA_DURING_RESTRUC,
MSME_RESTRUC_SKIPPED, POSSESSION_DEFECT, NOTICE_FORMAT_DEFECT, AO_AUTHORIZATION,
AUCTION_NOTICE_AFFIXING, AUCTION_DURING_STAY, PENDING_SA_CONCEALED,
THIRD_PARTY_ATS, AUCTION_PURCHASER, RIGHT_OF_REDEMPTION, SECOND_SA_FRESH_CAUSE,
UNKNOWN"""


def extract_facts_batch(
    paragraphs: list[dict],  # each: {para_id, text_for_extraction, doc_type}
    max_retries: int = 2,
) -> list[dict | None]:
    """
    Single Claude API call extracting facts from up to BATCH_SIZE paragraphs.
    Returns list of extraction dicts, same order as input.
    Returns None for a paragraph slot if extraction failed.
    Never raises for JSON/timeout failures — those return None entries.
    RateLimitError and AuthenticationError propagate to Celery (see error contracts).
    """
    if not paragraphs:
        return []

    doc_type = paragraphs[0].get("doc_type", "UNKNOWN")
    count = len(paragraphs)

    paragraphs_prompt = json.dumps([
        {"index": i, "text": p["text_for_extraction"]}
        for i, p in enumerate(paragraphs)
    ], ensure_ascii=False, indent=2)

    prompt = BATCH_USER_TEMPLATE.format(
        doc_type=doc_type,
        count=count,
        paragraphs_json=paragraphs_prompt,
    )

    system_prompt = get_batch_system_prompt()

    for attempt in range(max_retries + 1):
        try:
            response = client.messages.create(
                model=settings.claude_model,
                max_tokens=4000,
                temperature=settings.llm_temperature,  # always 0.0
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = response.content[0].text.strip()
            raw = raw.replace("```json", "").replace("```", "").strip()
            result = json.loads(raw)

            if not isinstance(result, list) or len(result) != count:
                raise ValueError(
                    f"Expected list of {count}, got {type(result).__name__} "
                    f"len={len(result) if isinstance(result, list) else 'N/A'}"
                )
            return result

        except (json.JSONDecodeError, ValueError) as exc:
            logger.warning("nlp_layer: bad extraction response (attempt %d/%d): %s", attempt + 1, max_retries + 1, exc)
            if attempt == max_retries:
                return [None] * count
            time.sleep(1)

        except anthropic.APITimeoutError as exc:
            logger.warning("nlp_layer: Claude API timeout (attempt %d/%d): %s", attempt + 1, max_retries + 1, exc)
            if attempt == max_retries:
                return [None] * count
            time.sleep(5)

        except anthropic.RateLimitError:
            raise  # re-raise to Celery for exponential backoff retry

        except anthropic.AuthenticationError:
            raise  # fatal — wrong key, Celery sets case FAILED

        except Exception:
            logger.exception("nlp_layer: unexpected error extracting batch of %d paragraphs", count)
            return [None] * count


def process_paragraphs_for_extraction(
    all_paragraphs: list[dict],
    batch_size: int = BATCH_SIZE,
) -> list[dict | None]:
    """
    Entry point for NLP extraction in Chain A.
    Groups paragraphs by doc_type, handles oversized paragraphs solo,
    batches the rest. Returns results in same order as input.
    """
    results: list[dict | None] = [None] * len(all_paragraphs)

    from itertools import groupby

    indexed = list(enumerate(all_paragraphs))
    indexed_sorted = sorted(indexed, key=lambda x: x[1].get("doc_type", ""))

    for _, group_iter in groupby(indexed_sorted, key=lambda x: x[1].get("doc_type", "")):
        group = list(group_iter)
        solos = [(i, p) for i, p in group if len(p["text_for_extraction"]) > OVERSIZED_CHARS]
        batched = [(i, p) for i, p in group if len(p["text_for_extraction"]) <= OVERSIZED_CHARS]

        for orig_idx, para in solos:
            r = extract_facts_batch([para], max_retries=2)
            results[orig_idx] = r[0] if r else None

        for start in range(0, len(batched), batch_size):
            slice_ = batched[start:start + batch_size]
            orig_indices = [i for i, _ in slice_]
            paras = [p for _, p in slice_]
            batch_result = extract_facts_batch(paras, max_retries=2)
            for orig_idx, extraction in zip(orig_indices, batch_result):
                results[orig_idx] = extraction

    return results
