"""Banking adapter boundary for authorized Iranian bank integrations.

The worker never stores banking passwords, OTPs, card PINs, certificates, or
private signing material. A real bank integration must provide an approved
API/bridge and explicit account authorization.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass(frozen=True)
class BankAccountPolicy:
    account_id: str
    bank_name: str
    revenue_share_wallet_1: Decimal = Decimal("0.10")
    revenue_share_wallet_2: Decimal = Decimal("0.90")
    wallet_2_outbound_allowed: bool = False

    def validate(self) -> None:
        if self.revenue_share_wallet_1 + self.revenue_share_wallet_2 != Decimal("1.00"):
            raise ValueError("Revenue shares must total 100%.")
        if self.revenue_share_wallet_2 != Decimal("0.90"):
            raise ValueError("Wallet 2 share must remain 90%.")
        if self.wallet_2_outbound_allowed:
            raise PermissionError("Wallet 2 is deposit-only by owner policy.")


class IranianBankAdapter:
    name = "iranian_bank"

    def __init__(self, policy: BankAccountPolicy) -> None:
        policy.validate()
        self.policy = policy

    def capabilities(self) -> list[str]:
        return [
            "account_balance",
            "transactions",
            "revenue_split",
            "deposit_wallet_1",
            "deposit_wallet_2",
        ]

    def allocate_revenue(self, amount: Decimal) -> dict[str, Decimal]:
        if amount < 0:
            raise ValueError("Revenue amount cannot be negative.")
        return {
            "wallet_1": amount * self.policy.revenue_share_wallet_1,
            "wallet_2": amount * self.policy.revenue_share_wallet_2,
        }

    def execute(self, capability: str, payload: dict[str, Any]) -> dict[str, Any]:
        if capability not in self.capabilities():
            raise ValueError(f"Unsupported banking capability: {capability}")
        return {
            "status": "bank_bridge_required",
            "adapter": self.name,
            "capability": capability,
            "account_id": self.policy.account_id,
            "message": "Connect an authorized bank API/bridge before financial execution.",
        }
