from django.shortcuts import get_object_or_404, render

from .models import Product


def marketplace(request):
    products = Product.objects.filter(active=True).order_by("-updated_at")
    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(name__icontains=query)
    return render(
        request,
        "marketplace/index.html",
        {"products": products[:100], "query": query},
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    return render(request, "marketplace/detail.html", {"product": product})
