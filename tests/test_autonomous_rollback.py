import tempfile
import unittest
from pathlib import Path

from autonomous_core.rollback_policy import AutonomousRollback


class AutonomousRollbackTests(unittest.TestCase):
    def test_restore_requires_owner_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "demo.txt"
            target.write_text("safe", encoding="utf-8")
            rollback = AutonomousRollback(str(root))
            backup = rollback.prepare(["demo.txt"])["backup"]
            target.write_text("changed", encoding="utf-8")
            blocked = rollback.restore(backup, ["demo.txt"])
            self.assertEqual(blocked["status"], "approval_required")

    def test_restore_after_owner_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "demo.txt"
            target.write_text("safe", encoding="utf-8")
            rollback = AutonomousRollback(str(root))
            backup = rollback.prepare(["demo.txt"])["backup"]
            target.write_text("changed", encoding="utf-8")
            result = rollback.restore(backup, ["demo.txt"], owner_approved=True)
            self.assertTrue(result["success"])
            self.assertEqual(target.read_text(encoding="utf-8"), "safe")


if __name__ == "__main__":
    unittest.main()
