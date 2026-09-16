import json
import tempfile
import unittest
from pathlib import Path

from autonomous_core.autonomous_decision_engine import AutonomousDecisionEngine


class AutonomousDecisionEngineTests(unittest.TestCase):
    def test_prefers_syntax_repair_and_never_enables_real_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data").mkdir()
            (root / "data" / "project_discovery.json").write_text(json.dumps({
                "django_detected": True,
                "files": [{"path": "broken.py", "syntax_ok": False}],
            }), encoding="utf-8")
            result = AutonomousDecisionEngine(root).assess()
            self.assertEqual(result["decision"], "quality.syntax_repair")
            self.assertTrue(result["owner_approval_required"])
            self.assertFalse(result["real_changes_allowed"])
            self.assertTrue(result["sandbox_only"])

    def test_django_without_templates_selects_template_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data").mkdir()
            (root / "data" / "project_discovery.json").write_text(json.dumps({
                "django_detected": True,
                "files": [{"path": "manage.py", "syntax_ok": True}],
            }), encoding="utf-8")
            result = AutonomousDecisionEngine(root).assess()
            self.assertEqual(result["decision"], "site.django_templates")


if __name__ == "__main__":
    unittest.main()
