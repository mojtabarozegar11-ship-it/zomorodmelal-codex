#!/usr/bin/env bash
set -euo pipefail

: "${HOST_BRIDGE_URL:?HOST_BRIDGE_URL is required}"
: "${HOST_BRIDGE_TOKEN:?HOST_BRIDGE_TOKEN is required}"

payload="$(python - <<'PY'
import json, os
keys = [
    "status", "repository", "branch", "commit", "workflow",
    "run_id", "run_number", "job", "message", "error",
    "timestamp", "environment"
]
out = {}
for k in keys:
    v = os.environ.get(k)
    if v:
        out[k] = v[:4000]
print(json.dumps(out, ensure_ascii=False))
PY
)"

curl --fail --silent --show-error \
  --connect-timeout 10 \
  --max-time 20 \
  -X POST "$HOST_BRIDGE_URL" \
  -H "Content-Type: application/json" \
  -H "X-Bridge-Token: $HOST_BRIDGE_TOKEN" \
  --data "$payload"
