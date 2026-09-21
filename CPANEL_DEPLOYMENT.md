# راهنمای نصب نهایی زمرد ملل روی Pars Web Server / cPanel

این نسخه برای اجرای Django با Passenger آماده شده است.

## قرارداد اجرای تولید و cPanel

- دامنه: `https://zomorodmelal.ir`
- Application Root: `/home/zomorodm/zomorodmelal-app`
- Python App root must expose `manage.py` and `passenger_wsgi.py` directly
- Startup File: `passenger_wsgi.py`
- Entry Point: `application`
- Python: 3.11.x
- تنظیم Django: `DJANGO_SETTINGS_MODULE=config.settings`

ریشه Application Root باید مستقیماً شامل این موارد باشد:

```text
manage.py
passenger_wsgi.py
config/
apps/
templates/
static/
requirements.txt
requirements-host.txt
```

## متغیرهای محیطی cPanel

در Python App/Passenger محیط تولید این مقادیر را تنظیم کنید:

```text
DJANGO_SETTINGS_MODULE=config.settings
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=zomorodmelal.ir,www.zomorodmelal.ir
DJANGO_CSRF_TRUSTED_ORIGINS=https://zomorodmelal.ir,https://www.zomorodmelal.ir
DJANGO_SECRET_KEY=<یک مقدار محرمانه و طولانی>
```

در صورت استفاده از PostgreSQL:

```text
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DBNAME
```

کلیدهای سرویس‌های AI فقط در Environment Variables هاست قرار گیرند و داخل Git commit نشوند.

## نصب دستی و بررسی Passenger

از Terminal/SSH هاست:

```bash
cd /home/zomorodm/zomorodmelal-app
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-host.txt

python manage.py check
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput
python -c "import config.wsgi; import passenger_wsgi; print('WSGI OK')"
touch tmp/restart.txt
```

اگر `tmp` وجود ندارد:

```bash
mkdir -p tmp
touch tmp/restart.txt
```

## تنظیم Passenger در cPanel

در بخش Setup Python App:

- Python version = 3.11.x
- Application root = `zomorodmelal-app`
- Application URL = `https://zomorodmelal.ir`
- Startup file = `passenger_wsgi.py`
- Entry point = `application`

پس از هر تغییر کد، Restart Application را انجام دهید.

## تست نهایی

```bash
curl -I https://zomorodmelal.ir/
```

خروجی نباید Directory Listing یا صفحه خام LiteSpeed باشد؛ باید پاسخ برنامه Django باشد.

همچنین:

```bash
python manage.py check --deploy
python -c "import passenger_wsgi; print(passenger_wsgi.application)"
```

## نکته مهم

پروژه نباید برای حل مشکل Passenger داخل `public_html` کپی شود. اگر دامنه Directory Listing نشان می‌دهد، ابتدا VirtualHost/Domain mapping، Application Root و Passenger را اصلاح کنید.
