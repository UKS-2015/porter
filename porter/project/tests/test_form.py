from core.forms import ProjectForm
from django.core.urlresolvers import reverse
from django.test import TestCase


class ProjectTests(TestCase):
    fixtures = ['test_fixture.json']

    def test_form_valid(self):
        form = ProjectForm(data={'title': 'Project', 'description': 'Project description'})
        self.assertTrue(form.is_valid(), 'Project form should be valid: %s' % form.errors)

    def test_form_invalid(self):
        # Missing values
        form = ProjectForm(data={'title': 'Test'})
        self.assertFalse(form.is_valid(), 'Project form should be invalid: %s' % form.errors)

        form = ProjectForm(data={'description': 'Test description'})
        self.assertFalse(form.is_valid(), 'Project form should be invalid: %s' % form.errors)

        # Uniqueness constraint
        form = ProjectForm(data={'title': 'Test', 'description': 'Test description'})
        self.assertFalse(form.is_valid(), 'Project form should be valid: %s' % form.errors)

    def test_project_settings_form(self):
        logged_in = self.client.login(username='owner', password='admin1234')
        self.assertTrue(logged_in)

        response = self.client.get(reverse('project:overview', kwargs={'project_title': 'Test'}))
        self.assertEquals(response.status_code, 200)
        self.assertTrue('project' in response.context)

        project = response.context['project']
        # Form would be invalid because of uniqueness constraint
        # We know that it exists because we fetched it, so we can change its title
        project.title = 'New title'
        form = ProjectForm(data={'title': project.title, 'description': project.description})
        self.assertTrue(form.is_valid(), form.errors)
