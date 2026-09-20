# Host Handoff Checklist

## Repository readiness
- [x] Django application root is canonical and root-level
- [x] Passenger WSGI entrypoint present
- [x] ASGI entrypoint present
- [x] Production settings use environment variables
- [x] Root requirements.txt is self-contained
- [x] requirements-host.txt exists
- [x] cPanel deployment instructions match repository layout
- [x] CI release checks defined

## Host-side actions
- [ ] Upload the release package to /home/zomorodm/zomorodmelal-app
- [ ] Create/activate the host Python virtual environment
- [ ] Install requirements-host.txt
- [ ] Set private production environment values
- [ ] Run python manage.py check
- [ ] Run python manage.py check --deploy
- [ ] Run python manage.py migrate
- [ ] Run python manage.py collectstatic --noinput
- [ ] Create a Django superuser
- [ ] Verify /admin/
- [ ] Verify the public root URL
- [ ] Restart Passenger after deployment
- [ ] Verify HTTPS and static files
- [ ] Verify LiteSpeed/Passenger vhost mapping

## Security
- [x] Secrets are not stored in repository configuration
- [ ] Rotate any existing host credentials if they were previously exposed
- [ ] Enable secure cookies/SSL redirect after HTTPS is confirmed

## Important
GitHub can prepare and validate the source release, but it cannot prove host-level Passenger/vhost mapping, DNS, HTTPS, database credentials, or service startup on the real cPanel server.
