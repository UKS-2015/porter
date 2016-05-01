from core.models import Project, UserProjectRole
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group


def check_permissions(user, required_permissions, **kwargs):
    """
    Authorization check for current user in three steps:
    1. Check if user is logged in
    2. Retrieve user's role on current project (guest if none)
    3. Check if user's role contains required permissions (required_permissions field)

    Additional parameters project_title and repository_title can be passed to determine whether permissions are checked
    on project level or repository level.

    Can be used to determine which part of templates should be or shouldn't be rendered.
    :param user: user for which permissions are checked (usually current user)
    :param required_permissions:
    :return: True if allowed, False if not
    """

    if not user.is_authenticated():
        return False
    # Only check on project level
    # If view is on project level, it will have project_title as URL parameter
    if 'project_title' not in kwargs:
        return True

    if not required_permissions:
        return True

    project = Project.objects.get(title=kwargs['project_title'])
    try:
        role = UserProjectRole.objects.get(user=user, project=project).role
    except UserProjectRole.DoesNotExist:
        role = Group.objects.get(name='Guest')
    for permission in role.permissions.all():
        print(permission.codename)

    # Convert to collection
    if not hasattr(required_permissions, '__iter__') \
            or isinstance(required_permissions, str):
        required_permissions = (required_permissions,)

    for required_permission in required_permissions:
        # print(required_permission)
        if not any(permission.codename == required_permission for permission in role.permissions.all()):
            return False
    return True


class PorterAccessMixin(UserPassesTestMixin):
    """
    Authorization check for current user in three steps:
    1. Check if user is logged in
    2. Retrieve user's role on current project (guest if none)
    3. Check if user's role contains required permissions (required_permissions field)
    """

    required_permissions = None

    def test_func(self):
        return check_permissions(self.request.user, self.required_permissions, **self.kwargs)
