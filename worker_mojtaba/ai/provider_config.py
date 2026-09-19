"""Configuration model for external AI providers.

Secrets are referenced by environment-variable names, never stored here.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class ProviderConfig:
    name: str
    endpoint: str
    api_key_env: str
    capabilities: tuple[str, ...]
    priority: int = 100

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("Provider name is required.")
        if not self.endpoint.startswith(("https://", "http://")):
            raise ValueError("Provider endpoint must be HTTP(S).")
        if not self.api_key_env.isidentifier():
            raise ValueError("api_key_env must be a valid environment variable name.")
