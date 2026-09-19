"""Generic HTTP JSON AI provider adapter.

The adapter reads credentials from an environment variable at execution time.
It does not persist or log the secret.
"""
from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from typing import Any

from worker_mojtaba.ai.adapter import AIProviderAdapter


class HTTPJSONProvider(AIProviderAdapter):
    def __init__(
        self,
        name: str,
        endpoint: str,
        api_key_env: str,
        *,
        timeout_seconds: int = 60,
        auth_header: str = "Authorization",
        auth_prefix: str = "Bearer ",
    ) -> None:
        self.name = name
        self.endpoint = endpoint
        self.api_key_env = api_key_env
        self.timeout_seconds = timeout_seconds
        self.auth_header = auth_header
        self.auth_prefix = auth_prefix

    def generate(self, request: str, *, capability: str) -> dict[str, Any]:
        api_key = os.getenv(self.api_key_env)
        if not api_key:
            return {
                "status": "provider_auth_required",
                "provider": self.name,
                "capability": capability,
            }

        payload = json.dumps(
            {"request": request, "capability": capability}
        ).encode("utf-8")
        http_request = Request(
            self.endpoint,
            data=payload,
            headers={
                "Content-Type": "application/json",
                self.auth_header: self.auth_prefix + api_key,
            },
            method="POST",
        )
        try:
            with urlopen(http_request, timeout=self.timeout_seconds) as response:
                body = response.read().decode("utf-8")
            return {
                "status": "completed",
                "provider": self.name,
                "capability": capability,
                "response": json.loads(body),
            }
        except HTTPError as exc:
            return {
                "status": "provider_http_error",
                "provider": self.name,
                "code": exc.code,
            }
        except (URLError, TimeoutError, ValueError):
            return {
                "status": "provider_unavailable",
                "provider": self.name,
            }
