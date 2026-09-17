class PreFlight:
    def __init__(self):
        self.checks = []

    def add_check(self, name, status=True):
        self.checks.append({"name": name, "status": status})

    def run(self):
        return all(item["status"] for item in self.checks)
