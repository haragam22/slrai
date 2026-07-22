"""Full pipeline evaluation — seeds one case, runs Chain B end to end
including task_generate_report (H9), against a live docker-compose stack
with a real ANTHROPIC_API_KEY. Not a pytest test, not collected by CI.

Run inside the worker container:
    docker cp tests/manual/full_eval_run.py slrai-worker-1:/app/tests/manual/full_eval_run.py
    docker compose exec worker python -m tests.manual.full_eval_run
"""
import uuid

from app.models.db import Bank, Case, CaseFact, SAGround, SyncSessionLocal, User

FACTS = {
    "sa_applicant_type": "BORROWER",
    "demand_notice_date": "2025-01-01",
    "sixty_day_period_elapsed": "True",
    "demand_notice_amount": "1000000",
    "actual_outstanding_amount": "1020000",
    "notice_service_mode": "registered_post_ad",
    "notice_dispatch_proof_present": "True",
    "notice_service_date": "2025-01-05",
    "notice_content_complete": "True",
    "possession_notice_date": "2025-04-01",
    "authorized_officer_name": "R. Kumar",
    "authorized_officer_designation": "Chief Manager",
    "ao_has_written_authorization": "False",  # M1_C8 -> FAIL FATAL
    "bank_reply_given": "False",
    "reply_sent_date": "",
}

# Ground codes chosen to also hit the one seeded Class A judgment
# (RIGHT_OF_REDEMPTION / AUCTION_PURCHASER / AUCTION_GAP_DEFECT), which
# exercises the live Claude API applicability check with a real key.
GROUNDS = ["SERVICE_DEFECT", "AMOUNT_DISPUTE", "AUCTION_GAP_DEFECT"]


def seed_case(db) -> str:
    bank = db.query(Bank).first()
    user = db.query(User).first()
    if bank is None or user is None:
        raise SystemExit("No bank/user row found — seed a bank+user first (need FK targets).")

    case = Case(
        id=uuid.uuid4(),
        bank_id=bank.id,
        created_by=user.id,
        borrower_name="Full Eval Run Borrower",
        status="ANALYSING",
    )
    db.add(case)
    db.flush()

    for field_name, value in FACTS.items():
        if value == "":
            continue
        db.add(CaseFact(
            case_id=case.id,
            field_name=field_name,
            field_value=str(value),
            human_confirmed=True,
            extraction_method="regex",
            confidence=1.0,
        ))

    for gc in GROUNDS:
        db.add(SAGround(case_id=case.id, ground_code=gc))

    db.commit()
    return str(case.id)


def run_chain_b_inline(case_id: str):
    from app.tasks.chain_b import (
        task_check_judgment_coverage, task_compute_compliance_score,
        task_compute_ground_statistics, task_evaluate_applicability,
        task_generate_recommendation, task_generate_report, task_resolve_precedence,
        task_retrieve_judgments, task_run_compliance_engine, task_score_grounds,
    )

    for fn in (
        task_run_compliance_engine, task_retrieve_judgments, task_evaluate_applicability,
        task_compute_ground_statistics, task_check_judgment_coverage, task_resolve_precedence,
        task_score_grounds, task_compute_compliance_score, task_generate_recommendation,
        task_generate_report,
    ):
        print(f"--- {fn.__name__} ---")
        fn(case_id)


def report(case_id: str):
    from app.models.db import ComplianceResult, GroundScore, Report

    with SyncSessionLocal() as db:
        results = db.query(ComplianceResult).filter_by(case_id=case_id).all()
        scores = db.query(GroundScore).filter_by(case_id=case_id).all()
        rep = db.query(Report).filter_by(case_id=case_id).first()

        print(f"\n=== FULL EVAL (case_id={case_id}) ===")
        for r in results:
            print(f"  {r.rule_id:10s} {r.status:8s} {r.severity or '-':10s} {r.message[:70] if r.message else ''}")
        for s in scores:
            print(f"  ground={s.ground_code:20s} factual={s.factual_score} judicial={s.judicial_score} strength={s.ground_strength}")
        if rep:
            print(f"  compliance_score={rep.compliance_score}  litigation_exposure={rep.litigation_exposure}  recommendation={rep.recommendation}")
            print(f"  pdf_url={rep.pdf_url}")
        else:
            print("  NO REPORT ROW")


if __name__ == "__main__":
    with SyncSessionLocal() as db:
        case_id = seed_case(db)

    print(f"case_id={case_id}")
    run_chain_b_inline(case_id)
    report(case_id)
