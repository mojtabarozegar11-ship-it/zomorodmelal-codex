"""Execution engine connecting intent detection, planner, tools and memory."""
from __future__ import annotations
from typing import Any

from worker_mojtaba.core.intent import IntentParser
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
        self.intent_parser = IntentParser()

    def run(self, request: str) -> dict[str, Any]:
        intent = self.intent_parser.parse(request)
        plan = self.planner.make_plan(request)
        route = self.router.route(intent.capability, [tool["name"] for tool in self.tools.list()])
        self.memory.remember_short(
            {"request": request, "intent": intent.name, "route": route, "plan": plan}
        )
        return {
            "status": "planned",
            "request": request,
            "intent": intent.name,
            "route": route,
            "plan": plan,
            "tools": self.tools.list(),
        }
