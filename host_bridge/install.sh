#!/usr/bin/env bash
set -euo pipefail

ROOT="${HOST_BRIDGE_ROOT:-/home/zomorodm/zomorodmelal-app}"
TOKEN_FILE="${HOST_BRIDGE_TOKEN_FILE:-/home/zomorodm/.host_bridge_token}"
AUDIT_FILE="${HOST_BRIDGE_AUDIT_FILE:-/home/zomorodm/.host_bridge_audit.log}"

if [ ! -d "$ROOT" ]; then
  echo "Host Bridge root not found: $ROOT" >&2
  exit 1
fi

mkdir -p "$(dirname "$TOKEN_FILE")"
touch "$TOKEN_FILE"
chmod 600 "$TOKEN_FILE"
touch "$AUDIT_FILE"
chmod 600 "$AUDIT_FILE"

echo "Host Bridge host prerequisites prepared."
echo "ROOT=$ROOT"
echo "TOKEN_FILE=$TOKEN_FILE"
echo "AUDIT_FILE=$AUDIT_FILE"
echo "Next: deploy host_bridge/ to the web root and configure a strong token in TOKEN_FILE."
