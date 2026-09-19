"""Provider-agnostic media capability registry."""

class MediaCapability:
    SUPPORTED = ("text_to_image", "image_edit", "text_to_video", "image_to_video", "text_to_audio")

    def supports(self, capability: str) -> bool:
        return capability in self.SUPPORTED

    def describe(self) -> list[str]:
        return list(self.SUPPORTED)
