"""Events exchanged between Django and Master Agent."""


class WebsiteEvent:
    def __init__(self, name, payload=None):
        self.name = name
        self.payload = payload or {}

    def to_dict(self):
        return {
            "event": self.name,
            "payload": self.payload
        }
