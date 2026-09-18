from autonomous_core.execution_policy import ExecutionPolicy
from autonomous_core.policy_adapter import PolicyAdapter


def test_adapter_blocks_without_approval():
    result = PolicyAdapter(ExecutionPolicy()).check("deploy")
    assert result["allowed"] is False
    assert result["action"] == "deploy"


def test_adapter_allows_with_approval():
    result = PolicyAdapter(ExecutionPolicy()).check("deploy", approved=True)
    assert result["allowed"] is True
