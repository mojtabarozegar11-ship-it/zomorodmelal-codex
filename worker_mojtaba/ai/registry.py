"""Registry connecting configured AI capabilities to provider adapters."""
from __future__ import annotations

from worker_mojtaba.ai.adapter import AIProviderAdapter, UnconfiguredProvider
from worker_mojtaba.ai.router import AIRouter


class AIProviderRegistry:
    def __init__(self, router: AIRouter | None = None) -> None:
        self.router = router or AIRouter()
        self.adapters: dict[str, AIProviderAdapter] = {}
        self.fallback = UnconfiguredProvider()

    def register(
        self,
        adapter: AIProviderAdapter,
        capabilities: list[str],
        *,
        priority: int = 100,
    ) -> None:
        self.adapters[adapter.name] = adapter
        self.router.register(adapter.name, capabilities, priority=priority)

    def generate(self, request: str, capability: str) -> dict:
        provider = self.router.choose(capability)
        if provider is None:
            return self.fallback.generate(request, capability=capability)
        adapter = self.adapters.get(provider.name)
        if adapter is None:
            return self.fallback.generate(request, capability=capability)
        return adapter.generate(request, capability=capability)
