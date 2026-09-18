from autonomous_core.runtime_guard import RuntimeGuard
from autonomous_core.approval_context import ApprovalContext

def test_noncritical_action_allowed_without_approval():
    assert RuntimeGuard().check(critical=False)["allowed"] is True

def test_critical_action_denied_without_approval():
    assert RuntimeGuard().check(critical=True)["allowed"] is False

def test_critical_action_allowed_with_approved_context():
    context = ApprovalContext(approved=True, request_id=21)
    assert RuntimeGuard().check(critical=True, context=context)["allowed"] is True
