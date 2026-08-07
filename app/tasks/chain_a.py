"""Chain A — document upload → PENDING_HUMAN_REVIEW (fires automatically on upload)."""
import logging

import anthropic
from celery import chain

from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="tasks.chain_a.run", max_retries=2)
def run_chain_a(self, case_id: str, doc_id: str):
    """Fires automatically after first document upload. Ends at PENDING_HUMAN_REVIEW."""
    pipeline = chain(
        task_update_pipeline_stage.si(case_id, "OCR"),
        task_ocr_document.si(case_id, doc_id),
        task_update_pipeline_stage.si(case_id, "LANGUAGE_DETECTION"),
        task_detect_language.si(case_id),
        task_update_pipeline_stage.si(case_id, "TRANSLATION"),
        task_translate_hindi_paragraphs.si(case_id),
        task_update_pipeline_stage.si(case_id, "REGEX_EXTRACTION"),
        task_regex_extract_all.si(case_id),
        task_update_pipeline_stage.si(case_id, "NLP_EXTRACTION"),
        task_nlp_extract_facts.si(case_id),
        task_check_pre_intake_filters.si(case_id),
        task_update_pipeline_stage.si(case_id, "POPULATING_WORKBENCH"),
        task_populate_workbench.si(case_id),
        task_set_case_status.si(case_id, "PENDING_HUMAN_REVIEW"),
    )
    pipeline.delay()


@celery_app.task(name="tasks.chain_a.set_status")
def task_set_case_status(case_id: str, status: str) -> None:
    """Updates cases.status in DB. Uses .si() in chains — no passthrough arg.
    Never overwrites a terminal INTAKE_REJECTED status set by
    task_check_pre_intake_filters — a case that failed F1/F3/F4 (agricultural
    land bar / substantial repayment / IBC moratorium) must stay rejected,
    not get silently moved back to PENDING_HUMAN_REVIEW by the rest of the
    fixed Celery chain running after it."""
    logger.info("running task_set_case_status case=%s status=%s", case_id, status)
    from app.models.db import SyncSessionLocal, Case
    with SyncSessionLocal() as db:
        case = db.query(Case).filter_by(id=case_id).first()
        if case:
            if case.status == "INTAKE_REJECTED" and status != "INTAKE_REJECTED":
                logger.info("case=%s already INTAKE_REJECTED — skipping status=%s", case_id, status)
                return
            case.status = status
            case.pipeline_stage = None
            db.commit()


@celery_app.task(name="tasks.chain_a.update_stage")
def task_update_pipeline_stage(case_id: str, stage: str) -> None:
    """Updates pipeline_stage on the case row. Uses .si() in chains.
    Resets step_current/step_total — each stage reports its own progress
    from zero; a stale count from the previous stage would otherwise leak
    into get_pipeline_status's interpolation for the new one."""
    logger.info("running task_update_pipeline_stage case=%s stage=%s", case_id, stage)
    from app.models.db import SyncSessionLocal, Case
    with SyncSessionLocal() as db:
        case = db.query(Case).filter_by(id=case_id).first()
        if case:
            case.pipeline_stage = stage
            case.pipeline_step_current = 0
            case.pipeline_step_total = 0
            db.commit()


def _set_step_progress(db, case_id: str, current: int, total: int) -> None:
    """Shared helper — every Chain A task that loops over paragraphs/docs/
    batches calls this so pipeline-status reports real progress instead of
    the stage's flat band endpoint. See STAGE_PROGRESS_BANDS in cases.py."""
    from app.models.db import Case
    case = db.query(Case).filter_by(id=case_id).first()
    if case:
        case.pipeline_step_current = current
        case.pipeline_step_total = total
        db.commit()


