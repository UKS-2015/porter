from core.models import UserProjectRole, Project
from django.core.exceptions import PermissionDenied


def check_project_member():
    """
    Checks if the current user is assigned to a project.
    Decorated view's first argument should be request, from which the current user is determined.
    Project is determined by its title, which should be the first path fragment.
    E.g. /porter/porter_core/issues identifies project with title 'porter'.
    """
    def authorize(function):
        def wrapper(*args, **kwargs):
            request = args[0]
            # Splits the request path and eliminates empty strings
            request_path = list(filter(None, request.path.split('/')))
            # First path fragment should be project title
            project_title = request_path[0] if len(request_path) > 0 else None
            project = Project.objects.filter(title=project_title)

            # Check if the user is involved in the project
            upr_count = UserProjectRole.objects.filter(project=project, user=request.user).count()
            if upr_count > 0:
                return function(*args, **kwargs)
            else:
                raise PermissionDenied
        return wrapper
    return authorize
