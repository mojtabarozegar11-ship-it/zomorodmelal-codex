# چک‌لیست نهایی نصب زمرد ملل

## قبل از نصب

- [ ] Python 3.11.x فعال است.
- [ ] Passenger/Python App در cPanel فعال است.
- [ ] دامنه `zomorodmelal.ir` به هاست صحیح اشاره می‌کند.
- [ ] SSL فعال است.
- [ ] Application Root برابر `/home/zomorodm/zomorodmelal-app` است.
- [ ] Startup File برابر `passenger_wsgi.py` است.
- [ ] Entry Point برابر `application` است.
- [ ] متغیرهای Django در Environment تنظیم شده‌اند.
- [ ] Secretها داخل Git قرار نگرفته‌اند.

## نصب

- [ ] `requirements-host.txt` نصب شد.
- [ ] `python manage.py check` موفق شد.
- [ ] `python manage.py check --deploy` بررسی شد.
- [ ] migration اجرا شد.
- [ ] collectstatic اجرا شد.
- [ ] WSGI import موفق شد.
- [ ] `tmp/restart.txt` ساخته/به‌روزرسانی شد.

## بعد از نصب

- [ ] `https://zomorodmelal.ir/` پاسخ Django می‌دهد.
- [ ] Directory Listing دیده نمی‌شود.
- [ ] خطای 500 وجود ندارد.
- [ ] لاگ Passenger بررسی شد.
- [ ] مسیر static بررسی شد.
- [ ] دیتابیس و migrationها بررسی شدند.
- [ ] endpointهای اصلی سایت بررسی شدند.
- [ ] backup قبل از تغییر بعدی گرفته شد.

## وضعیت

این چک‌لیست «آماده نصب» است؛ موفقیت واقعی نصب فقط پس از اجرای دستورات روی حساب Pars Web Server و مشاهده پاسخ واقعی دامنه قابل تأیید است.
