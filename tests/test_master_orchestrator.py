import unittest

from agents.agent_registry import AgentRegistry
from app.security.approval import ApprovalSystem
from app.security.audit import AuditLogger
from master_agent import MasterOrchestrator, MasterRuntime, ToolRegistry


class MasterOrchestratorTests(unittest.TestCase):
    def test_denies_without_owner_approval(self):
        master = MasterOrchestrator(runtime=MasterRuntime())
        result = master.execute("publish update")
        self.assertEqual(result["status"], "approval_required")

    def test_connects_runtime_registry_and_tools(self):
        registry = AgentRegistry()
        registry.register("Research Agent", "Research")
        tools = ToolRegistry()
        tools.register("echo", lambda payload: payload)
        runtime = MasterRuntime(registry=registry, tools=tools, approval=ApprovalSystem(), audit=AuditLogger())
        master = MasterOrchestrator(runtime=runtime, registry=registry, tools=tools)
        result = master.execute("research market", approved=True)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(runtime.registry.get_all()[0]["name"], "Research Agent")
        self.assertIn("echo", runtime.tools.names())

    def test_failed_validation_is_reported(self):
        master = MasterOrchestrator(runtime=MasterRuntime())
        result = master.execute("run task", approved=True, validate=lambda _: False)
        self.assertEqual(result["status"], "validation_failed")


if __name__ == "__main__":
    unittest.main()
