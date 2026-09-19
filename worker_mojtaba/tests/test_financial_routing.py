"""Integration tests for financial routing and policy."""
from decimal import Decimal

from worker_mojtaba.api.service import WorkerService
from worker_mojtaba.core.router import Router
from worker_mojtaba.tools.iranian_bank_adapter import (
    BankAccountPolicy,
    IranianBankAdapter,
)


def test_wallet_intent_routes_to_finance():
    router = Router()
    assert router.route("wallet", ["finance"]) == "finance"


def test_revenue_allocation_is_10_90_through_bank_policy():
    bank = IranianBankAdapter(BankAccountPolicy("acct", "bank"))
    allocation = bank.allocate_revenue(Decimal("1000"))
    assert allocation == {
        "wallet_1": Decimal("100.00"),
        "wallet_2": Decimal("900.00"),
    }


def test_service_exposes_financial_adapter():
    service = WorkerService()
    capabilities = service.tool_center.list_capabilities()
    assert "finance" in capabilities
    assert service.bank.policy.revenue_share_wallet_1 == Decimal("0.10")
    assert service.bank.policy.revenue_share_wallet_2 == Decimal("0.90")

def test_service_selects_account_balance_capability():
    result = WorkerService().handle("موجودی کیف پول را بررسی کن")
    assert result["route"] == "finance"
    assert result["intent"] == "wallet"
    assert result["execution"]["status"] == "bank_bridge_required"
    assert result["execution"]["capability"] == "account_balance"
