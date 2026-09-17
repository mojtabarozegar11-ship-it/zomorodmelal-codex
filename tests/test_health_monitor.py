from autonomous_core.health_monitor import HealthMonitor


def test_health_ready():
    assert HealthMonitor().check()['status'] == 'ready'
