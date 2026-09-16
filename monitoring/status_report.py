"""Status report generator for Master Agent."""

from .health_check import status


def build_report():
    data = status()
    lines = ["MASTER AGENT STATUS"]
    lines.append(f"Approval: {'ENABLED' if data['approval_required'] else 'DISABLED'}")
    lines.append("Providers:")
    for name, enabled in data["providers"].items():
        lines.append(f"- {name}: {'READY' if enabled else 'OFF'}")
    return "\n".join(lines)
