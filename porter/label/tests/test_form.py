from core.forms import LabelForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from core.models import Label


class LabelFormTests(TestCase):
    fixtures = ['test_fixture.json']

    def test_form_valid(self):
        user = User.objects.get(username='owner')

        #without color
        form1 = LabelForm(data={'title': 'Label', 'color':'#ff0000','project':1})
        self.assertTrue(form1.is_valid(), 'IssueForm form1 should be valid: %s' % form1.errors)

        #without project
        form2 = LabelForm(data={'title': 'Issue','color':'#ff0000'})
        self.assertTrue(form2.is_valid(), 'MilestoneForm form2 should be valid: %s' % form2.errors)

        #no labels
        form3 = LabelForm(data={'title': 'Label', 'project':1,'color':'#ff0000' })
        self.assertTrue(form3.is_valid(), 'MilestoneForm form3 should be valid: %s' % form3.errors)


    def test_form_invalid(self):
        user = User.objects.get(username='owner')

        #title missing
        form1 = LabelForm(data={'color':'#ff0000','project':1 })
        self.assertFalse(form1.is_valid(), 'IssueForm form1 should be invalid: %s' % form1.errors)


    def test_label_update_form(self):
        logged_in = self.client.login(username='owner', password='admin1234')
        self.assertTrue(logged_in)

        label = Label.objects.get(pk=2)

        response = self.client.get(
            reverse(
                'project:label:change',
                kwargs={'project_title': 'Test', 'pk':2}
            )
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['project_title'], 'Test')


