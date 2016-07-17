import django

from django.contrib.auth.models import Group, User, AbstractUser
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models import OneToOneField
from porter import settings


class PorterUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    picture = models.ImageField(upload_to="users", null=True, blank=True)

    class Meta:
        permissions = [
            ('read_user', 'Can access detailed view for users.'),
            ('view_user', 'Can access the user application.'),
            ('view_member', 'Can access the list of project members'),
            ('add_member', 'Can add members to a project'),
            ('remove_member', 'Can remove members from a project'),
            ('assign_role', 'Can assign roles to members')
        ]

    def __str__(self):
        return self.user.username

    def to_dict(instance):
        opts = instance._meta
        data = {}
        data['picture'] = instance.picture
        data['first_name'] = instance.user.last_name
        data['last_name'] = instance.user.last_name
        data['username'] = instance.user.username
        data['last_login'] = instance.user.last_login
        data['date_joined'] = instance.user.date_joined
        return data


class Project(models.Model):
    title = models.CharField(max_length=50, unique=True, null=False, blank=False, default="Project")
    description = models.CharField(max_length=255, null=False, blank=False, default="")
    users = models.ManyToManyField(User)

    class Meta:
        permissions = [
            ('view_projects', 'Can view all existing projects.'),
        ]

    def __str__(self):
        return self.title

    def to_dict(instance):
        opts = instance._meta
        data = {}
        data['id'] = instance.id
        data['title'] = instance.title
        data['users'] = [user for user in instance.users.all()]
        for f in opts.concrete_fields:
            data[f.name] = f.value_from_object(instance)
        return data


class Repository(models.Model):
    title = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=False, blank=False, default="")

    class Meta:
        permissions = [
            ('view_repository', 'Can see repositories inside a project.')
        ]

    def __str__(self):
        return self.title

    def to_dict(instance):
        opts = instance._meta
        data = {}
        data['id'] = instance.id
        data['title'] = instance.title
        data['project'] = Project.objects.get(pk=instance.project.id)
        return data


class Milestone(models.Model):
    title = models.CharField(max_length=50)
    repository = models.ForeignKey(Repository, related_name='milestones')
    description = models.CharField(max_length=255, null=False, blank=False, default="")

    def get_absolute_url(self):
        return reverse('milestone-detail', kwargs={'pk': self.pk})

    class Meta:
        permissions = [
            ('view_milestone', 'Can see milestone.')
        ]

    def __str__(self):
        return self.title

    def to_dict(instance):
        opts = instance._meta
        data = {}
        data['id'] = instance.id
        data['title'] = instance.title
        return data


class Label(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        permissions = [
            ('view_label', 'Can see labels.')
        ]

    def __str__(self):
        return self.title

    def to_dict(instance):
        opts = instance._meta
        data = {}
        data['id'] = instance.id
        data['title'] = instance.title
        return data


class Issue(models.Model):
    title = models.CharField(max_length=50)
    creator = models.ForeignKey(User, related_name='issues')
    assignee = models.ForeignKey(User, null=True, blank=True)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    milestone = models.ForeignKey(Milestone, null=True, blank=True, related_name="issues")
    labels = models.ManyToManyField(Label, blank=True)
    description = models.CharField(max_length=255, null=False, blank=False, default="")

    STATUS_CHOICES = (
        ('OPENED', 'Opened'),
        ('ASSIGNED', 'Assigned'),
        ('CLOSED', 'Closed'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='Opened')

    class Meta:
        permissions = [
            ('view_issue', 'Can view issues inside a project.'),
            ('can_change_own_issue', 'Can only change owned issues'),
            ('can_delete_own_issue', 'Can only delete owned issues'),
            ('can_close_own_issue', 'Can only close owned issues'),
            ('can_close_issue', 'Can close issues'),
        ]

    def __str__(self):
        return self.title

    def to_dict(instance):
        data = {}
        data['id'] = instance.id
        data['title'] = instance.title
        data['creator'] = instance.creator
        if instance.assignee:
            data['assignee'] = instance.assignee

        data['repository'] = instance.repository

        if instance.milestone:
            data['milestone'] = instance.milestone.id

        data['labels'] = [label for label in instance.labels.all()]

        return data


class UserProjectRole(models.Model):
    role = models.ForeignKey(Group)
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)

    class Meta:
        permissions = [
            ('read_userprojectrole', 'Can access detailed view for user project role.'),
            ('view_userprojectrole', 'Can access the user project role application.')
        ]

    def __str__(self):
        return "Role: %s; User: %s; Project: %s" % (self.role, self.user, self.project)

    def to_dict(instance):
        data = {}
        data['id'] = instance.id
        data['role'] = instance.role
        data['user'] = [user for user in instance.user.all()]
        data['project'] = [project for project in instance.project.all()]
        return data


class IssueLog(models.Model):
    content = models.TextField()
    log_type = models.IntegerField()
    object_user = models.ForeignKey(User, related_name='issue_log_object')
    subject_user = models.ForeignKey(User, related_name='issue_log_subject')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(null=False, auto_now=True)

    class Meta:
        permissions = [
            ('read_issuelog', 'Can access detailed view for issue logs.'),
            ('view_issuelog', 'Can access the issue log application.')
        ]

    def __str__(self):
        return self.content

    def to_dict(instance):
        return {
            'id': instance.id,
            'content': instance.content,
            'log_type': instance.log_type,
            'object_user': User.objects.get(pk=instance.object_user.id),
            'subject_user': User.objects.get(pk=instance.subject_user.id),
            'issue': Issue.objects.get(pk=instance.issue.id)
        }


class PorterGroup(Group):
    """
    Proxy class used to add new permissions to Group class from
    django.contrib.auth.models module.
    """

    class Meta:
        proxy = True
        permissions = [
            ('read_group', 'Can access detailed view for groups.'),
            ('view_group', 'Can access the group application.'),
        ]

    def to_dict(instance):
        data = {}
        data['id'] = instance.id
        data['name'] = instance.name
        return data


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User)
    datestamp = models.DateTimeField(null=False, auto_now=True)
    issue = models.ForeignKey(Issue, related_name='issue_comments')

    def to_dict(instance):
        return {
            'id': instance.id,
            'content': instance.content,
            'user': User.objects.get(pk=instance.user.id),
            'datestamp': instance.datestamp,
            'issue': Issue.objects.get(pk=instance.issue.id)
        }
