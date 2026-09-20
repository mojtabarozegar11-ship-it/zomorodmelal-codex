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
- [x] Deployment authorization has been granted for this project; execution still requires real host credentials and target availability

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
Never commit secrets. Keep the real environment file outside Git. Deployment may proceed once the real host credentials and target configuration are present.

## Important
The repository is prepared for host handoff. Host-side commands, migrations, HTTPS, DNS, Passenger/vhost mapping, and service startup must still be verified against the actual cPanel environment; GitHub source access alone cannot perform or prove those host-level operations.
