def test_integration_health():
    from django_project.api.integration_health import integration_status

    result = integration_status()

    assert result["status"] == "connected_layer"
