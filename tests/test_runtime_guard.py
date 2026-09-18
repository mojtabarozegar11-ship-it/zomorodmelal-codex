from autonomous_core.runtime_guard import RuntimeGuard
from autonomous_core.approval_context import ApprovalContext

def test_critical_action_is_blocked_without_context():
    assert RuntimeGuard().check(critical=True)["allowed"] is False

def test_critical_action_is_allowed_with_approval():
    context = ApprovalContext(approved=True, request_id=11)
    assert RuntimeGuard().check(critical=True, context=context)["allowed"] is True
