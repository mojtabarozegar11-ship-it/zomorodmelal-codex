from autonomous_core.runtime_entrypoint import RuntimeEntrypoint
from autonomous_core.approval_context import ApprovalContext

class Guard:
    def check(self, critical, context):
        return {"allowed": (not critical) or context.allows(), "reason": "owner_approval_required"}

def test_critical_action_blocks_by_default():
    result = RuntimeEntrypoint(lambda a, p: True, Guard()).run("deploy", critical=True)
    assert result["status"] == "blocked"

def test_critical_action_runs_with_owner_approval():
    context = ApprovalContext(approved=True, request_id=9)
    result = RuntimeEntrypoint(lambda a, p: p, Guard()).run("deploy", {"ok": True}, critical=True, context=context)
    assert result["status"] == "executed"
    assert result["result"] == {"ok": True}
