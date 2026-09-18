from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST
import json
import os
from decimal import Decimal
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from .agents import EconomicMasterAgent
from .gateway import get_payment_gateway
from .models import (
    Asset,
    EconomicWorkItem,
    GoldOrder,
    MarketDataSnapshot,
    OrderIntent,
    Portfolio,
    SignalProduct,
    SignalPurchase,
    VirtualAssetProject,
)


IRANICARD_INSPIRED_SERVICES = [
    ("ارز و دارایی دیجیتال", [
        "خرید و فروش ارزهای دیجیتال",
        "تبادل و پرداخت بین‌المللی با رمزارز",
        "خدمات استیبل‌کوین و دارایی‌های دیجیتال",
        "خرید کیف پول سخت‌افزاری رمزارز",
    ]),
    ("پرداخت و مالی بین‌المللی", [
        "پرداخت ارزی در سایت‌های خارجی",
        "پرداخت با Visa و Mastercard",
        "پرداخت با PayPal",
        "پرداخت با Perfect Money و WebMoney",
        "پرداخت هزینه آزمون‌های بین‌المللی مانند IELTS، TOEFL و PTE",
        "پرداخت هزینه دانشگاه‌های خارجی",
        "پرداخت هزینه سفارت و خدمات ویزا",
        "پرداخت هاست و دامنه خارجی",
        "پرداخت رزرو هتل و خدمات سفر",
        "پرداخت همایش، کنفرانس و اشتراک سرویس‌ها",
    ]),
    ("کارت و حساب بین‌المللی", [
        "صدور و ارائه کارت‌های اعتباری بین‌المللی",
        "Visa Card و Mastercard",
        "کارت‌های پیش‌پرداخت و دبیت",
        "افتتاح حساب‌های پرداخت بین‌المللی مانند PayPal",
        "خدمات حساب‌های الکترونیکی مانند Skrill، WebMoney و Perfect Money",
        "افتتاح حساب Payeer",
    ]),
    ("درآمد ارزی و فریلنسری", [
        "نقد کردن درآمد ارزی",
        "تسویه درآمد فریلنسرها",
        "دریافت درآمد ارزی برای توسعه‌دهندگان و تولیدکنندگان محتوا",
    ]),
    ("خرید جهانی", [
        "خرید کالا از فروشگاه‌های خارجی",
        "خرید از Amazon و فروشگاه‌های بین‌المللی",
        "خرید از Amazon ایتالیا و ترکیه",
        "خرید از Trendyol ترکیه و فروشگاه‌های منتخب",
        "تحویل کالا و پیگیری سفارش",
    ]),
    ("گیفت‌کارت و سرگرمی دیجیتال", [
        "گیفت‌کارت Apple",
        "گیفت‌کارت PlayStation و Xbox",
        "گیفت‌کارت Amazon",
        "گیفت‌کارت Spotify و Netflix",
        "گیفت‌کارت بازی‌ها مانند PUBG و Free Fire",
        "خرید بازی و نرم‌افزار کامپیوتری",
        "خرید اشتراک و اکانت پریمیوم سرویس‌های خارجی",
    ]),
    ("فناوری و زیرساخت", [
        "شماره مجازی و سیم‌کارت بین‌المللی",
        "سرور مجازی و خدمات زیرساخت خارجی",
        "خرید هاست و دامنه خارجی",
        "خدمات توسعه‌دهنده مانند Apple Developer و Google Play Developer",
        "پرداخت سرویس‌های تخصصی مانند Envato، ThemeForest، Shutterstock، Zoom و Spotify",
    ]),
    ("طلا و جواهرات", [
        "قیمت لحظه‌ای طلای ۱۸ عیار، ۲۴ عیار، آبشده، سکه و اونس",
        "خرید و فروش آنلاین طلای آبشده با ثبت وزن و مبلغ",
        "کیف پول طلایی و نمایش موجودی برحسب گرم",
        "خرید طلا با مبالغ خرد و فروش در هر زمان",
        "تحویل فیزیکی طلای خریداری‌شده و ارسال بیمه‌شده",
        "خرید و فروش انواع سکه و شمش طلا",
        "فروشگاه شمش و پلاک طلا در وزن‌های مختلف",
        "گالری طلای زینتی و جواهرات؛ انگشتر، گردنبند، دستبند، النگو و گوشواره",
        "بازار طلای نو، دست‌دوم و جواهرات سنگ‌دار",
        "کارت هدیه طلا و هدیه‌های سرمایه‌ای",
        "محاسبه‌گر قیمت طلا، اجرت، سود، مالیات و ارزش نهایی",
        "محاسبه تبدیل گرم، سوت، مثقال و تومان",
        "استعلام و ثبت عیار، وزن، فاکتور و مشخصات کالا",
        "درخواست ری‌گیری و تعیین عیار",
        "نمودار و تحلیل تاریخی قیمت طلا و سکه",
        "مقایسه قیمت خرید و فروش و اسپرد",
        "باشگاه مشتریان و خدمات وفاداری",
        "خدمات سفارش ساخت و شخصی‌سازی طلا و جواهر",
        "خدمات تعمیر، تغییر سایز و سرویس جواهرات",
        "بازار آگهی و فروشندگان/نمایندگان طلا و جواهر",
        "خدمات خزانه، نگهداری امن و بیمه موجودی؛ فقط پس از اخذ مجوز و قراردادهای لازم",
    ]),
    ("هوش مصنوعی و خدمات آنلاین", [
        "پرداخت سرویس‌های هوش مصنوعی مانند ChatGPT و Midjourney",
        "خرید اشتراک سرویس‌های SaaS و ابزارهای حرفه‌ای",
        "پرداخت سرویس‌های آنلاین تخصصی و حرفه‌ای",
    ]),
]


