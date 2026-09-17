class AgentOrchestrationRuntime:
    def __init__(self, queue, memory, executor):
        self.queue = queue
        self.memory = memory
        self.executor = executor

    def submit(self, task):
        self.queue.add(task)
        self.memory.save('last_task', task)
        return task

    def process(self):
        task = self.queue.next()
        if task is None:
            return None
        return self.executor.execute(task)
