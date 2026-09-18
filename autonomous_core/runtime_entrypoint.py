"""Single entry point for guarded runtime dispatch."""
from autonomous_core.runtime_guard import RuntimeGuard

class RuntimeEntrypoint:
    def __init__(self, dispatch, guard=None):
        self.dispatch = dispatch
        self.guard = guard or RuntimeGuard()

    def run(self, action, payload=None, critical=False, context=None):
        decision = self.guard.check(critical=critical, context=context)
        if not decision["allowed"]:
            return {"status": "blocked", "action": action, "reason": decision["reason"]}
        return {"status": "executed", "action": action, "result": self.dispatch(action, payload or {})}
