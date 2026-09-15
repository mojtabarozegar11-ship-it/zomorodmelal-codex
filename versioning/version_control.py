import os
import shutil
from datetime import datetime


class VersionControl:
    def __init__(self):
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )
        self.backup_root = os.path.join(
            self.project_root, "data", "versions"
        )

        os.makedirs(self.backup_root, exist_ok=True)

    def create_backup(self, label="backup"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        version_name = f"{label}_{timestamp}"
        backup_path = os.path.join(self.backup_root, version_name)

        os.makedirs(backup_path, exist_ok=True)

        excluded = {
            ".git",
            "__pycache__",
            "data",
            "sandbox",
        }

        for item in os.listdir(self.project_root):
            if item in excluded:
                continue

            source = os.path.join(self.project_root, item)
            destination = os.path.join(backup_path, item)

            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)

        return backup_path

    def list_versions(self):
        if not os.path.exists(self.backup_root):
            return []

        return sorted(os.listdir(self.backup_root))

    def status(self):
        versions = self.list_versions()

        return {
            "version_control": True,
            "versions_count": len(versions),
            "versions": versions,
            "rollback_available": len(versions) > 0,
        }


if __name__ == "__main__":
    vc = VersionControl()

    print("🗂️ Version Control فعال شد.")

    backup = vc.create_backup("initial")

    print("✅ Backup ساخته شد:")
    print(backup)

    print("\n📦 وضعیت نسخه‌ها:")
    print(vc.status())
