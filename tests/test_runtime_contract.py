from autonomous_core.runtime_contract import RuntimeResult

def test_runtime_result_defaults():
    result = RuntimeResult(status="ok")
    assert result.ok is True
    assert result.executed == []

def test_runtime_result_pending_approval():
    result = RuntimeResult(status="waiting_approval", pending_approval=["deploy"])
    assert result.ok is False
    assert result.pending_approval == ["deploy"]
