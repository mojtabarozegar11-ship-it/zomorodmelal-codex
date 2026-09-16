"""Integration helper between supervisor runtime and Telegram bot manager."""

from autonomous_core.telegram_bot_manager import TelegramBotManager


class SupervisorTelegramIntegration:
    def __init__(self, project_root):
        self.bot_manager = TelegramBotManager(project_root)

    def ensure_bot(self):
        return self.bot_manager.ensure_running()

    def status(self):
        return self.bot_manager.status()
