"""Tool Center adapters for Android capabilities."""
from __future__ import annotations

from typing import Any

from worker_mojtaba.device.capability_registry import DeviceCapabilityRegistry
from worker_mojtaba.tools.adapter import ToolAdapter


class AndroidToolAdapter(ToolAdapter):
    name = "android"

    def __init__(self) -> None:
        self.registry = DeviceCapabilityRegistry()

    def capabilities(self) -> list[str]:
        return self.registry.list()

    def execute(self, capability: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.registry.supports(capability):
            raise ValueError(f"Unsupported Android capability: {capability}")
        return {
            "status": "device_permission_required",
            "adapter": self.name,
            "capability": capability,
            "request": payload,
            "message": "Android-side permission and bridge must be configured before execution.",
        }
