"""Adapter interface for external tools and services."""
from abc import ABC, abstractmethod
from typing import Any

class ToolAdapter(ABC):
    name = "abstract"

    @abstractmethod
    def capabilities(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def execute(self, capability: str, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError
