from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "django_project"
WORKFLOW = ROOT / ".github" / "workflows" / "cpanel-package.yml"
DEPLOY = ROOT / ".github" / "workflows" / "deploy-cpanel-ssh.yml"
DOC = ROOT / "CPANEL_DEPLOYMENT.md"

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
    print("ERROR: missing runtime files:")
    for item in missing:
        print(f" - {item}")
    sys.exit(1)

for path in (WORKFLOW, DEPLOY, DOC):
    if not path.exists():
        print(f"ERROR: missing {path.relative_to(ROOT)}")
        sys.exit(1)

workflow = WORKFLOW.read_text(encoding="utf-8")
deploy = DEPLOY.read_text(encoding="utf-8")
doc = DOC.read_text(encoding="utf-8")

checks = {
    "package": [
        "cp -a django_project/. package/zomorodmelal-app/",
        "test -f package/zomorodmelal-app/manage.py",
        "test -f package/zomorodmelal-app/passenger_wsgi.py",
        "test -f package/zomorodmelal-app/requirements-host.txt",
    ],
    "deploy": [
        "manage.py check --deploy",
        "manage.py migrate",
        "manage.py collectstatic --noinput",
        "import config.wsgi; import passenger_wsgi",
        "touch \"$APP_ROOT/tmp/restart.txt\"",
        "public_html",
        "https://zomorodmelal.ir/",
    ],
    "guide": [
        "/home/zomorodm/zomorodmelal-app",
        "passenger_wsgi.py",
        "Entry Point",
        "Python: `3.11.x`",
        "manage.py check --deploy",
        "manage.py migrate",
        "collectstatic --noinput",
    ],
}
sources = {"package": workflow, "deploy": deploy, "guide": doc}
for label, markers in checks.items():
    missing = [m for m in markers if m not in sources[label]]
    if missing:
        print(f"ERROR: incomplete {label} contract:")
        for item in missing:
            print(f" - {item}")
        sys.exit(1)

print("CPANEL_DEPLOYMENT_CONTRACT_OK")
