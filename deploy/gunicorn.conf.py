"""Gunicorn configuration for the Django application."""
bind = "127.0.0.1:8000"
workers = 2
threads = 2
timeout = 120
accesslog = "-"
errorlog = "-"
chdir = "django_project"
wsgi_app = "config.wsgi:application"
