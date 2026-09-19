import os

from worker_mojtaba.ai.http_provider import HTTPJSONProvider


def test_http_provider_requires_secret(monkeypatch):
    monkeypatch.delenv("WORKER_TEST_API_KEY", raising=False)
    provider = HTTPJSONProvider(
        "test",
        "https://example.invalid/ai",
        "WORKER_TEST_API_KEY",
    )
    result = provider.generate("hello", capability="text_model")
    assert result["status"] == "provider_auth_required"
    assert "api_key" not in result
