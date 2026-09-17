from autonomous_core.e2e_runtime_pipeline import E2ERuntimePipeline

class MockHealth:
    def check(self):
        return {"healthy": True}

class MockOrchestrator:
    def dispatch(self, task):
        return {"task": task, "status": "sent"}


def test_pipeline_dispatch():
    pipeline = E2ERuntimePipeline(MockOrchestrator(), MockHealth())
    assert pipeline.run("demo")["status"] == "sent"
