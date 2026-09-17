from autonomous_core.master_core_connector import MasterCoreConnector


def test_connector_health():
    connector = MasterCoreConnector(None, object())
    result = connector.health()
    assert result["cycle"] is True
