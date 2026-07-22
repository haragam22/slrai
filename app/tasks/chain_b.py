"""Chain B — officer-triggered (fires on POST /workbench/confirm-all).

NEVER connect Chain A to Chain B automatically — they are always separated by human review.
"""
import logging

from celery import chain

from app.tasks.celery_app import celery_app
from app.tasks.chain_a import task_set_case_status  # shared status updater

logger = logging.getLogger(__name__)

# Maps each rule_id to its primary ground code — used for lazy judgment
# retrieval (only retrieve for grounds actually raised/failed in this case)
# and by generator.py (_get_authority_for_rule) and workbench API.
# Ground code values match the valid ground_codes list in nlp_layer.py's
# BATCH_USER_TEMPLATE — must stay in sync with the extraction prompt.
RULE_TO_GROUND_MAP: dict[str, str] = {
    "M1_C1": "SERVICE_DEFECT",          "M1_C2": "AMOUNT_DISPUTE",
    "M1_C3": "SERVICE_DEFECT",          "M1_C4": "SERVICE_DEFECT",
    "M1_C5": "SERVICE_DEFECT",          "M1_C6": "NOTICE_FORMAT_DEFECT",
    "M1_C7": "SERVICE_DEFECT",          "M1_C8": "AO_AUTHORIZATION",
    "M2_C1": "REPLY_NOT_GIVEN",         "M2_C2": "REPLY_NOT_GIVEN",
    "M2_C3": "REPLY_NOT_GIVEN",
    "M3_C1": "AUCTION_GAP_DEFECT",      "M3_C2": "NEWSPAPER_PUB_DEFECT",
    "M3_C3": "AUCTION_GAP_DEFECT",      "M3_C4": "POSSESSION_DEFECT",
    "M3_C6": "AUCTION_NOTICE_AFFIXING", "M3_C7": "AUCTION_DURING_STAY",
    "M3_C8": "PENDING_SA_CONCEALED",
    "M4_C1": "LIMITATION_EXPIRED",      "M4_C2": "LIMITATION_EXPIRED",
    "M4_C3": "LIMITATION_EXPIRED",      "M4_C5": "SECOND_SA_FRESH_CAUSE",
    "M5_C1": "TENANCY_CLAIM",           "M5_C2": "TENANCY_CLAIM",
    "M5_C3": "TENANCY_CLAIM",           "M5_C4": "TENANCY_CLAIM",
    "M6_C1": "VALUATION_DISPUTE",       "M6_C2": "VALUATION_DISPUTE",
    "M6_C3": "VALUATION_DISPUTE",       "M6_C4": "VALUATION_DISPUTE",
    "M7_C1": "NOTICE_ALL_PARTIES",      "M7_C2": "NOTICE_ALL_PARTIES",
    "M8_C1": "NPA_PREMATURE",           "M8_C2": "NPA_DURING_RESTRUC",
    "M8_C3": "NPA_PREMATURE",           "M8_C4": "AMOUNT_DISPUTE",
    "M8_C6": "NPA_PREMATURE",
    "M9_C1": "MSME_RESTRUC_SKIPPED",    "M9_C2": "MSME_RESTRUC_SKIPPED",
    "M10_C1": "THIRD_PARTY_ATS",        "M10_C2": "THIRD_PARTY_ATS",
    "M10_C3": "THIRD_PARTY_ATS",        "M10_C4": "AUCTION_PURCHASER",
    "M10_C5": "RIGHT_OF_REDEMPTION",    "M10_C6": "SECOND_SA_FRESH_CAUSE",
}


@celery_app.task(bind=True, name="tasks.chain_b.run_from_judgments", max_retries=1, default_retry_delay=5)
def run_chain_b_from_judgments(self, case_id: str, triggered_by_user_id: str | None = None):
    """Entry point used by POST /cases/{case_id}/resume (officer-triggered).
    NEVER call this from Chain A.
    """
    try:
        run_chain_b.apply_async(args=[case_id])
    except Exception as exc:
        logger.exception("Failed to dispatch Chain B for case=%s", case_id)
        raise self.retry(exc=exc)


