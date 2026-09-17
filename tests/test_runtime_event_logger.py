from autonomous_core.runtime_event_logger import RuntimeEventLogger


def test_event_logger():
    logger = RuntimeEventLogger()
    logger.record("boot")
    assert len(logger.all()) == 1
