class E2ECycleRunner:
    def __init__(self, pipeline, reporter):
        self.pipeline = pipeline
        self.reporter = reporter

    def run(self, goal):
        result = self.pipeline.execute(goal)
        return self.reporter.build(result)