@celery_app.task(bind=True, name="tasks.chain_b.run", max_retries=1)
def run_chain_b(self, case_id: str):
    """Fired by POST /api/v1/cases/{case_id}/workbench/confirm-all."""
    pipeline = chain(
        task_set_case_status.si(case_id, "ANALYSING"),
        task_run_compliance_engine.si(case_id),
        task_retrieve_judgments.si(case_id),
        task_evaluate_applicability.si(case_id),
        task_compute_ground_statistics.si(case_id),
        task_check_judgment_coverage.si(case_id),
        task_resolve_precedence.si(case_id),
        task_score_grounds.si(case_id),
        task_compute_compliance_score.si(case_id),
        task_generate_recommendation.si(case_id),
        task_generate_report.si(case_id),
        task_set_case_status.si(case_id, "COMPLETE"),
    )
    pipeline.delay()


@celery_app.task(name="tasks.chain_b.run_compliance_engine")
def task_run_compliance_engine(case_id: str) -> None:
    """Run the YAML rule engine (M1-M9; M10 added later for third-party
    applicants — see H8) against this case's confirmed facts, persisting
    each RuleResult as a compliance_results row.
    """
    logger.info("running task_run_compliance_engine case=%s", case_id)
    from app.models.db import ComplianceResult, SyncSessionLocal
    from app.services.compliance.engine import load_confirmed_facts, run_all_modules

    with SyncSessionLocal() as db:
        confirmed_facts = load_confirmed_facts(case_id, db)

        applicant_type = confirmed_facts.get("sa_applicant_type", {}).get("value", "BORROWER")
        modules_to_run = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9"]
        if applicant_type not in ["BORROWER", "GUARANTOR", None]:
            modules_to_run.append("M10")

        results = run_all_modules(confirmed_facts, modules_to_run=modules_to_run)

        db.query(ComplianceResult).filter_by(case_id=case_id).delete()
        for r in results:
            db.add(ComplianceResult(
                case_id=case_id,
                rule_id=r.rule_id,
                module=r.module,
                status=r.status,
                severity=r.severity,
                message=r.message,
                detail_json=r.detail,
                judgment_tags=r.judgment_tags,
            ))
        db.commit()


@celery_app.task(name="tasks.chain_b.retrieve_judgments")
def task_retrieve_judgments(case_id: str) -> None:
    """Lazy retrieval from sarfaesi_judgments for SA-raised (or compliance-failed)
    ground codes only. Logs candidate counts; task_evaluate_applicability does
    the actual retrieval + persistence (Celery .si() passes no data between
    tasks, so re-deriving ground codes there is cheap and keeps tasks decoupled).
    """
    logger.info("running task_retrieve_judgments case=%s", case_id)
    from app.models.db import Case, SyncSessionLocal
    from app.services.compliance.engine import load_confirmed_facts
    from app.services.judgments.retrieval import (
        build_case_keywords, get_relevant_ground_codes, is_qdrant_reachable, retrieve_candidate_judgments,
    )

    if not is_qdrant_reachable():
        # Contract §18.3 — do not fail the case; note it and let Chain B continue
        # without a judgment section. task_evaluate_applicability makes the same
        # check and skips retrieval entirely.
        logger.error("Qdrant unavailable for case=%s — skipping judgment retrieval", case_id)
        with SyncSessionLocal() as db:
            case = db.query(Case).filter_by(id=case_id).first()
            if case:
                case.judgment_coverage_alerts = (case.judgment_coverage_alerts or []) + [{
                    "ground_code": None,
                    "severity": "UNAVAILABLE",
                    "message": "Judgment database temporarily unavailable.",
                    "action_required": False,
                }]
                db.commit()
        return

    with SyncSessionLocal() as db:
        ground_codes = get_relevant_ground_codes(case_id, db)
        confirmed_facts_raw = load_confirmed_facts(case_id, db)

    confirmed_facts = {k: v["value"] for k, v in confirmed_facts_raw.items()}
    case_keywords = build_case_keywords(confirmed_facts)

    for ground_code in ground_codes:
        class_a, class_b = retrieve_candidate_judgments(ground_code, case_keywords=case_keywords)
        logger.info(
            "case=%s ground=%s class_a=%d class_b=%d",
            case_id, ground_code, len(class_a), len(class_b),
        )


