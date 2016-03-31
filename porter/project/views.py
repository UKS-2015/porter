from core.models import Project, Repository
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect


def overview(request, project_title):
    project = Project.objects.get(title=project_title)
    repos = Repository.objects.filter(project=project)
    return render(request, 'project/overview.html', {'project': project, 'repos': repos})


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

    # Won't work when a function is passed (NoReverseMatch error)
    return redirect('/%s/members/' % project_title)


def add_member(request, project_title):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        project = Project.objects.get(title=project_title)
        user = User.objects.get(pk=user_id)
        project.users.add(user)

        # Won't work when a function is passed (NoReverseMatch error)
        return redirect('/%s/members/' % project_title)
    elif request.method == 'GET':
        paginator = Paginator(User.objects.all(), 25)
        page = request.GET.get('page')

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        return render(request, 'project/members_add.html', {'project_title': project_title, 'users': users})
    else:
        return HttpResponseBadRequest
