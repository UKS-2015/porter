from core.models import IssueLog
from django import template
from django.db.models import Q

register = template.Library()

@register.inclusion_tag('show_recent_logs.html')
def show_recent_logs(**kwargs):

    user = kwargs.get('user')

    recent_logs_deleted = IssueLog.objects.filter(Q(object_user=user)
        | Q(subject_user=user))
    recent_logs_other = IssueLog.objects.filter(
        issue__repository__project__users=user)

    # TODO: This union operand doesn't work as expected (bug #49)
    recent_logs = (recent_logs_deleted |
                   recent_logs_other).order_by('-date_modified')[:5]

    return {'recent_logs': recent_logs or []}
