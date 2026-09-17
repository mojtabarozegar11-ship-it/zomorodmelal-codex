"""Stage 34 runtime event bus."""

class RuntimeEventBus:
    def publish(self, event):
        return {"event": event, "published": True}
