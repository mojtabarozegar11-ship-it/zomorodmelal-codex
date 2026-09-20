# cPanel Deployment — Zomorod Melal

## Source-of-truth architecture

The Git repository is the development/automation repository. The Django runtime source is:

`/django_project`

cPanel does **not** run the repository root.

The GitHub cPanel packaging workflow copies the contents of `django_project/` into the package directory:

`zomorodmelal-app/`

Therefore after extraction the cPanel Application Root contains the Django files directly.

## cPanel Python Application

Use these exact values:

```text
Application Root
/home/zomorodm/zomorodmelal-app

Application URL
https://zomorodmelal.ir

Application Startup File
passenger_wsgi.py

Application Entry Point
application

Python version
3.11.x
```

The application root must contain:

- `manage.py`
- `passenger_wsgi.py`
- `config/`
- `apps/`
- `templates/`
- `static/`
- `requirements.txt`
- `requirements-host.txt`

There must be **no** `django_project/` subdirectory inside the cPanel Application Root.

## Environment

Set these in cPanel:

```text
DJANGO_SETTINGS_MODULE=config.settings
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=zomorodmelal.ir,www.zomorodmelal.ir
DJANGO_CSRF_TRUSTED_ORIGINS=https://zomorodmelal.ir,https://www.zomorodmelal.ir
DJANGO_SECRET_KEY=<private-production-secret>
```

Keep secrets outside Git.

## Installation and verification

From the cPanel Application Root:

```bash
cd /home/zomorodm/zomorodmelal-app
python -m pip install -r requirements-host.txt
python manage.py check
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput
python -c "import config.wsgi; import passenger_wsgi; print('WSGI OK')"
```

Restart the Python application from cPanel after installation or code changes.

## Directory Listing / 503 diagnosis

If the domain shows a LiteSpeed directory listing:

1. Confirm the Python Application is **Started**.
2. Confirm Application Root is exactly `/home/zomorodm/zomorodmelal-app`.
3. Confirm Startup File is exactly `passenger_wsgi.py`.
4. Confirm Entry Point is exactly `application`.
5. Confirm `passenger_wsgi.py` is physically inside the Application Root.
6. Confirm the package was extracted directly into the Application Root.
7. Restart the Python application.
8. If all seven pass and directory listing remains, the remaining fault is LiteSpeed/Passenger virtual-host mapping.

If a 503 occurs, inspect the Passenger application error log before changing Python versions or paths.

## Release package

The authoritative release artifact is produced by:

`.github/workflows/cpanel-package.yml`

It creates:

`ZOMORODMEL.IR.zip`

with this extraction layout:

```text
/home/zomorodm/zomorodmel-app/
├── manage.py
├── passenger_wsgi.py
├── config/
├── apps/
├── templates/
├── static/
├── requirements.txt
└── requirements-host.txt
```

Do not manually upload the repository root as the cPanel application.

## Important

GitHub can build and validate the release package. The actual LiteSpeed/Passenger mapping, DNS, HTTPS, database credentials, migrations, and running process still have to be verified on the cPanel server.
