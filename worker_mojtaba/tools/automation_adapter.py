"""Tool Center adapters for scheduling."""
from __future__ import annotations

from typing import Any

from worker_mojtaba.automation.engine import AutomationEngine
from worker_mojtaba.tools.adapter import ToolAdapter


class AutomationToolAdapter(ToolAdapter):
    name = "automation"

    def __init__(self) -> None:
        self.engine = AutomationEngine()

    def capabilities(self) -> list[str]:
        return ["schedule_task", "list_tasks"]

    def execute(self, capability: str, payload: dict[str, Any]) -> dict[str, Any]:
        if capability == "schedule_task":
            task = self.engine.schedule(
                str(payload.get("name", "worker-task")),
                str(payload.get("expression", "")),
            )
            return {"status": "scheduled", "name": task.name, "expression": task.expression}
        if capability == "list_tasks":
            return {
                "status": "completed",
                "tasks": [task.__dict__ for task in self.engine.list()],
            }
        raise ValueError(f"Unsupported automation capability: {capability}")
