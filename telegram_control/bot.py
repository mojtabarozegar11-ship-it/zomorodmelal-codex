import os


class TelegramBotController:
    """Telegram gateway for Master Agent.

    Real Telegram API wiring can be attached here without exposing secrets.
    """

    def __init__(self, router=None):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.router = router

    def handle_message(self, user_id, message):
        if self.router:
            return self.router.route(message, user_id)
        return {"status": "received", "message": message}

    def send_message(self, user_id, text):
        return {"user_id": user_id, "text": text}
