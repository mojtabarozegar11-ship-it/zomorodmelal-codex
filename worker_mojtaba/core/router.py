"""Capability router with explicit capability aliases."""
from __future__ import annotations


class Router:
    _aliases = {
        "general": "echo",
        "media_generation": "media",
        "task_automation": "automation",
        "document_management": "documents",
        "research": "research",
        "camera": "android",
        "audio": "android",
        "wallet": "finance",
        "social_publishing": "social",
        "communications": "communications",
        "calendar": "automation",
    }

    def route(self, intent: str, available_tools: list[str]) -> str:
        candidate = self._aliases.get(intent, intent)
        return candidate if candidate in available_tools else "text_model"
