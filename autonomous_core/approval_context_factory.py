"""Create explicit approval contexts at runtime boundaries."""
from autonomous_core.approval_context import ApprovalContext

def denied_context(request_id=0):
    return ApprovalContext(approved=False, request_id=request_id)

def approved_context(request_id):
    return ApprovalContext(approved=True, request_id=request_id)
