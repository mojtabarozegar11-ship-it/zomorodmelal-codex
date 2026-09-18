"""Thin integration layer over the existing ExecutionController."""
from execution.execution_controller import ExecutionController

class SafeRuntime:
    def __init__(self, controller=None):
        self.controller = controller or ExecutionController()

    def stage(self, request_id, action, files=None, approved=False):
        return self.controller.execute(request_id, action, approved=approved, files=files or [])

    def status(self):
        return self.controller.status()
