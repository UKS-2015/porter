from django.contrib.auth.models import User
from django.test import TestCase
from core.models import PorterUser
from porter.issue.views import IssueLogType

def with_login(username, password, get='/porter/'):
    """Decorator that wraps test method to ensure that certain user is logged in
    before test execution and logged out after it.
    Also handles PorterUser creation for users that don't have it set already."""
    def _with_login(test_method):
        def wrapped_test(instance):
            # Make a porter user of user if it's needed
            user = User.objects.get(username=username)

            if not PorterUser.objects.filter(user__username=username).exists():
                pu = PorterUser()
                pu.user = user
                pu.save()

            instance.client.login(username=username, password=password)

            # Retrieving server response
            response = instance.client.get(get)

            # call original test method
            test_method(instance, response, user)

            instance.client.logout()

        return wrapped_test
    return _with_login

class IssueLogTest(TestCase):
    fixtures = ['test_fixture_recent_log_tests']

    @with_login('developer', 'admin1234')
    def test_recent_logs_not__empty(self, response, _):
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['recent_logs']) > 0)

    @with_login('newbie', 'admin1234')
    def test_recent_logs_empty(self, response, _):
        """newbie's recent logs feed is empty since he's not assigned
        on any of them."""
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['recent_logs']) == 0)

    @with_login('developer', 'admin1234')
    def test_recent_logs_not_longer_than_5(self, response, _):
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['recent_logs']) <= 5)

    @with_login('developer', 'admin1234')
    def test_recent_logs_authenticity(self, response, user):
        """Is every issue log related to currently logged user?"""
        self.assertEqual(response.status_code, 200)

        for rl in response.context['recent_logs']:
            self.assertTrue(rl.subject_user == user or
                            rl.object_user == user)

    @with_login('developer', 'admin1234')
    def test_recent_logs_repository_validity(self, response, user):
        """Does logged user participate in repository from which recent logs
        are originated?"""
        self.assertEqual(response.status_code, 200)

        for rl in response.context['recent_logs']:
            self.assertTrue(rl.issue.repository.project.users.filter(
                username=user.username).exists())

    @with_login('jonas', 'admin1234')
    def test_recent_logs_overflow(self, response, _):
        """jonas is an active user, he should receive exactly 5 logs."""
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['recent_logs']) == 5)

    @with_login('jonas', 'admin1234')
    def test_recent_log_nature_validity__object(self, response, user):
        """All the jonas recent logs are issue assignments to him, so he should
        be object user of all issue logs."""
        self.assertEqual(response.status_code, 200)

        for rl in response.context['recent_logs']:
            self.assertTrue(rl.object_user == user)

    @with_login('novak', 'novak12345')
    def test_recent_log_nature_validity__subject(self, response, user):
        """All novak's recent logs are issue assignments, so he should be
        subject user of all issue logs."""
        self.assertEqual(response.status_code, 200)

        for rl in response.context['recent_logs']:
            self.assertTrue(rl.subject_user == user)

    @with_login('aphyr', 'admin1234')
    def test_recent_log_of_delete_issue(self, response, user):
        """aphyr was made an issue and then deleted it. He should receive
        two recent logs, first should be deletion, second should be creation of
        an issue."""
        self.assertEqual(response.status_code, 200)

        rl = response.context['recent_logs']

        self.assertEqual(len(rl), 2)

        self.assertEqual(rl[0].log_type,
                         IssueLogType.to_num(IssueLogType.DELETED))
        self.assertEqual(rl[1].log_type,
                         IssueLogType.to_num(IssueLogType.CREATED))

    @with_login('aphyr', 'admin1234')
    def test_recent_log_of_delete_issue__no_issue(self, response, user):
        """IssueLogs originated from deletion should have issue field
        set to None"""
        self.assertEqual(response.status_code, 200)

        for rl in response.context['recent_logs']:
            self.assertEqual(None, rl.issue)
