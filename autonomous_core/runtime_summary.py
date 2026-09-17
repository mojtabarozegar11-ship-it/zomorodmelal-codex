class RuntimeSummary:
    def build(self, status, events):
        return {
            "status": status,
            "events": len(events)
        }
