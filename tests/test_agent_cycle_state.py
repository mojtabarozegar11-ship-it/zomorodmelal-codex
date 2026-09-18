from autonomous_core.agent_cycle_state import AgentCycleState

def test_state_update():
    state = AgentCycleState()
    assert state.set_status("running") == "running"
