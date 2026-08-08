"""Shared LLM client — Claude via GCP Vertex AI, or Gemini for a one-off
pipeline smoke test (set LLM_PROVIDER=gemini). Gemini path also goes through
Vertex AI (ADC auth, billed GCP project) — not the AI Studio API-key path,
which has a hard 0 free-tier quota on unlinked projects."""
from anthropic import APITimeoutError, RateLimitError, AuthenticationError  # noqa: F401

from app.config import settings

if settings.llm_provider == "gemini":
    from google import genai as _genai
    from app.services.gemini_rate_limiter import GeminiRateLimiter

    _gemini_client = _genai.Client(
        vertexai=True,
        project=settings.gemini_vertex_project or settings.gcp_project_id,
        location=settings.gemini_vertex_location,
    )
    _limiter = GeminiRateLimiter(settings.gemini_rpm_limit, settings.gemini_rpd_limit)

    class _TextPart:
        def __init__(self, text: str):
            self.text = text

    class _GeminiResponse:
        def __init__(self, text: str):
            self.content = [_TextPart(text)]

    def _flatten_system(system) -> str:
        """Claude callers pass system as either a plain string or a list of
        content blocks (for prompt caching, e.g. [{"type": "text", "text":
        ..., "cache_control": ...}]) — Gemini's system_instruction wants a
        single string either way."""
        if isinstance(system, str):
            return system
        return "\n\n".join(block["text"] for block in system if "text" in block)

    class _GeminiMessages:
        @staticmethod
        def create(model: str, max_tokens: int, temperature: float, system: str,
                    messages: list[dict]) -> _GeminiResponse:
            """Translates google-genai's own exceptions into the anthropic
            exception types re-exported above — nlp_layer.py and
            applicability.py both write `except llm_client.RateLimitError`
            etc, which only ever matched anthropic.RateLimitError regardless
            of which provider was actually active. When LLM_PROVIDER=gemini,
            every real Gemini error (429 rate limit, 401/403 auth, network
            timeout) fell straight through every except clause into the
            generic `except Exception: return [None]*count` — no Celery
            retry (autoretry_for=(anthropic.RateLimitError,) never matched),
            no case FAILED on auth errors, no retry loop in extract_facts_batch
            either (the generic handler returns immediately, doesn't loop).
            A single transient Gemini hiccup silently killed that whole batch
            permanently and looked identical to "extraction found nothing
            here" in every downstream consumer. This was live in production
            (LLM_PROVIDER=gemini is what actually generated the report this
            whole debugging session started from) — not a theoretical gap."""
            import httpx
            import google.genai.errors as genai_errors
            import requests

            # anthropic's exception constructors require real httpx
            # Request/Response objects (APIStatusError.__init__ does
            # response.request, response.status_code — passing None crashes
            # with a confusing AttributeError instead of raising the
            # intended exception). Build the minimum valid stand-ins.
            _dummy_request = httpx.Request("POST", "https://gemini.invalid/")

            def _dummy_response(status_code: int) -> httpx.Response:
                return httpx.Response(status_code, request=_dummy_request)

            _limiter.before_call()
            prompt = messages[0]["content"]
            try:
                resp = _gemini_client.models.generate_content(
                    model=settings.gemini_model,
                    contents=prompt,
                    config={
                        "system_instruction": _flatten_system(system),
                        "temperature": temperature,
                        "max_output_tokens": max_tokens,
                    },
                )
            except genai_errors.APIError as exc:
                if exc.code == 429:
                    raise RateLimitError(str(exc), response=_dummy_response(429), body=None) from exc
                if exc.code in (401, 403):
                    raise AuthenticationError(str(exc), response=_dummy_response(exc.code), body=None) from exc
                if exc.code in (408, 504):
                    raise APITimeoutError(_dummy_request) from exc
                raise  # 5xx server errors etc — let the generic handler catch and log these
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
                raise APITimeoutError(_dummy_request) from exc
            return _GeminiResponse(resp.text)

    class _GeminiClient:
        messages = _GeminiMessages()

    client = _GeminiClient()
    MODEL = settings.gemini_model
else:
    from anthropic import AnthropicVertex

    client = AnthropicVertex(
        project_id=settings.gcp_project_id,
        region=settings.gcp_vertex_region,
    )
    MODEL = settings.claude_model
