#!/usr/bin/env python3
from __future__ import annotations
import json, os, platform, shutil, subprocess, time
from pathlib import Path

ROOT = Path(os.environ.get("DEVICE_BRIDGE_ROOT", Path.home() / "zomorodmelal-codex"))
BRANCH = os.environ.get("DEVICE_BRIDGE_BRANCH", "device-bridge-galaxy-a9")
POLL_SECONDS = int(os.environ.get("DEVICE_BRIDGE_POLL_SECONDS", "30"))
COMMANDS = ROOT / "device_bridge" / "commands"
RESULTS = ROOT / "device_bridge" / "results"
ARCHIVE = ROOT / "device_bridge" / "archive"
REPO_GUARD = os.environ.get("DEVICE_BRIDGE_REPO_GUARD", "private-required")
ALLOWED_ACTIONS = {"ping", "storage_summary", "list_top_level", "delete_path"}
SAFE_ROOTS = [Path("/storage/emulated/0"), Path.home()]

def run_git(*args):
    p = subprocess.run(["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return p.stdout.strip()

def sync_in():
    run_git("fetch", "origin", BRANCH)
    run_git("checkout", BRANCH)
    run_git("reset", "--hard", f"origin/{BRANCH}")

def sync_out():
    run_git("add", "device_bridge")
    status = subprocess.run(["git","status","--porcelain","--","device_bridge"], cwd=ROOT, text=True, stdout=subprocess.PIPE, check=True).stdout.strip()
    if not status: return
    run_git("commit", "-m", "device bridge: device result")
    run_git("push", "origin", BRANCH)

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)

def under_safe_root(path):
    try: resolved = path.expanduser().resolve()
    except FileNotFoundError: resolved = path.expanduser().absolute()
    return any(resolved == root or root in resolved.parents for root in SAFE_ROOTS if root.exists())

def dispatch(cmd):
    action = cmd.get("action")
    if action == "ping":
        return {"ok": True, "device": {"platform": platform.platform(), "python": platform.python_version(), "termux_home": str(Path.home())}}
    if action == "storage_summary":
        target = Path("/storage/emulated/0")
        if not target.exists(): target = Path.home()
        total, used, free = shutil.disk_usage(target)
        return {"ok": True, "path": str(target), "bytes": {"total": total, "used": used, "free": free}}
    if action == "list_top_level":
        target = Path("/storage/emulated/0")
        if not target.exists(): target = Path.home()
        return {"ok": True, "path": str(target), "entries": [{"name":p.name,"type":"dir" if p.is_dir() else "file"} for p in sorted(target.iterdir(), key=lambda x:x.name.lower())]}
    if action == "delete_path":
        args = cmd.get("args") or {}
        if args.get("confirm") is not True: return {"ok":False,"error":"delete requires confirm=true"}
        path = Path(str(args.get("path","")).strip()).expanduser()
        if not str(path): return {"ok":False,"error":"missing path"}
        if not under_safe_root(path): return {"ok":False,"error":"path outside safe roots"}
        resolved = path.resolve()
        if resolved in {Path.home().resolve(), ROOT.resolve()} or ROOT.resolve() in resolved.parents: return {"ok":False,"error":"protected path"}
        if not path.exists(): return {"ok":False,"error":"path not found"}
        if path.is_dir(): return {"ok":False,"error":"directory deletion is disabled"}
        size = path.stat().st_size
        path.unlink()
        return {"ok":True,"deleted":str(path),"bytes":size}
    return {"ok":False,"error":"action not allowed","action":action}

def main():
    for d in (COMMANDS, RESULTS, ARCHIVE): d.mkdir(parents=True, exist_ok=True)
    if REPO_GUARD != "verified-private":
        print("SAFETY STOP: verify the GitHub repository is PRIVATE, then set DEVICE_BRIDGE_REPO_GUARD=verified-private")
        return
    while True:
        try:
            sync_in()
            for cmd_path in sorted(COMMANDS.glob("*.json")):
                try:
                    cmd = json.loads(cmd_path.read_text(encoding="utf-8"))
                    cmd_id = str(cmd.get("id") or cmd_path.stem)
                    result = {"id":cmd_id,"processed_at":time.strftime("%Y-%m-%dT%H:%M:%S%z"),"action":cmd.get("action"),"result":dispatch(cmd)}
                except Exception as exc:
                    result = {"id":cmd_path.stem,"processed_at":time.strftime("%Y-%m-%dT%H:%M:%S%z"),"ok":False,"error":f"{type(exc).__name__}: {exc}"}
                write_json(RESULTS / f"{cmd_path.stem}.json", result)
                cmd_path.rename(ARCHIVE / cmd_path.name)
            sync_out()
        except Exception as exc:
            print(f"bridge cycle error: {type(exc).__name__}: {exc}")
        time.sleep(POLL_SECONDS)

if __name__ == "__main__": main()
