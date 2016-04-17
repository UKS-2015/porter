from core.forms import RepositoryForm, RepositoryProjectForm
from core.models import Repository, Issue, Project
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404


def overview(request, repository_title, project_title=None):
    repository = get_object_or_404(Repository, title=repository_title)
    issues = Issue.objects.filter(repository__title=repository_title)
    return render(request, 'repository/overview.html', {'issues': issues, 'project_title': project_title})


def create(request, project_title):
    if request.method == 'POST':
        form = RepositoryProjectForm(request.POST, auto_id=True)
        if form.is_valid():
            repository = form.instance
            repository.project = Project.objects.get(title=project_title)
            Repository.save(repository)
            # return redirect('/{0}/repository/{1}/'.format(project_title, repository.title))
            return redirect(reverse('repo_overview',
                                    kwargs={
                                        'project_title': project_title,
                                        'repository_title': repository.title
                                    }))
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
        repository = get_object_or_404(Repository, title=repository_title)
        form = RepositoryProjectForm(instance=repository)

    return render(request, 'repository/change.html', {'repository': form, 'project_title': project_title})


def list_all(request, project_title):
    project = Project.objects.get(title=project_title)
    paginator = Paginator(Repository.objects.filter(project=project), 25)
    page = request.GET.get('page')

    try:
        repos = paginator.page(page)
    except PageNotAnInteger:
        repos = paginator.page(1)
    except EmptyPage:
        repos = paginator.page(paginator.num_pages)
    return render(request, 'repository/list.html', {'repository_list': repos, 'project_title': project_title})


def delete(request, repository_title, project_title=None):
    repository = get_object_or_404(Repository, title=repository_title)
    Repository.delete(repository)
    return redirect(reverse('repo_list_all', kwargs={'project_title': project_title}))
