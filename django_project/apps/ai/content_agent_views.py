from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .content_agent import ContentAgent
from .content_agent_models import ContentBrief, ContentChannel, ContentPublication


def _staff_only(request):
    return request.user.is_authenticated and request.user.is_staff


@login_required
def content_agent_dashboard(request):
    if not _staff_only(request):
        return JsonResponse({"detail": "staff access required"}, status=403)
    channels = ContentChannel.objects.filter(active=True).prefetch_related("competitors")
    return render(
        request,
        "ai/content_agent_dashboard.html",
        {"channels": channels},
    )


@login_required
@require_POST
def create_content_brief(request):
    if not _staff_only(request):
        return JsonResponse({"detail": "staff access required"}, status=403)
    channel = get_object_or_404(
        ContentChannel,
        pk=request.POST.get("channel_id"),
        active=True,
    )
    brief = ContentAgent().generate_brief(
        channel=channel,
        topic=request.POST.get("topic", ""),
        user=request.user,
    )
    return JsonResponse(
        {"id": brief.pk, "status": brief.status, "topic": brief.topic}
    )


@login_required
@require_POST
def generate_content_assets(request, brief_id):
    if not _staff_only(request):
        return JsonResponse({"detail": "staff access required"}, status=403)
    brief = get_object_or_404(ContentBrief, pk=brief_id)
    assets = ContentAgent().create_draft_assets(brief, actor=request.user)
    return JsonResponse(
        {
            "brief_id": brief.pk,
            "status": brief.status,
            "assets": [
                {"type": a.asset_type, "version": a.version, "approved": a.approved}
                for a in assets
            ],
        }
    )


@login_required
@require_POST
def approve_content_brief(request, brief_id):
    if not _staff_only(request):
        return JsonResponse({"detail": "staff access required"}, status=403)
    brief = get_object_or_404(ContentBrief, pk=brief_id)
    ContentAgent().approve_brief(brief, actor=request.user)
    return JsonResponse(
        {"id": brief.pk, "status": brief.status, "owner_approved": brief.owner_approved}
    )


@login_required
@require_POST
def queue_content_publication(request, brief_id):
    if not _staff_only(request):
        return JsonResponse({"detail": "staff access required"}, status=403)
    brief = get_object_or_404(ContentBrief, pk=brief_id)
    channel = get_object_or_404(ContentChannel, pk=request.POST.get("channel_id"), active=True)
    publication = ContentAgent().queue_publication(
        brief=brief,
        channel=channel,
        actor=request.user,
    )
    return JsonResponse(
        {
            "id": publication.pk,
            "status": publication.status,
            "owner_approved": publication.owner_approved,
        }
    )


@login_required
@require_POST
def approve_content_publication(request, publication_id):
    if not _staff_only(request):
        return JsonResponse({"detail": "staff access required"}, status=403)
    publication = get_object_or_404(ContentPublication, pk=publication_id)
    approved = request.POST.get("approved", "true").lower() in {"1", "true", "yes", "on"}
    ContentAgent().approve_publication(
        publication,
        approved=approved,
        actor=request.user,
    )
    return JsonResponse(
        {
            "id": publication.pk,
            "status": publication.status,
            "owner_approved": publication.owner_approved,
        }
    )


@login_required
@require_POST
def publish_content(request, publication_id):
    if not _staff_only(request):
        return JsonResponse({"detail": "staff access required"}, status=403)
    publication = get_object_or_404(ContentPublication, pk=publication_id)
    ContentAgent().publish(publication, actor=request.user)
    return JsonResponse(
        {
            "id": publication.pk,
            "status": publication.status,
            "external_id": publication.external_id,
        }
    )
