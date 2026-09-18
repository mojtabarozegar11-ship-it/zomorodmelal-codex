"""cPanel Passenger entrypoint for Zomorod Melal."""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DJANGO_DIR = os.path.join(BASE_DIR, "django_project")

if DJANGO_DIR not in sys.path:
    sys.path.insert(0, DJANGO_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config.wsgi import application  # noqa: E402,F401
