from core.forms import RepositoryForm, RepositoryProjectForm
from core.models import Repository, Issue, Project
from django.shortcuts import render, redirect


def overview(request, repository_title, project_title=None):
    issues = Issue.objects.filter(repository__title=repository_title)
    return render(request, 'repository/overview.html', {'issues': issues})


def create(request, project_title):
    if request.method == 'POST':
        form = RepositoryProjectForm(request.POST, auto_id=True)
        if form.is_valid():
            repository = form.instance
            repository.project = Project.objects.get(title=project_title)
            Repository.save(repository)
            return redirect('/{0}/repository/{1}/'.format(project_title, repository.title))
    else:
        form = RepositoryProjectForm()

    return render(request, 'repository/create.html', {'repository': form, 'project_title': project_title})


def change(request, repository_title, project_title):
    if request.method == 'POST':
        form = RepositoryForm(request.POST, auto_id=True)
        if form.is_valid():
            Repository.save(form.instance)
            return redirect(overview)
    else:
        repository = Repository.objects.get(title=repository_title)
        print(repository)
        form = RepositoryProjectForm(instance=repository)

    return render(request, 'repository/change.html', {'repository': form, 'project_title': project_title})
