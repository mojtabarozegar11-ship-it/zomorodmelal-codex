"""Adapters that connect the canonical orchestrator to existing runtime services."""
from app.runtime.system_orchestrator import SystemOrchestrator
from app.core.executor import Executor
from agents.agent_registry import AgentRegistry
from app.security.approval import ApprovalSystem
from app.security.audit import AuditLogger


class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, func):
        self.tools[name] = func

    def get(self, name):
        return self.tools.get(name)

    def names(self):
        return tuple(sorted(self.tools))


class MasterRuntime:
    def __init__(self, runner=None, registry=None, tools=None, approval=None, audit=None):
        self.registry = registry or AgentRegistry()
        self.tools = tools or ToolRegistry()
        self.approval = approval or ApprovalSystem()
        self.audit = audit or AuditLogger()
        self.runner = runner
        self.system = None
        if runner is not None:
            self.system = SystemOrchestrator(startup=getattr(runner, "startup", runner), runner=runner)

    def execute(self, plan):
        if self.runner is not None and hasattr(self.runner, "run"):
            result = self.runner.run(plan["goal"])
        else:
            result = {"status": "planned", "goal": plan["goal"], "steps": plan["steps"]}
        self.audit.log("RUNTIME_EXECUTE", result)
        return result
