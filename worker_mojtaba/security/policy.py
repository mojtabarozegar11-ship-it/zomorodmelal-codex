"""Capability authorization policy for the personal assistant.

This layer is deliberately explicit: an allow-list can be supplied by the
owner/runtime, and disabling the policy denies all capability execution.
"""

from __future__ import annotations


class Policy:
    def __init__(self, allowed: set[str] | None = None) -> None:
        self.enabled = True
        self.allowed = set(allowed or ())

    def check_capability(self, capability: str) -> bool:
        name = capability.strip()
        if not self.enabled or not name:
            return False
        return name in self.allowed

    def allow(self, capability: str) -> None:
        name = capability.strip()
        if name:
            self.allowed.add(name)

    def deny(self, capability: str) -> None:
        self.allowed.discard(capability.strip())

    def disable(self) -> None:
        self.enabled = False