@celery_app.task(name="tasks.chain_a.ocr_document")
def task_ocr_document(case_id: str, doc_id: str) -> None:
    """OCR a document via Google Document AI, parse paragraphs, save to DB."""
    logger.info("running task_ocr_document case=%s doc=%s", case_id, doc_id)
    from app.models.db import Document, SyncSessionLocal
    from app.services.extraction.doc_classifier import classify_document
    from app.services.ocr.docai_ocr import extract_layout
    from app.services.ocr.layout_parser import parse_ocr_result, save_paragraphs_to_db
    from app.services.storage import download_document

    from app.models.db import Case

    with SyncSessionLocal() as db:
        document = db.query(Document).filter_by(id=doc_id).first()
        if not document:
            return
        try:
            file_bytes = download_document(document.file_url)
            ocr_result = extract_layout(file_bytes)
            paragraphs = parse_ocr_result(ocr_result)
            save_paragraphs_to_db(doc_id, paragraphs)

            first_500 = "".join(p["text_original"] for p in paragraphs)[:500]
            document.doc_type = classify_document(first_500) if first_500 else document.doc_type
            document.page_count = ocr_result["page_count"]
            document.ocr_status = "COMPLETE"
            db.commit()
        except Exception:
            # Contract §18.1 — OCR failure is a quota/key/document issue, not a
            # pipeline crash: FAILED status + workbench flag, no retry, no raise.
            # Downstream Chain A tasks no-op on a document with zero paragraphs,
            # so the pipeline still reaches PENDING_HUMAN_REVIEW for manual entry.
            logger.exception("OCR failed case=%s doc=%s", case_id, doc_id)
            document.ocr_status = "FAILED"
            case = db.query(Case).filter_by(id=case_id).first()
            if case:
                case.pipeline_stage = "OCR_FAILED"
            from app.services.extraction.fact_persistence import upsert_case_fact
            upsert_case_fact(db, case_id, f"ocr_failed_{doc_id}", {
                "field_value": f"OCR failed for document {doc_id}. Manual text entry required.",
                "confidence": 0.0,
                "extraction_method": "nlp_implied",
                "source_document_id": doc_id,
            })
            db.commit()


@celery_app.task(name="tasks.chain_a.detect_language")
def task_detect_language(case_id: str) -> None:
    """Detect/refresh language of extracted paragraphs for all case documents."""
    logger.info("running task_detect_language case=%s", case_id)
    from app.models.db import Document, Paragraph, SyncSessionLocal
    from app.services.ocr.layout_parser import detect_paragraph_language

    with SyncSessionLocal() as db:
        paragraphs = (
            db.query(Paragraph)
            .join(Document, Paragraph.document_id == Document.id)
            .filter(Document.case_id == case_id)
            .all()
        )
        for i, para in enumerate(paragraphs, start=1):
            para.language = detect_paragraph_language(para.text_original)
            if i % 25 == 0 or i == len(paragraphs):
                _set_step_progress(db, case_id, i, len(paragraphs))
        db.commit()


@celery_app.task(name="tasks.chain_a.translate_hindi_paragraphs")
def task_translate_hindi_paragraphs(case_id: str) -> None:
    """Batched IndicTrans2 translation of Hindi/mixed paragraphs for this case."""
    logger.info("running task_translate_hindi_paragraphs case=%s", case_id)
    from app.models.db import Document, Paragraph, SyncSessionLocal
    from app.services.translation.indictrans import translate_paragraphs

    with SyncSessionLocal() as db:
        paragraphs = (
            db.query(Paragraph)
            .join(Document, Paragraph.document_id == Document.id)
            .filter(Document.case_id == case_id)
            .all()
        )
        if not paragraphs:
            return

        payload = [
            {"para_id": p.id, "text_original": p.text_original}
            for p in paragraphs
        ]
        translated = translate_paragraphs(payload)

        by_id = {p.id: p for p in paragraphs}
        for item in translated:
            if item.get("text_translated"):
                by_id[item["para_id"]].text_translated = item["text_translated"]

        db.commit()


