from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from autonomous_core.agent_orchestrator import AgentOrchestrator


class MasterBrainController:
    """Autonomous mission coordinator; real-world actions remain approval-gated."""

    def __init__(self, root: Union[str, Path]) -> None:
        self.root = Path(root).resolve()
        self.orchestrator = AgentOrchestrator(self.root)
        self.path = self.root / "data" / "master_brain_state.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _write(self, state: Dict[str, Any]) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def plan(self, goal: Optional[str]) -> Dict[str, Any]:
        text = str(goal or "").strip()
        if not text:
            text = "general autonomous improvement"
        route = self.orchestrator.route(text)
        state = {
            "goal": text,
            "mission_status": "planned",
            "route": route,
            "owner_approval_required": True,
            "real_world_actions": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._write(state)
        return state

    def observe(self) -> Dict[str, Any]:
        try:
            state = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(state, dict):
                return state
        except (OSError, ValueError, TypeError):
            pass
        return {"mission_status": "idle", "owner_approval_required": True, "real_world_actions": False}

    def cycle(self, goal: Optional[str] = None) -> Dict[str, Any]:
        started = time.monotonic()
        state = self.plan(goal) if goal is not None else self.observe()
        route = state.get("route") or self.orchestrator.route(state.get("goal"))
        state["route"] = route
        state["mission_status"] = "sandbox_planned"
        state["last_cycle_seconds"] = round(time.monotonic() - started, 3)
        state["next_step"] = "execute sandbox missions and evaluate results"
        state["owner_approval_required"] = True
        state["real_world_actions"] = False
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._write(state)
        return state

    def status(self) -> Dict[str, Any]:
        state = self.observe()
        return {
            "status": state.get("mission_status", "idle"),
            "goal": state.get("goal"),
            "agent_count": len((state.get("route") or {}).get("agents", [])),
            "owner_approval_required": True,
            "real_world_actions": False,
            "autonomous_planning": True,
        }
