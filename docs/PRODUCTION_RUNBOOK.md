# Production Environment Runbook

## Required environment
Set these in the host or GitHub production environment, never in source:
- DJANGO_SECRET_KEY
- DJANGO_ALLOWED_HOSTS
- DJANGO_DEBUG=false
- DJANGO_DB_ENGINE=postgresql
- POSTGRES_DB / POSTGRES_USER / POSTGRES_PASSWORD / POSTGRES_HOST / POSTGRES_PORT
- REDIS_URL
- DJANGO_SECURE_SSL_REDIRECT=true
- DJANGO_SESSION_COOKIE_SECURE=true
- DJANGO_CSRF_COOKIE_SECURE=true
- DJANGO_HSTS_SECONDS (after HTTPS verification)
- DEEPSEEK_API_KEY / OPENAI_API_KEY / GEMINI_API_KEY / ANTHROPIC_API_KEY as required
- AI_PROVIDER_ENABLED=true only after keys and provider connectivity are verified

## Host / SSL
Use deployment/docker-compose.production.yml with Caddy. Caddy terminates TLS for SITE_DOMAIN and proxies Django to web:8000.

## Static / media
Run Django collectstatic during deployment. Static and media volumes are mounted read-only into Caddy.

## Backup / recovery
Run deployment/backup.sh on a scheduled host job. Restore using pg_restore into a verified recovery database before production recovery.

## Monitoring
At minimum monitor HTTP health (/health/), PostgreSQL availability, Redis availability, container restarts, disk volume capacity, backup freshness, and TLS expiry.

## Security
Before enabling production traffic run:
- python manage.py check --deploy
- API authentication/authorization tests
- CSRF/session/security-header checks
- dependency vulnerability scanning
- backup restore drill
