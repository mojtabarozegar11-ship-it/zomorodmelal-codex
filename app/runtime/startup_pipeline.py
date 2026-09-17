class StartupPipeline:
    def __init__(self):
        self.steps = []

    def add_step(self, name):
        self.steps.append(name)

    def status(self):
        return {
            "pipeline": "ready",
            "steps": self.steps
        }
