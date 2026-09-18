from autonomous_core.approval_context import ApprovalContext

def test_default_context_denies_execution():
    assert ApprovalContext().allows() is False

def test_approved_context_allows_execution():
    assert ApprovalContext(approved=True, request_id=5).allows() is True
