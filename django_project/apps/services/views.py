from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import ServiceCategory, ServiceOffering, ServiceRequest

POPULAR_SERVICES = [
    ("پرداخت و امور مالی", "پرداخت و خدمات مالی با رعایت شرایط قانونی و اجرایی"),
    ("طلا و جواهر", "خدمات مرتبط با طلا و جواهر با شرایط و تأییدهای لازم"),
    ("خرید و بازار", "خرید کالا، فروش، بازارچه و مزایده"),
    ("کشاورزی", "مشاوره، تولید، نهاده، باغ، گلخانه و محصولات"),
    ("فناوری و هوش مصنوعی", "وب، نرم‌افزار، هوش مصنوعی و خدمات دیجیتال"),
    ("آموزش و مشاوره", "آموزش، پژوهش و مشاوره تخصصی"),
]


def index(request):
    categories = ServiceCategory.objects.filter(active=True).prefetch_related("services")
    services = ServiceOffering.objects.filter(active=True).select_related("category")
    query = request.GET.get("q", "").strip()
    if query:
        services = services.filter(name__icontains=query)
    context = {
        "categories": categories,
        "popular_services": POPULAR_SERVICES,
        "services": services,
        "query": query,
        "service_count": ServiceOffering.objects.filter(active=True).count(),
    }
    return render(request, "services/index.html", context)


def detail(request, slug):
    service = get_object_or_404(ServiceOffering, slug=slug, active=True)
    return render(request, "services/detail.html", {"service": service})


@login_required
@require_http_methods(["GET", "POST"])
def request_service(request, slug):
    service = get_object_or_404(ServiceOffering, slug=slug, active=True)
    if not service.request_enabled:
        return HttpResponseForbidden("ثبت درخواست برای این خدمت فعال نیست.")
    if request.method == "POST":
        details = request.POST.get("details", "").strip()
        if details:
            item = ServiceRequest.objects.create(user=request.user, service=service, details=details)
            if service.owner_approval_required or service.compliance_required:
                item.status = "review"
                item.save(update_fields=("status", "updated_at"))
            return redirect("service-request-detail", tracking_code=item.tracking_code)
    return render(request, "services/request.html", {"service": service})


@login_required
def request_detail(request, tracking_code):
    item = get_object_or_404(ServiceRequest, tracking_code=tracking_code)
    if item.user_id != request.user.id and not request.user.is_staff:
        return HttpResponseForbidden("دسترسی مجاز نیست.")
    return render(request, "services/request_detail.html", {"item": item})
