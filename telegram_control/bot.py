import os


class TelegramBotController:
    """Telegram gateway for Master Agent.

    Handles messages and approval callbacks.
    Real Telegram API wiring can be attached without exposing secrets.
    """

    def __init__(self, router=None, approval_gateway=None, executor=None):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.router = router
        self.approval_gateway = approval_gateway
        self.executor = executor

    def handle_message(self, user_id, message):
        if self.router:
            return self.router.route(message, user_id)
        return {"status": "received", "message": message}

    def handle_callback(self, user_id, callback_data):
        """Handle inline keyboard callbacks.

        Expected formats:
        approve:<action_id>
        reject:<action_id>
        """
        if not self.approval_gateway:
            return {"status": "approval_gateway_missing"}

        action, _, action_id = callback_data.partition(":")

        if action == "approve":
            result = self.approval_gateway.approve(action_id)
            if result.get("status") == "approved" and self.executor:
                execution = self.executor.execute(result.get("action"))
                return {
                    "status": "executed",
                    "result": execution,
                }
            return result

        if action == "reject":
            return self.approval_gateway.reject(action_id)

        return {"status": "unknown_callback", "data": callback_data}

    def send_message(self, user_id, text):
        return {"user_id": user_id, "text": text}
