from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

required = [
    ROOT / "manage.py",
    ROOT / "passenger_wsgi.py",
    ROOT / "requirements.txt",
    ROOT / "requirements-host.txt",
    ROOT / "config",
]

legacy = ROOT / "django_project"

missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]

if legacy.exists():
    print("ERROR: legacy django_project/ directory must not exist in the canonical release layout")
    sys.exit(1)

if missing:
    print("ERROR: missing required paths:")
    for item in missing:
        print(f" - {item}")
    sys.exit(1)

requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
if "-r django_project/" in requirements or "django_project/" in requirements:
    print("ERROR: requirements.txt contains a legacy django_project reference")
    sys.exit(1)

print("CPANEL_LAYOUT_OK")