def dashboard(request):
    return render(request, "economy/dashboard.html", {
        "assets": Asset.objects.filter(active=True).count(),
        "portfolios": Portfolio.objects.filter(active=True).count(),
        "orders": OrderIntent.objects.count(),
        "market_points": MarketDataSnapshot.objects.count(),
        "signals": SignalProduct.objects.filter(active=True).count(),
        "virtual_assets": VirtualAssetProject.objects.filter(active=True).count(),
        "work_items": EconomicWorkItem.objects.exclude(status="done").count(),
        "agents": EconomicMasterAgent().capabilities(),
        "international_services": IRANICARD_INSPIRED_SERVICES,\n        "super_app_services": SUPER_APP_SERVICES,
    })


def health(request):
    return JsonResponse({
        "economic_agent": "ready",
        "specialized_agents": EconomicMasterAgent().capabilities(),
        "paper_trading": True,
        "real_execution": False,
        "owner_approval_required": True,
        "virtual_asset_issuance": "gated",
        "legal_review_required": True,
        "signal_sales": True,
        "payment_gateway": "sandbox",
    })


def signal_store(request):
    return render(request, "economy/signals.html", {"products": SignalProduct.objects.filter(active=True).order_by("-created_at")})


@require_POST
def signal_checkout(request, product_id):
    product = get_object_or_404(SignalProduct, pk=product_id, active=True)
    if not request.user.is_authenticated:
        return redirect("/admin/login/?next=/economy/signals/")
    purchase = SignalPurchase.objects.create(product=product, user=request.user, amount=product.price, currency=product.currency)
    checkout = get_payment_gateway().create_checkout(purchase)
    return render(request, "economy/checkout.html", {"purchase": purchase, "checkout": checkout})


def signal_checkout_page(request, purchase_id):
    purchase = get_object_or_404(SignalPurchase, pk=purchase_id)
    if request.user.is_authenticated and purchase.user_id != request.user.id and not request.user.is_staff:
        return JsonResponse({"detail": "forbidden"}, status=403)
    return render(request, "economy/checkout.html", {"purchase": purchase, "checkout": {"authority": purchase.authority, "sandbox": True}})


@require_GET
def gold_market(request):
    api_key = os.environ.get("ARZHAM_API_KEY", "")
    if not api_key:
        return JsonResponse({"status": "not_configured", "configure": "ARZHAM_API_KEY"}, status=503)
    req = Request("https://arzhaam.ir/api/rates/latest", headers={"X-App-Key": api_key})
    try:
        with urlopen(req, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        return JsonResponse({"status": "provider_error", "detail": str(exc)}, status=502)
    return JsonResponse({"status": "ok", "provider": "arzhaam", "data": payload})

@require_POST
def gold_order_create(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "authentication_required"}, status=401)
    try:
        weight = Decimal(request.POST.get("weight_grams", "0"))
    except Exception:
        return JsonResponse({"detail": "invalid_weight"}, status=400)
    if weight <= 0:
        return JsonResponse({"detail": "weight_must_be_positive"}, status=400)
    side = request.POST.get("side", "buy")
    if side not in {"buy", "sell"}:
        return JsonResponse({"detail": "invalid_side"}, status=400)
    order = GoldOrder.objects.create(user=request.user, side=side, product=request.POST.get("product", "gold_18"), weight_grams=weight, status="pending_approval")
    return JsonResponse({"status": "pending_approval", "order_id": order.pk, "owner_approval_required": True})


