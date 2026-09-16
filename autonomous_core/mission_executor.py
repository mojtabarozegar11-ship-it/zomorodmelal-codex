from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Union

from autonomous_core.mission_queue import MissionQueue


class MissionExecutor:
    """Execute only bounded, sandbox-safe follow-up missions."""

    MAX_REPAIR_ATTEMPTS = 3

    def __init__(self, root: Union[str, Path]) -> None:
        self.root = Path(root).resolve()
        self.queue = MissionQueue(self.root)
        self.state_path = self.root / "data" / "mission_executor.json"
        self.state_path.parent.mkdir(parents=True, exist_ok=True)

    def _save(self, value: Dict[str, Any]) -> None:
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.state_path)

    def execute_next(self) -> Dict[str, Any]:
        mission = self.queue.peek()
        if not mission:
            result = {"status": "idle", "mission": None, "owner_approval_required": True,
                      "real_world_changes": False, "sandbox_only": True}
            self._save(result)
            return result

        mission_id = str(mission.get("id"))
        mission_type = str(mission.get("type", "improvement"))
        attempt = int(mission.get("attempt", 0) or 0) + 1
        if mission_type == "self_repair":
            if attempt > self.MAX_REPAIR_ATTEMPTS:
                mission["status"] = "quarantined"
                self.queue.enqueue(mission)
                result = {"status": "quarantined", "mission": mission_id, "attempt": attempt - 1,
                          "owner_approval_required": True, "real_world_changes": False, "sandbox_only": True}
                self._save(result)
                return result
            command = [sys.executable, "-m", "unittest", "tests.test_master_core", "tests.test_autonomous_cycle_goal"]
            try:
                completed = subprocess.run(command, cwd=self.root, capture_output=True, text=True,
                                            timeout=8, shell=False)
                passed = completed.returncode == 0
                status = "verified" if passed else "retry_pending"
                if passed:
                    self.queue.complete(mission_id)
                else:
                    mission["attempt"] = attempt
                    mission["status"] = status
                    self.queue.enqueue(mission)
                result = {"status": status, "mission": mission_id, "attempt": attempt,
                          "tests_passed": passed, "returncode": completed.returncode,
                          "stdout": completed.stdout[-4000:], "stderr": completed.stderr[-4000:],
                          "owner_approval_required": True, "real_world_changes": False, "sandbox_only": True}
            except subprocess.TimeoutExpired as exc:
                mission["attempt"] = attempt
                mission["status"] = "retry_pending"
                self.queue.enqueue(mission)
                result = {"status": "retry_pending", "mission": mission_id, "attempt": attempt,
                          "tests_passed": False, "failure_kind": "timeout", "stderr": str(exc),
                          "owner_approval_required": True, "real_world_changes": False, "sandbox_only": True}
        else:
            self.queue.complete(mission_id)
            result = {"status": "completed", "mission": mission_id, "attempt": attempt,
                      "owner_approval_required": True, "real_world_changes": False, "sandbox_only": True}
        result["timestamp"] = datetime.now(timezone.utc).isoformat()
        self._save(result)
        return result
