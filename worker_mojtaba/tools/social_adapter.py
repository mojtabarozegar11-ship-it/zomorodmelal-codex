"""Tool Center adapter for authorized social-media publishing."""
from typing import Any
from worker_mojtaba.social.publisher import PublishRequest, SocialPublisher
from worker_mojtaba.tools.adapter import ToolAdapter

class SocialPublishingToolAdapter(ToolAdapter):
    name = "social"
    def __init__(self) -> None:
        self.publisher = SocialPublisher()
    def capabilities(self) -> list[str]:
        return list(self.publisher.capabilities)
    def execute(self, capability: str, payload: dict[str, Any]) -> dict[str, Any]:
        request = payload.get("request", "")
        if capability == "publish_video":
            return self.publisher.publish_video(PublishRequest(media_path=request))
        if capability == "schedule_video":
            return self.publisher.schedule_video(PublishRequest(media_path=request), payload.get("publish_at", "owner-configured"))
        if capability == "list_channels":
            return self.publisher.list_channels()
        if capability == "publish_status":
            return {"status": "provider_connection_required"}
        raise ValueError(f"Unsupported capability: {capability}")
