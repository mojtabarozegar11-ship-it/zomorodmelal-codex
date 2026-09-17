"""Runtime monitoring layer for Auto Agent.

Tracks health signals from Scheduler, Worker, Queue and Execution Engine.
"""

from datetime import datetime


class RuntimeMonitor:
    def __init__(self):
        self.events = []

    def record(self, component, status, detail=None):
        self.events.append({
            "component": component,
            "status": status,
            "detail": detail,
            "time": datetime.utcnow().isoformat(),
        })

    def health(self):
        return {
            "status": "ok",
            "events": len(self.events),
        }
