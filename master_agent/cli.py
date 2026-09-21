"""CLI for the canonical Master Agent runtime."""
from __future__ import annotations
import argparse
import json
from typing import Sequence
from .runtime import CanonicalMasterAgent

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Zomorod Melal Canonical Master Agent")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--goal")
    parser.add_argument("--json", action="store_true")
    return parser

def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    agent = CanonicalMasterAgent()
    if args.check:
        payload = agent.check()
    elif args.status:
        payload = agent.status()
    elif args.once:
        payload = agent.run_once(args.goal)
    else:
        payload = agent.check()
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload.get("ready", True) else 1

if __name__ == "__main__":
    raise SystemExit(main())