SUPER_APP_SERVICES = [
    ("پرداخت و بانک", ["کارت‌به‌کارت", "استعلام موجودی کارت", "کیف پول دیجیتال", "شارژ کیف پول", "پرداخت QR", "پرداخت درون‌برنامه‌ای", "تاریخچه تراکنش و رسید دیجیتال"]),
    ("قبوض و پرداخت‌های دوره‌ای", ["آب", "برق", "گاز", "تلفن ثابت", "تلفن همراه", "قبض خدمات شهری", "عوارض و بدهی‌های شهری"]),
    ("موبایل و اینترنت", ["شارژ همراه اول", "شارژ ایرانسل", "شارژ رایتل", "بسته اینترنت همراه اول", "بسته اینترنت ایرانسل", "بسته اینترنت رایتل", "بسته رومینگ", "خرید خودکار شارژ و بسته"]),
    ("خودرو و موتور", ["استعلام و پرداخت خلافی", "عوارض آزادراه", "عوارض سالانه خودرو", "طرح ترافیک", "پارک حاشیه‌ای", "استعلام بیمه شخص ثالث", "استعلام معاینه فنی", "سوابق پلاک", "وضعیت گواهینامه و نمره منفی", "مالیات نقل‌وانتقال", "استعلام اصالت و مدارک خودرو"]),
    ("سفر و گردشگری", ["بلیط هواپیما", "بلیط قطار", "بلیط اتوبوس", "رزرو هتل", "رزرو اقامتگاه", "تور و خدمات گردشگری", "بلیط موزه و اماکن گردشگری", "بلیط شهربازی", "مدیریت مسافران و سوابق سفر"]),
    ("بیمه", ["شخص ثالث", "بدنه", "آتش‌سوزی", "عمر و بازنشستگی", "درمان تکمیلی", "بیمه سفر", "مقایسه و استعلام بیمه", "پرداخت نقدی یا اقساطی در صورت ارائه توسط شرکت بیمه"]),
    ("چک و اعتبار", ["ثبت چک صیادی", "استعلام چک", "ثبت دریافت چک", "انتقال چک", "استعلام اعتبار صادرکننده", "اعتبارسنجی اشخاص حقیقی و حقوقی"]),
    ("بورس و سرمایه‌گذاری", ["خدمات سجام", "ثبت‌نام و احراز هویت سجام", "خدمات بازار سرمایه", "اطلاع‌رسانی و داده بازار", "ابزارهای تحلیل و مدیریت پرتفوی", "عرضه‌ها و پذیره‌نویسی‌های مجاز"]),
    ("قضایی و دولتی", ["خدمات و استعلام‌های قوه قضاییه در صورت اتصال رسمی", "پرداخت جرایم", "خدمات شهرداری", "عوارض ملک", "نوسازی و پسماند", "استعلام‌های دولتی در صورت دسترسی رسمی"]),
    ("خدمات شهری و حمل‌ونقل", ["پرداخت کرایه تاکسی", "QR پرداخت", "پارکینگ و پارک حاشیه‌ای", "خدمات حمل‌ونقل شهری", "عوارض شهری"]),
    ("خرید دیجیتال", ["گیفت‌کارت", "کارت هدیه دیجیتال", "اشتراک سرویس‌های دیجیتال", "بازی و اعتبار بازی", "خرید نرم‌افزار و محتوای دیجیتال"]),
    ("سرگرمی و محتوا", ["فیلم و سریال", "بازی و سرگرمی", "مسابقه و باشگاه مشتریان", "امتیاز و پاداش", "کش‌بک در سرویس‌های مجاز"]),
    ("نیکوکاری", ["کمک به خیریه‌ها", "کمک اضطراری", "پرداخت نذورات و کمک‌های مجاز", "گزارش شفاف تراکنش‌های نیکوکاری"]),
    ("خدمات کسب‌وکار", ["درگاه پرداخت", "لینک پرداخت", "QR پذیرندگی", "تسویه فروشندگان", "تسهیم تراکنش در سرویس‌های مجاز", "فاکتور و پرداخت آنلاین", "باشگاه مشتریان", "گزارش فروش و تراکنش"]),
]
