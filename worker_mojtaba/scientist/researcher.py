"""Scientist engine skeleton for research, experiments and evaluation."""
from dataclasses import dataclass

@dataclass
class ResearchTask:
    question: str
    hypotheses: list[str]

class Scientist:
    def research(self, question: str, hypotheses: list[str] | None = None) -> ResearchTask:
        return ResearchTask(question=question, hypotheses=hypotheses or [])

    def compare(self, results: list[dict]) -> dict:
        return {"count": len(results), "status": "compared"}
