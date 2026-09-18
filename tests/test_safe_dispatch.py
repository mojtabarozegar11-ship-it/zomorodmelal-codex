from autonomous_core.safe_dispatch import SafeDispatch

class Policy:
    def check(self, action, approved):
        if action == "critical" and not approved:
            return {"allowed": False, "reason": "approval required"}
        return {"allowed": True}

def executor(action, payload):
    return {"action": action, "payload": payload}

def test_critical_action_requires_approval():
    result = SafeDispatch(Policy(), executor).dispatch("critical")
    assert result.status == "waiting_approval"

def test_approved_action_executes():
    result = SafeDispatch(Policy(), executor).dispatch("critical", {"x": 1}, approved=True)
    assert result.ok
    assert result.executed == ["critical"]
