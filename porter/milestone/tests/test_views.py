from core.models import Milestone, Repository
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
        self.milestones = Milestone.objects.filter(repository = 5)
        self.milestone = Milestone.objects.get(pk=1)
        self.repository = Repository.objects.get(pk=self.milestone.repository.id)
        logged_in = self.client.login(username='owner', password='admin1234')
        self.assertTrue(logged_in)

    def test_milestone_list(self):
        response = self.client.get(
            reverse('project:repository:milestone:list', kwargs={'project_title': self.repository.project.title, 'repository_title':self.repository.title})
        )
        self.assertEquals(response.status_code, 200)

        self.assertEquals(len([x for x in response.context['milestone_list'] if x in self.milestones]), len(self.milestones))

    def test_add_milestone(self):
        title = 'New milestone'
        description = 'New issue description'
        response = self.client.post(
            reverse('project:repository:milestone:new', kwargs={'project_title': self.repository.project.title, 'repository_title':self.repository.title}),
            {'title': title, 'description': description}
        )
        self.assertRedirects(
            response,
            reverse('project:repository:milestone:list', kwargs={'project_title': self.repository.project.title, 'repository_title':self.repository.title})
        )

        new_milestone_added = Milestone.objects.filter(title=title).exists()
        self.assertTrue(new_milestone_added)
        self.assertTrue(Milestone.objects.filter(title=title)[0].description,description)
        self.assertTrue(Milestone.objects.filter(title=title)[0].repository.title,self.repository.title)

    def test_milestone_overview(self):
        response = self.client.get(
            reverse(
                'project:repository:milestone:overview',
                kwargs={'project_title': self.repository.project.title, 'repository_title': self.repository.title, 'pk':self.milestone.pk}
            )
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['repository_title'], self.repository.title)
        self.assertEquals(response.context['project_title'], self.repository.project.title)

    def test_milestone_update(self):
        response = self.client.get(
            reverse(
                'project:repository:milestone:change',
                kwargs={'project_title': self.repository.project.title, 'repository_title': self.repository.title, 'pk':self.milestone.pk}
            )
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['form'].instance, self.milestone)

        new_title = 'New title'
        new_description = 'New description'
        response = self.client.post(
            reverse(
                'project:repository:milestone:change',
                kwargs={'project_title': self.repository.project.title, 'repository_title': self.repository.title, 'pk':self.milestone.pk}
            ),
            {'title': new_title, 'description': new_description}
        )
        self.assertRedirects(
            response,
            reverse(
                'project:repository:milestone:list',
                kwargs={'project_title': self.repository.project.title, 'repository_title': self.repository.title}
            )
        )

        newMilestone = Milestone.objects.get(pk=self.milestone.id)
        self.assertEquals(newMilestone.title, new_title)
        self.assertEquals(newMilestone.description, new_description)
        self.assertEquals(newMilestone.repository, self.repository)

    # def test_milestone_delete(self):
    #     response = self.client.post(
    #         reverse(
    #             'project:repository:milestone:delete',
    #             kwargs={'project_title': self.repository.project.title, 'repository_title': self.repository.title, 'pk':self.milestone.pk}
    #         )
    #     )
    #     self.assertRedirects(
    #         response,
    #         reverse('project:repository:milestone:list', kwargs={'project_title': self.repository.project.title, 'repository_title': self.repository.title})
    #     )
    #
    #     milestone_exists = Milestone.objects.filter(pk=self.milestone.id).exists()
    #     self.assertFalse(milestone_exists)
