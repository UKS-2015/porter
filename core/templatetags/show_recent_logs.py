from core.models import IssueLog
from django import template

register = template.Library()


@register.inclusion_tag('show_recent_logs.html')
def show_recent_logs(**kwargs):

    user = None
    project_title = None
    repository_title = None

    if 'user' in kwargs:
        user = kwargs['user']
    if 'project_title' in kwargs:
        project_title = kwargs['project_title']
    if 'repository_title' in kwargs:
        repository_title = kwargs['repository_title']

    recent_logs = []

    if user and repository_title:
        recent_logs = IssueLog.objects.filter(issue__repository__title=repository_title,
                                              issue__repository__project__users=user).order_by('-date_modified')[:5]
    elif user and project_title:
        recent_logs = IssueLog.objects.filter(issue__repository__project__title=repository_title,
                                              issue__repository__project__users=user).order_by('-date_modified')[:5]
    elif project_title:
        recent_logs = IssueLog.objects.filter(
            issue__repository__project__title=repository_title).order_by('-date_modified')[:5]
    elif repository_title:
        recent_logs = IssueLog.objects.filter(
            issue__repository__title=repository_title).order_by('-date_modified')[:5]
    elif user:
        recent_logs = IssueLog.objects.filter(issue__repository__project__users=user).order_by('-date_modified')[:5]

    return {'recent_logs': recent_logs}
