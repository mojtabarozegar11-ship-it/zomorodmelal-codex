"""Owner verification handoff policy.

The worker must pause when a provider requires owner identity verification and
return a safe action link/instruction for the owner. Credentials and verification
codes are never stored by the worker.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class VerificationRequest:
    provider: str
    action_url: str
    reason: str

    def as_dict(self) -> dict[str, str]:
        return {
            "status": "owner_verification_required",
            "provider": self.provider,
            "action_url": self.action_url,
            "reason": self.reason,
            "instruction": "Complete verification yourself, then return to the worker.",
        }


class VerificationManager:
    def request_owner_verification(
        self, provider: str, action_url: str, reason: str
    ) -> dict[str, str]:
        if not action_url.startswith(("https://", "http://")):
            raise ValueError("Verification URL must be an explicit HTTP(S) URL.")
        return VerificationRequest(provider, action_url, reason).as_dict()
