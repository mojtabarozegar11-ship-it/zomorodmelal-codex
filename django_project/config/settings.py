"""Phase 1 Django settings for Zomorod Melal platform.
Runs without external AI API.
"""

SECRET_KEY = 'change-this-in-production'
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'apps.agriculture',
    'apps.marketplace',
    'apps.encyclopedia',
    'apps.research',
    'apps.services',
    'apps.ai',
]

ROOT_URLCONF = 'config.urls'

AI_PROVIDER_ENABLED = False
