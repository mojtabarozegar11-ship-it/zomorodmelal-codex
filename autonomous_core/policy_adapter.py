"""Compatibility adapter between the stable execution policy and dispatch contract."""


class PolicyAdapter:
    def __init__(self, policy):
        self.policy = policy

    def check(self, action, approved=False):
        if not action or not str(action).strip():
            return {
                "allowed": False,
                "reason": "Action name is required.",
                "action": action,
            }
        allowed = self.policy.can_execute(approved=approved)
        return {
            "allowed": bool(allowed),
            "reason": "" if allowed else "Owner approval required.",
            "action": action,
        }
