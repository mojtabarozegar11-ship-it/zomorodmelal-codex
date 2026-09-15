import tempfile
import unittest
from pathlib import Path

from autonomous_core.safe_builder import SafeBuilder


class SafeBuilderTests(unittest.TestCase):
    def test_builds_inside_sandbox_and_returns_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = SafeBuilder(tmp).build({"demo.py": "x = 1\n"})
            self.assertEqual(result[0]["path"], "demo.py")
            self.assertEqual(result[0]["size"], 6)
            self.assertTrue(result[0]["syntax_ok"])
            self.assertTrue(Path(tmp, "demo.py").exists())

    def test_rejects_escape_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                SafeBuilder(tmp).build({"../outside.py": "x = 1\n"})

    def test_rejects_invalid_python(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                SafeBuilder(tmp).build({"broken.py": "def broken(:\n"})

    def test_rejects_disallowed_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                SafeBuilder(tmp).build({"run.sh": "echo unsafe\n"})

    def test_rejects_large_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                SafeBuilder(tmp, max_file_size=3).build({"a.txt": "1234"})


if __name__ == "__main__":
    unittest.main()
