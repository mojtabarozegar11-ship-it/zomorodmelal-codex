from autonomous_core.integration_bridge import IntegrationBridge


class DummyRuntime:
    def execute(self, task):
        return task


def test_bridge_dispatch():
    bridge = IntegrationBridge(None, DummyRuntime())
    assert bridge.dispatch('task') == 'task'
