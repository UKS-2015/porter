from core.models import Project, UserProjectRole, Repository
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.test import TestCase

GUEST_ROLE = 'Guest'
OWNER_ROLE = 'Project owner'
LEAD_ROLE = 'Project lead'
DEVELOPER_ROLE = 'Developer'


class RepositoryTests(TestCase):
    fixtures = ['test_fixture.json']

    def setUp(self):
        self.repository = Repository.objects.get(title='Test repository')
        self.project = Project.objects.get(title='Test')
        logged_in = self.client.login(username='owner', password='admin1234')
        self.assertTrue(logged_in)

    def test_repository_list(self):
        self.porter_project = Project.objects.get(title='Porter')
        response = self.client.get(
            reverse('project:repository:list_all', kwargs={'project_title': self.repository.project.title})
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['repository_list'], [self.repository.to_dict()])

    def test_add_repository(self):
        repository_title = 'New repository'
        description = 'New repository description'
        response = self.client.post(
            reverse('project:repository:create', kwargs={'project_title': self.repository.project.title}),
            {'title': repository_title, 'description': description}
        )
        self.assertRedirects(
            response,
            reverse('project:repository:list_all', kwargs={'project_title': self.repository.project.title})
        )

        new_repository_added = Repository.objects.filter(title=repository_title).exists()
        self.assertTrue(new_repository_added)

    def test_repository_overview(self):
        response = self.client.get(
            reverse(
                'project:repository:overview',
                kwargs={'project_title': self.repository.project.title, 'repository_title': self.repository.title}
            )
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['repository'], self.repository)

    def test_repository_update(self):
        response = self.client.get(
            reverse(
                'project:repository:change',
                kwargs={'project_title': self.repository.project.title, 'repository_title': self.repository.title}
            )
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['form'].instance, self.repository)

        new_title = 'New title'
        new_description = 'New description'
        response = self.client.post(
            reverse(
                'project:repository:change',
                kwargs={'project_title': self.repository.project.title, 'repository_title': self.repository.title}
            ),
            {'title': new_title, 'description': new_description}
        )
        self.assertRedirects(
            response,
            reverse(
                'project:repository:overview',
                kwargs={'project_title': self.repository.project.title, 'repository_title': new_title}
            )
        )

        repository = Repository.objects.get(pk=self.repository.id)
        self.assertEquals(repository.title, new_title)
        self.assertEquals(repository.description, new_description)

    def test_repository_delete(self):
        response = self.client.post(
            reverse(
                'project:repository:delete',
                kwargs={'project_title': self.repository.project.title, 'repository_title': self.repository.title}
            )
        )
        self.assertRedirects(
            response,
            reverse('project:repository:list_all', kwargs={'project_title': self.repository.project.title})
        )

        repository_exists = Repository.objects.filter(pk=self.repository.id).exists()
        self.assertFalse(repository_exists)
