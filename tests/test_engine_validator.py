from app.core.engine_validator import EngineValidator


def test_engine_validator():
    validator = EngineValidator()
    result = validator.validate({"core": True, "agents": True})
    assert result["status"] == "ready"
