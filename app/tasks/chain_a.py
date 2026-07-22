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
        task_update_pipeline_stage.si(case_id, "POPULATING_WORKBENCH"),
        task_populate_workbench.si(case_id),
        task_set_case_status.si(case_id, "PENDING_HUMAN_REVIEW"),
    )
    pipeline.delay()


@celery_app.task(name="tasks.chain_a.set_status")
def task_set_case_status(case_id: str, status: str) -> None:
    """Updates cases.status in DB. Uses .si() in chains — no passthrough arg."""
    logger.info("running task_set_case_status case=%s status=%s", case_id, status)
    from app.models.db import SyncSessionLocal, Case
    with SyncSessionLocal() as db:
        case = db.query(Case).filter_by(id=case_id).first()
        if case:
            case.status = status
            case.pipeline_stage = None
            db.commit()


@celery_app.task(name="tasks.chain_a.update_stage")
def task_update_pipeline_stage(case_id: str, stage: str) -> None:
    """Updates pipeline_stage on the case row. Uses .si() in chains."""
    logger.info("running task_update_pipeline_stage case=%s stage=%s", case_id, stage)
    from app.models.db import SyncSessionLocal, Case
    with SyncSessionLocal() as db:
        case = db.query(Case).filter_by(id=case_id).first()
        if case:
            case.pipeline_stage = stage
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
        for para in paragraphs:
            para.language = detect_paragraph_language(para.text_original)
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
        for para in paragraphs:
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
    """
    logger.info("running task_nlp_extract_facts case=%s", case_id)
    from app.models.db import Case, Document, Paragraph, SAGround, SyncSessionLocal
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

        paragraphs_payload = [
            {
                "para_id": para.id,
                "text_for_extraction": para.get_text(),
                "doc_type": doc_type,
            }
            for para, doc_type in rows
        ]

        try:
            results = process_paragraphs_for_extraction(paragraphs_payload)
        except anthropic.AuthenticationError:
            logger.error("ANTHROPIC_AUTH_FAILED case=%s", case_id)
            case = db.query(Case).filter_by(id=case_id).first()
            if case:
                case.status = "FAILED"
                case.pipeline_stage = None
            db.commit()
            return  # fatal, no retry

        for (para, _doc_type), result in zip(rows, results):
            if not result:
                upsert_case_fact(db, case_id, f"nlp_extraction_failed_{para.id}", {
                    "field_value": f"NLP extraction failed for paragraph {para.id}. Manual review required.",
                    "confidence": 0.0,
                    "extraction_method": "nlp_implied",
                    "source_document_id": para.document_id,
                    "source_page": para.page_number,
                    "source_paragraph_id": para.id,
                })
                continue

            for ground in result.get("ground_codes", []):
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
            for field_name, value in result.get("boolean_facts", {}).items():
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

            # NOTE: only balance_payment_date is wired here. The many other
            # named date fields the rule engine depends on (auction_date,
            # demand_notice_date, sale_certificate_date, mortgage_date,
            # lease_date, valuation_date, npa_classification_date, etc.) have
            # the same gap — the generic "dates":[{date,context}] array below
            # is never persisted to named CaseFact rows. See docs/schema_gaps.md.
            for field_name, value in result.get("date_facts", {}).items():
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

        aggregate_metadata(case_id, results, db)
        db.commit()


@celery_app.task(name="tasks.chain_a.populate_workbench")
def task_populate_workbench(case_id: str) -> None:
    """No-op marker — the workbench is a live query (GET /workbench), not a
    materialized table. requires_workbench routing already happened at
    upsert time (confidence_router.route_fact). Kept as a pipeline stage
    for UI progress display, matching STAGE_PROGRESS/STAGE_MESSAGES in cases.py.
    """
    logger.info("running task_populate_workbench case=%s", case_id)
