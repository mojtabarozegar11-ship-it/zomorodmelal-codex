from decimal import Decimal
from django.test import TestCase
from .models import Asset, OrderIntent, Portfolio
from .services import TradingGate, paper_execute


class EconomySafetyTests(TestCase):
    def setUp(self):
        self.asset = Asset.objects.create(symbol="TEST", name="Test Asset")
        self.portfolio = Portfolio.objects.create(name="Paper", cash_balance=Decimal("1000"), paper_trading=True)

    def test_real_execution_is_blocked(self):
        order = OrderIntent.objects.create(portfolio=self.portfolio, asset=self.asset, side="buy", quantity=Decimal("1"), limit_price=Decimal("10"), real_execution_requested=True)
        ok, _ = TradingGate.validate(order)
        self.assertFalse(ok)
        self.assertEqual(order.__class__.objects.get(pk=order.pk).status, "blocked")

    def test_paper_buy(self):
        order = OrderIntent.objects.create(portfolio=self.portfolio, asset=self.asset, side="buy", quantity=Decimal("2"), limit_price=Decimal("10"))
        ok, _ = paper_execute(order)
        self.assertTrue(ok)
        self.assertEqual(order.__class__.objects.get(pk=order.pk).status, "paper_executed")
        self.assertEqual(Portfolio.objects.get(pk=self.portfolio.pk).cash_balance, Decimal("980"))
