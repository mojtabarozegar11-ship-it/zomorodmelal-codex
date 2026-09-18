"""Minimal safe runtime bridge for the Django integration.

All execution requests remain approval-gated: no external action is performed
without explicit owner approval.
"""


class SafeAgentLoop:
    """Approval-gated runtime used by the Django API bridge."""

    def execute_cycle(self, goal):
        goal = str(goal or "").strip()
        return {
            "status": "awaiting_owner_approval",
            "goal": goal,
            "owner_approval_required": True,
            "executed": False,
        }
