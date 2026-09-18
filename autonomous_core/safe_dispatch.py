"""Single dispatch boundary for agent actions."""
from .runtime_contract import RuntimeResult

class SafeDispatch:
    def __init__(self, policy, executor):
        self.policy = policy
        self.executor = executor

    def dispatch(self, action, payload=None, approved=False):
        payload = payload or {}
        decision = self.policy.check(action=action, approved=approved)
        if not decision.get("allowed"):
            return RuntimeResult(
                status="waiting_approval",
                message=decision.get("reason", "Owner approval required."),
                pending_approval=[action],
            )
        value = self.executor(action, payload)
        return RuntimeResult(status="ok", message="Action executed.", executed=[action], data={"result": value})
