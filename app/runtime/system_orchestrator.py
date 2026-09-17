class SystemOrchestrator:
    def __init__(self, startup, runner):
        self.startup = startup
        self.runner = runner

    def boot(self):
        checks = self.startup.run_checks()
        return {
            "status": "ready" if checks else "failed",
            "checks": checks
        }

    def execute(self, goal):
        return self.runner.run(goal)
