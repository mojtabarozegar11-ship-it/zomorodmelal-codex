# Targeted refactor notes

- The uploaded project should be transferred to `moj1` before source cleanup is applied.
- Exact duplicate identified in the extracted project: `passenger_wsgi.py` and `django_project/passenger_wsgi.py` have identical contents.
- The root `passenger_wsgi.py` is the project-level entrypoint; `django_project/passenger_wsgi.py` is the duplicate candidate. Removal must be validated after the full project is present in the branch.
- Runtime/cache artifacts such as `__pycache__/`, `*.pyc`, and `.pytest_cache/` should not be committed.
- No changes are being applied to `main`.
