from django.shortcuts import render, redirect, get_object_or_404
from core.models import Project
from core.forms import ProjectForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def list(request):
    paginator = Paginator(Project.objects.all(), 25)
    page = request.GET.get('page')

    try:
        project_list = paginator.page(page)
    except PageNotAnInteger:
        project_list = paginator.page(1)
    except EmptyPage:
        project_list = paginator.page(paginator.num_pages)

    return render(request, 'project/list.html', {'project_list': project_list})

def add(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, auto_id=True)
        if form.is_valid():
            Project.save(form.instance)
            return redirect(list)
    else:
        form = ProjectForm()

    return render(request, 'project/add.html', {'project': form})

def detail(request, project_id):
    project = Project.objects.get(pk=project_id)
    form = ProjectForm(instance = project)
    return render(request, 'project/profile.html', {'project': form.as_p()})

def change(request, project_id):
    if request.method == 'GET':
        project = get_object_or_404(Project, pk=project_id)
        form = ProjectForm(instance=project)
        return render(request, 'project/change.html', {'project': form})
    elif request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.instance
            project.id = project_id
            Project.save(project)
            return redirect(list)

def delete(request, project_id):
    if request.method == 'GET':
        project = get_object_or_404(Project, pk=project_id)
        form = ProjectForm(instance=project)
        return render(request, 'project/delete.html', {'project': form})
    elif request.method == 'POST':
        project = Project.objects.get(pk=project_id)
        Project.delete(project)
        return redirect(list)
    else:
        redirect(list)