@celery_app.task(name="tasks.chain_b.evaluate_applicability")
def task_evaluate_applicability(case_id: str) -> None:
    """Two-path: Class A (wiki + single Claude call) fact-graph applicability,
    Class B (Qdrant) similarity flag. Persists JudgmentApplicability rows."""
    logger.info("running task_evaluate_applicability case=%s", case_id)
    from app.models.db import Judgment, JudgmentApplicability, SyncSessionLocal
    from app.services.compliance.engine import load_confirmed_facts
    from app.services.judgments.applicability import (
        evaluate_class_a_applicability, process_class_b_candidates,
    )
    from app.services.judgments.retrieval import (
        build_case_keywords, get_relevant_ground_codes, is_qdrant_reachable, retrieve_candidate_judgments,
    )

    if not is_qdrant_reachable():
        logger.error("Qdrant unavailable for case=%s — skipping applicability evaluation", case_id)
        return

    with SyncSessionLocal() as db:
        ground_codes = get_relevant_ground_codes(case_id, db)
        if not ground_codes:
            return

        confirmed_facts_raw = load_confirmed_facts(case_id, db)
        confirmed_facts = {k: v["value"] for k, v in confirmed_facts_raw.items()}
        case_keywords = build_case_keywords(confirmed_facts)

        db.query(JudgmentApplicability).filter_by(case_id=case_id).delete()

        seen_class_a_ids: set = set()
        all_class_a_payloads: dict[str, dict] = {}
        for ground_code in ground_codes:
            class_a, class_b = retrieve_candidate_judgments(ground_code, case_keywords=case_keywords)
            for j in class_a:
                all_class_a_payloads[j.get("citation", j.get("short_name", ""))] = j

            for entry in process_class_b_candidates(class_b):
                judgment_uuid = entry["judgment"].get("id")
                if not judgment_uuid:
                    continue
                db.add(JudgmentApplicability(
                    case_id=case_id,
                    judgment_id=judgment_uuid,
                    ground_code=ground_code,
                    status=entry["status"],
                    reason=entry["reason"],
                ))

        if all_class_a_payloads:
            results = evaluate_class_a_applicability(
                confirmed_facts=confirmed_facts,
                sa_grounds=list(ground_codes),
                judgment_count=len(all_class_a_payloads),
            )
            for r in results:
                judgment = db.query(Judgment).filter_by(citation=r.get("citation")).first()
                if judgment is None:
                    continue
                status = "APPLICABLE" if r.get("applicable") else "NOT_APPLICABLE"
                for ground_code in (judgment.ground_codes or []):
                    if ground_code not in ground_codes:
                        continue
                    db.add(JudgmentApplicability(
                        case_id=case_id,
                        judgment_id=judgment.id,
                        ground_code=ground_code,
                        status=status,
                        reason=r.get("reason", ""),
                    ))

        db.commit()


@celery_app.task(name="tasks.chain_b.compute_ground_statistics")
def task_compute_ground_statistics(case_id: str) -> None:
    """Queries Qdrant payload filters for corpus win rates (verified + full),
    stores both in ground_scores."""
    logger.info("running task_compute_ground_statistics case=%s", case_id)
    from app.models.db import GroundScore, SAGround, SyncSessionLocal
    from app.services.judgments.statistics import get_ground_statistics

    with SyncSessionLocal() as db:
        grounds = db.query(SAGround).filter_by(case_id=case_id).all()
        for ground in grounds:
            stats = get_ground_statistics(ground.ground_code)
            score_row = db.query(GroundScore).filter_by(case_id=case_id, ground_code=ground.ground_code).first()
            if score_row is None:
                score_row = GroundScore(case_id=case_id, ground_code=ground.ground_code)
                db.add(score_row)
            score_row.corpus_total              = stats["verified"]["total"]
            score_row.corpus_borrower_wins       = stats["verified"]["borrower_wins"]
            score_row.corpus_bank_wins           = stats["verified"]["bank_wins"]
            score_row.corpus_confidence          = stats["data_confidence"]
            score_row.full_corpus_total          = stats["full"]["total"]
            score_row.full_corpus_borrower_wins  = stats["full"]["borrower_wins"]
            score_row.full_corpus_bank_wins      = stats["full"]["bank_wins"]
        db.commit()


