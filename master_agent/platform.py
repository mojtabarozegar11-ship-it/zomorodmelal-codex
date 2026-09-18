"""Adapters connecting the canonical orchestrator to the existing runtime, registry and tools."""
from agents.agent_registry import AgentRegistry
from app.security.approval import ApprovalSystem
from app.security.audit import AuditLogger


class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, func):
        if not name or not callable(func):
            raise ValueError("tool name and callable function are required")
        self.tools[name] = func

    def get(self, name):
        return self.tools.get(name)

    def execute(self, name, payload=None):
        tool = self.get(name)
        if tool is None:
            raise KeyError(f"tool not found: {name}")
        return tool(payload)

    def names(self):
        return tuple(sorted(self.tools))


class MasterRuntime:
    def __init__(self, runner=None, registry=None, tools=None, approval=None, audit=None):
        self.registry = registry or AgentRegistry()
        self.tools = tools or ToolRegistry()
        self.approval = approval or ApprovalSystem()
        self.audit = audit or AuditLogger()
        self.runner = runner

    def execute(self, plan):
        if self.runner is None:
            result = {"status": "planned", "goal": plan["goal"], "steps": plan["steps"]}
        elif hasattr(self.runner, "run"):
            result = self.runner.run(plan["goal"])
        elif hasattr(self.runner, "execute"):
            result = self.runner.execute(plan["goal"])
        else:
            raise TypeError("runner must expose run() or execute()")
        self.audit.log("RUNTIME_EXECUTE", result)
        return result
