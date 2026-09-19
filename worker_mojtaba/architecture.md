# معماری نسخه 0.1

Android App
  -> Chat / Voice UI
  -> Core Brain
     -> Memory
     -> Planner
     -> Model Router
     -> Tool Engine
     -> Agent Manager
  -> Android Device Adapter
  -> Media Adapter
  -> Web/API Adapter
  -> Digital Asset Adapter
  -> Security + Audit

## اصول
- ماژولار و افزونه‌ای
- جداسازی هسته از ابزارها
- ثبت عملیات و خطاها
- اسرار خارج از کد و در Secure Storage/secret manager
- Sandbox پیش از استقرار
- امکان rollback نسخه‌ها
- استفاده فقط از دسترسی‌های واقعی و معتبر
