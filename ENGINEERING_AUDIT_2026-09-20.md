# گزارش کارشناسی فنی و مهندسی — Zomorod Melal Codex

تاریخ بررسی: 2026-09-20
شاخه: main

## دامنه بررسی
معماری repository، Django canonical application، Agent/AI layers، CI/CD، cPanel/Passenger handoff، امنیت تنظیمات، تست و وضعیت عملیاتی.

## شواهد بررسی‌شده
- `README.md`
- `django_project/config/settings.py`
- `django_project/config/urls.py`
- `django_project/passenger_wsgi.py`
- `django_project/requirements.txt`
- `django_project/requirements-host.txt`
- `.github/workflows/ci.yml`
- `.github/workflows/django_test.yml`
- `.github/workflows/mvp-tests.yml`
- `.github/workflows/production-sanity.yml`
- `.github/workflows/production-deploy.yml`
- `.github/workflows/cpanel-package.yml`
- `.cpanel.yml`
- `CPANEL_DEPLOYMENT.md`
- `HOST_HANDOFF_CHECKLIST.md`
- `deployment/host_adapter.py`
- معماری repository از Git tree شاخه `main`

## وضعیت CI در زمان ممیزی
در آخرین اجراهای مشاهده‌شده روی commit `6068532cc098e8ae85a658b41c751f33052fca10`:
- Django Offline Test: success
- Production Sanity: success
- Zomorod Melal Django CI: success
- Master Agent MVP Tests: success
- Build cPanel ZIP: success

بنابراین صحت اجرای تست‌های موجود در GitHub Actions برای این commit تأیید شده است؛ این موضوع به‌تنهایی صحت اتصال هاست، DNS، TLS، Passenger/vhost یا اجرای production را اثبات نمی‌کند.

## یافته‌های معماری

### 1. Canonical Django
نقطه ورود canonical وب `django_project/` است و `config.settings` و `config.wsgi.application` استفاده می‌شوند. این تصمیم باید حفظ شود.

ریسک موجود: repository دارای کدها و لایه‌های موازی/Legacy از جمله `website/` و چند لایه Agent/AI در root است. بدون مرزبندی معماری، drift و خطای deployment محتمل است.

اقدام:
- `django_project/` تنها production web tree بماند.
- `website/` فقط compatibility/reference باشد.
- قرارداد import و dependency direction مستند شود.
- هر migration از Legacy به canonical دارای برنامه خروج مشخص باشد.

### 2. لایه Agent/AI
Repository دارای `agents`, `agent_runtime`, `ai_engine`, `ai_providers`, `master_agent` و لایه‌های execution/security است.

ریسک:
- وجود چند abstraction برای AI/provider و agent می‌تواند duplication و رفتار ناسازگار ایجاد کند.
- contract واحد برای lifecycle، permissions، events، tools و execution هنوز کافی نیست.

اقدام:
- یک interface مرجع برای AgentRuntime و Provider تعریف شود.
- Capability registry و policy engine مرکزی ایجاد شود.
- اجرای toolها از model output مستقل و allowlist شود.

### 3. Security
نقاط مثبت:
- `DJANGO_SECRET_KEY` در environment نگهداری می‌شود.
- `DEBUG=False` در production اجباری شده است.
- `ECONOMIC_REAL_EXECUTION_ENABLED` به‌صورت fail-safe خاموش است.
- owner approval و deployment gate در معماری مستند شده‌اند.
- host adapter از `shell=False` استفاده می‌کند و command را ساده نگه می‌دارد.

ریسک:
- `MASTER_AGENT_DEPLOY_COMMAND` هنوز یک نقطه اجرای بیرونی قدرتمند است؛ حتی با محدودیت argv باید command allowlist/identity binding و audit کامل داشته باشد.
- برای عملیات حساس، policy باید مرکزی و قبل از execution enforce شود، نه اینکه صرفاً در چند component تکرار شود.
- برای تراکنش واقعی، idempotency، replay protection، rate limit و immutable audit الزامی است.
- HSTS/secure cookies در محیط فعلی عمداً قابل تنظیم هستند و باید پس از اثبات HTTPS فعال شوند.

### 4. Data / Accounting
طبق ممیزی قبلی، foundation اقتصادی موجود است اما ledger double-entry کامل هنوز هدف است.

