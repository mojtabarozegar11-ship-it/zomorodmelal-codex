"""Execution engine connecting intent, planning, AI routing and the Tool Center."""
from __future__ import annotations

from typing import Any

from worker_mojtaba.ai.registry import AIProviderRegistry
from worker_mojtaba.core.intent import IntentParser
from worker_mojtaba.core.planner import Planner
from worker_mojtaba.core.router import Router
from worker_mojtaba.core.memory import MemoryStore
from worker_mojtaba.tools.registry import ToolRegistry
from worker_mojtaba.tools.executor import ToolExecutor
from worker_mojtaba.tools.center import ToolCenter
from worker_mojtaba.core.result_state import normalize_execution_status
from worker_mojtaba.security.policy import Policy


class ExecutionEngine:
    def __init__(
        self,
        memory: MemoryStore,
        tools: ToolRegistry,
        ai_registry: AIProviderRegistry | None = None,
        tool_center: ToolCenter | None = None,
        policy: Policy | None = None,
    ) -> None:
        self.memory = memory
        self.tools = tools
        self.executor = ToolExecutor(tools)
        self.ai_registry = ai_registry or AIProviderRegistry()
        self.planner = Planner()
        self.router = Router()
        self.intent_parser = IntentParser()
        self.tool_center = tool_center
        self.policy = policy or Policy()

    def run(self, request: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        intent = self.intent_parser.parse(request)
        plan = self.planner.make_plan(request)

        registry_tools = [tool["name"] for tool in self.tools.list()]
        center_tools = (
            list(self.tool_center.list_capabilities().keys())
            if self.tool_center is not None
            else []
        )
        available = sorted(set(registry_tools + center_tools))
        route = self.router.route(intent.capability, available)

        ai_result = self.ai_registry.generate(request, intent.capability)
        authorized = self.policy.check_capability(intent.capability)
        execution: dict[str, Any] = {
            "status": "planned",
            "reason": "no registered tool for this capability",
        }

        if route != "text_model" and not authorized:
            execution = {
                "status": "blocked",
                "reason": "capability_not_authorized_by_policy",
                "capability": intent.capability,
            }
            execution = normalize_execution_status(execution)
        elif route != "text_model":
            if self.tool_center is not None and route in center_tools:
                capabilities = self.tool_center.list_capabilities()[route]
                capability = intent.capability
                if capability in capabilities:
                    execution = self.tool_center.execute(
                        route, capability, {"request": request}
                    )
                    execution = {
                        **execution,
                        "adapter": route,
                        "capability": capability,
                    }
                    execution = normalize_execution_status(execution)
                else:
                    execution = {
                        "status": "capability_selection_required",
                        "adapter": route,
                        "available_capabilities": capabilities,
                    }
                    execution = normalize_execution_status(execution)
            else:
                tool = self.tools.get(route)
                if tool is not None:
                    execution = self.executor.execute(route, {"request": request, "context": context})
                    execution = normalize_execution_status(execution)

        self.memory.remember_short({
            "request": request,
            "intent": intent.name,
            "route": route,
            "plan": plan,
            "ai_status": ai_result.get("status"),
            "execution_status": execution.get("status"),
        })
        return {
            "status": ai_result.get("status", "planned"),
            "request": request,
            "intent": intent.name,
            "route": route,
            "plan": plan,
            "ai": ai_result,
            "execution": execution,
            "tools": available,
            "authorization": {"capability": intent.capability, "allowed": authorized},
        }
