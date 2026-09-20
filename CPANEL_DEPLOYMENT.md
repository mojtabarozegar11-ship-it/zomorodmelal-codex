# cPanel Deployment — Zomorod Melal

## Canonical application layout

The Django application root is:

`/home/zomorodm/zomorodmelal-app`

The Django runtime files must be directly in that directory:

- `manage.py`
- `config/`
- `apps/`
- `passenger_wsgi.py`
- `requirements.txt`
- `requirements-host.txt`
- `templates/`
- `static/`
- `host_bridge/`

There is no `django_project/` subdirectory in the canonical release layout.

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
```

Do not point Passenger at the Git repository parent directory.

## Environment

Set production values in cPanel's Python Application environment:

```text
DJANGO_SETTINGS_MODULE=config.settings
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=zomorodmelal.ir,www.zomorodmelal.ir
DJANGO_CSRF_TRUSTED_ORIGINS=https://zomorodmelal.ir,https://www.zomorodmelal.ir
DJANGO_SECRET_KEY=<private-production-secret>
```

Keep secrets outside Git.

## Installation and verification

From the application root:

```bash
cd /home/zomorodm/zomorodmelal-app
python -m pip install --upgrade pip
python -m pip install -r requirements-host.txt
python manage.py check
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput
python -c "import config.wsgi; print('WSGI OK')"
```

Restart the Python application after code or environment changes.

## Directory Listing / 503 troubleshooting

If the domain shows a LiteSpeed directory listing, verify:

1. Application Root is exactly `/home/zomorodm/zomorodmelal-app`.
2. Startup File is exactly `passenger_wsgi.py`.
3. Entry Point is exactly `application`.
4. `passenger_wsgi.py` exists in the application root.
5. The Python application has been restarted.
6. LiteSpeed/Passenger has the domain mapped to that application.

If all six are correct and directory listing continues, the remaining work is host-side virtual-host/Passenger mapping.

## cPanel package rules

The release archive must extract directly to the application root.

Correct:

```text
/home/zomorodm/zomorodmelal-app/
├── manage.py
├── passenger_wsgi.py
├── config/
├── apps/
├── templates/
├── static/
├── host_bridge/
├── requirements.txt
└── requirements-host.txt
```

Incorrect:

```text
/home/zomorodm/zomorodmelal-app/django_project/
```

## Release requirement

A package is considered cPanel-ready only when CI has passed the deployment-layout check and the Django/WSGI checks. Host-level Passenger mapping, DNS, HTTPS certificates, migrations, and database credentials still require verification on the actual server.
