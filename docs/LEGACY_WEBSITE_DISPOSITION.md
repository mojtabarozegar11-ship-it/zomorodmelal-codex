# Legacy website disposition

The legacy `website/` tree is not imported by the primary Django application and is not wired into `django_project/config/urls.py`.

CI must prove:
1. `django_project/config.wsgi` and `config.asgi` import successfully.
2. Primary Django app tests pass.
3. No production URL depends on `website/`.

Deletion is intentionally gated until these checks are green in GitHub Actions. The current milestone therefore marks the legacy tree as **isolated/deprecating**, not silently deleted.
