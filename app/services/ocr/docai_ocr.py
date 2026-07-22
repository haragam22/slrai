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
        result = client.process_document(request=request)
        document = result.document
    except GoogleAPICallError as exc:
        # ponytail: Document AI unreachable (billing/quota/auth) — local pypdf
        # text-layer fallback so the pipeline still runs on born-digital PDFs.
        # Scanned/image-only PDFs still need real Document AI OCR.
        logger.warning(
            "DOCAI_FALLBACK_TRIGGERED: Document AI call failed (%s) — "
            "using local pypdf text-layer extraction instead. "
            "Extracted text will have no bbox/confidence and scanned/image-only "
            "PDFs will yield empty output.",
            exc,
        )
        return _extract_local(file_bytes)

    full_text = document.text
    paragraphs = []
    seq = 0
    for page in document.pages:
        page_num = page.page_number
        for para in page.paragraphs:
            text = _layout_text(full_text, para.layout)
            if not text.strip():
                continue
            bbox = _bbox_from_layout(para.layout)
            confidence = para.layout.confidence if para.layout else None
            paragraphs.append({
                "page_number":    page_num,
                "para_sequence":  seq,
                "text":           text,
                "bbox":           bbox,
                "ocr_confidence": confidence,
                "role":           None,
            })
            seq += 1

    return {
        "paragraphs": paragraphs,
        "page_count": len(document.pages),
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


def _layout_text(full_text: str, layout: "documentai.Document.Page.Layout") -> str:
    if not layout or not layout.text_anchor or not layout.text_anchor.text_segments:
        return ""
    parts = []
    for seg in layout.text_anchor.text_segments:
        start = int(seg.start_index) if seg.start_index else 0
        end = int(seg.end_index)
        parts.append(full_text[start:end])
    return "".join(parts)


def _bbox_from_layout(layout: "documentai.Document.Page.Layout") -> dict | None:
    if not layout or not layout.bounding_poly or not layout.bounding_poly.normalized_vertices:
        return None
    verts = layout.bounding_poly.normalized_vertices
    if len(verts) < 3:
        return None
    return {
        "x1": verts[0].x, "y1": verts[0].y,
        "x2": verts[2].x, "y2": verts[2].y,
    }
