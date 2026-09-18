"""Production-safe Django settings for Zomorod Melal platform."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

def env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in {"1","true","yes","on"}

def env_list(name, default=""):
    return [x.strip() for x in os.environ.get(name, default).split(",") if x.strip()]

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = env_bool("DJANGO_DEBUG", False)
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions",
    "django.contrib.messages","django.contrib.staticfiles","apps.common","apps.site","apps.agriculture",
    "apps.marketplace","apps.encyclopedia","apps.research","apps.services","apps.ai","apps.economy","apps.studio",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware",
]
ROOT_URLCONF="config.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[BASE_DIR/"templates"],"APP_DIRS":True,
"OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth",
"django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION="config.wsgi.application"
ASGI_APPLICATION="config.asgi.application"
DB_ENGINE=os.environ.get("DJANGO_DB_ENGINE","sqlite").lower()
if DB_ENGINE in {"postgres","postgresql"}:
    DATABASES={"default":{"ENGINE":"django.db.backends.postgresql","NAME":os.environ.get("POSTGRES_DB","zomorodmelal"),
    "USER":os.environ.get("POSTGRES_USER","zomorodmelal"),"PASSWORD":os.environ.get("POSTGRES_PASSWORD",""),
    "HOST":os.environ.get("POSTGRES_HOST","localhost"),"PORT":os.environ.get("POSTGRES_PORT","5432"),
    "CONN_MAX_AGE":int(os.environ.get("POSTGRES_CONN_MAX_AGE","60")),
    "OPTIONS":{"sslmode":os.environ.get("POSTGRES_SSLMODE","prefer")}}}
else:
    DATABASES={"default":{"ENGINE":"django.db.backends.sqlite3","NAME":os.environ.get("DJANGO_DB_PATH",str(BASE_DIR/"db.sqlite3"))}}
LANGUAGE_CODE="fa"
TIME_ZONE=os.environ.get("DJANGO_TIME_ZONE","Asia/Tehran")
USE_I18N=True
USE_TZ=True
STATIC_URL="/static/"
STATIC_ROOT=Path(os.environ.get("DJANGO_STATIC_ROOT",str(BASE_DIR/"staticfiles")))
STATICFILES_DIRS=[BASE_DIR/"static"]
MEDIA_URL="/media/"
MEDIA_ROOT=Path(os.environ.get("DJANGO_MEDIA_ROOT",str(BASE_DIR/"media")))
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
AI_PROVIDER_ENABLED=env_bool("AI_PROVIDER_ENABLED",False)
REDIS_URL=os.environ.get("REDIS_URL","")
SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO","https")
ECONOMIC_REAL_EXECUTION_ENABLED=False
SECURE_SSL_REDIRECT=env_bool("DJANGO_SECURE_SSL_REDIRECT",False)
SESSION_COOKIE_SECURE=env_bool("DJANGO_SESSION_COOKIE_SECURE",not DEBUG)
CSRF_COOKIE_SECURE=env_bool("DJANGO_CSRF_COOKIE_SECURE",not DEBUG)
SECURE_HSTS_SECONDS=int(os.environ.get("DJANGO_HSTS_SECONDS","0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS=env_bool("DJANGO_HSTS_INCLUDE_SUBDOMAINS",False)
SECURE_HSTS_PRELOAD=env_bool("DJANGO_HSTS_PRELOAD",False)
SECURE_CONTENT_TYPE_NOSNIFF=True
X_FRAME_OPTIONS=os.environ.get("DJANGO_X_FRAME_OPTIONS","DENY")
REFERRER_POLICY=os.environ.get("DJANGO_REFERRER_POLICY","same-origin")
