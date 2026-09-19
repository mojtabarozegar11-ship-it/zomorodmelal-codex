from pathlib import Path

from worker_mojtaba.evolution.audited_controller import AuditedUpgradeController


def test_audited_upgrade_records_approved_result(tmp_path: Path):
    audit_path = tmp_path / "audit.jsonl"
    controller = AuditedUpgradeController()
    controller.audit = __import__(
        "worker_mojtaba.security.audit", fromlist=["AuditLog"]
    ).AuditLog(str(audit_path))

    result = controller.run("1.0.0", ["improve-memory"], lambda: True)

    assert result.action == "awaiting_owner_approval"
    events = controller.audit.tail()
    assert events[-1]["action"] == "evolution_upgrade"
    assert events[-1]["status"] == "approved"
    assert events[-1]["metadata"]["checkpoint_id"] == "1.0.0-pre-upgrade"


def test_audited_upgrade_records_rejected_result(tmp_path: Path):
    from worker_mojtaba.security.audit import AuditLog

    audit = AuditLog(str(tmp_path / "audit.jsonl"))
    controller = AuditedUpgradeController(audit=audit)
    result = controller.run("1.0.0", ["bad-change"], lambda: False)

    assert result.action == "rollback_available"
    events = audit.tail()
    assert events[-1]["status"] == "rejected"
    assert events[-1]["metadata"]["tests_passed"] is False
