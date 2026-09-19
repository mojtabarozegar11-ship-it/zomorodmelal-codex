"""Tool Center for capability adapters.

Adapters are explicitly registered by the application; unknown capabilities
never fall through to arbitrary execution.
"""
from __future__ import annotations

from typing import Any

from worker_mojtaba.tools.adapter import ToolAdapter


class ToolCenter:
    def __init__(self) -> None:
        self._adapters: dict[str, ToolAdapter] = {}

    def register(self, adapter: ToolAdapter) -> None:
        self._adapters[adapter.name] = adapter

    def list_capabilities(self) -> dict[str, list[str]]:
        return {
            name: adapter.capabilities()
            for name, adapter in self._adapters.items()
        }

    def execute(
        self, adapter_name: str, capability: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        adapter = self._adapters.get(adapter_name)
        if adapter is None:
            raise KeyError(f"Unknown tool adapter: {adapter_name}")
        if capability not in adapter.capabilities():
            raise ValueError(f"Unsupported capability: {capability}")
        return adapter.execute(capability, payload)
