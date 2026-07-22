import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import auth, cases, documents, pipeline, results, system, workbench, reports
from app.tasks.celery_app import celery_app  # noqa — initialises Celery on import

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    logger.info("SLRAI API starting up")

    try:
        from app.services.storage import ensure_bucket_exists
        ensure_bucket_exists()
        logger.info("MinIO bucket ready")
    except Exception as exc:
        logger.warning("MinIO bucket setup skipped: %s", exc)

    try:
        from app.services.judgments.retrieval import setup_qdrant_collections
        await setup_qdrant_collections()
        logger.info("Qdrant collections initialised")
    except Exception as exc:
        logger.warning("Qdrant setup skipped: %s", exc)

    try:
        from app.services.extraction.nlp_layer import get_batch_system_prompt
        get_batch_system_prompt()
        logger.info("System prompt pre-loaded")
    except Exception as exc:
        logger.warning("System prompt pre-load skipped: %s", exc)

    yield

    # shutdown
    logger.info("SLRAI API shutting down")


app = FastAPI(title="SLRAI", version="1.0.0", lifespan=lifespan)

app.include_router(auth.router,       prefix="/api/v1/auth",      tags=["auth"])
app.include_router(cases.router,      prefix="/api/v1/cases",     tags=["cases"])
app.include_router(documents.router,  prefix="/api/v1/cases",     tags=["documents"])
app.include_router(pipeline.router,   prefix="/api/v1/cases",     tags=["pipeline"])
app.include_router(workbench.router,  prefix="/api/v1/cases",     tags=["workbench"])
app.include_router(reports.router,    prefix="/api/v1/cases",     tags=["reports"])
app.include_router(results.router,    prefix="/api/v1/cases",     tags=["results"])
app.include_router(system.router,     prefix="",                  tags=["system"])
