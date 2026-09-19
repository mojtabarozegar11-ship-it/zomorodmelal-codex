"""Tool Center adapter for authorized WhatsApp/email/SMS providers."""
from typing import Any
from worker_mojtaba.communications.messaging import MessagingManager
from worker_mojtaba.tools.adapter import ToolAdapter

class CommunicationsToolAdapter(ToolAdapter):
    name = "communications"
    def __init__(self) -> None:
        self.messaging = MessagingManager()
    def capabilities(self) -> list[str]:
        return ["send_whatsapp", "send_email", "send_sms"]
    def execute(self, capability: str, payload: dict[str, Any]) -> dict[str, Any]:
        provider = {"send_whatsapp":"whatsapp","send_email":"email","send_sms":"sms"}[capability]
        return self.messaging.send(provider, str(payload.get("recipient","")), str(payload.get("message","")))
