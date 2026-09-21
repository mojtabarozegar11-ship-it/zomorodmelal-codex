# زمرد ملل — معماری و انتشار

پروژه «زمرد ملل» دو لایهٔ قابل‌اجرا دارد:

- **اپلیکیشن اندروید / کارگر مجتبی** در `worker_mojtaba/android`
- **سرویس Django/Passenger** در `django_project` برای استقرار اختیاری روی Pars Web Server / cPanel و ارائه API

## مسیرهای انتشار

### Android
هستهٔ اصلی Android از `MasterAgentCoordinator` و `MasterAgentEngine` استفاده می‌کند. اجرای عملیات واقعی خارجی به‌صورت پیش‌فرض غیرفعال است و نقاط حساس نیازمند تأیید مالک هستند.

خروجی‌های CI:
- APK برای نصب/آزمون
- AAB برای انتشار

### Pars Web Server / cPanel
برای دامنهٔ `https://zomorodmelal.ir`، مسیر رسمی استقرار Django با Passenger در `CPANEL_DEPLOYMENT.md` مستند شده است.

قرارداد:
- Application Root: `/home/zomorodm/zomorodmelal-app`
- Startup File: `passenger_wsgi.py`
- Entry Point: `application`
- Python: 3.11.x

بستهٔ cPanel توسط workflow مربوطه ساخته می‌شود و شامل runtime Django و ماژول‌های ریشه‌ای لازم است.

## امنیت
کلیدها و رمزهای سرویس در Environment/Secrets نگهداری شوند و داخل commit قرار نگیرند. اجرای واقعی و عملیات حساس باید صریح و کنترل‌شده باشد.

## وضعیت واقعی
CI می‌تواند صحت ساختار، syntax، تست‌ها و قرارداد بستهٔ استقرار را بررسی کند؛ اجرای واقعی روی Pars Web Server فقط با دسترسی به همان حساب/هاست قابل تأیید است.
