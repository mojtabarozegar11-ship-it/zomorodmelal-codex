from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "django_project"
WORKFLOW = ROOT / ".github" / "workflows" / "cpanel-package.yml"

required = [
    APP / "manage.py",
    APP / "passenger_wsgi.py",
    APP / "config" / "settings.py",
    APP / "config" / "wsgi.py",
    APP / "requirements.txt",
    APP / "requirements-host.txt",
]

missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
if missing:
    print("ERROR: missing cPanel runtime source files:")
    for item in missing:
        print(f" - {item}")
    sys.exit(1)

if not WORKFLOW.exists():
    print("ERROR: cPanel packaging workflow is missing")
    sys.exit(1)

workflow = WORKFLOW.read_text(encoding="utf-8")
required_markers = [
    "cp -a django_project/. package/zomorodmelal-app/",
    "test -f zomorodmelal-app/manage.py",
    "test -f zomorodmelal-app/passenger_wsgi.py",
    "test -f zomorodmelal-app/config/settings.py",
    "test -f zomorodmelal-app/requirements-host.txt",
]
missing_markers = [m for m in required_markers if m not in workflow]
if missing_markers:
    print("ERROR: cPanel packaging workflow is not flattening the Django runtime correctly:")
    for item in missing_markers:
        print(f" - {item}")
    sys.exit(1)

print("CPANEL_SOURCE_LAYOUT_OK")
