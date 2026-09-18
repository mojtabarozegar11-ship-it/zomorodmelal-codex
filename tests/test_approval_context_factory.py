from autonomous_core.approval_context_factory import approved_context, denied_context

def test_denied_context_defaults_to_no_approval():
    context = denied_context(3)
    assert context.approved is False
    assert context.request_id == 3

def test_approved_context_requires_request_id():
    context = approved_context(8)
    assert context.approved is True
    assert context.request_id == 8
