from core.forms import RepositoryForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class RepositoryTests(TestCase):
    fixtures = ['test_fixture.json']

    def test_form_valid(self):
        user = User.objects.get(username='owner')
        form = RepositoryForm(data={'title': 'Repository', 'description': 'Repository description', 'users': [user]})
        self.assertTrue(form.is_valid(), 'Repository form should be valid: %s' % form.errors)

    def test_form_invalid(self):
        # Missing values
        form = RepositoryForm(data={'title': 'Test'})
        self.assertFalse(form.is_valid(), 'Repository form should be invalid: %s' % form.errors)

        form = RepositoryForm(data={'description': 'Test description'})
        self.assertFalse(form.is_valid(), 'Repository form should be invalid: %s' % form.errors)

    def test_repository_update_form(self):
        logged_in = self.client.login(username='owner', password='admin1234')
        self.assertTrue(logged_in)

        response = self.client.get(
            reverse(
                'project:repository:overview',
                kwargs={'project_title': 'Test', 'repository_title': 'Test repository'}
            )
        )
        self.assertEquals(response.status_code, 200)
        self.assertTrue('repository' in response.context)

        repository = response.context['repository']
        # Form would be invalid because of uniqueness constraint
        # We know that it exists because we fetched it, so we can change its title
        repository.title = 'New title'
        form = RepositoryForm(data={'title': repository.title, 'description': repository.description})
        self.assertTrue(form.is_valid(), form.errors)
