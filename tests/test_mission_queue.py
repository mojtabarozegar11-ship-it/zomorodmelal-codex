import tempfile
import unittest

from autonomous_core.mission_queue import MissionQueue


class MissionQueueTests(unittest.TestCase):
    def test_queue_persists_deduplicates_and_prioritizes(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = MissionQueue(tmp)
            queue.enqueue({"id": "low", "priority": 10, "status": "ready"})
            queue.enqueue({"id": "high", "priority": 90, "status": "ready"})
            queue.enqueue({"id": "low", "priority": 20, "status": "ready"})
            self.assertEqual(queue.peek()["id"], "high")
            self.assertEqual(len(queue.pending()), 2)
            self.assertTrue(queue.complete("high"))
            self.assertEqual(queue.peek()["id"], "low")

    def test_queue_survives_new_instance(self):
        with tempfile.TemporaryDirectory() as tmp:
            MissionQueue(tmp).enqueue({"id": "persisted", "priority": 50})
            self.assertEqual(MissionQueue(tmp).peek()["id"], "persisted")


if __name__ == "__main__":
    unittest.main()
