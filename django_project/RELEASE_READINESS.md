# Zomorod Melal — Host Release Readiness

## Scope
This document is the handoff gate for the Django application in `django_project/`.

## Required production configuration
- `DJANGO_DEBUG=False`
- `DJANGO_SECRET_KEY` set to a strong secret
- `DJANGO_ALLOWED_HOSTS` set to the real host names
- `DJANGO_CSRF_TRUSTED_ORIGINS` set to the HTTPS origins
- `DJANGO_SECURE_SSL_REDIRECT=True` after HTTPS is confirmed at cPanel
- `DJANGO_SESSION_COOKIE_SECURE=True`
- `DJANGO_CSRF_COOKIE_SECURE=True`
- PostgreSQL is supported through `DATABASE_URL`; SQLite is available as the fallback for smaller deployments
- Run `python manage.py migrate`
- Run `python manage.py collectstatic --noinput`
- Configure Passenger to import `passenger_wsgi.py`

## AI
AI remains disabled by default. Enable it only after the owner explicitly configures and approves a provider.
Supported environment variables:
- `AI_PROVIDER_ENABLED=True`
- `DEEPSEEK_API_KEY`
- optional `DEEPSEEK_BASE_URL`
- optional `DEEPSEEK_MODEL`

The Django Admin may also hold a provider configuration. API keys are never returned by the application API.

## Content Agent
The admin content workflow includes:
research snapshots -> competitor patterns -> brief -> draft assets -> owner approval -> queue/schedule -> publication.

Actual third-party social publication is not claimed until a real platform adapter and its credentials are configured. The built-in adapter is sandbox/manual and returns synthetic IDs.

## Sensitive actions
Owner approval is required for sensitive publication and economic execution paths. Real economic execution remains disabled unless explicitly enabled in production configuration.

## Release gate
Do not treat a generated cPanel ZIP as proof of runtime readiness by itself. The release gate is:
1. GitHub checks are green for the release commit.
2. Django migrations report no pending model changes.
3. WSGI/ASGI import checks pass.
4. The cPanel ZIP is generated from the same release commit.
5. Production environment variables are configured.
6. HTTPS is verified.
7. `/admin/`, public pages, health endpoints, and critical workflows are smoke-tested after deployment.
