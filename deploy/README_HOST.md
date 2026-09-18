# Host deployment guide

## Layout
Place the repository on the host and use `django_project` as the Django working directory.

## Install
1. Create a virtual environment.
2. Install `django_project/requirements.txt`.
3. Copy `django_project/.env.example` to a private environment file and set production values.
4. Never commit the real `.env` or the DeepSeek key.

## Initialize
Run:
- `python manage.py check`
- `python manage.py migrate`
- `python manage.py collectstatic --noinput`
- create a Django superuser with `python manage.py createsuperuser`

## Run
Gunicorn can use `deploy/gunicorn.conf.py` from repository root:
`gunicorn -c deploy/gunicorn.conf.py`

## Android admin
After HTTPS is active, open:
`https://<domain>/mobile-admin/`
in Android Chrome and use Add to Home Screen / Install App.

The PWA is a management shell; authentication remains Django's session-based admin authentication.

## DeepSeek
Enter the key through Django Admin under AI configuration. The key is masked and not rendered back into the form.

Keep `AI_PROVIDER_ENABLED=False` until the owner explicitly approves external AI use.
