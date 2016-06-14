from core.decorators import check_project_member
from core.models import Project, IssueLog, Issue, PorterUser
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from core.mixins import check_permissions
from django.core.urlresolvers import reverse

# Create your views here.

# TODO: Testing only
from django.shortcuts import redirect, render

def index(request):
    if request.user:
        return redirect(reverse('user_dashboard'))
    else:
        return redirect(reverse('login'))

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
    porteruser = PorterUser.objects.get(user=user)
    # Get 5 most recent logs from all user's projects
    recent_logs = IssueLog.objects.filter(issue__repository__project__users=user).order_by('-date_modified')[:5]
    return render(request, 'registration/dashboard.html',
                  {'recent_logs': recent_logs, 'porteruser' : porteruser})

@login_required()
def user_projects(request, *args, **kwargs):
    user = request.user
    paginator = Paginator(Project.objects.filter(users=user).all(), 25)
    page = request.GET.get('page')

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    add_project =  check_permissions(user, 'view_project', **kwargs)
    return render(request, 'registration/projects.html', {'projects': projects, 'add_project':add_project})

@login_required()
def user_issues(request):
    user = request.user
    issues = []
    for project in Project.objects.filter(users=user):
        project_issues = Issue.objects.filter(repository__project=project).all()
        if len(project_issues)>0:
            issues.extend(project_issues)

    paginator = Paginator(issues, 25)
    page = request.GET.get('page')

    try:
        issues = paginator.page(page)
    except PageNotAnInteger:
        issues = paginator.page(1)
    except EmptyPage:
        issues = paginator.page(paginator.num_pages)
    return render(request, 'registration/issues.html', {'issues': issues})
