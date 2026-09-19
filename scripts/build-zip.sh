#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/dist"
rm -rf "$OUT"
mkdir -p "$OUT"
cd "$ROOT"
git archive --format=zip --output="$OUT/zomorodmelal-cpanel.zip" HEAD
echo "Created $OUT/zomorodmelal-cpanel.zip"
