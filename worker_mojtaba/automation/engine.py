"""Calendar-aware task scheduling primitives."""
from dataclasses import dataclass, field
from typing import Any, Optional

@dataclass
class ScheduledTask:
    name: str
    expression: str
    calendar: str = "gregorian"
    action: dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    run_count: int | None = None
    occasion_key: Optional[str] = None

class AutomationEngine:
    def __init__(self) -> None:
        self.tasks: list[ScheduledTask] = []

    def schedule(self, name: str, expression: str, calendar: str = "gregorian",
                 action: dict[str, Any] | None = None, run_count: int | None = None,
                 occasion_key: Optional[str] = None) -> ScheduledTask:
        if calendar not in ("gregorian", "persian", "hijri"):
            raise ValueError("Unsupported calendar")
        if run_count is not None and run_count < 1:
            raise ValueError("run_count must be positive or None")
        task = ScheduledTask(name, expression, calendar, action or {}, True, run_count, occasion_key)
        self.tasks.append(task)
        return task

    def schedule_for_occasion(self, occasion_key: str, name: str, expression: str,
                               calendar: str = "gregorian",
                               action: dict[str, Any] | None = None) -> ScheduledTask:
        """Schedule an unlimited recurring action associated with an occasion key."""
        if not occasion_key.strip():
            raise ValueError("occasion_key is required")
        return self.schedule(
            name=name, expression=expression, calendar=calendar,
            action=action, run_count=None, occasion_key=occasion_key,
        )

    def list(self) -> list[ScheduledTask]:
        return list(self.tasks)
