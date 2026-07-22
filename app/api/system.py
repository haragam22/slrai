"""System endpoints — GET /health pings every backing service so an outage
in any one of them (Postgres, Redis, Qdrant, MinIO) is visible in one call,
not discovered later as a mysterious pipeline failure."""
from __future__ import annotations

import logging

from fastapi import APIRouter
from sqlalchemy import text

from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


def _check_db() -> bool:
    from app.models.db import SyncSessionLocal
    try:
        with SyncSessionLocal() as db:
            db.execute(text("SELECT 1"))
        return True
    except Exception:
        logger.exception("health check: postgres unreachable")
        return False


def _check_redis() -> bool:
    import redis
    try:
        redis.from_url(settings.redis_url, socket_connect_timeout=3).ping()
        return True
    except Exception:
        logger.exception("health check: redis unreachable")
        return False


def _check_qdrant() -> bool:
    from app.services.judgments.retrieval import is_qdrant_reachable
    return is_qdrant_reachable()


def _check_minio() -> bool:
    from app.services.storage import get_s3_client
    try:
        get_s3_client().list_buckets()
        return True
    except Exception:
        logger.exception("health check: minio/s3 unreachable")
        return False


@router.get("/health")
def health() -> dict:
    checks = {
        "db":     _check_db(),
        "redis":  _check_redis(),
        "qdrant": _check_qdrant(),
        "minio":  _check_minio(),
    }
    status = "healthy" if all(checks.values()) else "degraded"
    return {"status": status, **checks}
