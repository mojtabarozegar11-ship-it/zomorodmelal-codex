# Host Handoff Checklist

## Repository readiness
- [x] Django manage.py
- [x] WSGI entrypoint
- [x] ASGI entrypoint
- [x] Production-oriented settings environment variables
- [x] Static root configuration
- [x] Gunicorn configuration
- [x] Android-installable admin PWA
- [x] Masked DeepSeek key entry
- [x] DeepSeek runtime configuration bridge
- [x] Host dependency manifest
- [x] Deployment remains owner-approved and disabled by default

## Host-side actions
- [ ] Upload repository
- [ ] Create Python virtual environment
- [ ] Install django_project/requirements-host.txt
- [ ] Set private production environment values
- [ ] Run python manage.py check
- [ ] Run python manage.py migrate
- [ ] Run python manage.py collectstatic --noinput
- [ ] Create Django superuser
- [ ] Start Gunicorn behind the host HTTPS/web server
- [ ] Verify /admin/ and /mobile-admin/
- [ ] Enter DeepSeek key in Admin
- [ ] Explicitly approve and then enable external AI if desired

## Storage
The repository is currently small; a 1 GB host can support the initial deployment. Growth will come from the database, static/media files, logs, and future content. The planned 30 GB upgrade provides substantially more operating room.

## Security
Never commit secrets. Keep the real environment file outside Git and keep production deployment disabled until explicitly approved.

## Important
The repository is prepared for host handoff, but host-side commands, migrations, HTTPS, DNS, and service startup have not been executed from GitHub and therefore remain pending external actions.
