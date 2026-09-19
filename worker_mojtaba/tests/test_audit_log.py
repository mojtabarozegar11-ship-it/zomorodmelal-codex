from worker_mojtaba.security.audit import AuditLog


def test_audit_record_returns_event_and_tail_reads_json(tmp_path):
    path = tmp_path / "audit.jsonl"
    log = AuditLog(str(path))

    event = log.record(
        "task",
        "blocked",
        {"capability": "wallet", "authorized": False},
    )

    assert event.status == "blocked"
    assert log.tail(1)[0]["metadata"]["authorized"] is False
