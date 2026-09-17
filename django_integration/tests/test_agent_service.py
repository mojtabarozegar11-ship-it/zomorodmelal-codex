from django_integration.agent_service import AgentService


def test_agent_service_without_runner():
    service = AgentService()
    result = service.run("test goal")
    assert result["status"] == "pending"
