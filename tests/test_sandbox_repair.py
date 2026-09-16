import tempfile
import unittest
from pathlib import Path

from autonomous_core.sandbox_repair import SandboxRepairEngine


class SandboxRepairTests(unittest.TestCase):
    def test_verified_repair_stays_inside_sandbox(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "sandbox" / "demo.py"
            target.parent.mkdir()
            target.write_text("value = 1\n", encoding="utf-8")
            engine = SandboxRepairEngine(root)
            result = engine.repair(
                [{"path": "demo.py", "content": "value = 2\n"}],
                ["python", "-m", "py_compile", "demo.py"],
            )
            self.assertEqual(result["status"], "verified")
            self.assertFalse(result["real_world_changes"])
            self.assertEqual(target.read_text(encoding="utf-8"), "value = 2\n")

    def test_failed_repair_rolls_back_automatically(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "sandbox" / "demo.py"
            target.parent.mkdir()
            target.write_text("value = 1\n", encoding="utf-8")
            engine = SandboxRepairEngine(root)
            result = engine.repair(
                [{"path": "demo.py", "content": "def broken(:\n"}],
                ["python", "-m", "py_compile", "demo.py"],
            )
            self.assertEqual(result["status"], "rolled_back")
            self.assertTrue(result["rolled_back"])
            self.assertEqual(target.read_text(encoding="utf-8"), "value = 1\n")

    def test_path_escape_is_rejected_without_touching_outside(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root / "outside.txt"
            outside.write_text("safe", encoding="utf-8")
            engine = SandboxRepairEngine(root)
            with self.assertRaises(ValueError):
                engine.repair([{"path": "../outside.txt", "content": "unsafe"}])
            self.assertEqual(outside.read_text(encoding="utf-8"), "safe")

    def test_unsafe_test_command_causes_rollback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "sandbox" / "demo.txt"
            target.parent.mkdir()
            target.write_text("safe", encoding="utf-8")
            engine = SandboxRepairEngine(root)
            result = engine.repair(
                [{"path": "demo.txt", "content": "changed"}],
                ["sh", "-c", "echo unsafe"],
            )
            self.assertEqual(result["status"], "rolled_back")
            self.assertEqual(result["verification"]["kind"], "invalid_test_command")
            self.assertEqual(target.read_text(encoding="utf-8"), "safe")

    def test_duplicate_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine = SandboxRepairEngine(Path(tmp))
            with self.assertRaises(ValueError):
                engine.repair([
                    {"path": "demo.txt", "content": "one"},
                    {"path": "demo.txt", "content": "two"},
                ])


if __name__ == "__main__":
    unittest.main()
