from core.forms import IssueWithRepoForm, IssueForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from core.models import Issue


class IssueWithRepoFormTests(TestCase):
    fixtures = ['test_fixture.json']

    def test_form_valid(self):
        user = User.objects.get(username='owner')

        #without assignee
        form1 = IssueWithRepoForm(data={'title': 'Issue','creator':user, 'assignee':None, 'description': 'Issue description', 'labels':[]})
        self.assertTrue(form1.is_valid(), 'IssueForm form1 should be valid: %s' % form1.errors)

        #no labels
        form3 = IssueWithRepoForm(data={'title': 'Issue','creator':user, 'assignee':None, 'description': 'Issue description', 'labels':[]})
        self.assertTrue(form3.is_valid(), 'IssueForm form3 should be valid: %s' % form3.errors)

        #labels missing
        form4 = IssueWithRepoForm(data={'title': 'Issue','creator':user, 'assignee':None, 'description': 'Issue description'})
        self.assertTrue(form3.is_valid(), 'IssueForm form4 should be valid: %s' % form4.errors)

        #assignee missing
        form5 = IssueWithRepoForm(data={'title': 'Issue','creator':user, 'description': 'Issue description', 'labels':[]})
        self.assertTrue(form5.is_valid(), 'IssueForm form5 should be valid: %s' % form5.errors)

        #creator missing
        form6 = IssueWithRepoForm(data={'title': 'Issue', 'description': 'Issue description'})
        self.assertTrue(form6.is_valid(), 'IssueForm form6 should be invalid: %s' % form6.errors)

    def test_form_invalid(self):
        user = User.objects.get(username='owner')

        #description missing
        form1 = IssueWithRepoForm(data={'title': 'Test','creator':user})
        self.assertFalse(form1.is_valid(), 'IssueForm form1 should be invalid: %s' % form1.errors)

        #title missing
        form3 = IssueWithRepoForm(data={'creator':user, 'description': 'Issue description'})
        self.assertFalse(form3.is_valid(), 'IssueForm form3 should be invalid: %s' % form3.errors)

    def test_issue_update_form(self):
        logged_in = self.client.login(username='owner', password='admin1234')
        self.assertTrue(logged_in)

        issue = Issue.objects.get(pk=1)

        response = self.client.get(
            reverse(
                'project:repository:issue:change',
                kwargs={'project_title': 'Test', 'repository_title': 'Test repository', 'pk':1}
            )
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['project_title'], 'Test')


