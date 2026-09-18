from decimal import Decimal

from django.test import TestCase

from .agents import ComplianceAgent, EconomicMasterAgent
from .models import Asset, OrderIntent, Portfolio, VirtualAssetProject
from .services import paper_execute


class EconomicLifecycleTests(TestCase):
    def test_master_agent_has_specialized_domains(self):
        caps = EconomicMasterAgent().capabilities()
        for expected in [
            "behavioral_economics",
            "financial_markets",
            "innovation",
            "virtual_assets",
            "compliance",
            "revenue",
            "analytics",
        ]:
            self.assertIn(expected, caps)
        self.assertIn("owner_approval_gate", caps)

    def test_virtual_asset_is_not_issuable_without_gates(self):
        project = VirtualAssetProject.objects.create(
            name="Test Asset", symbol="TST", concept="Test"
        )
        result = ComplianceAgent().review(project)
        self.assertFalse(result["ready_for_issuance"])
        self.assertFalse(project.issuance_approved)

    def test_paper_buy_updates_cash_and_position(self):
        portfolio = Portfolio.objects.create(
            name="Paper", paper_trading=True, cash_balance=Decimal("1000")
        )
        asset = Asset.objects.create(symbol="TST", name="Test")
        order = OrderIntent.objects.create(
            portfolio=portfolio,
            asset=asset,
            side="buy",
            quantity=Decimal("2"),
            limit_price=Decimal("100"),
        )
        ok, message = paper_execute(order)
        self.assertTrue(ok, message)
        portfolio.refresh_from_db()
        self.assertEqual(portfolio.cash_balance, Decimal("800"))
        self.assertEqual(order.trade.executed_quantity, Decimal("2"))

    def test_real_execution_is_blocked_by_default(self):
        portfolio = Portfolio.objects.create(
            name="Real", paper_trading=True, cash_balance=Decimal("1000")
        )
        asset = Asset.objects.create(symbol="TST2", name="Test 2")
        order = OrderIntent.objects.create(
            portfolio=portfolio,
            asset=asset,
            side="buy",
            quantity=Decimal("1"),
            limit_price=Decimal("100"),
            real_execution_requested=True,
            owner_approved=True,
        )
        ok, _ = paper_execute(order)
        self.assertFalse(ok)
        order.refresh_from_db()
        self.assertEqual(order.status, "blocked")
