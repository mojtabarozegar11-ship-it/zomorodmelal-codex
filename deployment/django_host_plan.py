from __future__ import annotations

import os
import shlex
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class DjangoHostPlan:
    """Describe, without executing, the approved Django production sequence."""
    backup_command: str
    migrate_command: str
    health_command: str
    restart_command: str
    rollback_command: str


class DjangoHostPlanner:
    """Build a host-specific plan from explicit environment configuration."""

    def __init__(self) -> None:
        self.manage = os.environ.get("MASTER_AGENT_DJANGO_MANAGE", "python manage.py")
        self.health_url = os.environ.get("MASTER_AGENT_HEALTH_URL", "https://zomorodmelal.ir/")
        self.restart_command = os.environ.get("MASTER_AGENT_RESTART_COMMAND", "")
        self.backup_command = os.environ.get("MASTER_AGENT_BACKUP_COMMAND", "")
        self.rollback_command = os.environ.get("MASTER_AGENT_ROLLBACK_COMMAND", "")

    @staticmethod
    def _safe_words(value: str) -> List[str]:
        words = shlex.split(value)
        if not words or any(x in {"&&", "||", ";", "|", ">", ">>", "<"} for x in words):
            raise ValueError("host command must be a simple argv list")
        return words

    def plan(self) -> DjangoHostPlan:
        self._safe_words(self.manage)
        if not self.health_url.startswith(("https://", "http://")):
            raise ValueError("health URL must use HTTP(S)")
        if self.restart_command:
            self._safe_words(self.restart_command)
        if self.backup_command:
            self._safe_words(self.backup_command)
        if self.rollback_command:
            self._safe_words(self.rollback_command)
        return DjangoHostPlan(
            backup_command=self.backup_command,
            migrate_command=self.manage + " migrate --noinput",
            health_command="python -c " + repr("import urllib.request; urllib.request.urlopen(" + repr(self.health_url) + ", timeout=15).read(1)"),
            restart_command=self.restart_command,
            rollback_command=self.rollback_command,
        )

    def status(self) -> Dict[str, object]:
        return {
            "django_manage_configured": bool(self.manage),
            "health_url": self.health_url,
            "backup_configured": bool(self.backup_command),
            "restart_configured": bool(self.restart_command),
            "rollback_configured": bool(self.rollback_command),
            "owner_approval_required": True,
            "real_world_changes": False,
        }
