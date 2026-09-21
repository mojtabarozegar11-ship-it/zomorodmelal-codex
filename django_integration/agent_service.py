"""Application service for Django to communicate with the unified Worker runtime."""
from __future__ import annotations

from .agent_bridge import AgentBridge


class AgentService:
    def __init__(self, bridge: AgentBridge | None = None):
        self.bridge = bridge or AgentBridge()

    def run(self, goal: str, *, context=None, approved: bool = False):
        return self.bridge.execute_goal(goal, context=context or {}, approved=approved)

    def health(self):
        return self.bridge.health()
