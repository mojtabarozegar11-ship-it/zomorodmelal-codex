"""Financial Tool Center boundary.

All financial execution is policy-first: allocation can be calculated locally,
while real bank/wallet execution requires an authorized provider bridge.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any

from worker_mojtaba.tools.adapter import ToolAdapter
from worker_mojtaba.tools.iranian_bank_adapter import IranianBankAdapter
from worker_mojtaba.wallet.wallet import WalletManager


class FinancialToolAdapter(ToolAdapter):
    name = "finance"

    def __init__(self, bank: IranianBankAdapter, wallets: WalletManager) -> None:
        self.bank = bank
        self.wallets = wallets

    def capabilities(self) -> list[str]:
        return [
            "allocate_revenue",
            "account_balance",
            "transactions",
            "deposit_wallet_1",
            "deposit_wallet_2",
        ]

    def execute(self, capability: str, payload: dict[str, Any]) -> dict[str, Any]:
        if capability == "allocate_revenue":
            amount = Decimal(str(payload.get("amount", "0")))
            allocation = self.wallets.allocate_revenue(amount)
            return {
                "status": "allocated",
                "wallet_1": str(allocation["wallet_1"]),
                "wallet_2": str(allocation["wallet_2"]),
            }

        if capability in self.capabilities():
            return self.bank.execute(capability, payload)

        raise ValueError(f"Unsupported financial capability: {capability}")
