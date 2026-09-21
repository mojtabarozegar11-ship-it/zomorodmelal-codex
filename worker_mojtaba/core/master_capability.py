"""Unified Master capability lifecycle inside Worker Mojtaba."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable

@dataclass(frozen=True)
class MasterTask:
    goal: str
    context: dict[str, Any] = field(default_factory=dict)

class MasterCapability:
    def __init__(self, planner: Callable[[str], list[str]] | None = None,
                 validator: Callable[[dict[str, Any]], bool] | None = None) -> None:
        self._planner = planner or (lambda goal: ["analyze", "execute", "validate", "report"])
        self._validator = validator or (lambda result: True)

    def build_plan(self, goal: str) -> MasterTask:
        cleaned = goal.strip()
        if not cleaned:
            raise ValueError("goal must be a non-empty string")
        return MasterTask(cleaned)

    def run(self, goal: str, *, approved: bool,
            dispatch: Callable[[str, dict[str, Any]], dict[str, Any]],
            context: dict[str, Any] | None = None) -> dict[str, Any]:
        task = self.build_plan(goal)
        plan = self._planner(task.goal)
        if not approved:
            return {"status": "approval_required", "goal": task.goal, "plan": plan}
        result = dispatch(task.goal, context or {})
        valid = bool(self._validator(result))
        return {
            "status": "completed" if valid else "validation_failed",
            "goal": task.goal,
            "plan": plan,
            "result": result,
            "validated": valid,
        }
