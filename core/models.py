import django

from django.contrib.auth.models import Group, User
from django.db import models
from django.core.urlresolvers import reverse

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

    def to_dict(instance):
        opts = instance._meta
        data = {}
        data['id'] = instance.id
        data['first_name'] = instance.first_name
        data['last_name'] = instance.last_name
        data['username'] = instance.username
        return data


class Project(models.Model):
    title = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    users = models.ManyToManyField(django.contrib.auth.models.User)
    class Meta:
        permissions = [
            ('read_userprojectrole', 'Can access detailed view for user project role.'),
            ('view_userprojectrole', 'Can access the user project role application.')
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

    class Meta:
        permissions = [
            ('read_repository', 'Can access detailed view for repositories.'),
            ('view_repository', 'Can access the user repository application.')
        ]

    def __str__(self):
        return self.title

    def to_dict(instance):
        opts = instance._meta
        data = {}
        data['id'] = instance.id
        data['title'] = instance.title
        data['project'] = Project.objects.get(pk = instance.project.id)
        return data

class Milestone(models.Model):
    title = models.CharField(max_length=50)
    repository = models.ForeignKey(Repository, related_name='milestones')

    def get_absolute_url(self):
        return reverse('milestone-detail', kwargs={'pk': self.pk})

    class Meta:
        permissions = [
            ('read_milestone', 'Can access detailed view milestones.'),
            ('view_milestone', 'Can access the user milestone application.')
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
            ('read_label', 'Can access detailed view for labels.'),
            ('view_label', 'Can access the label application.')
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
    labels = models.ManyToManyField(Label)
    class Meta:
        permissions = [
            ('read_issue', 'Can access detailed view for issues.'),
            ('view_issue', 'Can access the issue application.')
        ]

    def __str__(self):
        return self.title

    def to_dict(instance):
        data = {}
        data['id'] = instance.id
        data['title'] = instance.title
        data['creator'] = User.objects.get(pk = instance.creator.id)
        data['assignee'] = User.objects.get(pk = instance.assignee.id)
        data['repository'] = Repository.objects.get(pk = instance.repository.id)
        data['milestone'] = Milestone.objects.get(pk = instance.milestone.id)
        data['labels'] = [label for label in instance.labels.all()]
        return data

class UserProjectRole(models.Model):
    role = models.ForeignKey(Group)
    user = models.ManyToManyField(User, related_name='user_roles')
    project = models.ManyToManyField(Project, related_name='project_roles')
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
        data = {}
        data['id'] = instance.id
        data['content'] = instance.content
        data['log_type'] = instance.log_type
        data['object_user'] = User.objects.get(pk = instance.object_user.id)
        data['subject_user'] = User.objects.get(pk = instance.subject_user.id)
        data['issue'] = Issue.objects.get(pk = instance.issue.id)
        return data

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

    def to_dict(instance):
        data = {}
        data['id'] = instance.id
        data['name'] = instance.name
        return data
