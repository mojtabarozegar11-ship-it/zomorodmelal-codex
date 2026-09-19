# Galaxy A9 Termux ↔ GitHub Device Bridge

This bridge provides a controlled command channel between Termux on the Galaxy A9 and GitHub.

## Privacy requirement
The GitHub repository MUST be PRIVATE before the bridge is enabled. Device reports may contain local information.

After verifying the repository is private:
```bash
export DEVICE_BRIDGE_REPO_GUARD=verified-private
```

## Install
```bash
git clone -b device-bridge-galaxy-a9 git@github.com:mojtabarozegar11-ship-it/zomorodmelal-codex.git ~/zomorodmelal-codex
cd ~/zomorodmelal-codex
export DEVICE_BRIDGE_REPO_GUARD=verified-private
python device_bridge/termux_bridge.py
```

Allowed actions: ping, storage_summary, list_top_level, delete_path.
There is NO arbitrary shell-command execution. File deletion is limited to a single file under safe roots and requires confirm=true; directory deletion is disabled.

Commands are JSON files under device_bridge/commands/. Results are written to device_bridge/results/ and processed commands are moved to device_bridge/archive/.
