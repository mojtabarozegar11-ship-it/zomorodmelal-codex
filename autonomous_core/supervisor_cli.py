from __future__ import annotations

import argparse

from .supervisor import AutonomousSupervisor


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the safe autonomous supervisor.")
    parser.add_argument("--interval", type=int, default=300, help="seconds between safe cycles")
    parser.add_argument("--goal", default=None, help="optional initial goal")
    args = parser.parse_args()
    AutonomousSupervisor(interval_seconds=args.interval).run_forever(args.goal)


if __name__ == "__main__":
    main()
