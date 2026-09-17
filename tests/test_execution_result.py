from autonomous_core.execution_result import ExecutionResult


def test_execution_result():
    result = ExecutionResult(True, 'ok')
    assert result.success is True
