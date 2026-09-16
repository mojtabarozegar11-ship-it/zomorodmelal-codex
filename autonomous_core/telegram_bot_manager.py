"""Manage Telegram bot runtime from the autonomous supervisor."""

import subprocess
import sys
from pathlib import Path


class TelegramBotManager:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.bot_file = self.project_root / "main.py"
        self.process = None

    def is_running(self):
        return self.process is not None and self.process.poll() is None

    def start(self):
        if self.is_running():
            return {"status": "running"}

        if not self.bot_file.exists():
            return {"status": "error", "message": "main.py not found"}

        self.process = subprocess.Popen(
            [sys.executable, str(self.bot_file)],
            cwd=str(self.project_root)
        )
        return {"status": "started", "pid": self.process.pid}

    def stop(self):
        if self.is_running():
            self.process.terminate()
        return {"status": "stopped"}
