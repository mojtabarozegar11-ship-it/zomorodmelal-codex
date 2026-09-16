from __future__ import annotations

import argparse
import json
import os

from .autonomous_cycle_100 import AutonomousCycle100
from .supervisor import AutonomousSupervisor


class MasterAgent100Supervisor(AutonomousSupervisor):
    """Supervisor whose default autonomous cycle is controlled by Master Agent 100."""

    def __init__(self, project_root=None, interval_seconds=300, cycle_factory=None):
        super().__init__(
            project_root=project_root,
            interval_seconds=interval_seconds,
            cycle_factory=cycle_factory or AutonomousCycle100,
        )

    def status(self):
        result = super().status()
        result.update({
            "master_agent": "MasterAgent100",
            "master_version": "100.0.0",
            "max_generation": 100,
            "owner_approval_required": True,
            "real_changes_allowed": False,
        })
        return result


def _parse_args():
    parser = argparse.ArgumentParser(description="Run Master Agent 100 safe autonomous supervisor")
    parser.add_argument("--goal", default=os.environ.get("MASTER_AGENT_GOAL"))
    parser.add_argument("--interval", type=int, default=int(os.environ.get("SUPERVISOR_INTERVAL_SECONDS", "300")))
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--stop", action="store_true")
    parser.add_argument("--status", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    supervisor = MasterAgent100Supervisor(interval_seconds=args.interval)
    if args.status:
        print(json.dumps(supervisor.status(), ensure_ascii=False, indent=2))
    elif args.stop:
        supervisor.set_desired_state("stopped")
        print(json.dumps(supervisor.status(), ensure_ascii=False, indent=2))
    elif args.once:
        print(json.dumps(supervisor.run_once(args.goal), ensure_ascii=False, indent=2))
    else:
        supervisor.set_desired_state("running")
        supervisor.run_forever(args.goal)
