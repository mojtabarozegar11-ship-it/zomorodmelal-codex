"""Base Django settings for Zomorod Melal Platform.

AI providers remain disabled until API configuration is added.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.common",
    "apps.agriculture",
    "apps.marketplace",
    "apps.encyclopedia",
    "apps.research",
    "apps.services",
    "apps.ai",
]

AI_PROVIDER_ENABLED = False
