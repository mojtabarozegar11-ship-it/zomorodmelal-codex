from fastapi.testclient import TestClient

from worker_mojtaba.api.server import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_task_endpoint():
    response = client.post("/v1/tasks", json={"request": "سلام"})
    assert response.status_code == 200
    body = response.json()
    assert body["request"] == "سلام"
    assert "plan" in body
    assert "ai" in body
