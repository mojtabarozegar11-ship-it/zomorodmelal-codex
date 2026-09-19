from worker_mojtaba.api.service import WorkerService
from worker_mojtaba.social.publisher import PublishRequest, SocialPublisher

def test_social_adapter_is_registered():
    capabilities = WorkerService().tool_center.list_capabilities()
    assert "social" in capabilities
    assert "publish_video" in capabilities["social"]

def test_publish_requires_real_provider_connection():
    result = SocialPublisher().publish_video(
        PublishRequest(media_path="/tmp/video.mp4", platforms=("youtube", "instagram"))
    )
    assert result["status"] == "provider_connection_required"
    assert result["platforms"] == ["youtube", "instagram"]

def test_publish_intent_routes_to_social():
    result = WorkerService().handle("انتشار ویدئو در یوتیوب")
    assert result["route"] == "social"
    assert result["intent"] == "social_publishing"
    assert result["execution"]["status"] == "provider_connection_required"
