from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .agents import EconomicMasterAgent
from .gateway import get_payment_gateway
from .models import Asset, EconomicWorkItem, MarketDataSnapshot, OrderIntent, Portfolio, SignalProduct, SignalPurchase, VirtualAssetProject


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
    ("هوش مصنوعی و خدمات آنلاین",
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
        "international_services": IRANICARD_INSPIRED_SERVICES,
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
