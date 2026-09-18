"""Read-only health probe for the guarded autonomous runtime."""


class RuntimeHealthProbe:
    def __init__(self, runtime):
        self.runtime = runtime

    def snapshot(self):
        status = self.runtime.status()
        return {
            "healthy": bool(status),
            "owner_approval_required": bool(status.get("owner_approval_required", True)),
            "project_promotion": bool(status.get("project_promotion", False)),
            "external_deployment": bool(status.get("external_deployment", False)),
            "generated_code_executed": bool(status.get("generated_code_executed", False)),
        }
