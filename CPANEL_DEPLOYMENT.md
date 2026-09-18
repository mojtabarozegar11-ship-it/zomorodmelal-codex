# cPanel Deployment — Zomorod Melal

## معماری صحیح سایت

سایت اصلی شرکت با Django/Python اجرا می‌شود؛ بنابراین برای این پروژه نباید دنبال index.php، composer.json، vendor یا WordPress باشید.

برنامه اصلی در GitHub در مسیر `django_project/` است و فایل‌های کلیدی آن:
- `manage.py`
- `config/settings.py`
- `config/wsgi.py`
- `passenger_wsgi.py`
- `requirements.txt`
- `apps/`

درخت `website/` قدیمی/سازگاری است و نباید به عنوان برنامه اصلی Passenger ثبت شود.

## تنظیم Python Application در cPanel

Application Root باید به پوشه‌ای اشاره کند که همان‌جا `manage.py` و پوشه `config/` قرار دارند:

`/home/zomorodm/zomorodmelal-app/django_project`

Startup File باید فقط این مقدار باشد:

`passenger_wsgi.py`

در Startup File مسیر کامل فایل وارد نکنید.

## اگر Directory Listing می‌بینید

اگر `https://zomorodmelal.ir/` به جای صفحه سایت، فهرست فایل‌های LiteSpeed مانند `cgi-bin` و `php.ini` را نشان می‌دهد، درخواست دامنه هنوز به برنامه Django/Passenger متصل نشده است.

در این حالت فایل PHP یا WordPress به public_html اضافه نکنید. باید اتصال دامنه به Python Application و Application Root صحیح بررسی شود.

## متغیرهای محیطی

`DJANGO_SETTINGS_MODULE=config.settings`

`DJANGO_DEBUG=False`

`DJANGO_ALLOWED_HOSTS=zomorodmelal.ir,www.zomorodmelal.ir`

`DJANGO_SECRET_KEY=<private-production-secret>`

پس از تأیید کامل HTTPS می‌توان `DJANGO_SECURE_SSL_REDIRECT=True` را فعال کرد.

## بررسی و راه‌اندازی

از داخل Application Root:

```bash
python -m pip install -r requirements.txt
python manage.py check
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput
python -c "import config.wsgi; print('WSGI OK')"
```

سپس برنامه را از cPanel → Application Manager بازنشانی/Restart کنید.

## بررسی نهایی

پس از اتصال صحیح Passenger:

```bash
curl -I https://zomorodmelal.ir/
```

باید پاسخ از برنامه Django دریافت شود، نه Directory Listing پیش‌فرض LiteSpeed.

## مهم

فایل‌ها و پوشه‌های قدیمی هاست را تا زمانی که WSGI، مهاجرت‌ها، static و درخواست HTTPS با موفقیت آزمایش نشده‌اند حذف نکنید.