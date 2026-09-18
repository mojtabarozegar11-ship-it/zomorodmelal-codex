"""Approval-gated runtime bridge for the Zomorod Melal Master Agent.

Registered owner: Mojtaba Rozegar (مجتبی روزگار).
"""


class SafeAgentLoop:
    """Approval-gated runtime used by the Django API bridge."""

    OWNER_NAME = "مجتبی روزگار"

    def execute_cycle(self, goal):
        goal = str(goal or "").strip()
        return {
            "status": "awaiting_owner_approval",
            "goal": goal,
            "owner_approval_required": True,
            "owner": self.OWNER_NAME,
            "executed": False,
        }
