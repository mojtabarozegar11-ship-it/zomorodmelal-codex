"""
Production launcher for Auto Agent Runtime.
Connects startup flow to runtime components.
"""

class ProductionLauncher:
    def __init__(self, runtime):
        self.runtime = runtime

    def start(self):
        return self.runtime.start()

    def stop(self):
        return self.runtime.stop()
