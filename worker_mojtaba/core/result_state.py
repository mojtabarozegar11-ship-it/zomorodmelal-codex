"""Execution result-state normalization for the personal assistant.

The engine should expose a stable outcome contract instead of leaking
provider-specific states to callers.
"""

from __future__ import annotations

from typing import Any

COMPLETED = "completed"
PENDING = "pending"
FAILED = "failed"
PLANNED = "planned"
BLOCKED = "blocked"


def normalize_execution_status(execution: dict[str, Any]) -> dict[str, Any]:
    """Return a copy with a stable top-level result state."""
    result = dict(execution)
    raw = str(result.get("status", PLANNED)).strip().lower()

    if raw in {COMPLETED, PENDING, FAILED, PLANNED, BLOCKED}:
        result["result_state"] = raw
        return result

    if raw in {"scheduled", "queued", "provider_connection_required", "occasion_provider_required"}:
        result["result_state"] = PENDING
        return result

    if raw in {
        "capability_selection_required",
        "owner_verification_required",
        "bank_bridge_required",
        "blocked",
    }:
        result["result_state"] = BLOCKED
        return result

    if raw in {"error", "exception"}:
        result["result_state"] = FAILED
        return result

    result["result_state"] = PLANNED
    return result
