"""Backward-compatible entrypoint for the canonical MasterOrchestrator."""
from master_agent.orchestrator import MasterOrchestrator


class MasterAgent:
    def __init__(self, orchestrator=None):
        self.name = "Zomorod Melal Master Agent"
        self.orchestrator = orchestrator or MasterOrchestrator()

    def run(self, goal, approved=False, action=None, validate=None):
        return self.orchestrator.execute(goal, approved=approved, action=action, validate=validate)
