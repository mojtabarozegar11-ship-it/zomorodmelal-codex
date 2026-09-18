from app.system.execution_logger import ExecutionLogger


def test_logger():
    logger = ExecutionLogger()
    logger.log("START", "system started")
    assert len(logger.report()) == 1
