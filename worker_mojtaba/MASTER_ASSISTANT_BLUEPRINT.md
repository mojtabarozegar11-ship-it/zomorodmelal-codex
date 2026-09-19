# بازبینی جامع و طرح کامل دستیار شخصی «کارگر مجتبی»

## وضعیت معماری
معماری هدف به صورت لایه‌ای تعریف می‌شود:

Android Client
→ API / Transport
→ Personal Assistant Orchestrator
→ Intent + Planner
→ Memory + Context
→ AI/Model Router
→ Agent Manager
→ Tool Center
→ Domain Services
→ External Providers / Android OS
→ Audit + Security + Recovery

## دامنه‌های اصلی
1. امور شخصی و اداری
2. تقویم، برنامه‌ریزی، یادآوری و اتوماسیون
3. حسابداری و مدیریت مالی شخصی
4. پرداخت‌های خودکار از مسیرهای واقعی و مجاز
5. درآمدزایی قانونی و مدیریت درآمد
6. کیف‌پول‌ها و دارایی‌های مجازی طبق سیاست مالک
7. ارتباطات: WhatsApp، Email، SMS و تماس در محدوده API/مجوز
8. اسناد و اطلاعات
9. تولید و انتشار رسانه
10. Android و قابلیت‌های دستگاه
11. پژوهش و Scientist
12. حافظه و شخصی‌سازی
13. AI/Model Router
14. Agent Factory و مدیریت Agentها
15. امنیت، ممیزی، پشتیبان‌گیری و بازیابی
16. تکامل و ارتقای هفتگی

## چرخه اجرای هر درخواست
Request
→ Identity/Context
→ Intent
→ Plan
→ Authorization/Policy Check
→ Tool/Agent Selection
→ Execute
→ Verify
→ Audit
→ Memory Update
→ Result + Evidence

## اصل مهم نتیجه‌محوری
هر کار باید به یکی از وضعیت‌های زیر ختم شود:
- completed: نتیجه واقعی و قابل‌تأیید حاصل شده
- pending: منتظر مجوز، اتصال، کاربر یا سرویس است
- failed: اجرا شد ولی شکست خورد
- planned: فقط برنامه‌ریزی شده
- blocked: به دلیل سیاست/مجوز/دسترسی متوقف شده

## شکاف‌های شناسایی‌شده در بازبینی
- مسیر Context در ExecutionEngine با API همخوان نبود؛ اصلاح شد.
- وابستگی multipart برای endpoint صوتی در requirements وجود نداشت؛ اضافه شد.
- Intent مربوط به calendar_event با capabilityهای Automation همخوانی کامل ندارد و باید در مرحله بعد اصلاح شود.
- endpoint صوتی هنوز Speech-to-Text و Text-to-Speech واقعی ندارد و به Provider معتبر نیاز دارد.
- Android API URL هنوز placeholder است و اتصال واقعی دستگاه/سرور باید پیکربندی شود.
- بانک و سرویس‌های مالی هنوز bridge واقعی ندارند.
- Social Publishing هنوز provider connection required است.
- Occasion Provider هنوز اتصال واقعی ندارد.
- Audit فعلی فایل‌محور است و برای production به storage مقاوم، rotation و integrity نیاز دارد.
- Security Policy فعلی primitive است و باید به authorization واقعی، secrets manager، rate limits و recovery controls ارتقا یابد.
- Evolution Engine فعلی proposal/evaluation پایه است و هنوز چرخه خودکار build/test/deploy/rollback را اجرا نمی‌کند.
- Scheduler فعلی مدل/engine است و برای اجرای دائمی نیازمند worker/service واقعی است.
- حافظه فعلی نیازمند storage پایدار، encryption و کنترل retention در نسخه production است.

## ترتیب تکمیل
### مرحله A — هسته قابل اتکا
Context، Intent/Capability consistency، Result states، error handling و تست end-to-end.

### مرحله B — دستیار شخصی
Calendar، reminders، tasks، contacts، documents و personal administration.

### مرحله C — مالی
Accounting، budgets، authorized payment providers، bank bridges، revenue routing و audit مالی.

### مرحله D — ارتباطات و رسانه
Voice provider، WhatsApp/Email/SMS، media generation و social publishing.

### مرحله E — Android
Device bridge واقعی، notifications، files، camera/microphone، accessibility و app actions با permissionهای Android.

### مرحله F — استقلال عملیاتی
Persistent scheduler، backups، recovery، service health، provider health و offline/online modes.

### مرحله G — تکامل
Weekly evaluation، experiments، candidate versions، automated tests، approval gates، rollback و stage progression.

## تعریف تکمیل طرح
طرح زمانی «کامل از نظر معماری» است که همه دامنه‌ها، مسیر اجرا، سیاست دسترسی، خطا، ممیزی، بازیابی و چرخه تکامل مشخص باشند.
«فعال و عملیاتی» بودن هر قابلیت فقط پس از اتصال واقعی و تست موفق اعلام می‌شود.

## اصل مالک
مالک کنترل نهایی منابع حساس، حساب‌ها، مجوزها و سیاست‌های مالی را حفظ می‌کند. سیستم فقط در محدوده دسترسی واقعی و قوانین سرویس/سیستم‌عامل عمل می‌کند.
