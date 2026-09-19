from worker_mojtaba.api.service import WorkerService


def test_audit_receives_authorization_result_state(tmp_path):
    service = WorkerService()
    service.audit.path = tmp_path / "audit.jsonl"
    service.policy.allowed = {"calendar_event"}

    result = service.handle("کیف پول")
    assert result["execution"]["result_state"] == "blocked"

    lines = service.audit.path.read_text(encoding="utf-8").strip().splitlines()
    assert lines
    assert '"authorized": false' in lines[-1]
    assert '"execution_status": "blocked"' in lines[-1]
