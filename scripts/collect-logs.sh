#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/logs"
mkdir -p "$OUT"
{
  echo "=== UTC ==="
  date -u
  echo
  echo "=== GIT ==="
  git -C "$ROOT" status --short
  git -C "$ROOT" log -5 --oneline
  echo
  echo "=== PYTHON ==="
  python --version || true
  echo
  echo "=== DJANGO CHECK ==="
  cd "$ROOT/django_project"
  python manage.py check 2>&1 || true
  echo
  echo "=== DEPLOY CHECK ==="
  python manage.py check --deploy 2>&1 || true
} > "$OUT/failure-report.txt"
echo "$OUT/failure-report.txt"
