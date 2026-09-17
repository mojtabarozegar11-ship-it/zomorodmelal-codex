"""Base data models for agriculture domain.

Foundation layer for farms, products and production chains.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Farm:
    name: str
    location: str
    created_at: datetime = datetime.utcnow()


@dataclass
class Product:
    name: str
    category: str
    farm: str


@dataclass
class ProductionChain:
    name: str
    description: str
