"""Tool Center adapter for safe document metadata workflows."""
from __future__ import annotations

from typing import Any

from worker_mojtaba.tools.adapter import ToolAdapter


class DocumentToolAdapter(ToolAdapter):
    name = "documents"

    def capabilities(self) -> list[str]:
        return ["document_status", "document_metadata"]

    def execute(self, capability: str, payload: dict[str, Any]) -> dict[str, Any]:
        if capability == "document_status":
            return {
                "status": "document_bridge_required",
                "adapter": self.name,
                "message": "Connect an authorized Android/file bridge before accessing documents.",
            }
        if capability == "document_metadata":
            name = str(payload.get("name", "")).strip()
            return {
                "status": "metadata_planned",
                "name": name,
                "metadata": {},
            }
        raise ValueError(f"Unsupported document capability: {capability}")
