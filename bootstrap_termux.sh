#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/master_agent"
REPO="https://github.com/mojtabarozegar11-ship-it/zomorodmelal-codex.git"
BRANCH="master-agent-final-safe"

if [ ! -d "$ROOT/.git" ]; then
  git clone --branch "$BRANCH" "$REPO" "$ROOT"
else
  git -C "$ROOT" fetch origin "$BRANCH"
  git -C "$ROOT" checkout "$BRANCH"
  git -C "$ROOT" pull --ff-only origin "$BRANCH"
fi

cd "$ROOT"
python -m compileall -q autonomous_core approval controller testing evaluation evolution site_integration
mkdir -p data/sandbox data/change_packages
python -m autonomous_core.supervisor --status

echo "Master Agent installed in $ROOT"
echo "Safe mode: Sandbox only; real changes require owner approval."
echo "Start: cd $ROOT && python -m autonomous_core.supervisor"
