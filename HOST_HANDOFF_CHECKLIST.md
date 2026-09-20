# Host Handoff Checklist

## Repository / release
- [x] Django runtime source is `django_project/`
- [x] Passenger WSGI entrypoint exists in the Django source
- [x] cPanel package workflow flattens `django_project/` into `zomorodmelal-app/`
- [x] cPanel package validates manage.py, WSGI, settings and host requirements
- [x] CI validates the Django source tree

## cPanel
- [ ] Application Root = /home/zomorodm/zomorodmelal-app
- [ ] Application URL = https://zomorodmelal.ir
- [ ] Startup File = passenger_wsgi.py
- [ ] Entry Point = application
- [ ] Python = 3.11.x
- [ ] Application status = Started
- [ ] Install requirements-host.txt
- [ ] Set production environment variables
- [ ] Run migrate
- [ ] Run collectstatic
- [ ] Restart Passenger
- [ ] Verify public root URL
- [ ] Verify /admin/
- [ ] Verify static assets
- [ ] Verify LiteSpeed/Passenger mapping

## Critical rule

Do not place the Git repository itself at the cPanel Application Root. Upload/extract the generated `ZOMORODMEL.IR.zip` package so that `manage.py` and `passenger_wsgi.py` are directly in the Application Root.
