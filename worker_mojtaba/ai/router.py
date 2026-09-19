"""Provider-agnostic AI model router."""
from dataclasses import dataclass

@dataclass
class Provider:
    name: str
    capabilities: set[str]
    enabled: bool = True

class AIRouter:
    def __init__(self) -> None:
        self.providers: list[Provider] = []

    def register(self, name: str, capabilities: list[str]) -> None:
        self.providers.append(Provider(name, set(capabilities)))

    def choose(self, capability: str) -> Provider | None:
        for provider in self.providers:
            if provider.enabled and capability in provider.capabilities:
                return provider
        return None
