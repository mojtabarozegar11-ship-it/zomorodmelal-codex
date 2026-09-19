"""Digital asset portfolio abstraction."""
from dataclasses import dataclass

@dataclass
class AssetPosition:
    symbol: str
    amount: str
    network: str

class AssetManager:
    def __init__(self) -> None:
        self.positions: list[AssetPosition] = []

    def add_position(self, symbol: str, amount: str, network: str) -> None:
        self.positions.append(AssetPosition(symbol, amount, network))

    def list_positions(self) -> list[AssetPosition]:
        return list(self.positions)
