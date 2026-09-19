"""Messaging provider boundary for WhatsApp/email/SMS."""
class MessagingManager:
    providers = ("whatsapp", "email", "sms")
    def send(self, provider: str, recipient: str, message: str) -> dict:
        if provider not in self.providers:
            raise ValueError("Unsupported messaging provider")
        return {"status": "provider_connection_required", "provider": provider, "recipient": recipient}
