import subprocess
import sys
import unittest


class SupervisorCliTests(unittest.TestCase):
    def test_help_exposes_safe_runtime_controls(self):
        result = subprocess.run(
            [sys.executable, "-m", "autonomous_core.supervisor", "--help"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("--goal", result.stdout)
        self.assertIn("--interval", result.stdout)
        self.assertIn("--once", result.stdout)


if __name__ == "__main__":
    unittest.main()
