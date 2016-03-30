import django

from django.contrib.auth.models import Group
from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    class Meta:
        permissions = [
            ('read_user', 'Can access detailed view for users.'),
            ('view_user', 'Can access the user application.')
        ]

    def __str__(self):
        return self.username


class Project(models.Model):
    title = models.CharField(max_length=50)
    users = models.ManyToManyField(User)
    class Meta:
        permissions = [
            ('read_userprojectrole', 'Can access detailed view for user project role.'),
            ('view_userprojectrole', 'Can access the user project role application.')
        ]

    def __str__(self):
        return self.title

class Repository(models.Model):
    title = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    class Meta:
        permissions = [
            ('read_repository', 'Can access detailed view for repositories.'),
            ('view_repository', 'Can access the user repository application.')
        ]

    def __str__(self):
        return self.title

class Milestone(models.Model):
    title = models.CharField(max_length=50)
    class Meta:
        permissions = [
            ('read_milestone', 'Can access detailed view milestones.'),
            ('view_milestone', 'Can access the user milestone application.')
        ]

    def __str__(self):
        return self.title

class Label(models.Model):
    title = models.CharField(max_length=50)
    class Meta:
        permissions = [
            ('read_label', 'Can access detailed view for labels.'),
            ('view_label', 'Can access the label application.')
        ]

    def __str__(self):
        return self.title

class Issue(models.Model):
    title = models.CharField(max_length=50)
    creator = models.ForeignKey(User, related_name='issues')
    assignee = models.ForeignKey(User, null=True, blank=True)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    milestone = models.ForeignKey(Milestone, null=True, blank=True)
    labels = models.ManyToManyField(Label)
    class Meta:
        permissions = [
            ('read_issue', 'Can access detailed view for issues.'),
            ('view_issue', 'Can access the issue application.')
        ]

    def __str__(self):
        return self.title

    def __str__(self):
        return self.title

class UserProjectRole(models.Model):
    role = models.ForeignKey(Group)
    user = models.ManyToManyField(django.contrib.auth.models.User, related_name='user_roles')
    project = models.ManyToManyField(Project, related_name='project_roles')
    class Meta:
        permissions = [
            ('read_userprojectrole', 'Can access detailed view for user project role.'),
            ('view_userprojectrole', 'Can access the user project role application.')
        ]

    def __str__(self):
        return "Role: %s; User: %s; Project: %s" % (self.role, self.user, self.project)

class IssueLog(models.Model):
    content = models.TextField()
    log_type = models.IntegerField()
    object_user = models.ForeignKey(User, related_name='issue_log_object')
    subject_user = models.ForeignKey(User, related_name='issue_log_subject')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    class Meta:
        permissions = [
            ('read_issuelog', 'Can access detailed view for issue logs.'),
            ('view_issuelog', 'Can access the issue log application.')
        ]

    def __str__(self):
        return self.content


class PorterGroup(Group):
    """
    Proxy class used to add new permissions to Group class from
    django.contrib.auth.models module.
    """
    class Meta:
        proxy = True
        permissions = [
            ('read_group', 'Can access detailed view for groups.'),
            ('view_group', 'Can access the group application.')
        ]
