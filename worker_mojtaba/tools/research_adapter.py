"""Tool Center adapter for research workflows."""
from __future__ import annotations

from typing import Any

from worker_mojtaba.scientist.researcher import Scientist
from worker_mojtaba.tools.adapter import ToolAdapter


class ResearchToolAdapter(ToolAdapter):
    name = "research"

    def __init__(self) -> None:
        self.scientist = Scientist()

    def capabilities(self) -> list[str]:
        return ["research", "compare_results"]

    def execute(self, capability: str, payload: dict[str, Any]) -> dict[str, Any]:
        if capability == "research":
            question = str(payload.get("question") or payload.get("request") or "").strip()
            if not question:
                raise ValueError("Research question is required.")
            task = self.scientist.research(question)
            return {
                "status": "research_planned",
                "question": task.question,
                "hypotheses": task.hypotheses,
            }
        if capability == "compare_results":
            results = payload.get("results", [])
            if not isinstance(results, list):
                raise ValueError("results must be a list.")
            return self.scientist.compare(results)
        raise ValueError(f"Unsupported research capability: {capability}")
