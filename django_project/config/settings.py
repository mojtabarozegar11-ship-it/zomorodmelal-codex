"""Production-safe Django settings for Zomorod Melal platform."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


DEBUG = env_bool("DJANGO_DEBUG", False)


def load_runtime_secret():
    """Load the production secret from env or create a persistent private host secret."""
    configured = os.environ.get("DJANGO_SECRET_KEY", "").strip()
    if configured:
        return configured

    if DEBUG:
        return "local-development-secret-change-me"

    secret_path = Path.home() / ".zomorodmelal_secret_key"
    try:
        if not secret_path.exists():
            secret_path.parent.mkdir(parents=True, exist_ok=True)
            secret_path.write_text(__import__("secrets").token_urlsafe(64), encoding="utf-8", newline="")
            os.chmod(secret_path, 0o600)
        secret = secret_path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise RuntimeError(
            "DJANGO_SECRET_KEY is not configured and the persistent host secret "
            f"could not be created/read at {secret_path}."
        ) from exc

    if not secret:
        raise RuntimeError("The persistent host secret is empty.")
    return secret


SECRET_KEY = load_runtime_secret()

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
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.common.apps.CommonConfig",
    "apps.site",
    "apps.agriculture.apps.AgricultureConfig",
    "apps.marketplace.apps.MarketplaceConfig",
    "apps.encyclopedia.apps.EncyclopediaConfig",
    "apps.research.apps.ResearchConfig",
    "apps.services",
    "apps.ai",
    "apps.economy",
    "apps.studio",
    "apps.office",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
LANGUAGE_CODE = "fa"
if os.environ.get("DATABASE_URL"):
    import urllib.parse

    parsed = urllib.parse.urlparse(os.environ["DATABASE_URL"])
    if not parsed.scheme.startswith("postgres"):
        raise RuntimeError("DATABASE_URL must use PostgreSQL.")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": parsed.path.lstrip("/"),
            "USER": parsed.username or "",
            "PASSWORD": parsed.password or "",
            "HOST": parsed.hostname or "",
            "PORT": str(parsed.port or 5432),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.environ.get("DJANGO_DB_PATH", str(BASE_DIR / "db.sqlite3")),
        }
    }
TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE", "Asia/Tehran")
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = Path(os.environ.get("DJANGO_STATIC_ROOT", str(BASE_DIR / "staticfiles")))
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AI_PROVIDER_ENABLED = env_bool("AI_PROVIDER_ENABLED", False)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

ECONOMIC_REAL_EXECUTION_ENABLED = env_bool("ECONOMIC_REAL_EXECUTION_ENABLED", False) and not DEBUG

SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", not DEBUG)
SESSION_COOKIE_SECURE = env_bool("DJANGO_SESSION_COOKIE_SECURE", not DEBUG)
CSRF_COOKIE_SECURE = env_bool("DJANGO_CSRF_COOKIE_SECURE", not DEBUG)
SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("DJANGO_HSTS_INCLUDE_SUBDOMAINS", False)
SECURE_HSTS_PRELOAD = env_bool("DJANGO_HSTS_PRELOAD", False)
