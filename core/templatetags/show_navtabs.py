from core.mixins import check_permissions
from django import template

register = template.Library()

@register.inclusion_tag('show_navtabs.html')
def show_navtabs(user, project_title, active_tab):
    template_params = {
        'user': user, 'project_title': project_title, 'active_tab': active_tab,
        'view_repository': check_permissions(user, 'view_repository', project_title=project_title),
        'view_issue': check_permissions(user, 'view_issue', project_title=project_title),
        'view_milestone': check_permissions(user, 'view_milestone', project_title=project_title),
        'view_member': check_permissions(user, 'view_member', project_title=project_title)
    }
    return template_params
