"""Phase 1 Django settings for Zomorod Melal platform.
Runs without external AI API.
"""

SECRET_KEY = 'change-this-in-production'
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'agriculture',
    'marketplace',
    'encyclopedia',
    'research',
    'services',
    'ai',
]

ROOT_URLCONF = 'config.urls'

AI_PROVIDER_ENABLED = False
