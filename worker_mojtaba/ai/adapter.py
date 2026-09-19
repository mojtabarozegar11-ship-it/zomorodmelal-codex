"""Provider adapter interfaces with secret-safe request handling."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class AIProviderAdapter(ABC):
    name: str

    @abstractmethod
    def generate(self, request: str, *, capability: str) -> dict[str, Any]:
        raise NotImplementedError


class UnconfiguredProvider(AIProviderAdapter):
    """Explicit fallback until the owner configures a real provider."""

    name = "unconfigured"

    def generate(self, request: str, *, capability: str) -> dict[str, Any]:
        return {
            "status": "provider_configuration_required",
            "capability": capability,
            "request": request,
        }
