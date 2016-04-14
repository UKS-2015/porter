from core.models import Project, Repository
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect


def overview(request, project_title):
    print(project_title)
    project = Project.objects.get(title=project_title)
    repos = Repository.objects.filter(project=project)
    return render(request, 'project/overview.html', {'project': project})


def members(request, project_title):
    project = Project.objects.get(title=project_title)

    # If request method is POST, save then show all members
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(pk=user_id)
        project.users.add(user)

    # Show all project members
    paginator = Paginator(project.users.all(), 25)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'project/members.html', {'project_title': project_title, 'users': users})


def remove_member(request, project_title, user_id):
    project = Project.objects.get(title=project_title)
    user = User.objects.get(pk=user_id)
    project.users.remove(user)

    return redirect(reverse('project_members', kwargs={'project_title': project_title}))


def add_member(request, project_title):

    paginator = Paginator(User.objects.all(), 25)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        project = Project.objects.get(title=project_title)
        user = User.objects.get(pk=user_id)
        project.users.add(user)

        return render(request, 'project/members.html', {'project_title': project_title, 'users': users})
    elif request.method == 'GET':
        return render(request, 'project/members_add.html', {'project_title': project_title, 'users': users})
    else:
        return HttpResponseBadRequest
