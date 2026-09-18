"""Small guard used at the runtime boundary."""
from autonomous_core.approval_context import ApprovalContext

class RuntimeGuard:
    def check(self, critical=False, context=None):
        context = context or ApprovalContext()
        if critical and not context.allows():
            return {"allowed": False, "reason": "owner_approval_required"}
        return {"allowed": True, "reason": "allowed"}
