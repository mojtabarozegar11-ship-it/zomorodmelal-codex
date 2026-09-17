"""
Runtime Configuration Manager
Master Agent Auto Execution Layer
"""

import os


class ConfigManager:
    def __init__(self):
        self.environment = os.getenv("AGENT_ENV", "development")
        self.owner_approval_required = True
        self.runtime_enabled = os.getenv("RUNTIME_ENABLED", "true").lower() == "true"

    def get(self, key, default=None):
        return os.getenv(key, default)

    def status(self):
        return {
            "environment": self.environment,
            "runtime_enabled": self.runtime_enabled,
            "owner_approval_required": self.owner_approval_required,
        }
