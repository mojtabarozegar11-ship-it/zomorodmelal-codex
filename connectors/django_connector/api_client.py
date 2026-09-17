"""Django connector for Master Agent.

This module provides a small interface layer for a future Django website
integration.
"""

from datetime import datetime


class DjangoConnector:
    def __init__(self, agent):
        self.agent = agent

    def send_task(self, task, source="website"):
        return {
            "source": source,
            "task": task,
            "status": "received",
            "created_at": datetime.utcnow().isoformat()
        }

    def get_status(self):
        return self.agent.status() if self.agent else {"status": "unknown"}