@celery_app.task(name="tasks.chain_a.regex_extract_all")
def task_regex_extract_all(case_id: str) -> None:
    """Layer A deterministic regex extraction — dates, amounts, section/rule refs.
    Runs first, always. All hits confidence=1.0, never go to workbench.
    """
    logger.info("running task_regex_extract_all case=%s", case_id)
    from app.models.db import Document, Paragraph, SyncSessionLocal
    from app.services.extraction.fact_persistence import upsert_case_fact
    from app.services.extraction.regex_layer import extract_all

    with SyncSessionLocal() as db:
        paragraphs = (
            db.query(Paragraph)
            .join(Document, Paragraph.document_id == Document.id)
            .filter(Document.case_id == case_id)
            .all()
        )
        for para_idx, para in enumerate(paragraphs, start=1):
            text = para.get_text()
            hits = extract_all(text)
            for i, d in enumerate(hits["dates"]):
                upsert_case_fact(db, case_id, f"regex_date_{para.id}_{i}", {
                    "field_value": d["date"],
                    "confidence": 1.0,
                    "extraction_method": "regex",
                    "source_document_id": para.document_id,
                    "source_page": para.page_number,
                    "source_paragraph_id": para.id,
                })
            for i, a in enumerate(hits["amounts"]):
                upsert_case_fact(db, case_id, f"regex_amount_{para.id}_{i}", {
                    "field_value": a["amount"],
                    "confidence": 1.0,
                    "extraction_method": "regex",
                    "source_document_id": para.document_id,
                    "source_page": para.page_number,
                    "source_paragraph_id": para.id,
                })
            for i, s in enumerate(hits["section_refs"]):
                upsert_case_fact(db, case_id, f"regex_{s['ref_type']}_{para.id}_{i}", {
                    "field_value": s["section_number"],
                    "confidence": 1.0,
                    "extraction_method": "regex",
                    "source_document_id": para.document_id,
                    "source_page": para.page_number,
                    "source_paragraph_id": para.id,
                })
            if para_idx % 25 == 0 or para_idx == len(paragraphs):
                _set_step_progress(db, case_id, para_idx, len(paragraphs))
        db.commit()



