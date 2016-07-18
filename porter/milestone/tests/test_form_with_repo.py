from core.forms import MilestoneForm, MilestoneWithRepoForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from core.models import Milestone


class MilestoneFormWithRepoTests(TestCase):
    fixtures = ['test_fixture.json']

    def test_form_valid(self):
        user = User.objects.get(username='owner')
        form = MilestoneForm(data={'title': 'Milestone', 'repository': 5, 'description': 'Milestone description'})
        self.assertTrue(form.is_valid(), 'MilestoneForm should be valid: %s' % form.errors)

    def test_form_invalid(self):
        # Missing values
        form = MilestoneForm(data={'title': 'Test'})
        self.assertFalse(form.is_valid(), 'MilestoneForm should be invalid: %s' % form.errors)

        form = MilestoneForm(data={'description': 'Test description'})
        self.assertFalse(form.is_valid(), 'Project form should be invalid: %s' % form.errors)

    def test_milestone_update_form(self):
        logged_in = self.client.login(username='owner', password='admin1234')
        self.assertTrue(logged_in)

        response = self.client.get(
            reverse(
                'project:repository:milestone:change',
                kwargs={'project_title': 'Test', 'repository_title': 'Test repository', 'pk':1}
            )
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['repository_title'], 'Test repository')
        self.assertEquals(response.context['project_title'], 'Test')
