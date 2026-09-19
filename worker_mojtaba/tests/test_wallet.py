from decimal import Decimal

import pytest

from worker_mojtaba.wallet.wallet import WalletManager


def test_revenue_split_is_10_90():
    manager = WalletManager()
    assert manager.allocate_revenue(Decimal("100")) == {
        "wallet_1": Decimal("10.00"),
        "wallet_2": Decimal("90.00"),
    }


def test_wallet_2_is_deposit_only():
    manager = WalletManager()
    manager.configure_default_revenue_wallets()
    manager.assert_deposit_allowed("wallet_2")
    with pytest.raises(PermissionError):
        manager.assert_withdraw_allowed("wallet_2")


def test_wallet_1_withdrawal_is_allowed_by_policy():
    manager = WalletManager()
    manager.configure_default_revenue_wallets()
    manager.assert_withdraw_allowed("wallet_1")
