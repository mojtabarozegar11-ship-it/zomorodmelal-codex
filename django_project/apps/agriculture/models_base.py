"""Base data models for agriculture domain.

Foundation layer for farms, products and production chains.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Farm:
    name: str
    location: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Product:
    name: str
    category: str
    farm: str


@dataclass
class ProductionChain:
    name: str
    description: str
