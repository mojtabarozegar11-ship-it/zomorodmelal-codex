# Zomorod Melal Real Estate Portal

این بسته صفحه «املاک» را به‌صورت مستقل و آماده اتصال به پروژه Django اصلی فراهم می‌کند.

## اجزا
- `urls.py`: مسیر `/real-estate/`
- `views.py`: View صفحه اصلی
- `templates/real_estate_portal/index.html`: صفحه کامل فارسی RTL
- `static/real_estate_portal/real-estate.css`: استایل responsive
- `static/real_estate_portal/real-estate.js`: تعاملات سبک سمت کاربر

## اتصال به پروژه اصلی
در `config/urls.py` یا فایل urls ریشه:
```python
from django.urls import include, path

urlpatterns = [
    # ...
    path("real-estate/", include("real_estate_portal.urls")),
]
```

در هدر سایت:
```html
<a href="/real-estate/">املاک</a>
```

اگر پروژه از app registry استفاده می‌کند، پوشه را به INSTALLED_APPS اضافه کنید یا template/static را در ساختار اپ اصلی ادغام کنید.

## هدف محصول
صفحه صرفاً آگهی ملک نیست؛ یک درگاه اقتصادی برای:
- بازار ملک و زمین
- سرمایه‌گذاری و مشارکت
- زنجیره تأمین ساختمان
- بازار مصالح
- پیمانکاری
- کلینیک ساختمان
- خدمات مهندسی
- مناقصه و استعلام قیمت
- لجستیک و تجهیزات
- فرصت‌های درآمدی پلتفرم

است.
