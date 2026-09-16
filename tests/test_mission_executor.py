import tempfile
import unittest
from pathlib import Path

from autonomous_core.mission_executor import MissionExecutor


class MissionExecutorTests(unittest.TestCase):
    def test_empty_queue_is_idle_and_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = MissionExecutor(Path(tmp)).execute_next()
            self.assertEqual(result["status"], "idle")
            self.assertTrue(result["sandbox_only"])
            self.assertFalse(result["real_world_changes"])

    def test_safe_improvement_is_completed_without_external_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            executor = MissionExecutor(Path(tmp))
            executor.queue.enqueue({"id": "continuous.improvement", "type": "improvement", "status": "ready"})
            result = executor.execute_next()
            self.assertEqual(result["status"], "completed")
            self.assertIsNone(executor.queue.peek())
            self.assertTrue(result["owner_approval_required"])
            self.assertFalse(result["real_world_changes"])

    def test_repair_is_bounded(self):
        with tempfile.TemporaryDirectory() as tmp:
            executor = MissionExecutor(Path(tmp))
            executor.queue.enqueue({"id": "repair.test", "type": "self_repair", "status": "ready"})
            first = executor.execute_next()
            self.assertIn(first["status"], {"verified", "retry_pending"})
            self.assertLessEqual(first["attempt"], executor.MAX_REPAIR_ATTEMPTS)

    def test_repair_plan_is_applied_and_verified_in_sandbox(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "sandbox" / "demo.py"
            target.parent.mkdir()
            target.write_text("value = 1\n", encoding="utf-8")
            executor = MissionExecutor(root)
            executor.queue.enqueue({
                "id": "repair.plan",
                "type": "self_repair",
                "status": "ready",
                "repair": {
                    "changes": [{"path": "demo.py", "content": "value = 2\n"}],
                    "test_command": ["python", "-m", "py_compile", "demo.py"],
                },
            })
            result = executor.execute_next()
            self.assertEqual(result["status"], "verified")
            self.assertEqual(target.read_text(encoding="utf-8"), "value = 2\n")
            self.assertTrue(result["sandbox_only"])
            self.assertFalse(result["real_world_changes"])


if __name__ == "__main__":
    unittest.main()
