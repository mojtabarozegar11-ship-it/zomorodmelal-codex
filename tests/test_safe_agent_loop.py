import unittest

from autonomous_core.safe_agent_loop import SafeAgentLoop


class MockPlanner:
    def create_plan(self, goal):
        return {"actions": ["analyze", "prepare_report"]}


class MockApproval:
    def __init__(self):
        self.requests = []

    def request(self, action, reason):
        item = {"id": len(self.requests) + 1, "action": action, "reason": reason}
        self.requests.append(item)
        return item


class SafeAgentLoopTest(unittest.TestCase):
    def test_cycle_creates_approval_requests(self):
        loop = SafeAgentLoop(
            planner=MockPlanner(),
            executor=None,
            approval_gateway=MockApproval()
        )

        result = loop.execute_cycle("test goal")

        self.assertEqual(len(result["waiting"]), 2)
        self.assertEqual(result["goal"], "test goal")


if __name__ == "__main__":
    unittest.main()
