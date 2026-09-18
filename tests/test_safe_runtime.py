from execution.safe_runtime import SafeRuntime

class FakeController:
    def execute(self, request_id, action, approved=False, files=None):
        return {"request_id": request_id, "action": action, "approved": approved, "files": files}

    def status(self):
        return {"owner_approval_required": True, "project_promotion": False}

def test_safe_runtime_delegates_to_existing_controller():
    runtime = SafeRuntime(FakeController())
    result = runtime.stage(7, "critical_change", ["README.md"], approved=False)
    assert result["request_id"] == 7
    assert result["approved"] is False
    assert result["files"] == ["README.md"]

def test_safe_runtime_exposes_status():
    status = SafeRuntime(FakeController()).status()
    assert status["owner_approval_required"] is True
    assert status["project_promotion"] is False
