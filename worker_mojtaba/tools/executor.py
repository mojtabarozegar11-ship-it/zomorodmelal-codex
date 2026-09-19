"""Safe tool execution boundary.

Tools are registered explicitly and executed by name. Unknown tools are rejected;
there is no arbitrary shell/code execution path here.
"""
from __future__ import annotations
from typing import Any
from worker_mojtaba.tools.registry import ToolRegistry

class ToolExecutor:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def execute(self, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        tool = self.registry.get(name)
        if tool is None:
            raise KeyError(f"Unknown tool: {name}")
        result = tool.handler(**payload)
        if isinstance(result, dict):
            return result
        return {"result": result}
