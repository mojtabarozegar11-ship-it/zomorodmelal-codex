from autonomous_core.master_runtime_pipeline import MasterRuntimePipeline


def test_pipeline_dispatch():
    class Adapter:
        def dispatch(self, goal):
            return goal

    pipeline = MasterRuntimePipeline(None, None, Adapter())
    assert pipeline.run('test') == 'test'
