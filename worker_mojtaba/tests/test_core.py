from worker_mojtaba.api.service import WorkerService

def test_service_handles_request():
    result = WorkerService().handle("یک کار آزمایشی انجام بده")
    assert result["status"] == "ready"
    assert result["plan"]
