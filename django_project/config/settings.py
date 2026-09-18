"""Production-safe Django settings for Zomorod Melal platform."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = env_bool("DJANGO_DEBUG", False)
ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get(
        "DJANGO_ALLOWED_HOSTS",
        "zomorodmelal.ir,www.zomorodmelal.ir,localhost,127.0.0.1",
    ).split(",")
    if h.strip()
]
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "DJANGO_CSRF_TRUSTED_ORIGINS",
        "https://zomorodmelal.ir,https://www.zomorodmelal.ir",
    ).split(",")
    if origin.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "apps.common", "apps.site", "apps.agriculture", "apps.marketplace", "apps.encyclopedia",
    "apps.research", "apps.services", "apps.ai", "apps.economy", "apps.studio",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware", "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware", "django.contrib.messages.middleware.MessageMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [BASE_DIR / "templates"], "APP_DIRS": True,
    "OPTIONS": {"context_processors": ["django.template.context_processors.request", "django.contrib.auth.context_processors.auth", "django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.environ.get("DJANGO_DB_PATH", str(BASE_DIR / "db.sqlite3"))}}
LANGUAGE_CODE = "fa"
TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE", "Asia/Tehran")
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = Path(os.environ.get("DJANGO_STATIC_ROOT", str(BASE_DIR / "staticfiles")))
STATICFILES_DIRS = [BASE_DIR / "static"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AI_PROVIDER_ENABLED = env_bool("AI_PROVIDER_ENABLED", False)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
ECONOMIC_REAL_EXECUTION_ENABLED = False

# Production security switches. Enable HSTS only when HTTPS is confirmed at the host.
SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", False)
SESSION_COOKIE_SECURE = env_bool("DJANGO_SESSION_COOKIE_SECURE", not DEBUG)
CSRF_COOKIE_SECURE = env_bool("DJANGO_CSRF_COOKIE_SECURE", not DEBUG)
SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("DJANGO_HSTS_INCLUDE_SUBDOMAINS", False)
SECURE_HSTS_PRELOAD = env_bool("DJANGO_HSTS_PRELOAD", False)
