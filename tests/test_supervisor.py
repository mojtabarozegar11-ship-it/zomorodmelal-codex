import tempfile
import unittest
from pathlib import Path

from autonomous_core.supervisor import AutonomousSupervisor


class FakeCycle:
    calls = 0

    def __init__(self, root: Path) -> None:
        self.root = root

    def run(self, goal=None):
        type(self).calls += 1
        return {
            "report": {
                "cycle": type(self).calls,
                "phase": "approval",
                "goal": goal,
                "pending": ["owner_approval_for_real_changes"],
            }
        }


class SupervisorTests(unittest.TestCase):
    def test_run_once_persists_safe_blocked_state(self):
        FakeCycle.calls = 0
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            supervisor = AutonomousSupervisor(root, cycle_factory=FakeCycle)
            result = supervisor.run_once("research market")

            self.assertEqual(result["report"]["cycle"], 1)
            state = (root / "data" / "supervisor_state.json").read_text(encoding="utf-8")
            self.assertIn('"blocked": true', state)
            self.assertIn('"owner_approval_required": true', state)
            self.assertIn('"real_changes_allowed": false', state)


if __name__ == "__main__":
    unittest.main()
