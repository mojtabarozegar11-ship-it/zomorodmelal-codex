class E2ERuntimePipeline:
    def __init__(self, orchestrator, health_monitor):
        self.orchestrator = orchestrator
        self.health_monitor = health_monitor

    def run(self, task):
        health = self.health_monitor.check()
        if not health.get("healthy", False):
            return {"status": "blocked", "reason": "runtime unhealthy"}
        return self.orchestrator.dispatch(task)
