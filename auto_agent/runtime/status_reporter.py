"""Runtime status reporting layer.

Collects basic execution state and exposes a simple report structure
for Master Agent monitoring and CI integrations.
"""

from datetime import datetime, timezone


class StatusReporter:
    def build_report(self, component_states):
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "components": component_states,
            "status": "healthy" if all(component_states.values()) else "degraded",
        }

    def summary(self, report):
        return {
            "status": report["status"],
            "checked_at": report["timestamp"],
        }
