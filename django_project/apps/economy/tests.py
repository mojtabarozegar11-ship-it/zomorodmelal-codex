from django.test import TestCase
from .agents import EconomicMasterAgent, ComplianceAgent
from .models import VirtualAssetProject

class EconomicLifecycleTests(TestCase):
    def test_master_agent_has_specialized_domains(self):
        caps = EconomicMasterAgent().capabilities()
        for expected in ["behavioral_economics", "financial_markets", "innovation", "virtual_assets", "compliance", "revenue", "analytics"]:
            self.assertIn(expected, caps)
        self.assertIn("owner_approval_gate", caps)

    def test_virtual_asset_is_not_issuable_without_gates(self):
        project = VirtualAssetProject.objects.create(name="Test Asset", symbol="TST", concept="Test")
        result = ComplianceAgent().review(project)
        self.assertFalse(result["ready_for_issuance"])
        self.assertFalse(project.issuance_approved)
