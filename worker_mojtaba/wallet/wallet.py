"""Wallet allocation and permission policy.

Secrets/private keys must stay in secure external storage.
"""
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Wallet:
    wallet_id: str
    network: str
    address: str | None = None
    enabled: bool = True
    can_withdraw: bool = True
    can_deposit: bool = True


class WalletManager:
    """Manage wallet roles and revenue routing without holding secrets."""

    def __init__(self) -> None:
        self.wallets: dict[str, Wallet] = {}
        self.revenue_shares: dict[str, Decimal] = {
            "wallet_1": Decimal("0.10"),
            "wallet_2": Decimal("0.90"),
        }

    def create_placeholder(
        self,
        wallet_id: str,
        network: str,
        *,
        can_withdraw: bool = True,
        can_deposit: bool = True,
    ) -> Wallet:
        wallet = Wallet(
            wallet_id,
            network,
            can_withdraw=can_withdraw,
            can_deposit=can_deposit,
        )
        self.wallets[wallet_id] = wallet
        return wallet

    def configure_default_revenue_wallets(
        self,
        wallet_1_address: str | None = None,
        wallet_2_address: str | None = None,
        network: str = "unspecified",
    ) -> None:
        """Configure the two owner-defined revenue destinations.

        Wallet 1 receives 10% and may operate within its granted permissions.
        Wallet 2 receives 90% and is deposit-only: no withdrawals/transfers out.
        """
        self.wallets["wallet_1"] = Wallet(
            "wallet_1", network, wallet_1_address,
            can_withdraw=True, can_deposit=True,
        )
        self.wallets["wallet_2"] = Wallet(
            "wallet_2", network, wallet_2_address,
            can_withdraw=False, can_deposit=True,
        )

    def allocate_revenue(self, amount: Decimal) -> dict[str, Decimal]:
        if amount < 0:
            raise ValueError("Revenue amount cannot be negative.")
        return {
            wallet_id: (amount * share)
            for wallet_id, share in self.revenue_shares.items()
        }

    def assert_withdraw_allowed(self, wallet_id: str) -> None:
        wallet = self.wallets[wallet_id]
        if not wallet.can_withdraw:
            raise PermissionError(f"{wallet_id} is deposit-only.")

    def assert_deposit_allowed(self, wallet_id: str) -> None:
        wallet = self.wallets[wallet_id]
        if not wallet.can_deposit:
            raise PermissionError(f"{wallet_id} does not accept deposits.")

    def list_wallets(self) -> list[Wallet]:
        return list(self.wallets.values())
