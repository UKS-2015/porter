from django.shortcuts import render, redirect, get_object_or_404
from core.models import Repository
from core.forms import RepositoryForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def list(request):
    paginator = Paginator(Repository.objects.all(), 25)
    page = request.GET.get('page')

    try:
        repository_list = paginator.page(page)
    except PageNotAnInteger:
        repository_list = paginator.page(1)
    except EmptyPage:
        repository_list = paginator.page(paginator.num_pages)

    return render(request, 'repository/list.html', {'repository_list': repository_list})

def add(request):
    if request.method == 'POST':
        form = RepositoryForm(request.POST, auto_id=True)
        if form.is_valid():
            Repository.save(form.instance)
            return redirect(list)
    else:
        form = RepositoryForm()

    return render(request, 'repository/add.html', {'repository': form})

def detail(request, repository_id):
    repository = Repository.objects.get(pk=repository_id)
    form = RepositoryForm(instance = repository)
    return render(request, 'repository/detail.html', {'repository': form.as_p()})

def change(request, repository_id):
    if request.method == 'GET':
        repository = get_object_or_404(Repository, pk=repository_id)
        form = RepositoryForm(instance=repository)
        return render(request, 'repository/change.html', {'repository': form})
    elif request.method == 'POST':
        form = RepositoryForm(request.POST)
        if form.is_valid():
            repository = form.instance
            repository.id = repository_id
            Repository.save(repository)
            return redirect(list)

def delete(request, repository_id):
    if request.method == 'GET':
        repository = get_object_or_404(Repository, pk=repository_id)
        form = RepositoryForm(instance=repository)
        return render(request, 'repository/delete.html', {'repository': form})
    elif request.method == 'POST':
        repository = Repository.objects.get(pk=repository_id)
        Repository.delete(repository)
        return redirect(list)
    else:
        redirect(list)