@celery_app.task(name="tasks.chain_b.check_judgment_coverage")
def task_check_judgment_coverage(case_id: str) -> None:
    """Checks every SA ground has at least one APPLICABLE Class A judgment; stores alerts."""
    logger.info("running task_check_judgment_coverage case=%s", case_id)
    from app.models.db import SyncSessionLocal, Case, SAGround, JudgmentApplicability

    with SyncSessionLocal() as db:
        sa_grounds = db.query(SAGround).filter_by(case_id=case_id).all()
        alerts = []

        for ground in sa_grounds:
            applicable = db.query(JudgmentApplicability).filter_by(
                case_id=case_id,
                ground_code=ground.ground_code,
                status="APPLICABLE",
            ).count()

            similarity = db.query(JudgmentApplicability).filter_by(
                case_id=case_id,
                ground_code=ground.ground_code,
                status="SIMILARITY_RETRIEVED",
            ).count()

            if applicable == 0:
                alerts.append({
                    "ground_code": ground.ground_code,
                    "severity": "WARNING" if similarity > 0 else "NO_PRECEDENT",
                    "similarity_count": similarity,
                    "message": (
                        f"No verified precedent for '{ground.ground_code}'. "
                        f"{similarity} potentially relevant judgment(s) found "
                        f"but factual conditions not verified. Review manually."
                        if similarity > 0 else
                        f"No precedent of any kind found for '{ground.ground_code}'. "
                        f"Neutral judicial score (0.40) applied. "
                        f"Manual legal research required."
                    ),
                    "action_required": similarity == 0,
                })

        if alerts:
            case = db.query(Case).filter_by(id=case_id).first()
            if case:
                case.judgment_coverage_alerts = alerts
                db.commit()


@celery_app.task(name="tasks.chain_b.resolve_precedence")
def task_resolve_precedence(case_id: str) -> None:
    """Resolves conflicting APPLICABLE judgments per ground to a single
    controlling precedent; flags LEGAL_UNCERTAINTY where genuinely unresolvable."""
    logger.info("running task_resolve_precedence case=%s", case_id)
    from app.models.db import JudgmentApplicability, SyncSessionLocal
    from app.services.judgments.precedence import resolve_conflicts_for_ground

    with SyncSessionLocal() as db:
        rows = db.query(JudgmentApplicability).filter_by(case_id=case_id, status="APPLICABLE").all()

        by_ground: dict[str, list] = {}
        for row in rows:
            by_ground.setdefault(row.ground_code, []).append(row)

        for ground_code, ground_rows in by_ground.items():
            if len(ground_rows) < 2:
                continue
            judgments = [
                {
                    "id": row.judgment_id,
                    "citation": row.judgment.citation,
                    "court": row.judgment.court,
                    "bench_strength": row.judgment.bench_strength,
                    "judgment_date": row.judgment.judgment_date,
                }
                for row in ground_rows
            ]
            result = resolve_conflicts_for_ground(judgments)
            if result["controlling"] is None and "uncertainty_reason" in result:
                for row in ground_rows:
                    row.status = "LEGAL_UNCERTAINTY"
                    row.reason = result["uncertainty_reason"]

        db.commit()


