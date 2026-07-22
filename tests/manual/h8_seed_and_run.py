"""H8 manual test — NOT a pytest test, not collected by pytest, not run in CI.
Seeds two fixture cases (BORROWER, THIRD_PARTY_ATS) and runs Chain B
synchronously (task functions called in-process) against a live docker-compose
stack, skipping only task_generate_report (H9, not yet built).

Run inside the worker container (needs the code copied/mounted in first —
this file lives under tests/manual/, outside the image's COPY of app/):
    docker cp tests/manual/h8_seed_and_run.py slrai-worker-1:/app/tests/manual/h8_seed_and_run.py
    docker compose exec worker python -m tests.manual.h8_seed_and_run
"""
import uuid
from datetime import date

from app.models.db import Bank, Case, CaseFact, SAGround, SyncSessionLocal, User

BORROWER_FACTS = {
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
    "bank_reply_given": "False",  # drives M2 FAIL if such field used
    "reply_sent_date": "",
}

THIRD_PARTY_FACTS = dict(BORROWER_FACTS)
THIRD_PARTY_FACTS.update({
    "sa_applicant_type": "THIRD_PARTY_ATS",
    "ats_simultaneous_mortgage": "True",   # M10_C2 -> FAIL HIGH
    "ats_date": "2024-01-01",
    "mortgage_date": "2024-01-01",
    "ats_payments_made_to_loan_account": "False",
})

# Ground codes deliberately avoid RIGHT_OF_REDEMPTION / AUCTION_PURCHASER /
# AUCTION_GAP_DEFECT — the only Class A judgment currently seeded in Qdrant
# carries those, and triggering Class A evaluation calls the live Claude API
# (no real ANTHROPIC_API_KEY in this dev .env). Keeping clear of them lets
# the scoring/M10-routing pipeline run deterministically end to end.
BORROWER_GROUNDS = ["SERVICE_DEFECT", "AMOUNT_DISPUTE"]
THIRD_PARTY_GROUNDS = ["SERVICE_DEFECT", "THIRD_PARTY_ATS"]


def seed_case(db, applicant_type: str, facts: dict, grounds: list[str]) -> str:
    bank = db.query(Bank).first()
    user = db.query(User).first()
    if bank is None or user is None:
        raise SystemExit("No bank/user row found — seed a bank+user first (need FK targets).")

    case = Case(
        id=uuid.uuid4(),
        bank_id=bank.id,
        created_by=user.id,
        borrower_name=f"H8 Test {applicant_type}",
        status="ANALYSING",
    )
    db.add(case)
    db.flush()

    for field_name, value in facts.items():
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

    for gc in grounds:
        db.add(SAGround(case_id=case.id, ground_code=gc))

    db.commit()
    return str(case.id)


def run_chain_b_inline(case_id: str):
    from app.tasks.chain_b import (
        task_check_judgment_coverage, task_compute_compliance_score,
        task_compute_ground_statistics, task_evaluate_applicability,
        task_generate_recommendation, task_resolve_precedence,
        task_retrieve_judgments, task_run_compliance_engine, task_score_grounds,
    )

    for fn in (
        task_run_compliance_engine, task_retrieve_judgments, task_evaluate_applicability,
        task_compute_ground_statistics, task_check_judgment_coverage, task_resolve_precedence,
        task_score_grounds, task_compute_compliance_score, task_generate_recommendation,
    ):
        print(f"--- {fn.__name__} ---")
        fn(case_id)


def report(case_id: str, label: str):
    from app.models.db import ComplianceResult, GroundScore, Report

    with SyncSessionLocal() as db:
        results = db.query(ComplianceResult).filter_by(case_id=case_id).all()
        modules_hit = sorted({r.module for r in results})
        m10_ran = any(r.module == "M10_THIRD_PARTY" for r in results)

        scores = db.query(GroundScore).filter_by(case_id=case_id).all()
        rep = db.query(Report).filter_by(case_id=case_id).first()

        print(f"\n=== {label} (case_id={case_id}) ===")
        print(f"modules that fired: {modules_hit}")
        print(f"M10 ran: {m10_ran}")
        for r in results:
            print(f"  {r.rule_id:10s} {r.status:8s} {r.severity or '-':10s} {r.message[:70] if r.message else ''}")
        for s in scores:
            print(f"  ground={s.ground_code:20s} factual={s.factual_score} judicial={s.judicial_score} strength={s.ground_strength}")
        if rep:
            print(f"  compliance_score={rep.compliance_score}  litigation_exposure={rep.litigation_exposure}  recommendation={rep.recommendation}")
        else:
            print("  NO REPORT ROW")


if __name__ == "__main__":
    with SyncSessionLocal() as db:
        borrower_id = seed_case(db, "BORROWER", BORROWER_FACTS, BORROWER_GROUNDS)
        third_party_id = seed_case(db, "THIRD_PARTY_ATS", THIRD_PARTY_FACTS, THIRD_PARTY_GROUNDS)

    print(f"borrower_case_id={borrower_id}")
    print(f"third_party_case_id={third_party_id}")

    run_chain_b_inline(borrower_id)
    run_chain_b_inline(third_party_id)

    report(borrower_id, "BORROWER")
    report(third_party_id, "THIRD_PARTY_ATS")
