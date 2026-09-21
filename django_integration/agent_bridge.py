"""Django -> unified Worker Mojtaba runtime bridge."""
from __future__ import annotations

import os
from typing import Any

import httpx


class AgentBridge:
    def __init__(self, worker_base_url: str | None = None, token: str | None = None):
        self.worker_base_url = (
            worker_base_url or os.getenv("WORKER_MOJTABA_URL", "http://127.0.0.1:8787")
        ).rstrip("/")
        self.token = token or os.getenv("WORKER_API_TOKEN", "")

    def execute_goal(
        self,
        goal: str,
        *,
        context: dict[str, Any] | None = None,
        approved: bool = False,
    ) -> dict[str, Any]:
        if not self.token:
            return {"status": "worker_auth_not_configured"}
        payload = {
            "request": goal,
            "context": context or {},
            "approved": approved,
        }
        try:
            response = httpx.post(
                f"{self.worker_base_url}/v1/tasks",
                json=payload,
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=60.0,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            return {"status": "worker_unreachable", "message": str(exc)}
        return response.json()

    def health(self) -> dict[str, Any]:
        try:
            response = httpx.get(f"{self.worker_base_url}/health", timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as exc:
            return {"status": "worker_unreachable", "message": str(exc)}
