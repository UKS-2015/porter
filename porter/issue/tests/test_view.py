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
        self.issues = Issue.objects.filter(repository = 5)
        self.issue = Issue.objects.get(pk=1)
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

    def test_add_comment(self):
        issue = Issue.objects.get(pk=1)

        response = self.client.post(
            reverse(
                'project:repository:issue:overview',
                kwargs={
                    'project_title': issue.repository.project.title,
                    'repository_title': issue.repository.title,
                    'pk': issue.id
                }
            ),
            {'content': 'Hello!'}
        )

        self.assertRedirects(
            response,
            reverse(
                'project:repository:issue:overview',
                kwargs={
                    'project_title': issue.repository.project.title,
                    'repository_title': issue.repository.title,
                    'pk': issue.id
                }
            )
        )

        response = self.client.get(
            reverse(
                'project:repository:issue:overview',
                kwargs={
                    'project_title': issue.repository.project.title,
                    'repository_title': issue.repository.title,
                    'pk': issue.id
                }
            )
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['comments']), 1)
        self.assertEquals(response.context['comments'][0].content, 'Hello!')

    def test_issue_list(self):
        response = self.client.get(
            reverse('project:repository:issue:list', kwargs={'project_title': self.issue.repository.project.title, 'repository_title':self.issue.repository.title})
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len([x for x in response.context['issue_list'] if x in self.issues]), len(self.issues))

    def test_add_issue(self):
        title = 'New issue'
        description = 'New issue description'
        response = self.client.post(
            reverse('project:repository:issue:new', kwargs={'project_title': self.issue.repository.project.title, 'repository_title':self.issue.repository.title}),
            {'title': title, 'description': description}
        )
        self.assertRedirects(
            response,
            reverse('project:repository:issue:list', kwargs={'project_title': self.issue.repository.project.title, 'repository_title':self.issue.repository.title})
        )

        new_issue_added = Issue.objects.filter(title=title).exists()
        self.assertTrue(new_issue_added)
        self.assertTrue(Issue.objects.filter(title=title)[0].description,description)
        self.assertTrue(Issue.objects.filter(title=title)[0].repository.title,self.repository.title)

    def test_issue_overview(self):
        response = self.client.get(
            reverse(
                'project:repository:issue:overview',
                kwargs={'project_title': self.issue.repository.project.title, 'repository_title': self.issue.repository.title, 'pk':self.issue.pk}
            )
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['repository_title'], self.issue.repository.title)
        self.assertEquals(response.context['project_title'], self.issue.repository.project.title)

    def test_issue_update(self):
        response = self.client.get(
            reverse(
                'project:repository:issue:change',
                kwargs={'project_title': self.issue.repository.project.title, 'repository_title': self.issue.repository.title, 'pk':self.issue.pk}
            )
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['form'].instance, self.issue)

        new_title = 'New title'
        new_description = 'New description'
        response = self.client.post(
            reverse(
                'project:repository:issue:change',
                kwargs={'project_title': self.issue.repository.project.title, 'repository_title': self.issue.repository.title, 'pk':self.issue.pk}
            ),
            {'title': new_title, 'description': new_description}
        )
        self.assertRedirects(
            response,
            reverse(
                'project:repository:issue:list',
                kwargs={'project_title': self.issue.repository.project.title, 'repository_title': self.issue.repository.title}
            )
        )

        newIssue = Issue.objects.get(pk=self.issue.id)
        self.assertEquals(newIssue.title, new_title)
        self.assertEquals(newIssue.description, new_description)
        self.assertEquals(newIssue.repository, self.issue.repository)