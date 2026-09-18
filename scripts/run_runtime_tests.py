"""Deterministic local test runner for the Master Agent runtime."""
import os
import subprocess
import sys

def main():
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    env["AUTONOMOUS_CYCLE_INNER_TESTS"] = "1"
    return subprocess.call([sys.executable, "-m", "pytest", "-q"], env=env)

if __name__ == "__main__":
    raise SystemExit(main())
