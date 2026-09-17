class AutonomousCycleBridge:
    def __init__(self, runtime, reporter):
        self.runtime = runtime
        self.reporter = reporter

    def run_cycle(self, goal):
        result = self.runtime.execute(goal)
        return self.reporter.create(result)
