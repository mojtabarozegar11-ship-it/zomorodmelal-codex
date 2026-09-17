"""Create runtime health snapshots."""

from datetime import datetime

def snapshot(status="unknown"):
    return {"status": status, "time": datetime.utcnow().isoformat()}
