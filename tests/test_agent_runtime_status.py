from autonomous_core.agent_runtime_status import AgentRuntimeStatus


def test_status_change():
    status = AgentRuntimeStatus()
    status.set_status('running')
    assert status.get_status() == 'running'
