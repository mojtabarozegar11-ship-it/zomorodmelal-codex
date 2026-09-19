#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../django_project"
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
