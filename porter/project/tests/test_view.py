from core.models import Project, UserProjectRole
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.test import TestCase

GUEST_ROLE = 'Guest'
OWNER_ROLE = 'Project owner'
LEAD_ROLE = 'Project lead'
DEVELOPER_ROLE = 'Developer'


class ProjectTests(TestCase):
    fixtures = ['test_fixture.json']

    def setUp(self):
        self.project = Project.objects.get(title='Test')
        logged_in = self.client.login(username='owner', password='admin1234')
        self.assertTrue(logged_in)

    def test_user_projects(self):
        self.porter_project = Project.objects.get(title='Porter')
        response = self.client.get(reverse('user_projects'))
        self.assertEquals(response.status_code, 200)

    def test_add_project(self):
        project_title = 'New project'
        description = 'New description'
        user = User.objects.get(username='owner')
        response = self.client.post(
            reverse('new_project'),
            {'title': project_title, 'description': description, 'users': [user.id]}
        )
        self.assertRedirects(response, reverse('user_projects'))

        new_project_added = Project.objects.filter(title=project_title).exists()
        self.assertTrue(new_project_added)

    def test_project_details(self):
        response = self.client.get(reverse('project:overview', kwargs={'project_title': self.project.title}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['project'], self.project)

    # def test_project_settings(self):
    #     response = self.client.get(reverse('project:settings', kwargs={'project_title': self.project.title}))
    #     self.assertEquals(response.status_code, 200)
    #     self.assertEquals(response.context['project'], self.project)
    #
    #     new_title = 'New title'
    #     new_description = 'New description'
    #     response = self.client.post(
    #         reverse('project:settings', kwargs={'project_title': self.project.title}),
    #         {'title': new_title, 'description': new_description, 'users': [self.project.users]}
    #     )
    #     self.assertRedirects(response, reverse('project:overview', kwargs={'project_title': new_title}))
    #
    #     project = Project.objects.get(pk=self.project.id)
    #     self.assertEquals(project.title, new_title)
    #     self.assertEquals(project.description, new_description)

    def test_project_members(self):
        user = User.objects.get(username='porter')
        role = Group.objects.get(name=DEVELOPER_ROLE)
        upr = UserProjectRole(user=user, project=self.project, role=role)
        upr.save()

        # Make sure that user is added to project
        role_assigned = UserProjectRole.objects.filter(user=user, project=self.project, role=role).exists()
        self.assertTrue(role_assigned)

        response = self.client.get(reverse('project:members', kwargs={'project_title': self.project.title}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['project_title'], self.project.title)

        owner = User.objects.get(username='owner')
        users = [owner, user]
        self.assertEquals(response.context['users'], users)

    def test_add_members(self):
        # Default role is 'guest'
        user = User.objects.get(username='porter')
        role = Group.objects.get(name=GUEST_ROLE)
        response = self.client.post(
            reverse('project:add_member', kwargs={'project_title': self.project.title}),
            {'user_id': user.id}
        )
        self.assertRedirects(response, reverse('project:members', kwargs={'project_title': self.project.title}))

        member_added = UserProjectRole.objects.filter(user=user, project=self.project, role=role).exists()
        self.assertTrue(member_added)

    def test_assign_role(self):
        # Add user to project
        user = User.objects.get(username='porter')
        role = Group.objects.get(name=DEVELOPER_ROLE)
        upr = UserProjectRole(user=user, project=self.project, role=role)
        upr.save()

        response = self.client.post(
            reverse('project:assign_role', kwargs={'project_title': self.project.title}),
            {'user_id': user.id, 'role_id': role.id}
        )
        self.assertRedirects(response, reverse('project:members', kwargs={'project_title': self.project.title}))

        role_assigned = UserProjectRole.objects.filter(user=user, project=self.project, role=role).exists()
        self.assertTrue(role_assigned)

    def test_remove_role(self):
        # Add user to project
        user = User.objects.get(username='porter')
        role = Group.objects.get(name=DEVELOPER_ROLE)
        upr = UserProjectRole(user=user, project=self.project, role=role)
        upr.save()
        # Make sure that user is added to project
        role_assigned = UserProjectRole.objects.filter(user=user, project=self.project, role=role).exists()
        self.assertTrue(role_assigned)

        response = self.client.get(
            reverse('project:remove_member', kwargs={'project_title': self.project.title, 'user_id': user.id})
        )
        self.assertRedirects(response, reverse('project:members', kwargs={'project_title': self.project.title}))

        member_exists = UserProjectRole.objects.filter(user=user, project=self.project, role=role).exists()
        self.assertFalse(member_exists)

    def test_delete_project(self):
        response = self.client.post(
            reverse('project:delete', kwargs={'project_title': self.project.title})
        )
        self.assertRedirects(response, reverse('user_projects'))

        new_project_added = Project.objects.filter(pk=self.project.id).exists()
        self.assertFalse(new_project_added)
