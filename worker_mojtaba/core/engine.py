"""Execution engine connecting planner, tools and agents."""
from typing import Any
from worker_mojtaba.core.planner import Planner
from worker_mojtaba.core.router import Router
from worker_mojtaba.core.memory import MemoryStore
from worker_mojtaba.tools.registry import ToolRegistry

class ExecutionEngine:
    def __init__(self, memory: MemoryStore, tools: ToolRegistry) -> None:
        self.memory = memory
        self.tools = tools
        self.planner = Planner()
        self.router = Router()

    def run(self, request: str) -> dict[str, Any]:
        plan = self.planner.make_plan(request)
        self.memory.remember_short({"request": request, "plan": plan})
        return {"status": "ready", "request": request, "plan": plan, "tools": self.tools.list()}
