from autonomous_core.execution_policy import ExecutionPolicy


def test_policy_blocks_without_approval():
    policy = ExecutionPolicy()
    assert policy.can_execute(False) is False
