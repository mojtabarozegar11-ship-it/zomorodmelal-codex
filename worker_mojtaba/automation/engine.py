"""Persistent-friendly scheduling abstraction with calendar and action metadata."""
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ScheduledTask:
    name: str
    expression: str
    calendar: str = "gregorian"
    action: dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    run_count: int | None = None  # None means unlimited

class AutomationEngine:
    def __init__(self) -> None:
        self.tasks: list[ScheduledTask] = []

    def schedule(self, name: str, expression: str, calendar: str = "gregorian",
                 action: dict[str, Any] | None = None, run_count: int | None = None) -> ScheduledTask:
        if calendar not in ("gregorian", "persian", "hijri"):
            raise ValueError("Unsupported calendar")
        if run_count is not None and run_count < 1:
            raise ValueError("run_count must be positive or None")
        task = ScheduledTask(name, expression, calendar, action or {}, True, run_count)
        self.tasks.append(task)
        return task

    def list(self) -> list[ScheduledTask]:
        return list(self.tasks)
