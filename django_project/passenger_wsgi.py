"""Passenger WSGI entrypoint for the Zomorod Melal Django project."""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Keep both the Django application and the deployed repository support modules
# importable under cPanel Passenger.
for path in (BASE_DIR, os.path.dirname(BASE_DIR)):
    if path not in sys.path:
        sys.path.insert(0, path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config.wsgi import application  # noqa: E402,F401
