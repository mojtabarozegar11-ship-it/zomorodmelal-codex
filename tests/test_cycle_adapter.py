from autonomous_core.cycle_adapter import CycleAdapter


def test_cycle_adapter_exists():
    adapter = CycleAdapter(None, None)
    assert adapter is not None
