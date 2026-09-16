import unittest
from unittest.mock import patch

from controller.self_improvement_controller import SelfImprovementController


class SelfImprovementControllerSafetyTests(unittest.TestCase):
    @patch("controller.self_improvement_controller.ApprovalGateway")
    @patch("controller.self_improvement_controller.VersionControl")
    @patch("controller.self_improvement_controller.EvolutionEngine")
    @patch("controller.self_improvement_controller.ImprovementEngine")
    @patch("controller.self_improvement_controller.SelfAuditEngine")
    def test_cycle_only_proposes_changes_and_requires_owner_approval(
        self,
        audit_cls,
        improvement_cls,
        evolution_cls,
        versioning_cls,
        approval_cls,
    ):
        audit_cls.return_value.audit.return_value = {"status": "ok"}
        improvement_cls.return_value.analyze.return_value = [
            {"id": "proposal-1", "capability": "safe_refactor", "status": "proposed"}
        ]
        evolution_cls.return_value.get_proposals.return_value = []
        versioning_cls.return_value.create_backup.return_value = {"backup": True}
        approval_cls.return_value.request.return_value = {
            "id": 42,
            "status": "waiting_approval",
        }

        controller = SelfImprovementController()
        result = controller.run_cycle()

        audit_cls.return_value.audit.assert_called_once_with()
        improvement_cls.return_value.analyze.assert_called_once_with({"status": "ok"})
        evolution_cls.return_value.get_proposals.assert_called_once_with()
        versioning_cls.return_value.create_backup.assert_called_once_with()
        approval_cls.return_value.request.assert_called_once_with(
            action="self_improvement_cycle",
            reason="اجرای تغییرات پیشنهادی پس از ممیزی سیستم",
        )

        self.assertEqual(result["approval_request_id"], 42)
        self.assertTrue(result["owner_approval_required"])
        self.assertFalse(result["automatic_changes"])
        self.assertEqual(result["next_step"], "owner_approval")


if __name__ == "__main__":
    unittest.main()
