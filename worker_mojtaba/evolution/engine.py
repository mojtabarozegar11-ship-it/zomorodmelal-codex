"""Evolution engine for safe self-improvement workflows."""
from dataclasses import dataclass

@dataclass
class CandidateVersion:
    version: str
    changes: list[str]
    status: str = "candidate"

class EvolutionEngine:
    def propose(self, current_version: str, improvements: list[str]) -> CandidateVersion:
        return CandidateVersion(
            version=f"{current_version}-candidate",
            changes=improvements,
        )

    def evaluate(self, candidate: CandidateVersion, tests_passed: bool) -> CandidateVersion:
        candidate.status = "approved" if tests_passed else "rejected"
        return candidate
