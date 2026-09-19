"""Tool Center adapters for calendar-aware scheduling."""
from __future__ import annotations
from typing import Any
from worker_mojtaba.automation.engine import AutomationEngine\nfrom worker_mojtaba.calendar.model import CalendarEvent, CalendarManager
from worker_mojtaba.calendar.occasions import OccasionProvider
from worker_mojtaba.tools.adapter import ToolAdapter

class AutomationToolAdapter(ToolAdapter):
    name = "automation"
    def __init__(self) -> None:
        self.engine = AutomationEngine()
        self.occasions = OccasionProvider()\n        self.calendar = CalendarManager()
    def capabilities(self) -> list[str]:
        return ["schedule_task", "list_tasks", "calendar_event", "list_calendar_events", "list_occasions", "schedule_for_occasion"]
    def execute(self, capability: str, payload: dict[str, Any]) -> dict[str, Any]:
        if capability == "calendar_event":\n            event = CalendarEvent(\n                title=str(payload.get("title", payload.get("request", "calendar-event"))),\n                calendar=str(payload.get("calendar", "gregorian")),\n                date=str(payload.get("date", "")),\n                time=str(payload.get("time", "")),\n                recurrence=str(payload.get("recurrence", "")),\n                occasion=str(payload.get("occasion", "")),\n                action=payload.get("action", {}),\n            )\n            saved = self.calendar.add(event)\n            return {"status": "scheduled", "event": saved.__dict__}\n        if capability == "list_calendar_events":\n            return {"status": "completed", "events": [event.__dict__ for event in self.calendar.list()]}\n        if capability == "schedule_for_occasion":
            task = self.engine.schedule_for_occasion(
                str(payload.get("occasion_key", "")),
                str(payload.get("name", "occasion-task")),
                str(payload.get("expression", "")),
                str(payload.get("calendar", "gregorian")),
                payload.get("action", {}),
            )
            return {"status": "scheduled", **task.__dict__}
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
