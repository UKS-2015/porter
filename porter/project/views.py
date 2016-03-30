from core.forms import ProjectForm
from core.models import Project
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def overview(request, project_title):
    print(project_title)
    project = Project.objects.filter(title=project_title)
    return render(request, 'project/overview.html', {'project': project})
