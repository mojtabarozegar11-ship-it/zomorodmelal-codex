from django.http import JsonResponse


def health(request):
    return JsonResponse({
        "status": "ok",
        "service": "Zomorod Melal Website Core"
    })
