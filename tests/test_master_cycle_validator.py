from autonomous_core.master_cycle_validator import MasterCycleValidator

def test_validator():
    result = MasterCycleValidator().validate("cycle")
    assert result["valid"] is True
