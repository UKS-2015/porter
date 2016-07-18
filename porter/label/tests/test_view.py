from core.models import Label, UserProjectRole, Repository, Issue
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.test import TestCase

class IssueTests(TestCase):
    fixtures = ['test_fixture.json']

    def setUp(self):
        self.labels = Label.objects.filter(project = 4)
        self.label = Label.objects.get(pk=2)
        logged_in = self.client.login(username='owner', password='admin1234')
        self.assertTrue(logged_in)

    def test_label_list(self):
        response = self.client.get(
            reverse('project:label:list', kwargs={'project_title': self.label.project.title})
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len([x for x in response.context['label_list'] if x in self.labels]), len(self.labels))

    def test_add_label(self):
        title = 'New label'
        color = '#33ff77'
        response = self.client.post(
            reverse('project:label:new', kwargs={'project_title': self.label.project.title}),
            {'title': title, 'color': color}
        )
        self.assertRedirects(
            response,
            reverse('project:label:list', kwargs={'project_title': self.label.project.title})
        )

        new_label_added = Label.objects.filter(title=title).exists()
        self.assertTrue(new_label_added)
        self.assertTrue(Label.objects.filter(title=title)[0].color,color)
        self.assertTrue(Label.objects.filter(title=title)[0].project,self.label.project)
    #
    # def test_label_overview(self):
    #     response = self.client.get(
    #         reverse(
    #             'project:label:overview',
    #             kwargs={'project_title': self.label.project.title, 'pk':self.label.id}
    #         )
    #     )
    #     self.assertEquals(response.status_code, 200)
    #     self.assertEquals(response.context['project_title'], self.label.project.title)

    def test_label_update(self):
        response = self.client.get(
            reverse(
                'project:label:change',
                kwargs={'project_title': self.label.project.title,'pk':self.label.id}
            )
        )
        self.assertEquals(response.status_code, 200)

        new_title = 'New title'
        new_color = '#33ff77'
        response = self.client.post(
            reverse(
                'project:label:change',
                kwargs={'project_title': self.label.project.title, 'pk':self.label.id}
            ),
            {'title': new_title, 'color': new_color}
        )
        self.assertRedirects(
            response,
            reverse(
                'project:label:list',
                kwargs={'project_title': self.label.project.title}
            )
        )

        newLabel = Label.objects.get(pk=self.label.id)
        self.assertEquals(newLabel.title, new_title)
        self.assertEquals(newLabel.color, new_color)
        self.assertEquals(newLabel.project, self.label.project)