#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

INTERVAL_SECONDS="${SUPERVISOR_INTERVAL_SECONDS:-300}"
GOAL="${MASTER_AGENT_GOAL:-}"

if ! [[ "$INTERVAL_SECONDS" =~ ^[0-9]+$ ]] || [ "$INTERVAL_SECONDS" -lt 1 ]; then
  echo "SUPERVISOR_INTERVAL_SECONDS must be a positive integer" >&2
  exit 2
fi

export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
exec python -m autonomous_core.supervisor --interval "$INTERVAL_SECONDS" ${GOAL:+--goal "$GOAL"}
