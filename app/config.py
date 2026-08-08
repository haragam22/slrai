from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str

    # Redis
    redis_url: str
    celery_broker_url: str
    celery_result_backend: str

    # Object storage — MinIO only (self-hosted, dev and prod)
    s3_endpoint_url: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket_name: str

    # OCR — Google Cloud Document AI
    gcp_project_id: str = ""
    gcp_document_ai_location: str = "us"
    gcp_document_ai_processor_id: str = ""

    # Claude API — via GCP Vertex AI (AnthropicVertex client, uses ADC)
    gcp_vertex_region: str = "global"
    claude_model: str = "claude-sonnet-5"
    llm_temperature: float = 0.0    # always 0 — deterministic extraction

    # LLM provider switch — "claude" (default, Vertex) or "gemini" (pipeline
    # smoke test). See app/services/llm_client.py.
    llm_provider: str = "claude"
    gemini_model: str = "gemini-2.5-flash"
    # Gemini via Vertex AI (billed GCP project, ADC auth — same
    # GOOGLE_APPLICATION_CREDENTIALS as Document AI, no separate API key).
    # Falls back to gcp_project_id if unset.
    gemini_vertex_project: str = ""
    gemini_vertex_location: str = "us-central1"
    # Safety-margin caps — Vertex quota is per-project/region, not a hard 0
    # like the unlinked AI Studio free tier, but still worth throttling.
    gemini_rpm_limit: int = 12
    gemini_rpd_limit: int = 500

    # Qdrant
    qdrant_url: str
    qdrant_judgments_collection: str = "sarfaesi_judgments"

    ik_api_token: str = ""

    # OpenRouter — used only by scripts/summarize_judgments.py (offline
    # judgment-corpus ingestion), not the case pipeline (that's Bedrock above)
    openrouter_api_key: str = ""
    openrouter_model: str = "deepseek/deepseek-chat"
    # Stage 2 (LOCK — pure JSON reformat of stage 1's already-reasoned answer,
    # no new legal reasoning) doesn't need a thinking model. Measured: running
    # it on the same thinking model as stage 1 burned ~100s/file on a hidden
    # reasoning trace for a task that's supposed to do zero reasoning, and
    # that model's schema compliance was also flaky. Defaults to the same
    # non-thinking model as openrouter_model unless overridden.
    openrouter_lock_model: str = "qwen/qwen3-235b-a22b-2507"

    # Statutory wikis (injected into Claude extraction / applicability context)
    sarfaesi_law_wiki_path: str = "docs/wiki/sarfaesi_law_wiki.md"
    third_party_wiki_path: str = "docs/wiki/third_party_law_wiki.md"
    # Judgment corpus is loaded live from docs/judgments/*.md (see
    # applicability.py) — no compiled wiki cache file anymore.

    # Auth
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 480   # 8 hours

    # X-Forwarded-For is only honored when the direct TCP peer is one of these
    # IPs (the reverse proxy) — otherwise a client could spoof the audit-log IP.
    trusted_proxy_ips: set[str] = {"127.0.0.1", "::1"}

    # Translation — IndicTrans2 (Gala et al., TMLR 2023, arXiv:2305.16307)
    translation_model: str = "ai4bharat/indictrans2-hi-en-dist-200M"
    translation_device: str = "cpu"

    # Embeddings — law-ai/InLegalBERT (Paul et al., ICAIL 2023, arXiv:2209.06049)
    embedding_model: str = "law-ai/InLegalBERT"

    # Reports
    report_template_dir: str = "app/reports/templates"


settings = Settings()
