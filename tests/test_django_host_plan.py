import os
import unittest
from unittest.mock import patch

from deployment.django_host_plan import DjangoHostPlanner


class DjangoHostPlannerTests(unittest.TestCase):
    def test_plan_is_non_executing_and_uses_safe_commands(self):
        with patch.dict(os.environ, {"MASTER_AGENT_HEALTH_URL": "https://zomorodmelal.ir/"}, clear=True):
            plan = DjangoHostPlanner().plan()
        self.assertIn("migrate --noinput", plan.migrate_command)
        self.assertEqual(plan.restart_command, "")
        self.assertEqual(plan.rollback_command, "")

    def test_shell_operators_are_rejected(self):
        with patch.dict(os.environ, {"MASTER_AGENT_RESTART_COMMAND": "systemctl restart app && rm -rf /"}, clear=True):
            with self.assertRaises(ValueError):
                DjangoHostPlanner().plan()


if __name__ == "__main__":
    unittest.main()
