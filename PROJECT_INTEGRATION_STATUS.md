# Zomorod Melal — Integration Status

Date: 2026-09-21

This branch preserves the known-good Django/Passenger/cPanel architecture while preparing the full project source for final host deployment.

## Host runtime contract
- Python: 3.11.x
- Application Root: /home/zomorodm/zomorodmelal-app
- Startup File: passenger_wsgi.py
- Entry Point: application
- URL: https://zomorodmelal.ir

## Required host checks
1. Install requirements-host.txt
2. Set production environment variables outside Git
3. Run manage.py check --deploy
4. Run migrations
5. Collect static files
6. Import config.wsgi and passenger_wsgi
7. Restart Passenger
8. Verify the public HTTPS endpoint

## Important
The GitHub connection cannot upload the user-provided ZIP bytes directly through the available repository APIs. The source ZIP remains the authoritative local integration input. No production secrets are committed.
