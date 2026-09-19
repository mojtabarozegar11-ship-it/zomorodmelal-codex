import unittest

from autonomous_core.safe_agent_loop import SafeAgentLoop


class MockPlanner:
    def create_plan(self, goal):
        return {"actions": ["analyze", "prepare_report"]}


class MockExecutor:
    def __init__(self):
        self.actions = []

    def execute(self, action):
        self.actions.append(action)
        return {"status": "executed", "action": action}


class MockApproval:
    def __init__(self, approved=False):
        self.requests = []
        self.approved = approved

    def request(self, action, reason):
        item = {
            "id": len(self.requests) + 1,
            "action": action,
            "reason": reason,
            "approved": self.approved,
        }
        self.requests.append(item)
        return item


class SafeAgentLoopTest(unittest.TestCase):
    def test_cycle_creates_approval_requests_without_execution(self):
        executor = MockExecutor()
        loop = SafeAgentLoop(
            planner=MockPlanner(),
            executor=executor,
            approval_gateway=MockApproval(approved=False),
        )

        result = loop.execute_cycle("test goal")

        self.assertEqual(len(result["waiting"]), 2)
        self.assertEqual(result["goal"], "test goal")
        self.assertEqual(result["status"], "approval_required")
        self.assertEqual(executor.actions, [])

    def test_approved_action_is_executed(self):
        executor = MockExecutor()
        loop = SafeAgentLoop(
            planner=MockPlanner(),
            executor=executor,
            approval_gateway=MockApproval(approved=True),
        )

        result = loop.execute_cycle("test goal")

        self.assertEqual(executor.actions, ["analyze", "prepare_report"])
        self.assertEqual(len(result["executed"]), 2)
        self.assertTrue(all(item["approved"] for item in result["waiting"]))


if __name__ == "__main__":
    unittest.main()
