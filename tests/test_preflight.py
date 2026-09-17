def test_preflight_import():
    from app.runtime.preflight import PreFlight
    check = PreFlight()
    check.add_check("core", True)
    assert check.run() is True
