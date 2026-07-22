FROM python:3.11-slim

# System deps for WeasyPrint (PDF rendering) and build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    libcairo2 \
    fonts-liberation \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Hindi script (Devanagari) support for WeasyPrint PDF rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-noto-core \
    fonts-noto-extra \
    && fc-cache -fv \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir torch==2.3.1+cpu --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download IndicTrans2 model (~400MB) — prevents cold-start timeout in worker
# Reference: Gala et al., "IndicTrans2", TMLR 2023 (arXiv:2305.16307)
RUN --mount=type=secret,id=hf_token \
    export HF_TOKEN=$(cat /run/secrets/hf_token) && python -c "\
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer; \
name = 'ai4bharat/indictrans2-indic-en-dist-200M'; \
AutoTokenizer.from_pretrained(name, trust_remote_code=True); \
AutoModelForSeq2SeqLM.from_pretrained(name, trust_remote_code=True); \
print('IndicTrans2 pre-downloaded OK')"

# Pre-download InLegalBERT embedding model (~440MB) — prevents cold-start in Chain B
# Reference: Paul et al., "Pre-trained LMs for Indian Law", ICAIL 2023 (arXiv:2209.06049)
RUN python -c "\
from sentence_transformers import SentenceTransformer; \
SentenceTransformer('law-ai/InLegalBERT'); \
print('InLegalBERT pre-downloaded OK')"

# Run as non-root for security
RUN useradd -m appuser

# Copy application code, ownership set on-the-fly (avoids slow recursive chown)
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000
