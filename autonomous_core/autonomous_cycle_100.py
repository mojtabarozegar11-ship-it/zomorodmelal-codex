from __future__ import annotations

from pathlib import Path

from .autonomous_cycle import AutonomousCycle
from .master_core_generation_41_100 import MasterAgent100


class AutonomousCycle100(AutonomousCycle):
    """Runtime adapter that makes Master Agent 100 the cycle's control core."""

    MASTER_VERSION = "100.0.0"

    def __init__(self, project_root: str | Path | None = None) -> None:
        super().__init__(project_root)
        self.master = MasterAgent100(self.project_root)

    def runtime_status(self):
        return {
            "master_version": self.master.VERSION,
            "max_generation": self.master.MAX_GENERATION,
            "operating_snapshot": self.master.operating_snapshot(),
            "safety": dict(self.master.SAFETY_POLICY),
        }
