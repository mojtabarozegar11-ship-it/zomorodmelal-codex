"""Passenger entrypoint for the Zomorod Melal Django project.

This file is intended to be used when cPanel Passenger Application Root
is the project directory itself:

    /home/zomorodm/zomorodmelal-app/django_project

The file therefore does not append a nested "django_project" directory.
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config.wsgi import application  # noqa: E402,F401
