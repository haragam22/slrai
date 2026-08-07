"""Layer B — Claude API structured JSON extraction of case facts.

Never call Claude once per paragraph. process_paragraphs_for_extraction()
is the only entry point. temperature is always 0.0 (deterministic).
"""
import json
import logging
import time

from app.config import settings
from app.services import llm_client
from app.services.llm_client import client

logger = logging.getLogger(__name__)

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

Each object must have this exact structure. CRITICAL: "para_index" must match
the "index" field of the input paragraph this object extracts from. If a
paragraph contains what looks like a list or table with multiple distinct
items, still return exactly ONE object for it, with that paragraph's index —
do not split one input paragraph into multiple output objects.
{{
  "para_index": 0,
  "metadata": {{
    "drt_jurisdiction":      "DRT bench city/name if mentioned, else null",
    "sa_number":             "SA/application number if mentioned, else null",
    "primary_borrower":      "borrower name if mentioned, else null",
    "authorized_officer_name": "name of the bank's Authorized Officer who signed the notice/possession/sale documents, if mentioned, else null"
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
    "balance_payment_date":    "DD.MM.YYYY or null — date the auction purchaser deposited the balance 75% of the sale consideration to the bank (different from the auction date, when only 25% was deposited). Look for: 'balance amount deposited on', 'remaining 75% was paid on', 'balance sale consideration was deposited on'. Critical for Rule 9(4) — determines whether the balance was paid within the mandatory 90-day outer limit.",
    "demand_notice_date":      "DD.MM.YYYY or null — date the bank issued the Section 13(2) demand notice",
    "objection_date":          "DD.MM.YYYY or null — date the borrower filed their Section 13(3A) objection/reply to the demand notice",
    "bank_reply_date":         "DD.MM.YYYY or null — date the bank replied to the borrower's Section 13(3A) objection",
    "possession_notice_date":  "DD.MM.YYYY or null — date the Section 13(4) possession notice was issued",
    "npa_classification_date": "DD.MM.YYYY or null — date the loan account was classified Non-Performing Asset",
    "date_of_last_payment":    "DD.MM.YYYY or null — date of the borrower's last payment toward the loan before NPA classification",
    "valuation_date":          "DD.MM.YYYY or null — date the property valuation report was prepared",
    "sale_notice_date":        "DD.MM.YYYY or null — date the Rule 8(6) auction sale notice was issued to the borrower",
    "auction_date":            "DD.MM.YYYY or null — date the e-auction/public auction was actually conducted",
    "sale_certificate_date":   "DD.MM.YYYY or null — date the sale certificate was issued to the auction purchaser",
    "mortgage_date":           "DD.MM.YYYY or null — date the mortgage/security interest over the property was created",
    "lease_date":              "DD.MM.YYYY or null — date a claimed tenancy/lease began, if a third party is claiming tenancy rights",
    "ats_date":                "DD.MM.YYYY or null — date of an Agreement to Sell, if a third party is claiming rights under one",
    "measure_date":            "DD.MM.YYYY or null — date of the specific SARFAESI enforcement measure (notice/possession/auction) being challenged in this SA — drives the 45-day limitation clock",
    "sa_filing_date":          "DD.MM.YYYY or null — date the borrower filed this Securitisation Application at the DRT",
    "drt_stay_order_date":     "DD.MM.YYYY or null — date the DRT granted an interim stay order, if one was granted",
    "restructuring_approval_date": "DD.MM.YYYY or null — date a restructuring proposal was approved, if MSME/restructuring is at issue (M8)",
    "notice_service_date":     "DD.MM.YYYY or null — date the Section 13(2) demand notice was actually SERVED/RECEIVED by the borrower (different from demand_notice_date, the date it was issued — postal delay can put these days apart). Look for: 'notice was served on', 'received by the borrower on', postal/courier acknowledgment dates."
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
    "msme_status_claimed":              null,
    "msme_claimed_by_borrower":         null,
    "tenancy_claimed":                  null,
    "valuation_report_present":         null,
    "valuer_registered_under_rvact":    null,
    "notice_dispatch_proof_present":    null,
    "notice_content_complete":          null,
    "newspaper_publication_done":       null,
    "classification_notice_given":      null,
    "interest_application_correct":     null,
    "ao_has_written_authorization":     null,
    "restructuring_offered_pre_npa":    null,
    "sale_certificate_issued":          null,
    "possession_given_to_auction_purchaser": null,
    "previous_sa_filed":                null,
    "challenges_auction":               null,
    "auction_conducted_despite_stay":   null,
    "auction_notice_affixed_on_property": null,
    "auction_notice_discloses_pending_sa": null,
    "ats_simultaneous_mortgage":        null,
    "ats_payments_made_to_loan_account": null,
    "account_standard_at_auction_date": null,
    "bank_reply_gives_reasons":         null,
    "challenges_demand_notice":         null,
    "pending_sa_existed_at_auction_date": null,
    "restructuring_proposal_pending":   null,
    "udyam_cert_in_bank_file":          null,
    "ibc_moratorium_active":            null
  }},
  "sa_applicant_type": "THIRD_PARTY_ATS | AUCTION_PURCHASER | BORROWER | GUARANTOR | null — see THIRD PARTY AND POST-AUCTION GROUND DETECTION rules above",
  "notice_service_mode": "registered_post_ad | personal_service | substituted_service | email_if_agreed | null",
  "asset_type": "movable | immovable | null — type of the secured asset being enforced against",
  "secured_asset_type": "agricultural_land | other | null — SARFAESI does not apply to agricultural land (Section 31(i)); flag explicitly whenever the secured property's nature is stated",
  "measure_type": "the specific SARFAESI enforcement measure being challenged in this SA, e.g. 'Section 13(2) Demand Notice', 'Section 13(4) Possession', 'Auction Sale', 'IBC Section 7 Application', else null",
  "numeric_facts": {{
    "reserve_price":              "number or null — reserve price fixed for the auction under Rule 8(5)/9",
    "lease_duration_months":      "number or null — duration of a claimed tenancy in months",
    "borrowers_served_notice":    "number or null — count of borrowers actually served notice",
    "guarantors_served_notice":   "number or null — count of guarantors actually served notice",
    "total_borrowers_in_loan":    "number or null — total borrowers named on the loan",
    "total_guarantors_in_loan":   "number or null — total guarantors named on the loan",
    "demand_notice_amount":       "number or null — amount claimed/demanded in the Section 13(2) notice",
    "actual_outstanding_amount":  "number or null — the amount the borrower contends is actually outstanding, if disputed",
    "amount_repaid":              "number or null — total amount the borrower has repaid toward the loan, if stated"
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


_LIST_FIELDS = ("dates", "amounts", "dispatch_proof_methods", "ground_codes", "prayers", "ambiguous_elements")
_DICT_FIELDS = ("metadata", "date_facts", "boolean_facts", "numeric_facts")


def _merge_extraction_objects(objs: list[dict]) -> dict:
    """Merges multiple extraction objects the model incorrectly emitted for
    the same para_index (over-segmentation — see extract_facts_batch). List
    fields are concatenated+deduped, dict fields merged key-by-key (first
    non-null value wins), scalars take the first non-null/non-empty value,
    confidence takes the max, implied_facts_present is OR'd across the group."""
    merged: dict = {}

    for field in _LIST_FIELDS:
        combined = []
        seen = set()
        for obj in objs:
            for item in obj.get(field) or []:
                key = json.dumps(item, sort_keys=True, default=str)
                if key not in seen:
                    seen.add(key)
                    combined.append(item)
        merged[field] = combined

    for field in _DICT_FIELDS:
        combined_dict: dict = {}
        for obj in objs:
            for k, v in (obj.get(field) or {}).items():
                if v is not None and combined_dict.get(k) is None:
                    combined_dict[k] = v
        merged[field] = combined_dict

    merged["confidence"] = max((obj.get("confidence") or 0.0) for obj in objs)
    merged["implied_facts_present"] = any(obj.get("implied_facts_present") for obj in objs)

    for field in ("sa_prayer_text", "sa_applicant_type", "notice_service_mode", "asset_type",
                  "secured_asset_type", "measure_type"):
        merged[field] = next((obj.get(field) for obj in objs if obj.get(field)), None)

    return merged


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

    Correlates output objects to input paragraphs via "para_index", not
    strict list length — Gemini (unlike Claude, which this prompt was
    originally tuned against) sometimes splits one dense/tabular input
    paragraph into multiple output objects, which the old strict
    `len(result) != count` check rejected outright, discarding the entire
    batch (up to 7 paragraphs) on a single over-segmented one. Confirmed
    live via a real Gemini dry run on a document dense with scoring tables/
    numbered clauses — most batches were failing this way. Over-segmented
    paragraphs are now merged (see _merge_extraction_objects) instead of
    the whole batch being thrown away.
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
                model=llm_client.MODEL,
                max_tokens=64000,  # Claude Sonnet's max output — no artificial cap
                temperature=settings.llm_temperature,  # always 0.0
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = response.content[0].text.strip()
            raw = raw.replace("```json", "").replace("```", "").strip()
            try:
                result = json.loads(raw)
            except json.JSONDecodeError as parse_exc:
                # Gemini occasionally emits a complete, valid JSON array and
                # then keeps generating trailing content after it (seen live:
                # "Extra data" errors on responses hundreds of lines longer
                # than the array itself). temperature=0.0 means this repeats
                # identically on every retry — retrying alone never fixes it.
                # json.loads rejects the whole response for garbage AFTER a
                # valid value; raw_decode parses just the first complete
                # value and tells us where it ended, so real trailing noise
                # doesn't have to cost the batch. Only recovers from "Extra
                # data" (trailing garbage) — a genuinely truncated/malformed
                # array still raises and falls through to the normal retry path.
                if "Extra data" not in str(parse_exc):
                    raise
                result, _ = json.JSONDecoder().raw_decode(raw)
                logger.warning(
                    "nlp_layer: response had %d chars of trailing data after a valid JSON array — recovered, ignored the excess",
                    len(raw) - parse_exc.pos,
                )

            if not isinstance(result, list):
                raise ValueError(f"Expected a JSON array, got {type(result).__name__}")

            # Fast path — model followed instructions exactly (Claude
            # reliably does; this is also what most Gemini batches do).
            if len(result) == count and all(
                isinstance(obj, dict) and obj.get("para_index") == i for i, obj in enumerate(result)
            ):
                return result

            by_index: dict[int, list[dict]] = {}
            unindexed: list[dict] = []
            for obj in result:
                if not isinstance(obj, dict):
                    continue
                idx = obj.get("para_index")
                if isinstance(idx, int) and 0 <= idx < count:
                    by_index.setdefault(idx, []).append(obj)
                else:
                    unindexed.append(obj)

            # Model didn't include usable para_index anywhere but the count
            # matches — old strict-positional behavior as a fallback.
            if not by_index and len(unindexed) == count:
                return unindexed

            if not by_index:
                raise ValueError(
                    f"Could not correlate any of {len(result)} objects to "
                    f"{count} paragraphs by para_index"
                )

            merged: list[dict | None] = []
            for i in range(count):
                group = by_index.get(i)
                if not group:
                    merged.append(None)
                elif len(group) == 1:
                    merged.append(group[0])
                else:
                    logger.warning(
                        "nlp_layer: paragraph index %d returned as %d separate objects — merging",
                        i, len(group),
                    )
                    merged.append(_merge_extraction_objects(group))
            return merged

        except (json.JSONDecodeError, ValueError) as exc:
            logger.warning("nlp_layer: bad extraction response (attempt %d/%d): %s", attempt + 1, max_retries + 1, exc)
            if attempt == max_retries:
                return [None] * count
            time.sleep(1)

        except llm_client.APITimeoutError as exc:
            logger.warning("nlp_layer: Claude API timeout (attempt %d/%d): %s", attempt + 1, max_retries + 1, exc)
            if attempt == max_retries:
                return [None] * count
            time.sleep(5)

        except llm_client.RateLimitError:
            raise  # re-raise to Celery for exponential backoff retry

        except llm_client.AuthenticationError:
            raise  # fatal — wrong key, Celery sets case FAILED

        except Exception:
            logger.exception("nlp_layer: unexpected error extracting batch of %d paragraphs", count)
            return [None] * count


MAX_CONCURRENT_BATCHES = 5  # ponytail: fixed pool size, tune via settings if rate-limit errors show up


def process_paragraphs_for_extraction(
    all_paragraphs: list[dict],
    batch_size: int = BATCH_SIZE,
    on_batch_complete=None,
) -> list[dict | None]:
    """
    Entry point for NLP extraction in Chain A.
    Groups paragraphs by doc_type, handles oversized paragraphs solo,
    batches the rest. Every batch/solo call is an independent Claude request
    (system prompt is cached, so cost is per-call not per-token) — fired
    concurrently via a thread pool instead of one at a time. This was the
    pipeline's single biggest time cost (~40min/case, serial): N batches *
    per-call latency, when the calls have no dependency on each other.
    Returns results in same order as input.

    on_batch_complete(orig_indices, batch_result), if given, is called from
    the main thread (via as_completed, never from a worker thread) right as
    each batch finishes — lets the caller persist+commit results and advance
    progress incrementally instead of waiting for the whole call to return.
    This is what makes a mid-run RateLimitError retry resumable: work a
    prior attempt already persisted via this callback doesn't get redone.
    """
    results: list[dict | None] = [None] * len(all_paragraphs)

    from concurrent.futures import ThreadPoolExecutor, as_completed
    from itertools import groupby

    indexed = list(enumerate(all_paragraphs))
    indexed_sorted = sorted(indexed, key=lambda x: x[1].get("doc_type", ""))

    # Build the full job list across all doc_type groups first, then run
    # every job concurrently — no reason to finish one doc_type before
    # starting the next.
    jobs: list[tuple[list[int], list[dict]]] = []  # (orig_indices, paragraphs)
    for _, group_iter in groupby(indexed_sorted, key=lambda x: x[1].get("doc_type", "")):
        group = list(group_iter)
        solos = [(i, p) for i, p in group if len(p["text_for_extraction"]) > OVERSIZED_CHARS]
        batched = [(i, p) for i, p in group if len(p["text_for_extraction"]) <= OVERSIZED_CHARS]

        for orig_idx, para in solos:
            jobs.append(([orig_idx], [para]))

        for start in range(0, len(batched), batch_size):
            slice_ = batched[start:start + batch_size]
            jobs.append(([i for i, _ in slice_], [p for _, p in slice_]))

    if not jobs:
        return results

    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_BATCHES) as pool:
        futures = {
            pool.submit(extract_facts_batch, paras, max_retries=2): orig_indices
            for orig_indices, paras in jobs
        }
        for future in as_completed(futures):
            orig_indices = futures[future]
            batch_result = future.result()
            for orig_idx, extraction in zip(orig_indices, batch_result or [None] * len(orig_indices)):
                results[orig_idx] = extraction
            if on_batch_complete is not None:
                on_batch_complete(orig_indices, batch_result)

    return results
