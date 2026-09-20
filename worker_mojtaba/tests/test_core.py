from worker_mojtaba.api.service import WorkerService

def test_service_handles_request():
    result = WorkerService().handle("یک کار آزمایشی انجام بده")
    assert result["status"] == "completed"
    assert result["plan"]


def test_tool_center_rejects_unknown_adapter():
    from worker_mojtaba.tools.center import ToolCenter
    import pytest
    with pytest.raises(KeyError):
        ToolCenter().execute("missing", "text_to_video", {})

def test_media_adapter_requires_provider():
    from worker_mojtaba.tools.media_adapter import MediaToolAdapter
    result = MediaToolAdapter().execute("text_to_video", {"prompt": "test"})
    assert result["status"] == "provider_required"
