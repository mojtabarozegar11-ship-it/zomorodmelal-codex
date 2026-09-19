"""Deterministic intent and capability selection for the worker."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Intent:
    name: str
    capability: str

class IntentParser:
    _rules = (
        (("انتشار", "یوتیوب", "youtube", "شبکه اجتماعی", "social"), "social_publishing", "publish_video"),
        (("واتساپ", "whatsapp"), "communications", "send_whatsapp"),
        (("ایمیل", "email"), "communications", "send_email"),
        (("پیامک", "sms"), "communications", "send_sms"),
        (("فهرست رویدادهای تقویم", "لیست رویدادهای تقویم", "calendar events"), "calendar", "list_calendar_events"),\n        (("تقویم شمسی", "تقویم قمری", "تقویم میلادی", "مناسبت"), "calendar", "calendar_event"),
        (("زمان‌بندی انتشار", "زمان بندی انتشار", "schedule video"), "social_publishing", "schedule_video"),
        (("کانال", "channels"), "social_publishing", "list_channels"),
        (("ویدئو", "ویدیو", "video", "mp4"), "media_generation", "text_to_video"),
        (("یادآوری", "reminder"), "task_automation", "schedule_task"),
        (("کیف پول", "wallet", "موجودی"), "wallet", "account_balance"),
        (("تراکنش", "transaction"), "wallet", "transactions"),
        (("درآمد", "تقسیم درآمد", "allocate revenue"), "wallet", "allocate_revenue"),
        (("تحقیق", "پژوهش", "مطالعه"), "research", "research"),
        (("فایل", "سند", "document"), "document_management", "document_status"),
        (("متادیتای فایل", "document metadata"), "document_management", "document_metadata"),
        (("دوربین", "camera"), "camera", "camera"),
        (("صدا", "میکروفون", "microphone"), "audio", "microphone"),
    )
    def parse(self, request: str) -> Intent:
        text = request.strip().lower()
        for keywords, name, capability in self._rules:
            if any(k in text for k in keywords):
                return Intent(name, capability)
        return Intent("general", "echo")
