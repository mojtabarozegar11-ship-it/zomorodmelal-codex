"""Task scheduling abstraction."""
from dataclasses import dataclass

@dataclass
class ScheduledTask:
    name: str
    expression: str
    enabled: bool = True

class AutomationEngine:
    def __init__(self) -> None:
        self.tasks: list[ScheduledTask] = []

    def schedule(self, name: str, expression: str) -> ScheduledTask:
        task = ScheduledTask(name, expression)
        self.tasks.append(task)
        return task

    def list(self) -> list[ScheduledTask]:
        return list(self.tasks)
