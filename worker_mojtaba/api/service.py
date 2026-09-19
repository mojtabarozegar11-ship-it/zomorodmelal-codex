"""Application service boundary for Android clients."""
from typing import Any

from worker_mojtaba.ai.registry import AIProviderRegistry
from worker_mojtaba.core.engine import ExecutionEngine
from worker_mojtaba.core.memory import MemoryStore
from worker_mojtaba.tools.registry import ToolRegistry
from worker_mojtaba.security.audit import AuditLog


def _echo_tool(request: str) -> dict[str, Any]:
    """Deterministic built-in tool used to validate the safe tool boundary."""
    return {"status": "completed", "tool": "echo", "request": request}


class WorkerService:
    def __init__(self, ai_registry: AIProviderRegistry | None = None) -> None:
        self.memory = MemoryStore()
        self.tools = ToolRegistry()
        self.tools.register(
            "echo",
            "Safe diagnostic tool that returns the received request.",
            _echo_tool,
        )
        self.engine = ExecutionEngine(self.memory, self.tools, ai_registry)
        self.audit = AuditLog()

    def handle(self, request: str) -> dict[str, Any]:
        result = self.engine.run(request)
        self.audit.record(
            "task",
            result.get("status", "unknown"),
            {"request": request, "route": result.get("route")},
        )
        return result
