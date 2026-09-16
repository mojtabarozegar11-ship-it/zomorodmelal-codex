"""
Master Agent Runtime Service

Keeps the orchestration runtime separated from deployment concerns.
The service starts the supervisor loop when configured by the owner.
"""

import os
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("master_agent_runtime")


def owner_approval_required():
    return os.getenv("OWNER_APPROVAL_REQUIRED", "true").lower() == "true"


def run():
    logger.info("Master Agent runtime starting")
    logger.info("Owner approval required: %s", owner_approval_required())

    # Supervisor integration point.
    # The concrete supervisor import remains isolated so deployment can
    # configure the correct runtime module.
    while True:
        logger.info("Master Agent heartbeat")
        time.sleep(int(os.getenv("MASTER_HEARTBEAT_SECONDS", "300")))


if __name__ == "__main__":
    run()
