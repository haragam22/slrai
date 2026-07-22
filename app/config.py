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

    # Claude API
    anthropic_api_key: str
    claude_model: str = "claude-sonnet-4-6"
    llm_max_tokens: int = 1000
    llm_temperature: float = 0.0    # always 0 — deterministic extraction

    # Qdrant
    qdrant_url: str
    qdrant_judgments_collection: str = "sarfaesi_judgments"

    ik_api_token: str = ""

    # Statutory wikis (injected into Claude extraction / applicability context)
    sarfaesi_law_wiki_path: str = "docs/wiki/sarfaesi_law_wiki.md"
    third_party_wiki_path: str = "docs/wiki/third_party_law_wiki.md"
    class_a_judgments_wiki_path: str = "docs/wiki/class_a_judgments_wiki.md"

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
