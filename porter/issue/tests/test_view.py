from core.models import Project, UserProjectRole, Repository, Issue
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.test import TestCase

GUEST_ROLE = 'Guest'
OWNER_ROLE = 'Project owner'
LEAD_ROLE = 'Project lead'
DEVELOPER_ROLE = 'Developer'


class IssueTests(TestCase):
    fixtures = ['test_fixture.json']

    def setUp(self):
        self.repository = Repository.objects.get(title='Test repository')
        self.project = Project.objects.get(title='Test')
        logged_in = self.client.login(username='owner', password='admin1234')
        self.assertTrue(logged_in)

    def test_comments_list(self):
        issue = Issue.objects.get(pk=1)
        response = self.client.get(
            reverse(
                'project:repository:issue:overview',
                kwargs={
                    'project_title': issue.repository.project.title,
                    'repository_title': issue.repository.title,
                    'pk': issue.pk
                }
            )
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['object'], issue)
        self.assertEquals(response.context['comments'], [])

    # def test_add_comment(self):
    #     issue = Issue.objects.get(pk=1)
    #
    #     response = self.client.get(
    #         reverse(
    #             'project:repository:issue:overview',
    #             kwargs={
    #                 'project_title': issue.project.title,
    #                 'repository_title': issue.project.repository.title,
    #                 'pk': issue.project.repository.pk
    #             }
    #         ),
    #         {'content': 'Hello!'}
    #     )
    #
    #     self.assertRedirects(
    #         response,
    #         reverse(
    #             'project:repository:issue:overview',
    #             kwargs={
    #                 'project_title': issue.project.title,
    #                 'repository_title': issue.project.repository.title,
    #                 'pk': issue.project.repository.pk
    #             }
    #         )
    #     )
    #
    #     response = self.client.get(
    #         reverse(
    #             'project:repository:issue:overview',
    #             kwargs={
    #                 'project_title': issue.project.title,
    #                 'repository_title': issue.project.repository.title,
    #                 'pk': issue.project.repository.pk
    #             }
    #         )
    #     )
    #     self.assertEquals(response.status_code, 200)
    #     self.assertEquals(len(response.context['comments']), 1)
    #     self.assertEquals(response.context['comments'][0].content, 'Hello!')
