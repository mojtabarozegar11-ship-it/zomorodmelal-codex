from worker_mojtaba.ai.adapter import AIProviderAdapter
from worker_mojtaba.ai.registry import AIProviderRegistry


class FakeProvider(AIProviderAdapter):
    name = "fake"

    def generate(self, request: str, *, capability: str) -> dict:
        return {"status": "ok", "request": request, "capability": capability}


def test_registry_routes_to_registered_provider():
    registry = AIProviderRegistry()
    registry.register(FakeProvider(), ["text"], priority=1)
    result = registry.generate("hello", "text")
    assert result["status"] == "ok"


def test_registry_has_safe_unconfigured_fallback():
    registry = AIProviderRegistry()
    result = registry.generate("hello", "text")
    assert result["status"] == "provider_configuration_required"
