from master_agent.runtime import CanonicalMasterAgent

def test_canonical_runtime_health():
    agent = CanonicalMasterAgent()
    health = agent.health()
    assert health["status"] == "ready"
    assert health["kernel"].endswith("MasterCore")
    assert health["execution_mode"] == "sandbox_control_plane"
    assert health["owner_approval_required"] is True
    assert health["real_world_execution"] is False

def test_canonical_runtime_check():
    agent = CanonicalMasterAgent()
    result = agent.check()
    assert result["ready"] is True
    assert all(item["passed"] for item in result["checks"])

def test_canonical_runtime_cycle_is_sandbox_only(tmp_path):
    agent = CanonicalMasterAgent(tmp_path)
    result = agent.run_once("canonical runtime smoke test")
    assert result["runtime"] == agent.RUNTIME_NAME
    assert result["execution_mode"] == "sandbox_control_plane"
    assert result["safety"]["sandbox_only"] is True
    assert result["safety"]["real_deployment"] is False
    assert result["safety"]["owner_approval_required"] is True
