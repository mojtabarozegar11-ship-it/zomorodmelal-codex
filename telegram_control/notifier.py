class TelegramNotifier:
    def notify(self, user_id, message):
        return {
            "target": user_id,
            "message": message,
            "status": "queued"
        }
