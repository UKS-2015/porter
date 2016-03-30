from django.contrib.auth.models import Group
from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Project(models.Model):
    title = models.CharField(max_length=50)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.title

class Repository(models.Model):
    title = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Milestone(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Label(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Issue(models.Model):
    title = models.CharField(max_length=50)
    creator = models.ForeignKey(User, related_name='issues')
    assignee = models.ForeignKey(User, null=True, blank=True)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    milestone = models.ForeignKey(Milestone, null=True, blank=True)
    labels = models.ManyToManyField(Label)

    def __str__(self):
        return self.title

class UserProjectRole(models.Model):
    role = models.ForeignKey(Group)
    user = models.ManyToManyField(User, related_name='user_roles')
    repository = models.ManyToManyField(Repository, related_name='repository_roles')

class IssueLog(models.Model):
    content = models.TextField()
    log_type = models.IntegerField()
    object_user = models.ForeignKey(User, related_name='issue_log_object')
    subject_user = models.ForeignKey(User, related_name='issue_log_subject')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
