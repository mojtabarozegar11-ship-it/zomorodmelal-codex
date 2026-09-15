import os
import json
import shutil
from datetime import datetime


class ExecutionController:

    def __init__(self):
        self.root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.data_dir = os.path.join(self.root, "data")
        self.sandbox_dir = os.path.join(self.root, "sandbox", "execution_workspace")
        self.log_file = os.path.join(self.data_dir, "execution_log.json")
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.sandbox_dir, exist_ok=True)
        if not os.path.exists(self.log_file):
            self._save_logs([])

    def _load_logs(self):
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def _save_logs(self, logs):
        tmp_file = self.log_file + ".tmp"
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
        os.replace(tmp_file, self.log_file)

    def _log(self, action, status, details=None):
        logs = self._load_logs()
        logs.append({
            "id": len(logs) + 1,
            "action": action,
            "status": status,
            "details": details or {},
            "created_at": datetime.now().isoformat(),
        })
        self._save_logs(logs)

    def backup(self, files=None):
        backup_root = os.path.join(self.data_dir, "execution_backups")
        os.makedirs(backup_root, exist_ok=True)
        name = "backup_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        destination = os.path.join(backup_root, name)
        os.makedirs(destination, exist_ok=True)
        copied = []
        for relative_path in files or []:
            source = os.path.abspath(os.path.join(self.root, relative_path))
            if not source.startswith(self.root + os.sep) or not os.path.isfile(source):
                continue
            target = os.path.join(destination, relative_path)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copy2(source, target)
            copied.append(relative_path)
        self._log("backup", "created", {"path": destination, "files": copied})
        return destination

    def prepare_sandbox(self, files=None):
        prepared = []
        for relative_path in files or []:
            source = os.path.abspath(os.path.join(self.root, relative_path))
            if not source.startswith(self.root + os.sep):
                raise ValueError("Path خارج از پروژه مجاز است.")
            if not os.path.isfile(source):
                continue
            destination = os.path.join(self.sandbox_dir, relative_path)
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            shutil.copy2(source, destination)
            prepared.append(relative_path)
        self._log("sandbox_prepare", "ready", {"files": prepared})
        return prepared

    def execute(self, request_id, action, approved=False, files=None):
        if not approved:
            self._log(action, "blocked", {
                "request_id": request_id,
                "reason": "owner_approval_required",
                "project_promotion": False,
                "external_deployment": False,
            })
            return {
                "success": False,
                "request_id": request_id,
                "status": "blocked",
                "project_promotion": False,
                "external_deployment": False,
                "generated_code_executed": False,
                "message": "تأیید مالک لازم است.",
            }
        prepared = self.prepare_sandbox(files)
        backup_path = self.backup(files)
        self._log(action, "approved_staged", {
            "request_id": request_id,
            "backup": backup_path,
            "sandbox_files": prepared,
            "project_promotion": False,
            "external_deployment": False,
            "generated_code_executed": False,
        })
        return {
            "success": True,
            "request_id": request_id,
            "status": "approved_staged",
            "backup_created": True,
            "backup_path": backup_path,
            "sandbox_files": prepared,
            "project_promotion": False,
            "external_deployment": False,
            "generated_code_executed": False,
            "message": "تأیید شد؛ عملیات در Sandbox/Stage قرار گرفت.",
        }

    def status(self):
        return {
            "execution_controller": True,
            "sandbox_enabled": True,
            "backup_enabled": True,
            "audit_log_enabled": True,
            "owner_approval_required": True,
            "project_promotion": False,
            "external_deployment": False,
            "generated_code_executed": False,
        }


if __name__ == "__main__":
    controller = ExecutionController()
    print(json.dumps(controller.status(), ensure_ascii=False, indent=2))
