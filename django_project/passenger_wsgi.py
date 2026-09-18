
"""Passenger WSGI entrypoint for the Zomorod Melal Django project."""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

for path in (BASE_DIR, os.path.dirname(BASE_DIR)):
    if path not in sys.path:
        sys.path.insert(0, path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import config.wsgi

application = config.wsgi.application
