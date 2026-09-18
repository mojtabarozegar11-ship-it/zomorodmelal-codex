from django.shortcuts import get_object_or_404, render

from .models import ResearchProject


def research_home(request):
    projects = ResearchProject.objects.all().order_by("-updated_at")
    return render(request, "research/index.html", {"projects": projects[:100]})


def research_project(request, project_id):
    project = get_object_or_404(ResearchProject, pk=project_id)
    return render(request, "research/detail.html", {"project": project})
