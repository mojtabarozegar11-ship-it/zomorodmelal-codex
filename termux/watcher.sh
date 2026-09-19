#!/data/data/com.termux/files/usr/bin/bash
set -u
REPO="${REPO:-$HOME/zomorodmelal-codex}"
BRANCH="${BRANCH:-fix/all-errors-2026-09-19}"
INTERVAL="${INTERVAL:-300}"
cd "$REPO" || exit 1
while true; do
  echo "[$(date)] checking $BRANCH"
  git fetch origin --prune
  LOCAL="$(git rev-parse "$BRANCH" 2>/dev/null || true)"
  REMOTE="$(git rev-parse "origin/$BRANCH" 2>/dev/null || true)"
  if [ -n "$REMOTE" ] && [ "$LOCAL" != "$REMOTE" ]; then
    git checkout "$BRANCH"
    git pull --ff-only origin "$BRANCH" || true
  fi
  git status --short
  git log -1 --oneline
  sleep "$INTERVAL"
done
