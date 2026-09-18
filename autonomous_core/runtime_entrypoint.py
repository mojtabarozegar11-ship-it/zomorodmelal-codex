"""Single guarded entry point for runtime dispatch."""
from autonomous_core.approval_context import ApprovalContext
from autonomous_core.runtime_guard import RuntimeGuard

class RuntimeEntrypoint:
    def __init__(self, dispatch, guard=None):
        self.dispatch = dispatch
        self.guard = guard or RuntimeGuard()

    def run(self, action, payload=None, critical=False, context=None):
        context = context or ApprovalContext()
        decision = self.guard.check(critical=critical, context=context)
        if not decision["allowed"]:
            return {"status": "blocked", "action": action, "reason": decision["reason"]}
        return {"status": "executed", "action": action, "result": self.dispatch(action, payload or {})}
