"""Registry of Android capabilities exposed by adapters."""

class DeviceCapabilityRegistry:
    DEFAULT = (
        "storage", "notifications", "camera", "microphone",
        "accessibility", "apps", "termux"
    )

    def list(self) -> list[str]:
        return list(self.DEFAULT)

    def supports(self, capability: str) -> bool:
        return capability in self.DEFAULT
