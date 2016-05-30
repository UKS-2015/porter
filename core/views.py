from core.decorators import check_project_member
from core.models import Project, IssueLog, Issue
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse

# Create your views here.

# TODO: Testing only
from django.shortcuts import redirect, render


@login_required()
@check_project_member()
def project_test(request, project_name):
    return HttpResponse("Hello from %s!" % project_name)


def logout_view(request):
    logout(request)
    return redirect('/login')

@login_required()
def user_dashboard(request):
    user = request.user
    # Get 5 most recent logs from all user's projects
    recent_logs = IssueLog.objects.filter(issue__repository__project__users=user).order_by('-date_modified')[:5]
    projects = Project.objects.filter(users=user).all()
    return render(request, 'registration/dashboard.html', {'recent_logs': recent_logs})


def user_projects(request):
    user = request.user
    paginator = Paginator(Project.objects.filter(users=user).all(), 25)
    page = request.GET.get('page')

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    return render(request, 'registration/projects.html', {'projects': projects})

def user_issues(request):
    user = request.user
    paginator = Paginator(Issue.objects.filter(creator=user).all(), 25)
    page = request.GET.get('page')

    try:
        issues = paginator.page(page)
    except PageNotAnInteger:
        issues = paginator.page(1)
    except EmptyPage:
        issues = paginator.page(paginator.num_pages)
    return render(request, 'registration/issues.html', {'issues': issues})
