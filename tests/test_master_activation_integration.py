from autonomous_core.master_core import MasterCore


def test_master_core_activation_check_records_safe_decision(tmp_path):
    core = MasterCore(tmp_path)
    request = core.access_manager.request("web_research", "research market")
    core.access_manager.approve(request["request_id"])

    decision = core.check_activation(request["request_id"], "web_research")

    assert decision["authorized"] is True
    assert decision["owner_approval_required"] is True
    assert decision["credentials_acquired"] is False
    assert decision["activated"] is False
    assert decision["external_action_allowed"] is False
    assert core.state["activation_checks"][-1]["request_id"] == request["request_id"]


def test_master_core_activation_check_rejects_unapproved_request(tmp_path):
    core = MasterCore(tmp_path)
    request = core.access_manager.request("web_research", "research market")

    try:
        core.check_activation(request["request_id"], "web_research")
    except PermissionError:
        pass
    else:
        raise AssertionError("unapproved access request must not pass activation gate")
