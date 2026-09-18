# cPanel Deployment — Zomorod Melal

## Canonical application

Use the Django project under `django_project/`.

Expected files:

- `manage.py`
- `config/settings.py`
- `config/wsgi.py`
- `passenger_wsgi.py`
- `requirements-host.txt`
- `apps/`

Do not register the legacy `website/` tree as the production application.

## cPanel Application Manager

Create/register one Python application:

- Application path: the directory containing `manage.py` and `config/`
- Startup file: `passenger_wsgi.py`
- Deployment mode: Production
- Python: use the host Python version compatible with the project's Django requirement

Environment variables:

- `DJANGO_SETTINGS_MODULE=config.settings`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS=zomorodmelal.ir,www.zomorodmelal.ir`
- `DJANGO_SECRET_KEY=<set a private production secret>`
- `DJANGO_SECURE_SSL_REDIRECT=True` only after HTTPS is confirmed
- `DJANGO_SESSION_COOKIE_SECURE=True` when HTTPS is confirmed
- `DJANGO_CSRF_COOKIE_SECURE=True` when HTTPS is confirmed

## Terminal commands

Run as the cPanel user from the application directory:

```bash
python -m pip install -r requirements-host.txt
python manage.py check
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput
```

Then restart Passenger from cPanel/Application Manager or by touching the application's restart file as supported by the host.

## Verification

```bash
python -c "import config.wsgi; print('WSGI OK')"
curl -I https://zomorodmelal.ir/
```

If the application fails, inspect the Python application's `stderr.log` before changing project files.

## Important

Do not delete the old host directory until the canonical application has passed `check`, migrations, static collection, WSGI import, and an HTTPS request test.
