def test_validation_gate():
    from autonomous_core.validation_gate import ValidationGate
    assert ValidationGate().validate({})
