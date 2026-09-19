"""Central brain skeleton."""
from dataclasses import dataclass
from typing import Any

@dataclass
class Task:
    user_request: str
    context: dict[str, Any]

class CoreBrain:
    def __init__(self) -> None:
        self.session_memory: list[dict[str, Any]] = []

    def remember(self, item: dict[str, Any]) -> None:
        self.session_memory.append(item)

    def plan(self, task: Task) -> dict[str, Any]:
        self.remember({"role": "user", "request": task.user_request})
        return {"status":"planned","request":task.user_request,"next":"route"}
