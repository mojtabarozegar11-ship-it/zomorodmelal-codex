"""Social publishing orchestration with explicit provider connections."""
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class PublishRequest:
    media_path: str
    title: str = ""
    description: str = ""
    platforms: tuple[str, ...] = ("youtube",)
    privacy: str = "private"

class SocialPublisher:
    name = "social_publisher"
    capabilities = ("publish_video", "schedule_video", "list_channels", "publish_status")

    def publish_video(self, request: PublishRequest) -> dict[str, Any]:
        return {"status":"provider_connection_required","media_path":request.media_path,"platforms":list(request.platforms),"privacy":request.privacy}

    def schedule_video(self, request: PublishRequest, publish_at: str) -> dict[str, Any]:
        return {**self.publish_video(request), "scheduled_for": publish_at}

    def list_channels(self) -> dict[str, Any]:
        return {"status":"provider_connection_required","channels":[]}
