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


if __name__ == "__main__":
    unittest.main()
