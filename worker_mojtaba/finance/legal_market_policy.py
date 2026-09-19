"""Legal-market participation policy.

The worker may participate in Iranian financial/virtual-asset markets only when
the specific market, service, account and operation are legally available to
the owner/entity and the required regulator/provider authorization exists.
No capability may bypass licensing, KYC, AML, sanctions, payment, custody,
exchange or platform restrictions.
"""
from dataclasses import dataclass
from typing import FrozenSet


@dataclass(frozen=True)
class MarketAuthorization:
    market_id: str
    jurisdiction: str
    regulator: str
    permitted_operations: FrozenSet[str]
    settlement_assets: FrozenSet[str]
    authorization_reference: str = ""


class LegalMarketPolicy:
    ALLOWED_JURISDICTION = "IR"
    SUPPORTED_SETTLEMENT_ASSETS = frozenset({"IRR", "FX", "VIRTUAL_ASSET"})

    def __init__(self) -> None:
        self._authorizations: dict[str, MarketAuthorization] = {}

    def register_authorization(self, authorization: MarketAuthorization) -> None:
        if authorization.jurisdiction != self.ALLOWED_JURISDICTION:
            raise ValueError("unsupported_jurisdiction")
        if not authorization.permitted_operations:
            raise ValueError("no_permitted_operations")
        if not authorization.settlement_assets.issubset(self.SUPPORTED_SETTLEMENT_ASSETS):
            raise ValueError("unsupported_settlement_asset")
        self._authorizations[authorization.market_id] = authorization

    def can_operate(self, market_id: str, operation: str, settlement_asset: str) -> bool:
        auth = self._authorizations.get(market_id)
        return bool(
            auth
            and operation in auth.permitted_operations
            and settlement_asset in auth.settlement_assets
        )

    def require_authorization(self, market_id: str, operation: str, settlement_asset: str) -> None:
        if not self.can_operate(market_id, operation, settlement_asset):
            raise PermissionError("market_authorization_required")

    def list_authorized_markets(self) -> list[MarketAuthorization]:
        return list(self._authorizations.values())
