"""Execution engine connecting intent detection, planning, AI routing and safe tools."""
from __future__ import annotations
from typing import Any
from worker_mojtaba.ai.registry import AIProviderRegistry
from worker_mojtaba.core.intent import IntentParser
from worker_mojtaba.core.planner import Planner
from worker_mojtaba.core.router import Router
from worker_mojtaba.core.memory import MemoryStore
from worker_mojtaba.tools.registry import ToolRegistry
from worker_mojtaba.tools.executor import ToolExecutor

class ExecutionEngine:
    def __init__(
        self,
        memory: MemoryStore,
        tools: ToolRegistry,
        ai_registry: AIProviderRegistry | None = None,
    ) -> None:
        self.memory = memory
        self.tools = tools
        self.executor = ToolExecutor(tools)
        self.ai_registry = ai_registry or AIProviderRegistry()
        self.planner = Planner()
        self.router = Router()
        self.intent_parser = IntentParser()

    def run(self, request: str) -> dict[str, Any]:
        intent = self.intent_parser.parse(request)
        plan = self.planner.make_plan(request)
        available = [tool["name"] for tool in self.tools.list()]
        route = self.router.route(intent.capability, available)

        ai_result = self.ai_registry.generate(request, intent.capability)
        execution = {"status": "planned", "reason": "no registered tool for this capability"}
        if route != "text_model":
            tool = self.tools.get(route)
            if tool is not None:
                execution = self.executor.execute(route, {"request": request})
        self.memory.remember_short({
            "request": request,
            "intent": intent.name,
            "route": route,
            "plan": plan,
            "ai_status": ai_result.get("status"),
        })
        return {
            "status": ai_result.get("status", "planned"),
            "request": request,
            "intent": intent.name,
            "route": route,
            "plan": plan,
            "ai": ai_result,
            "execution": execution,
            "tools": self.tools.list(),
        }
