"""Non-custodial wallet abstraction; secret material must stay in secure storage."""
from dataclasses import dataclass

@dataclass
class Wallet:
    wallet_id: str
    network: str
    address: str | None = None
    enabled: bool = True

class WalletManager:
    def __init__(self) -> None:
        self.wallets: dict[str, Wallet] = {}

    def create_placeholder(self, wallet_id: str, network: str) -> Wallet:
        wallet = Wallet(wallet_id, network)
        self.wallets[wallet_id] = wallet
        return wallet

    def list_wallets(self) -> list[Wallet]:
        return list(self.wallets.values())
