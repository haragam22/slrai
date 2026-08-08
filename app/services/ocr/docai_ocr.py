"""OCR via Google Cloud Document AI — layout parser processor.

NEVER Azure Document Intelligence (see CLAUDE_v51.md tech stack — switched away).
Uses the layout processor so paragraph-level semantic grouping survives
(equivalent reasoning to Azure's "use result.paragraphs not page.lines":
we read visual_elements / paragraphs from the Document AI layout, not raw
line-level tokens, so a numbered clause split across lines stays one unit).
"""
import logging
import os

from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import GoogleAPICallError
from google.auth.exceptions import GoogleAuthError
from google.cloud import documentai

from app.config import settings

logger = logging.getLogger(__name__)

# Cache at module level — never instantiate per call.
_docai_client: documentai.DocumentProcessorServiceClient | None = None


def get_ocr_client() -> documentai.DocumentProcessorServiceClient:
    global _docai_client
    if _docai_client is None:
        # google-cloud libs look up ADC project via GOOGLE_CLOUD_PROJECT, not
        # our own GCP_PROJECT_ID setting — set it so client init stops warning
        # "No project ID could be determined".
        os.environ.setdefault("GOOGLE_CLOUD_PROJECT", settings.gcp_project_id)
        opts = ClientOptions(
            api_endpoint=f"{settings.gcp_document_ai_location}-documentai.googleapis.com"
        )
        _docai_client = documentai.DocumentProcessorServiceClient(client_options=opts)
    return _docai_client


def _processor_name() -> str:
    return (
        f"projects/{settings.gcp_project_id}"
        f"/locations/{settings.gcp_document_ai_location}"
        f"/processors/{settings.gcp_document_ai_processor_id}"
    )


MAX_PAGES_PER_CALL = 15  # Document AI sync process_document limit (non-imageless mode)


def _split_pdf_bytes(file_bytes: bytes, max_pages: int) -> list[bytes]:
    """Splits a PDF into <=max_pages chunks. Single-chunk PDFs still go
    through this path for a uniform call shape — pypdf overhead is negligible.
    """
    from io import BytesIO
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(BytesIO(file_bytes))
    total_pages = len(reader.pages)

    chunks = []
    for start in range(0, total_pages, max_pages):
        writer = PdfWriter()
        for page in reader.pages[start:start + max_pages]:
            writer.add_page(page)
        buf = BytesIO()
        writer.write(buf)
        chunks.append(buf.getvalue())

    return chunks


def extract_layout(file_bytes: bytes, mime_type: str = "application/pdf") -> dict:
    """
    Splits input into <=MAX_PAGES_PER_CALL chunks (Document AI sync page cap —
    see PAGE_LIMIT_EXCEEDED), calls Document AI once per chunk, and merges
    paragraphs in order with page_number/para_sequence renumbered across the
    whole document. SA petitions routinely exceed 15 pages, so single-shot
    extract_one_chunk() below is not called directly by pipeline code.
    """
    chunks = _split_pdf_bytes(file_bytes, MAX_PAGES_PER_CALL)

    all_paragraphs = []
    total_pages = 0
    seq = 0
    for chunk_bytes in chunks:
        result = extract_one_chunk(chunk_bytes, mime_type)
        for para in result["paragraphs"]:
            para["page_number"] += total_pages
            para["para_sequence"] = seq
            all_paragraphs.append(para)
            seq += 1
        total_pages += result["page_count"]

    return {
        "paragraphs": all_paragraphs,
        "page_count": total_pages,
    }


def extract_one_chunk(file_bytes: bytes, mime_type: str = "application/pdf") -> dict:
    """
    Layout extraction using Google Document AI (processor must be a
    Document OCR / Layout Parser processor — not the plain "read" OCR
    processor — so paragraph-level structure is returned).

    Returns paragraphs at semantic-paragraph granularity, not raw text lines.
    """
    try:
        client = get_ocr_client()
        raw_document = documentai.RawDocument(content=file_bytes, mime_type=mime_type)
        request = documentai.ProcessRequest(name=_processor_name(), raw_document=raw_document)
        # retry=None — a dead/expired ADC refresh token is not transient and
        # otherwise retries under gapic's default retry policy for minutes
        # before surfacing; fail fast so the pypdf fallback below can run.
        result = client.process_document(request=request, retry=None, timeout=30.0)
        document = result.document
    except (GoogleAPICallError, GoogleAuthError) as exc:
        # ponytail: Document AI unreachable (billing/quota/auth, incl. expired
        # ADC refresh token) — local pypdf text-layer fallback so the pipeline
        # still runs on born-digital PDFs. Scanned/image-only PDFs still need
        # real Document AI OCR.
        logger.warning(
            "DOCAI_FALLBACK_TRIGGERED: Document AI call failed (%s) — "
            "using local pypdf text-layer extraction instead. "
            "Extracted text will have no bbox/confidence and scanned/image-only "
            "PDFs will yield empty output.",
            exc,
        )
        return _extract_local(file_bytes)

    # Layout Parser processors return document.document_layout.blocks, not the
    # legacy document.pages[].paragraphs — no bounding_poly/confidence on
    # document.pages for this processor type, so we read blocks directly.
    paragraphs = []
    seq = 0
    page_count = 0
    for block in document.document_layout.blocks:
        text = block.text_block.text
        if not text.strip():
            continue
        # DocumentLayoutBlock has no bounding_box field (layout parser blocks
        # carry text_block/table_block/list_block/block_id/page_span only) —
        # bbox is unavailable at this granularity, same as the pypdf fallback.
        page_count = max(page_count, block.page_span.page_end)
        paragraphs.append({
            "page_number":    block.page_span.page_start,
            "para_sequence":  seq,
            "text":           text,
            "bbox":           None,
            "ocr_confidence": None,
            "role":           None,
        })
        seq += 1

    return {
        "paragraphs": paragraphs,
        "page_count": page_count,
    }


def _extract_local(file_bytes: bytes) -> dict:
    """pypdf text-layer extraction, paragraph-split on blank lines. No bbox/confidence."""
    from io import BytesIO
    from pypdf import PdfReader

    reader = PdfReader(BytesIO(file_bytes))
    paragraphs = []
    seq = 0
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for block in text.split("\n\n"):
            block = block.strip()
            if not block:
                continue
            paragraphs.append({
                "page_number":    page_num,
                "para_sequence":  seq,
                "text":           block,
                "bbox":           None,
                "ocr_confidence": None,
                "role":           None,
            })
            seq += 1

    return {"paragraphs": paragraphs, "page_count": len(reader.pages)}
