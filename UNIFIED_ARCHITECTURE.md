# معماری یکپارچه زمرد ملل

## اجزای اصلی
- سایت: رابط کاربر، داشبورد و API
- Master Agent: کنترل، هماهنگی، تأیید و گزارش
- کارگر مجتبی: Runtime واحد شامل Intent، Planner، Memory، AI، Tools، Security، Execution و Validation

## مسیر مرجع
Site -> Master Agent -> Worker Mojtaba -> ExecutionEngine -> Result -> Master Agent -> Site

## سیاست معماری
قابلیت‌های هوشمند در یک Runtime عملیاتی نگهداری می‌شوند تا دو موتور مستقل و متناقض ایجاد نشود. Master Agent لایه کنترل بالادستی است و اجرای واقعی در Worker انجام می‌شود.

## Endpointهای یکپارچه
- Worker: GET /health
- Worker: POST /v1/tasks
- Worker: POST /v1/voice
- Site: POST /api/execute-worker/
- Site: GET /api/worker-health/

## تنظیمات
WORKER_MOJTABA_URL=http://127.0.0.1:8787
WORKER_API_TOKEN=<strong-secret>
