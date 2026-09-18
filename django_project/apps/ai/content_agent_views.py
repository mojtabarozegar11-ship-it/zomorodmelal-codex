from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .content_agent import ContentAgent
from .content_agent_models import ContentChannel, ContentPublication


@login_required
def content_agent_dashboard(request):
    if not request.user.is_staff:
        return JsonResponse({"detail": "staff access required"}, status=403)
    channels = ContentChannel.objects.filter(active=True).prefetch_related("competitors")
    return render(request, "ai/content_agent_dashboard.html", {"channels": channels})


@login_required
def create_content_brief(request):
    if not request.user.is_staff:
        return JsonResponse({"detail": "staff access required"}, status=403)
    if request.method != "POST":
        return JsonResponse({"detail": "POST required"}, status=405)
    channel = get_object_or_404(ContentChannel, pk=request.POST.get("channel_id"), active=True)
    brief = ContentAgent().generate_brief(channel=channel, topic=request.POST.get("topic", ""), user=request.user)
    return JsonResponse({"id": brief.pk, "status": brief.status, "topic": brief.topic})


@login_required
def publish_content(request, publication_id):
    if not request.user.is_staff:
        return JsonResponse({"detail": "staff access required"}, status=403)
    if request.method != "POST":
        return JsonResponse({"detail": "POST required"}, status=405)
    publication = get_object_or_404(ContentPublication, pk=publication_id)
    ContentAgent().publish(publication, actor=request.user)
    return JsonResponse({"id": publication.pk, "status": publication.status, "external_id": publication.external_id})
