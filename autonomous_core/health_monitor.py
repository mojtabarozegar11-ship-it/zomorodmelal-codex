class HealthMonitor:
    def __init__(self):
        self.status = 'ready'

    def check(self):
        return {'status': self.status}
