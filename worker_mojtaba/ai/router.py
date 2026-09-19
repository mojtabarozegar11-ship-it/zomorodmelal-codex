"""AI provider routing with health, priority and cost metadata."""
from dataclasses import dataclass, field

@dataclass
class Provider:
    name: str
    capabilities: set[str]
    enabled: bool = True
    priority: int = 100
    metadata: dict[str, str] = field(default_factory=dict)

class AIRouter:
    def __init__(self) -> None:
        self.providers: list[Provider] = []

    def register(
        self,
        name: str,
        capabilities: list[str],
        *,
        priority: int = 100,
        metadata: dict[str, str] | None = None,
    ) -> None:
        self.providers.append(
            Provider(name, set(capabilities), True, priority, metadata or {})
        )
        self.providers.sort(key=lambda provider: provider.priority)

    def set_enabled(self, name: str, enabled: bool) -> None:
        for provider in self.providers:
            if provider.name == name:
                provider.enabled = enabled

    def choose(self, capability: str) -> Provider | None:
        for provider in self.providers:
            if provider.enabled and capability in provider.capabilities:
                return provider
        return None

    def list_enabled(self) -> list[Provider]:
        return [provider for provider in self.providers if provider.enabled]
