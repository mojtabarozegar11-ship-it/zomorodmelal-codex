from autonomous_core.execution_policy import ExecutionPolicy
from autonomous_core.safe_dispatch import SafeDispatch
from autonomous_core.runtime_entrypoint import RuntimeEntrypoint

def test_policy_blocks_without_approval():
    policy = ExecutionPolicy(owner_approval_required=True)
    result = SafeDispatch(policy, lambda action, payload: True).dispatch("critical")
    assert result.status == "waiting_approval"
    assert result.pending_approval == ["critical"]

def test_policy_allows_after_approval():
    policy = ExecutionPolicy(owner_approval_required=True)
    result = SafeDispatch(policy, lambda action, payload: payload).dispatch("critical", {"ok": True}, approved=True)
    assert result.ok
    assert result.data["result"] == {"ok": True}

def test_runtime_entrypoint_noncritical_path_executes():
    result = RuntimeEntrypoint(lambda action, payload: {"action": action, "payload": payload}).run("inspect", {"x": 1})
    assert result["status"] == "executed"
    assert result["result"]["action"] == "inspect"
