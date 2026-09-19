"""Checkpoint and recovery primitives for safe assistant evolution and execution."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Checkpoint:
    checkpoint_id: str
    state: dict[str, Any]
    created_at: str


class RecoveryManager:
    def __init__(self) -> None:
        self._checkpoints: list[Checkpoint] = []

    def checkpoint(self, checkpoint_id: str, state: dict[str, Any]) -> Checkpoint:
        if not checkpoint_id.strip():
            raise ValueError("checkpoint_id is required")
        cp = Checkpoint(
            checkpoint_id=checkpoint_id.strip(),
            state=dict(state),
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._checkpoints.append(cp)
        return cp

    def latest(self) -> Checkpoint | None:
        return self._checkpoints[-1] if self._checkpoints else None

    def restore(self, checkpoint_id: str) -> dict[str, Any]:
        for checkpoint in reversed(self._checkpoints):
            if checkpoint.checkpoint_id == checkpoint_id.strip():
                return dict(checkpoint.state)
        raise KeyError(f"checkpoint not found: {checkpoint_id}")

    def list_checkpoints(self) -> list[Checkpoint]:
        return list(self._checkpoints)
