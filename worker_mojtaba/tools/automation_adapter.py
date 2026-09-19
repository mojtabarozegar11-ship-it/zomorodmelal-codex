"""Tool Center adapters for calendar-aware scheduling."""
from __future__ import annotations
from typing import Any
from worker_mojtaba.automation.engine import AutomationEngine
from worker_mojtaba.calendar.occasions import OccasionProvider
from worker_mojtaba.tools.adapter import ToolAdapter

class AutomationToolAdapter(ToolAdapter):
    name = "automation"
    def __init__(self) -> None:
        self.engine = AutomationEngine()
        self.occasions = OccasionProvider()
    def capabilities(self) -> list[str]:
        return ["schedule_task", "list_tasks", "list_occasions"]
    def execute(self, capability: str, payload: dict[str, Any]) -> dict[str, Any]:
        if capability == "list_occasions":
            category = payload.get("category")
            return {"status": "completed", "occasions": [o.__dict__ for o in self.occasions.list(category)]}
        if capability == "schedule_task":
            task = self.engine.schedule(
                str(payload.get("name", "worker-task")),
                str(payload.get("expression", "")),
                str(payload.get("calendar", "gregorian")),
                payload.get("action", {}),
                payload.get("run_count"),
            )
            return {"status":"scheduled", **task.__dict__}
        if capability == "list_tasks":
            return {"status":"completed","tasks":[task.__dict__ for task in self.engine.list()]}
        raise ValueError(f"Unsupported automation capability: {capability}")
