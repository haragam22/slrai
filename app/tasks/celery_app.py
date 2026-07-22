import time

import structlog
from celery import Celery
from celery.signals import task_failure, task_postrun, task_prerun

from app.config import settings

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
)
_struct_logger = structlog.get_logger("celery.task")

_task_start_times: dict[str, float] = {}


def _case_id_from_args(args) -> str | None:
    # Every chain_a/chain_b task's first positional arg is case_id (bound
    # tasks still call with case_id as args[0] — `self` is not in `args`).
    return args[0] if args else None


@task_prerun.connect
def _on_task_prerun(task_id, task, args=None, **kwargs):
    _task_start_times[task_id] = time.monotonic()


@task_postrun.connect
def _on_task_postrun(task_id, task, args=None, retval=None, state=None, **kwargs):
    start = _task_start_times.pop(task_id, None)
    duration_ms = round((time.monotonic() - start) * 1000, 1) if start is not None else None
    _struct_logger.info(
        "task_completed",
        task_name=task.name,
        case_id=_case_id_from_args(args),
        duration_ms=duration_ms,
        result=state,
    )


@task_failure.connect
def _on_task_failure(task_id, exception=None, args=None, sender=None, **kwargs):
    _task_start_times.pop(task_id, None)
    _struct_logger.error(
        "task_failed",
        task_name=sender.name if sender else None,
        case_id=_case_id_from_args(args),
        error_type=type(exception).__name__ if exception else None,
        error_message=str(exception) if exception else None,
    )


celery_app = Celery(
    "slrai",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,            # re-queue on worker crash
    worker_prefetch_multiplier=1,   # one task at a time per worker (heavy OCR/NLP)
    broker_connection_retry_on_startup=True,
    task_routes={
        "tasks.chain_a.*": {"queue": "pipeline"},
        "tasks.chain_b.*": {"queue": "pipeline"},
    },
)

from app.tasks import chain_a, chain_b  # noqa: E402, F401 — registers tasks with celery_app
