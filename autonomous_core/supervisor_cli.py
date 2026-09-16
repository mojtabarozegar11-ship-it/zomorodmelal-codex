from __future__ import annotations

import argparse
import json
import os

from .supervisor import AutonomousSupervisor


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the safe autonomous supervisor.")
    parser.add_argument(
        "--interval",
        type=int,
        default=int(os.environ.get("SUPERVISOR_INTERVAL_SECONDS", "300")),
        help="seconds between safe cycles",
    )
    parser.add_argument("--goal", default=os.environ.get("MASTER_AGENT_GOAL"), help="optional initial goal")
    parser.add_argument("--once", action="store_true", help="run one safe cycle and exit")
    parser.add_argument("--stop", action="store_true", help="request a running supervisor to stop")
    parser.add_argument("--status", action="store_true", help="show current supervisor runtime status")
    args = parser.parse_args()

    supervisor = AutonomousSupervisor(interval_seconds=args.interval)
    if args.status:
        print(json.dumps(supervisor.status(), ensure_ascii=False, indent=2))
    elif args.stop:
        supervisor.set_desired_state("stopped")
        print(json.dumps(supervisor.status(), ensure_ascii=False, indent=2))
    elif args.once:
        supervisor.run_once(args.goal)
    else:
        supervisor.set_desired_state("running")
        supervisor.run_forever(args.goal)


if __name__ == "__main__":
    main()
