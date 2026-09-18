from django.shortcuts import render
from .models import StudioIdea, StudioProject


def studio_home(request):
    context = {
        "projects": StudioProject.objects.all()[:12],
        "ideas": StudioIdea.objects.all()[:8],
        "stages": [
            ("مطالعه", "تحقیق بازار و فناوری"),
            ("نوآوری", "تولید و اعتبارسنجی ایده"),
            ("طراحی", "طراحی بازی و محصول"),
            ("ساخت", "نمونه اولیه و توسعه"),
            ("آزمون", "کنترل کیفیت و تحلیل"),
            ("درآمد", "مدل درآمدی و رشد"),
            ("انتشار", "آماده‌سازی و انتشار با تأیید مالک"),
            ("توسعه", "بهبود مستمر بر اساس داده"),
        ],
    }
    return render(request, "studio/home.html", context)
