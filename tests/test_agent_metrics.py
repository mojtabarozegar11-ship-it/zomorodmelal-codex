from autonomous_core.agent_metrics import AgentMetrics


def test_metrics_record():
    metrics = AgentMetrics()
    metrics.record(True)
    assert metrics.summary()["successes"] == 1
