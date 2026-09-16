import json
import tempfile
import unittest
from pathlib import Path

from autonomous_core.agent_factory import AgentFactory
from autonomous_core.agent_orchestrator import AgentOrchestrator
from autonomous_core.self_evolution_controller import SelfEvolutionController


class NextGenAgentSystemTests(unittest.TestCase):
    def test_factory_is_idempotent_and_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            factory = AgentFactory(root)
            first = factory.ensure_agent("testing", "repair tests")
            second = factory.ensure_agent("testing", "repair tests")
            self.assertEqual(first["agent_id"], second["agent_id"])
            self.assertFalse(first["permissions"]["real_world_write"])
            self.assertTrue(first["owner_approval_required"])

    def test_orchestrator_builds_multi_agent_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = AgentOrchestrator(root).route("site repair and security testing")
            self.assertGreaterEqual(len(plan["agents"]), 3)
            self.assertEqual(plan["status"], "sandbox_planned")
            self.assertFalse(plan["real_world_actions"])

    def test_evolution_advances_only_after_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            controller = SelfEvolutionController(root)
            failed = controller.evaluate({"passed": False}, 4)
            self.assertEqual(failed["generation"], 1)
            passed = controller.evaluate({"passed": True}, 4)
            self.assertEqual(passed["generation"], 2)
            saved = json.loads((root / "data" / "evolution_state.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["generation"], 2)
            self.assertTrue(saved["owner_approval_required"])
            self.assertFalse(saved["real_world_changes"])


if __name__ == "__main__":
    unittest.main()
