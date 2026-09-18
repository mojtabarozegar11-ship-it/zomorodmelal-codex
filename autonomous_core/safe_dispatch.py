"""Single dispatch boundary for agent actions."""
from .runtime_contract import RuntimeResult
from .policy_adapter import PolicyAdapter


class SafeDispatch:
    def __init__(self, policy, executor):
        self.policy = policy
        self.executor = executor
        self._policy_adapter = PolicyAdapter(policy)

    def dispatch(self, action, payload=None, approved=False):
        payload = payload or {}
        decision = self._policy_adapter.check(action=action, approved=approved)
        if not decision["allowed"]:
            return RuntimeResult(
                status="waiting_approval",
                message=decision["reason"],
                pending_approval=[action],
            )
        value = self.executor(action, payload)
        return RuntimeResult(
            status="ok",
            message="Action executed.",
            executed=[action],
            data={"result": value},
        )
