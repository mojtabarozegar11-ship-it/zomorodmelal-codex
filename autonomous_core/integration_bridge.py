class IntegrationBridge:
    """Bridge runtime components without direct execution bypass."""

    def __init__(self, orchestrator, runtime):
        self.orchestrator = orchestrator
        self.runtime = runtime

    def dispatch(self, task):
        return self.runtime.execute(task)
