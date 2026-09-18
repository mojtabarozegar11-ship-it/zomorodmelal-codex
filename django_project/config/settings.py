"""Runtime-safe Django settings for Zomorod Melal platform."""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "true").lower() in {"1","true","yes"}
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS","").split(",") if h.strip()] or ["localhost","127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    "apps.common","apps.agriculture","apps.marketplace","apps.encyclopedia","apps.research","apps.services","apps.ai",
]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware"]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND":"django.template.backends.django.DjangoTemplates","APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "config.wsgi.application"
DATABASES = {"default":{"ENGINE":"django.db.backends.sqlite3","NAME":os.environ.get("DJANGO_DB_PATH", os.path.join(BASE_DIR,"db.sqlite3"))}}
LANGUAGE_CODE = "fa"
TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE","Asia/Tehran")
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AI_PROVIDER_ENABLED = os.environ.get("AI_PROVIDER_ENABLED","false").lower() in {"1","true","yes"}