@celery_app.task(
    bind=True,
    name="tasks.chain_a.nlp_extract_facts",
    autoretry_for=(anthropic.RateLimitError,),
    retry_kwargs={"max_retries": 3},
    retry_backoff=False,
    default_retry_delay=60,  # Contract §18.2 — max_retries=3, countdown=60
)
def task_nlp_extract_facts(self, case_id: str) -> None:
    """Layer B Claude API structured fact extraction (batched, temperature=0.0).
    Persists SAGround rows and CaseFact rows (via confidence-routed upsert).

    Contract §18.2: RateLimitError retries via Celery (autoretry_for above).
    AuthenticationError is fatal — case FAILED, no retry (caught below, not
    added to autoretry_for). Malformed-JSON/timeout failures are already
    handled inside nlp_layer.extract_facts_batch (returns None, no raise).

    Resumable retry: each paragraph's result is persisted+committed as soon
    as its batch completes (via on_batch_complete below), and marked done
    with a `nlp_done_{para.id}` CaseFact. A prior attempt that got cut off
    mid-run by a RateLimitError (Celery's autoretry_for) already saved
    everything up to that point — this attempt only (re)processes whatever's
    still pending, instead of re-running every batch for the whole document
    from scratch on every retry (was silently multiplying the Gemini call
    count by up to 4x — max_retries=3 — on any doc large enough to hit the
    rate limit before finishing one pass).
    """
    logger.info("running task_nlp_extract_facts case=%s", case_id)
    from app.models.db import Case, CaseFact, Document, Paragraph, SAGround, SyncSessionLocal
    from app.services.extraction.confidence_router import route_fact
    from app.services.extraction.fact_persistence import aggregate_metadata, upsert_case_fact
    from app.services.extraction.nlp_layer import process_paragraphs_for_extraction

    with SyncSessionLocal() as db:
        rows = (
            db.query(Paragraph, Document.doc_type)
            .join(Document, Paragraph.document_id == Document.id)
            .filter(Document.case_id == case_id)
            .all()
        )
        if not rows:
            return

        done_ids = {
            para_id for (para_id,) in db.query(CaseFact.source_paragraph_id)
            .filter(CaseFact.case_id == case_id, CaseFact.field_name.like("nlp_done_%"))
            .all()
        }
        pending_rows = [(para, doc_type) for para, doc_type in rows if para.id not in done_ids]

        case = db.query(Case).filter_by(id=case_id).first()
        if case:
            _set_step_progress(db, case_id, len(rows) - len(pending_rows), len(rows))

        if not pending_rows:
            return  # a prior attempt already finished every paragraph

        by_para_id = {para.id: para for para, _ in pending_rows}
        paragraphs_payload = [
            {"para_id": para.id, "text_for_extraction": para.get_text(), "doc_type": doc_type}
            for para, doc_type in pending_rows
        ]

        def _persist_one(para, result) -> None:
            if not result:
                upsert_case_fact(db, case_id, f"nlp_extraction_failed_{para.id}", {
                    "field_value": f"NLP extraction failed for paragraph {para.id}. Manual review required.",
                    "confidence": 0.0,
                    "extraction_method": "nlp_implied",
                    "source_document_id": para.document_id,
                    "source_page": para.page_number,
                    "source_paragraph_id": para.id,
                })
                # marked done below — a persistently-failing paragraph must
                # not be retried forever on every RateLimitError retry.
            else:
                # Gemini/Claude sometimes emit an explicit `null` for a group
                # key instead of omitting it — `.get(key, {})` only applies
                # the default when the key is missing, not when its value IS
                # None, so an unguarded `.items()` below crashes the whole
                # task (AttributeError, not a RateLimitError — no autoretry,
                # permanent failure). `or {}`/`or []` catch both cases.
                for ground in result.get("ground_codes") or []:
                    code = ground.get("code")
                    if not code or code == "UNKNOWN":
                        continue
                    exists = (
                        db.query(SAGround)
                        .filter_by(case_id=case_id, ground_code=code, source_paragraph_id=para.id)
                        .first()
                    )
                    if not exists:
                        db.add(SAGround(
                            case_id=case_id,
                            ground_code=code,
                            statutory_basis=ground.get("statutory_basis"),
                            source_paragraph_id=para.id,
                            confidence=result.get("confidence", 0.0),
                        ))

                confidence = result.get("confidence", 0.0)
                implied = result.get("implied_facts_present", False)

                # boolean_facts/date_facts/numeric_facts — same generic
                # confidence-routed persistence for every named key each
                # group can contain (see nlp_layer.py's BATCH_USER_TEMPLATE
                # for the full field list per group).
                for group_key in ("boolean_facts", "date_facts", "numeric_facts"):
                    for field_name, value in (result.get(group_key) or {}).items():
                        if value is None:
                            continue
                        routed = route_fact(field_name, {
                            "field_value": str(value),
                            "confidence": confidence,
                            "implied": implied,
                            "extraction_method": "nlp_explicit",
                        })
                        upsert_case_fact(db, case_id, field_name, {
                            "field_value": routed["field_value"],
                            "confidence": routed["confidence"],
                            "extraction_method": routed["extraction_method"],
                            "source_document_id": para.document_id,
                            "source_page": para.page_number,
                            "source_paragraph_id": para.id,
                        })

                # Flat single-value fields (not nested under boolean_facts/
                # date_facts because they're enums, not booleans) — sa_applicant_type
                # drives THIRD_PARTY_ATS/AUCTION_PURCHASER routing (M10),
                # notice_service_mode drives M1_C3.
                for field_name in ("sa_applicant_type", "notice_service_mode", "asset_type", "measure_type", "secured_asset_type"):
                    value = result.get(field_name)
                    if value is None:
                        continue
                    routed = route_fact(field_name, {
                        "field_value": str(value),
                        "confidence": confidence,
                        "implied": implied,
                        "extraction_method": "nlp_explicit",
                    })
                    upsert_case_fact(db, case_id, field_name, {
                        "field_value": routed["field_value"],
                        "confidence": routed["confidence"],
                        "extraction_method": routed["extraction_method"],
                        "source_document_id": para.document_id,
                        "source_page": para.page_number,
                        "source_paragraph_id": para.id,
                    })

                aggregate_metadata(case_id, [result], db)

            upsert_case_fact(db, case_id, f"nlp_done_{para.id}", {
                "field_value": "1",
                "confidence": 1.0,
                "extraction_method": "nlp_implied",
                "source_document_id": para.document_id,
                "source_page": para.page_number,
                "source_paragraph_id": para.id,
            })

        already_done = len(rows) - len(pending_rows)

        def on_batch_complete(orig_indices, batch_result) -> None:
            for orig_idx, extraction in zip(orig_indices, batch_result or [None] * len(orig_indices)):
                para_id = paragraphs_payload[orig_idx]["para_id"]
                _persist_one(by_para_id[para_id], extraction)
            db.commit()
            nonlocal already_done
            already_done += len(orig_indices)
            _set_step_progress(db, case_id, already_done, len(rows))

        try:
            process_paragraphs_for_extraction(paragraphs_payload, on_batch_complete=on_batch_complete)
        except anthropic.AuthenticationError:
            logger.error("ANTHROPIC_AUTH_FAILED case=%s", case_id)
            if case:
                case.status = "FAILED"
                case.pipeline_stage = None
                db.commit()
            return  # fatal, no retry


