import os
import unittest
from unittest.mock import patch

from deployment.host_adapter import HostDeploymentAdapter


class HostDeploymentAdapterTests(unittest.TestCase):
    def test_disabled_by_default(self):
        with patch.dict(os.environ, {}, clear=True):
            result = HostDeploymentAdapter().deploy()
        self.assertFalse(result.success)
        self.assertEqual(result.status, "adapter_disabled")

    def test_missing_command_is_safe_failure(self):
        with patch.dict(os.environ, {"MASTER_AGENT_DEPLOY_ENABLED": "true"}, clear=True):
            result = HostDeploymentAdapter().deploy()
        self.assertFalse(result.success)
        self.assertEqual(result.status, "configuration_error")

    def test_shell_operators_are_rejected(self):
        adapter = HostDeploymentAdapter(enabled=True, command="python deploy.py && rm -rf /")
        result = adapter.deploy()
        self.assertFalse(result.success)
        self.assertEqual(result.status, "configuration_error")

    def test_argv_command_can_execute(self):
        adapter = HostDeploymentAdapter(enabled=True, command="python -c 'print(\"ok\")'")
        result = adapter.deploy()
        self.assertTrue(result.success)
        self.assertEqual(result.status, "completed")
        self.assertIn("ok", result.stdout)


if __name__ == "__main__":
    unittest.main()
