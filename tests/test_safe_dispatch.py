from autonomous_core.execution_policy import ExecutionPolicy
from autonomous_core.safe_dispatch import SafeDispatch


def executor(action, payload):
    return {"action": action, "payload": payload}


def test_critical_action_requires_approval():
    result = SafeDispatch(ExecutionPolicy(), executor).dispatch("critical")
    assert result.status == "waiting_approval"
    assert result.pending_approval == ["critical"]


def test_approved_action_executes():
    result = SafeDispatch(ExecutionPolicy(), executor).dispatch(
        "critical", {"x": 1}, approved=True
    )
    assert result.ok
    assert result.executed == ["critical"]
    assert result.data["result"]["payload"] == {"x": 1}


def test_policy_without_approval_requirement_executes():
    policy = ExecutionPolicy(owner_approval_required=False)
    result = SafeDispatch(policy, executor).dispatch("inspect", {"x": 1})
    assert result.ok