@celery_app.task(name="tasks.chain_a.check_pre_intake_filters")
def task_check_pre_intake_filters(case_id: str) -> None:
    """F1/F3/F4 (terminating) + F5/F6 (routing) — see pre_intake.py.

    These were fully coded (correct logic, correct messaging) but never
    called anywhere in the pipeline — the module docstring claimed "F1, F3,
    F4 run during Chain A after document extraction" but no task_* function
    anywhere actually invoked them. Confirmed via full-codebase grep before
    concluding this, not assumed. Practical effect: a case with an active
    IBC moratorium (Section 14 stay) or secured against agricultural land
    (statutory SARFAESI exclusion, Section 31(i)) could reach a PROCEED
    recommendation with nothing in the pipeline ever having checked either
    condition. F5/F6 (non-terminating routing flags) were separately found
    reimplemented ad-hoc in chain_b.py (M10 trigger) and report.html.j2
    (third-party notice text) — those still work despite this function
    never firing, only F1/F3/F4 had zero equivalent anywhere.

    Runs on RAW extracted facts (any confidence, not human_confirmed-gated)
    — these are pre-workbench filters by design (see pre_intake.py's F2
    precedent at case-creation time, same pattern), not YAML compliance
    checks. F1/F3/F4 only fire when their specific fact is actually present
    and matches — they're naturally no-ops on cases where the fact doesn't
    apply, not something imposed on every case.
    """
    logger.info("running task_check_pre_intake_filters case=%s", case_id)
    from app.models.db import Case, CaseFact, SyncSessionLocal
    from app.services.compliance.pre_intake import run_pre_intake_filters_chain_a, run_route_flags

    with SyncSessionLocal() as db:
        case = db.query(Case).filter_by(id=case_id).first()
        if not case:
            return

        raw_facts = {row.field_name: row.field_value for row in db.query(CaseFact).filter_by(case_id=case_id).all()}
        # principal_loan_amount for F3's repayment-ratio check is the same
        # figure as Case.principal_amount set at intake — no separate
        # extraction field for it, reuse what's already on the case row.
        if case.principal_amount is not None:
            raw_facts.setdefault("principal_loan_amount", str(case.principal_amount))

        terminating = run_pre_intake_filters_chain_a(raw_facts)
        route_flags = run_route_flags(raw_facts)

        if route_flags:
            case.judgment_coverage_alerts = (case.judgment_coverage_alerts or []) + [
                {**flag, "severity": "INFO", "action_required": False} for flag in route_flags
            ]

        if terminating is not None:
            case.status = "INTAKE_REJECTED"
            case.intake_filter_result = terminating.model_dump()
            logger.warning(
                "case=%s REJECTED at pre-intake: %s — %s",
                case_id, terminating.filter_id, terminating.reason,
            )

        db.commit()


@celery_app.task(name="tasks.chain_a.populate_workbench")
def task_populate_workbench(case_id: str) -> None:
    """No-op marker — the workbench is a live query (GET /workbench), not a
    materialized table. requires_workbench routing already happened at
    upsert time (confidence_router.route_fact). Kept as a pipeline stage
    for UI progress display, matching STAGE_PROGRESS/STAGE_MESSAGES in cases.py.
    """
    logger.info("running task_populate_workbench case=%s", case_id)
