# cPanel Deployment — Zomorod Melal

## Canonical cPanel layout

The Django application directory is:

`/home/zomorodm/zomorodmelal-app/django_project`

That directory must contain:

- `manage.py`
- `config/`
- `apps/`
- `passenger_wsgi.py`
- `requirements.txt`

Passenger must use the application directory itself as its Application Root.

## cPanel Python Application

Use these exact values:

```text
Application Root
/home/zomorodm/zomorodmelal-app/django_project

Application URL
https://zomorodmelal.ir

Application Startup File
passenger_wsgi.py

Application Entry Point
application
```

Do not point Passenger at the repository root and do not use the legacy `website/` directory as the Django application.

## Required environment

Set these in cPanel's Python Application environment:

```text
DJANGO_SETTINGS_MODULE=config.settings
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=zomorodmelal.ir,www.zomorodmelal.ir
DJANGO_CSRF_TRUSTED_ORIGINS=https://zomorodmelal.ir,https://www.zomorodmelal.ir
DJANGO_SECRET_KEY=<private-production-secret>
DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_SESSION_COOKIE_SECURE=False
DJANGO_CSRF_COOKIE_SECURE=False
```

After HTTPS is confirmed working through Passenger, the SSL redirect and secure-cookie settings may be enabled.

## Python environment

Use a Python version supported by the host and by the repository CI, preferably Python 3.11 or 3.12.

From the application root:

```bash
cd /home/zomorodm/zomorodmelal-app/django_project
python -m pip install -r requirements-host.txt
python manage.py check
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput
python -c "import config.wsgi; print('WSGI OK')"
```

## Restart

After changing code or environment variables, restart the Python application from cPanel Application Manager.

If the host exposes Passenger's restart file, the repository also provides a cPanel deployment hook that touches:

`/home/zomorodm/zomorodmelal-app/django_project/tmp/restart.txt`

## Directory Listing / 503 troubleshooting

If `https://zomorodmelal.ir/` shows the LiteSpeed directory listing instead of Django, the domain is not reaching the Passenger application. Do not add PHP or WordPress files.

Verify, in order:

1. Application Root is exactly the canonical path above.
2. Startup File is exactly `passenger_wsgi.py`.
3. Entry Point is exactly `application`.
4. `passenger_wsgi.py` exists inside the Application Root.
5. The application has been restarted.
6. The domain is mapped by LiteSpeed/Passenger to the Python application.

If all six are correct and the directory listing remains, the hosting provider must rebuild/fix the LiteSpeed virtual-host mapping. That is a host-level operation and cannot be completed by GitHub alone.

## cPanel package structure

The GitHub cPanel workflow builds a clean package without an extra repository-name directory. After extraction, the expected structure is:

```text
/home/zomorodm/zomorodmelal-app/
└── django_project/
    ├── manage.py
    ├── passenger_wsgi.py
    ├── config/
    ├── apps/
    └── requirements.txt
```

Do not extract the package into:

`/home/zomorodm/zomorodmelal-app/django_project/django_project/`

## Final verification

After Passenger is connected:

```bash
curl -I https://zomorodmelal.ir/
```

The response must come from the Django application, not the default LiteSpeed directory listing.

Do not delete legacy host files until the Django application, migrations, static files, HTTPS, and the root URL have been verified successfully.
