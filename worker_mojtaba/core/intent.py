"""Deterministic intent and capability selection for the worker."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Intent:
    name: str
    capability: str

class IntentParser:
    _rules = (
        (("ویدئو", "ویدیو", "video", "mp4"), "media_generation"),
        (("یادآوری", "reminder", "یادداشت"), "task_automation"),
        (("کیف پول", "wallet", "درآمد", "تراکنش"), "wallet"),
        (("تحقیق", "پژوهش", "مطالعه"), "research"),
        (("فایل", "سند", "document"), "document_management"),
        (("دوربین", "camera"), "camera"),
        (("صدا", "میکروفون", "microphone"), "audio"),
    )
    def parse(self, request: str) -> Intent:
        text = request.strip().lower()
        for keywords, capability in self._rules:
            if any(k in text for k in keywords):
                return Intent(capability, capability)
        return Intent("general", "echo")
