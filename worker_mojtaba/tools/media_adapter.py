"""Deterministic media tool adapter boundary."""
from __future__ import annotations

from typing import Any

from worker_mojtaba.tools.adapter import ToolAdapter
from worker_mojtaba.tools.media import MediaCapability


class MediaToolAdapter(ToolAdapter):
    name = "media"

    def __init__(self) -> None:
        self._capabilities = MediaCapability()

    def capabilities(self) -> list[str]:
        return self._capabilities.describe()

    def execute(self, capability: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not self._capabilities.supports(capability):
            raise ValueError(f"Unsupported media capability: {capability}")
        return {
            "status": "provider_required",
            "adapter": self.name,
            "capability": capability,
            "request": payload,
            "message": "Configure an authorized media provider before generation.",
        }
