"""Banking policy tests."""
from decimal import Decimal

from worker_mojtaba.tools.iranian_bank_adapter import (
    BankAccountPolicy,
    IranianBankAdapter,
)


def test_bank_revenue_split_is_10_90():
    adapter = IranianBankAdapter(
        BankAccountPolicy("acct", "bank")
    )
    assert adapter.allocate_revenue(Decimal("100")) == {
        "wallet_1": Decimal("10.00"),
        "wallet_2": Decimal("90.00"),
    }


def test_bank_policy_rejects_wallet_2_outbound():
    try:
        BankAccountPolicy(
            "acct",
            "bank",
            wallet_2_outbound_allowed=True,
        ).validate()
    except PermissionError:
        pass
    else:
        raise AssertionError("wallet_2 outbound must be rejected")


def test_bank_adapter_does_not_execute_without_bridge():
    adapter = IranianBankAdapter(BankAccountPolicy("acct", "bank"))
    result = adapter.execute("transactions", {})
    assert result["status"] == "bank_bridge_required"
