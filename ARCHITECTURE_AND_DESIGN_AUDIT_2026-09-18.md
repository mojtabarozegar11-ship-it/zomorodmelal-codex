# ممیزی تخصصی پروژه زمرد ملل

تاریخ ممیزی: 2026-09-18
شاخه بررسی‌شده: main

## خلاصه مدیریتی
این مخزن یک اکوسیستم چندلایه دارد: هسته Master Agent، چند زیرسامانه Python، و اپلیکیشن Django در `django_project/`. از نظر ایده و تفکیک حوزه‌ها ظرفیت توسعه بالایی دارد؛ اما برای تبدیل شدن به یک محصول production-grade باید مرز «هسته آزمایشی/Legacy» و «هسته canonical» شفاف‌تر شود و قراردادهای API، امنیت، طراحی سیستم و تست سرتاسری یکدست شوند.

## یافته‌های معماری
- `django_project/` طبق README هسته canonical وب است.
- همزمان در ریشه و `website/` کدهای قدیمی/موازی وجود دارد؛ این دوگانگی خطر drift و خطای استقرار ایجاد می‌کند.
- لایه‌های agent، AI provider و Django apps وجود دارند، اما قرارداد مشترک واضح برای agent lifecycle، permissions، events و tool execution باید تثبیت شود.
- سرویس‌های اقتصادی در حال حاضر بیشتر «catalog/presentation + domain models» هستند و اتصال واقعی providerها باید از UI جدا و پشت adapter/connector قرار گیرد.
- ERP فعلی یک foundation است، نه ERP کامل: CRUD/API، گزارش‌های رسمی، گردش‌کارهای کامل، انبار و حسابداری double-entry هنوز نیاز به تکمیل دارند.

## ممیزی طراحی و UX
- زبان بصری فعلی منسجم است: RTL، mobile responsive، رنگ‌های forest/gold/cream و کامپوننت‌های تکرارشونده.
- ساختار صفحه‌ها هنوز بیشتر section-based است تا یک Design System کامل.
- navigation باید بر اساس وظیفه کاربر و product hierarchy بازطراحی شود؛ لینک‌های متعدد به routeهای مختلف نباید جای IA مشخص را بگیرند.
- برای محصول بزرگ، نیاز به tokens، component library، states، فرم‌ها، table، modal، toast، loading، error و empty-state استاندارد وجود دارد.
- دسترس‌پذیری باید با semantic HTML، focus states، keyboard navigation، contrast و فرم‌های قابل‌استفاده ممیزی شود.
- CSS فعلی فشرده و عمدتاً monolithic است؛ برای رشد محصول بهتر است به فایل‌های ماژولار/توکن‌ها/کامپوننت‌ها شکسته شود.

## ممیزی امنیت
- `ECONOMIC_REAL_EXECUTION_ENABLED = False` یک fail-safe مهم است.
- اصل owner approval در بخش‌هایی از مدل‌ها پیاده شده، ولی باید به یک policy مرکزی و غیرقابل دورزدن برای تمام actionهای حساس تبدیل شود.
- احراز نقش شرکت‌ها موجود است؛ اعمال آن باید به صورت middleware/service policy و نه فقط در viewها یکدست شود.
- برای تراکنش‌های مالی، idempotency key، audit trail کامل، nonce/replay protection، rate limit و transaction boundary ضروری است.
- secretها نباید وارد repository شوند؛ تنظیمات محیطی فعلی مسیر مناسبی دارد.
- تنظیمات HSTS/HTTPS به صورت env-controlled است؛ production باید پس از تأیید کامل TLS فعال شود.

## ممیزی داده و مالی
- مدل‌های اقتصادی و ERP برای شروع مناسب‌اند، ولی ledger مالی باید double-entry واقعی با journal/batch balancing، currency/FX، reconciliation و immutable posting داشته باشد.
- AccountingEntry فعلی به‌تنهایی تضمین نمی‌کند هر سند متوازن باشد.
- CashTransaction و AccountingEntry نباید موازی و بدون source-of-truth مشترک رشد کنند.
- سفارش‌های مالی و طلا نیاز به state machine، idempotency و provider reference استاندارد دارند.

## ممیزی API و یکپارچه‌سازی
- APIهای موجود محدودند و بیشتر health/summary یا endpointهای دامنه‌ای اولیه هستند.
- یک API contract versioned مانند `/api/v1/` لازم است.
- provider integration باید interface واحد، timeout/retry، circuit breaker، structured errors و observability داشته باشد.
- سرویس‌های بانکی، بیمه، دولتی و بین‌المللی باید «capability registry + provider adapter + legal gate» داشته باشند.

## ممیزی تست و DevOps
- چند workflow و مجموعه تست وجود دارد.
- CI فعلی روی Python 3.11/3.12/3.13 اجرا می‌شود؛ با توجه به سابقه پروژه، نسخه runtime production باید صریحاً تثبیت شود.
- compileall به‌تنهایی صحت Django deployment را تضمین نمی‌کند.
- باید test stages شامل Django checks، migrations، URL smoke tests، unit/integration tests، security checks و build/deploy verification باشد.
- نیاز به coverage threshold و artifact گزارش تست وجود دارد.

## ریسک‌های اولویت‌دار
### P0
1. یکسان‌سازی canonical architecture و تعیین تکلیف `website/` قدیمی.
2. policy مرکزی برای owner approval و action execution.
3. قرارداد API نسخه‌دار و error model.
4. double-entry ledger واقعی برای حسابداری.
5. تست سرتاسری deployment و Django system checks.

### P1
1. Design System کامل.
2. RBAC/ABAC یکپارچه برای company/user/agent.
3. service connector architecture.
4. observability و audit events.
5. performance و caching.

### P2
1. native mobile clients روی API هسته.
2. analytics/product telemetry.
3. game-studio production pipeline.
4. marketplace maturity و fulfillment.

## طرح اصلاح پیشنهادی
معماری هدف:
```
Experience Layer
  Web / PWA / Native Mobile
          |
API Gateway / Versioned API
          |
Domain Services
  Economy | Office | Marketplace | Agriculture | Research | Encyclopedia | Studio
          |
Shared Platform
  Identity | RBAC | Owner Approval | Audit | Events | Files | Notifications
          |
Integration Layer
  Provider Adapters | Payment | Travel | Insurance | Government | AI
          |
Data Layer
  PostgreSQL | Cache | Object Storage | Queue
```

## نتیجه ممیزی
پروژه قابلیت توسعه به یک پلتفرم بزرگ را دارد، اما وضعیت فعلی باید «Foundation / Active Development» تلقی شود، نه محصول production-complete. تمرکز بعدی باید روی معماری یکپارچه، Design System، امنیت اجرایی، ledger، API contract و تست سرتاسری باشد.
