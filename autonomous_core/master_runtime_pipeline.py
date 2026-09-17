class MasterRuntimePipeline:
    def __init__(self, registry, policy, adapter):
        self.registry = registry
        self.policy = policy
        self.adapter = adapter

    def run(self, goal):
        return self.adapter.dispatch(goal)