@celery_app.task(name="tasks.chain_b.score_grounds")
def task_score_grounds(case_id: str) -> None:
    """Corpus-informed per-ground borrower strength score. Combines this case's
    compliance rule outcomes (factual_score) with corpus win-rate statistics and
    any case-specific applicable Class A judgments (judicial_score)."""
    logger.info("running task_score_grounds case=%s", case_id)
    from app.models.db import ComplianceResult, GroundScore, JudgmentApplicability, SyncSessionLocal
    from app.services.scoring.ground_strength import compute_ground_strength

    with SyncSessionLocal() as db:
        results = db.query(ComplianceResult).filter_by(case_id=case_id).all()

        # Worst status per ground (FAIL > UNKNOWN > PASS) across rules mapped to it.
        status_rank = {"FAIL": 2, "UNKNOWN": 1, "PASS": 0, "REVIEW": 1}
        status_by_ground: dict[str, str] = {}
        for r in results:
            ground_code = RULE_TO_GROUND_MAP.get(r.rule_id)
            if ground_code is None:
                continue
            current = status_by_ground.get(ground_code)
            if current is None or status_rank.get(r.status, 0) > status_rank.get(current, 0):
                status_by_ground[ground_code] = r.status

        score_rows = db.query(GroundScore).filter_by(case_id=case_id).all()
        for score_row in score_rows:
            applicable = db.query(JudgmentApplicability).filter_by(
                case_id=case_id, ground_code=score_row.ground_code, status="APPLICABLE",
            ).all()
            applicable_judgments = [
                {"court": a.judgment.court, "favor": a.judgment.favor} for a in applicable
            ]
            corpus_stats = {
                "verified": {
                    "total": score_row.corpus_total,
                    "borrower_win_pct": (
                        round(score_row.corpus_borrower_wins / score_row.corpus_total * 100, 1)
                        if score_row.corpus_total else None
                    ),
                },
                "full": {
                    "total": score_row.full_corpus_total,
                    "borrower_win_pct": (
                        round(score_row.full_corpus_borrower_wins / score_row.full_corpus_total * 100, 1)
                        if score_row.full_corpus_total else None
                    ),
                },
                "data_confidence": score_row.corpus_confidence,
            }
            compliance_status = status_by_ground.get(score_row.ground_code, "UNKNOWN")
            scored = compute_ground_strength(
                score_row.ground_code, compliance_status, applicable_judgments, corpus_stats,
            )
            score_row.factual_score = scored["factual_score"]
            score_row.judicial_score = scored["judicial_score"]
            score_row.ground_strength = scored["ground_strength"]

        db.commit()


@celery_app.task(name="tasks.chain_b.compute_compliance_score")
def task_compute_compliance_score(case_id: str) -> None:
    """Aggregate bank procedural compliance score and litigation exposure; stash
    both on a scratch Report row (finalised by task_generate_report in H9)."""
    logger.info("running task_compute_compliance_score case=%s", case_id)
    from app.models.db import ComplianceResult, GroundScore, Report, SyncSessionLocal
    from app.services.scoring.compliance_score import compute_compliance_score
    from app.services.scoring.ground_strength import compute_litigation_exposure

    with SyncSessionLocal() as db:
        results = db.query(ComplianceResult).filter_by(case_id=case_id).all()
        score = compute_compliance_score(results)

        ground_scores = db.query(GroundScore).filter_by(case_id=case_id).all()
        exposure = compute_litigation_exposure([
            {"ground_strength": g.ground_strength} for g in ground_scores if g.ground_strength is not None
        ])

        report = db.query(Report).filter_by(case_id=case_id).order_by(Report.generated_at.desc()).first()
        if report is None:
            report = Report(case_id=case_id)
            db.add(report)
        report.compliance_score = score
        report.litigation_exposure = exposure
        db.commit()


@celery_app.task(name="tasks.chain_b.generate_recommendation")
def task_generate_recommendation(case_id: str) -> None:
    """Matrix lookup: compliance_score × litigation_exposure → recommendation."""
    logger.info("running task_generate_recommendation case=%s", case_id)
    from app.models.db import ComplianceResult, Report, SyncSessionLocal
    from app.services.scoring.recommendation import get_recommendation

    with SyncSessionLocal() as db:
        report = db.query(Report).filter_by(case_id=case_id).order_by(Report.generated_at.desc()).first()
        if report is None or report.compliance_score is None or report.litigation_exposure is None:
            logger.warning("task_generate_recommendation: no scored report for case=%s", case_id)
            return

        absolute_bar_triggered = db.query(ComplianceResult).filter_by(
            case_id=case_id, status="FAIL", severity="ABSOLUTE_BAR",
        ).first() is not None

        rec = get_recommendation(report.compliance_score, report.litigation_exposure, absolute_bar_triggered)
        report.recommendation = rec["label"]
        db.commit()


@celery_app.task(name="tasks.chain_b.generate_report")
def task_generate_report(case_id: str) -> None:
    """WeasyPrint PDF report with precedents, statutory citations, scores."""
    logger.info("running task_generate_report case=%s", case_id)
    from app.reports.generator import generate_report
    generate_report(case_id, user_id=None)