برای production مالی:
- journal/batch balancing
- immutable postings
- currency/FX
- reconciliation
- idempotency
- provider reference
- state machine
باید به یک مدل منبع حقیقت مشترک تبدیل شوند.

### 5. API
مسیرهای API وجود دارند، اما برای مقیاس پلتفرم قرارداد versioned باید مرجع شود:
`/api/v1/`

اقدام:
- schema/serializer/response envelope واحد
- error code استاندارد
- authentication/authorization واحد
- timeout/retry/circuit-breaker برای provider adapters
- correlation/request ID

### 6. CI/CD
نقطه قوت: چند workflow مستقل برای Django، repository tests، sanity، package و production gate وجود دارد و در آخرین commit بررسی‌شده موفق بوده‌اند.

ریسک:
- تعداد workflowها زیاد است و بخشی از مسئولیت‌ها هم‌پوشان است.
- runtime production باید در یک سند و workflow واحد pin شود.
- تست deployment واقعی و host verification هنوز جدا از CI repository است.

اقدام:
- Pipeline به مراحل مشخص تقسیم شود: lint → unit → integration → Django deploy checks → package → host handoff → production smoke.
- artifactهای deployment دارای manifest و SHA باشند.
- آخرین artifact با hash/commit به deployment gate bind شود.

### 7. cPanel / Passenger
Repository مستند کرده که Application Root باید:
`/home/zomorodm/zomorodmelal-app/django_project`

و Startup:
`passenger_wsgi.py`

و Entry Point:
`application`

باشد.

`.cpanel.yml` نیز restart file را در همین مسیر touch می‌کند.

اما:
**GitHub نمی‌تواند صحت mapping در LiteSpeed/Passenger، DNS/TLS، process runtime یا دسترسی واقعی host را از روی source code اثبات کند.**

این همان مرز فنی مشکل Directory Listing / 503 است که باید روی هاست آزمایش شود.

### 8. Host Bridge
بخش `host_bridge/` اکنون در repository قرار گرفته است:
- `receive.php`
- `status.php`
- `report.sh`
- `.htaccess`
- `README.md`

طراحی فعلی:
- دریافت فقط POST
- توکن جدا برای write
- فیلدهای allowlisted
- ذخیره خارج از web root
- endpoint خواندنی
- عدم اجرای shell/Git/cPanel command در PHP

این لایه برای diagnostics مناسب است؛ برای production باید HTTPS، secret rotation، rate limiting و در صورت نیاز IP/range restrictions نیز بررسی شوند.

## اولویت اصلاحات

### P0 — قبل از production واقعی
1. تثبیت canonical architecture و کاهش ambiguity بین Legacy و canonical.
2. اتصال واقعی cPanel/Passenger و اثبات end-to-end response.
3. central policy برای owner approval / sensitive execution.
4. API contract نسخه‌دار.
5. production database migration و backup/restore test.
6. audit/idempotency برای عملیات اقتصادی.
7. secret management و rotation.
8. deployment artifact hash binding.

### P1
1. observability استاندارد.
2. RBAC/ABAC مرکزی.
3. provider adapter contract.
4. test coverage و thresholds.
5. performance budget و caching.
6. design system و accessibility.

### P2
1. native mobile clients.
2. analytics/telemetry.
3. marketplace maturity.
4. games production pipeline.
5. cross-provider automation.

## جمع‌بندی مهندسی
Repository از نظر ساختار، مستندات deployment و CI برای یک foundation فعال قابل استفاده است. آخرین وضعیت CI روی commit بررسی‌شده موفق است. با این حال، «سبز بودن CI» مساوی «production operational» نیست.

گلوگاه اصلی فعلی، خود کد Django نیست؛ مرز بین repository و محیط واقعی cPanel/Passenger و همچنین یکپارچه‌سازی نهایی policy/security/API/data contracts است.

## معیار پذیرش production
پروژه زمانی باید production-operational تلقی شود که همه موارد زیر با evidence واقعی تأیید شوند:
- Application Root صحیح
- Passenger Startup/Entry Point صحیح
- HTTPS/TLS صحیح
- root URL از Django پاسخ دهد
- /admin/ و API smoke تست شوند
- migrations موفق
- static assets سرو شوند
- process restart verified
- host bridge health/status verified
- backup/restore test موفق
- external providerها جداگانه و کنترل‌شده فعال شوند
