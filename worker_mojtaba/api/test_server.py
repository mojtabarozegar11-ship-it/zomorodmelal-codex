from fastapi.testclient import TestClient

from worker_mojtaba.api.server import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_task_endpoint_requires_auth():
    response = client.post("/v1/tasks", json={"request": "سلام"})
    assert response.status_code in (401, 503)


def test_task_endpoint_with_configured_auth(monkeypatch):
    monkeypatch.setenv("WORKER_API_TOKEN", "ci-test-token")
    response = client.post(
        "/v1/tasks",
        json={"request": "سلام"},
        headers={"Authorization": "Bearer ci-test-token"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["request"] == "سلام"
    assert "plan" in body
    assert "ai" in body


def test_task_endpoint_rejects_invalid_auth(monkeypatch):
    monkeypatch.setenv("WORKER_API_TOKEN", "ci-test-token")
    response = client.post(
        "/v1/tasks",
        json={"request": "سلام"},
        headers={"Authorization": "Bearer wrong-token"},
    )
    assert response.status_code == 401


def test_voice_requires_auth(monkeypatch):
    response = client.post(
        "/v1/voice",
        files={"audio": ("voice.m4a", b"audio", "audio/mp4")},
    )
    assert response.status_code in (401, 503)


def test_voice_size_limit(monkeypatch):
    monkeypatch.setenv("WORKER_API_TOKEN", "ci-test-token")
    oversized = b"x" * (10 * 1024 * 1024 + 1)
    response = client.post(
        "/v1/voice",
        files={"audio": ("voice.m4a", oversized, "audio/mp4")},
        headers={"Authorization": "Bearer ci-test-token"},
    )
    assert response.status_code == 413
