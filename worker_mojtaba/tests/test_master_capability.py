from worker_mojtaba.core.master_capability import MasterCapability

def test_master_requires_approval():
    master = MasterCapability()
    result = master.run("demo", approved=False, dispatch=lambda g, c: {"ok": True})
    assert result["status"] == "approval_required"

def test_master_dispatches_worker_runtime():
    master = MasterCapability()
    result = master.run("demo", approved=True, dispatch=lambda g, c: {"status": "completed"})
    assert result["status"] == "completed"
    assert result["validated"] is True
