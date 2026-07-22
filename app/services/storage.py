"""
S3/MinIO object storage service.

SECURITY:
  - S3 keys are built from UUIDs only — no user input touches the path.
  - All objects stored with AES-256 SSE.
  - No public ACL — bucket must be private.
  - Max upload: 25 MB. Allowed types: application/pdf only.
"""

from __future__ import annotations

import hashlib
from typing import Generator

import boto3
from botocore.exceptions import ClientError

from app.config import settings

MAX_UPLOAD_SIZE_MB = 25
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024

# OCR (extract_layout) splits input as a PDF via pypdf — only PDF is actually
# supported end-to-end, so only PDF is accepted here.
ALLOWED_CONTENT_TYPES = {"application/pdf"}

_s3_client = None


class StorageError(Exception):
    """Base class for storage-layer errors. Not a web-framework type — this
    module is imported by both async API routes and sync Celery tasks, so it
    must not raise fastapi.HTTPException. API routes translate these to HTTP
    responses; Celery tasks catch and log them."""


class UnsupportedMediaTypeError(StorageError):
    def __init__(self, content_type: str):
        self.content_type = content_type
        super().__init__(f"Unsupported media type '{content_type}'. Only PDF files are accepted.")


class FileTooLargeError(StorageError):
    def __init__(self, max_mb: int):
        self.max_mb = max_mb
        super().__init__(f"File exceeds maximum size of {max_mb} MB.")


class StorageUploadError(StorageError):
    pass


class StorageDownloadError(StorageError):
    pass


class DocumentNotFoundError(StorageError):
    pass


def get_s3_client():
    global _s3_client
    if _s3_client is None:
        kwargs = dict(
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
        )
        if settings.s3_endpoint_url:
            kwargs["endpoint_url"] = settings.s3_endpoint_url
        _s3_client = boto3.client("s3", **kwargs)
    return _s3_client


# ─── KEY BUILDERS ──────────────────────────────────────────────────────────────

def document_s3_key(case_id: str, doc_id: str) -> str:
    return f"cases/{case_id}/documents/{doc_id}.pdf"


def report_pdf_s3_key(case_id: str, report_id: str) -> str:
    return f"cases/{case_id}/reports/{report_id}.pdf"


def report_json_s3_key(case_id: str, report_id: str) -> str:
    return f"cases/{case_id}/reports/{report_id}.json"


# ─── INTEGRITY ────────────────────────────────────────────────────────────────

def compute_sha256(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()


# ─── VALIDATION ───────────────────────────────────────────────────────────────

def validate_file_type(content_type: str) -> None:
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise UnsupportedMediaTypeError(content_type)


# ─── UPLOAD ──────────────────────────────────────────────────────────────────

def upload_document(
    file_bytes: bytes,
    case_id: str,
    doc_id: str,
    content_type: str = "application/pdf",
) -> tuple[str, str]:
    """Upload a case document. Returns (s3_key, sha256_hash)."""
    if len(file_bytes) > MAX_UPLOAD_SIZE_BYTES:
        raise FileTooLargeError(MAX_UPLOAD_SIZE_MB)
    s3_key = document_s3_key(case_id, doc_id)
    sha256 = compute_sha256(file_bytes)
    try:
        get_s3_client().put_object(
            Bucket=settings.s3_bucket_name,
            Key=s3_key,
            Body=file_bytes,
            ContentType=content_type,
            ServerSideEncryption="AES256",
        )
    except ClientError as exc:
        raise StorageUploadError("Storage upload failed.") from exc
    return s3_key, sha256


def upload_report_pdf(
    pdf_bytes: bytes,
    case_id: str,
    report_id: str,
) -> str | None:
    """Upload a generated PDF report. Returns s3_key or None on failure (non-fatal)."""
    s3_key = report_pdf_s3_key(case_id, report_id)
    try:
        get_s3_client().put_object(
            Bucket=settings.s3_bucket_name,
            Key=s3_key,
            Body=pdf_bytes,
            ContentType="application/pdf",
            ServerSideEncryption="AES256",
        )
        return s3_key
    except ClientError:
        return None


def upload_report_json(
    json_str: str,
    case_id: str,
    report_id: str,
) -> str | None:
    """Upload a report JSON payload. Returns s3_key or None on failure (non-fatal)."""
    s3_key = report_json_s3_key(case_id, report_id)
    try:
        get_s3_client().put_object(
            Bucket=settings.s3_bucket_name,
            Key=s3_key,
            Body=json_str.encode("utf-8"),
            ContentType="application/json",
            ServerSideEncryption="AES256",
        )
        return s3_key
    except ClientError:
        return None


# ─── DOWNLOAD ────────────────────────────────────────────────────────────────

def download_document(s3_key: str) -> bytes:
    """Download document bytes. Raises 404 if not found, 500 on other errors."""
    try:
        resp = get_s3_client().get_object(Bucket=settings.s3_bucket_name, Key=s3_key)
        return resp["Body"].read()
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code in ("NoSuchKey", "404"):
            raise DocumentNotFoundError("Document not found in storage.") from exc
        raise StorageDownloadError("Storage download failed.") from exc


def stream_document(s3_key: str) -> Generator[bytes, None, None]:
    """Stream document in 64 KB chunks."""
    try:
        resp = get_s3_client().get_object(Bucket=settings.s3_bucket_name, Key=s3_key)
        body = resp["Body"]
        while True:
            chunk = body.read(65536)
            if not chunk:
                break
            yield chunk
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code in ("NoSuchKey", "404"):
            raise DocumentNotFoundError("Document not found in storage.") from exc
        raise StorageDownloadError("Storage stream failed.") from exc


# ─── BUCKET SETUP (MinIO only) ───────────────────────────────────────────────

def ensure_bucket_exists() -> None:
    """Creates the bucket if running against MinIO. No-op for AWS (bucket pre-exists)."""
    if not settings.s3_endpoint_url:
        return
    s3 = get_s3_client()
    try:
        s3.head_bucket(Bucket=settings.s3_bucket_name)
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code in ("404", "NoSuchBucket"):
            s3.create_bucket(Bucket=settings.s3_bucket_name)
