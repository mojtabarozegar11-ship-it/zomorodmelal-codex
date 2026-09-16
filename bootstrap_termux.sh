#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/master_agent"
REPO="https://github.com/mojtabarozegar11-ship-it/zomorodmelal-codex.git"
BRANCH="main"

if [ ! -d "$ROOT/.git" ]; then
  git clone --branch "$BRANCH" "$REPO" "$ROOT"
else
  git -C "$ROOT" fetch origin "$BRANCH"
  git -C "$ROOT" checkout "$BRANCH"
  git -C "$ROOT" pull --ff-only origin "$BRANCH"
fi

cd "$ROOT"
mkdir -p data/sandbox data/change_packages
python -m compileall -q autonomous_core approval controller testing evaluation evolution
python -m autonomous_core.supervisor --once
python -m autonomous_core.supervisor --status

echo "Master Agent safe autonomous runtime is ready."
echo "Sandbox work runs automatically; real deployment remains owner-approved."
exec python -m autonomous_core.supervisor
