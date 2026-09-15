import tempfile
import unittest
from pathlib import Path

from controller.rollback_manager import RollbackManager


class RollbackManagerTests(unittest.TestCase):
    def test_backup_and_rollback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "demo.txt"
            target.write_text("before", encoding="utf-8")
            manager = RollbackManager(root)

            backup = manager.create_backup(["demo.txt"])
            target.write_text("after", encoding="utf-8")
            result = manager.rollback(backup, ["demo.txt"])

            self.assertTrue(result["success"])
            self.assertEqual(target.read_text(encoding="utf-8"), "before")
            self.assertEqual(manager.audit()[-1]["event"], "rollback_completed")

    def test_rejects_backup_outside_controlled_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manager = RollbackManager(root)
            with self.assertRaises(ValueError):
                manager.rollback(str(root.parent), [])


if __name__ == "__main__":
    unittest.main()
