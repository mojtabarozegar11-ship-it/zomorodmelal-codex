"""Owner contact records and communication preferences."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Contact:
    name: str
    phone: str = ""
    email: str = ""
    whatsapp: str = ""
