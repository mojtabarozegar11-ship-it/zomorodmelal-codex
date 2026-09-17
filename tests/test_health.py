from app.health.check import HealthCheck


def test_health():
    result = HealthCheck().status()
    assert result["status"] == "ready"
