from bootstrap3 import forms
from core.models import IssueLog, UserProjectRole, \
    Milestone, Label, Issue, User, Project, Repository, PorterUser
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.forms import ModelForm, inlineformset_factory, PasswordInput

PorterUserFormSet = inlineformset_factory(User, PorterUser, fields=('picture',))


class IssueLogForm(ModelForm):
    def __init__(self, project_title=None, **kwargs):
        super(ModelForm, self).__init__(**kwargs)
        # Show only issues and users related the the project
        if project_title:
            self.fields['issue'].queryset = Issue.objects.filter(repository__project__title=project_title).all()

            users = Project.objects.get(title=project_title).users
            self.fields['object_user'].queryset = users
            self.fields['subject_user'].queryset = users

    class Meta:
        model = IssueLog
        fields = ['content', 'log_type', 'object_user', 'subject_user', 'issue']


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']


class UserProjectRoleForm(ModelForm):
    class Meta:
        model = UserProjectRole
        fields = '__all__'


class MilestoneForm(ModelForm):
    class Meta:
        model = Milestone
        fields = ['title']


class LabelForm(ModelForm):
    class Meta:
        model = Label
        fields = '__all__'

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'assignee', 'repository', 'milestone', 'labels']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class PorterUserForm(ModelForm):
    class Meta:
        model = PorterUser
        fields = ['picture']


class UserPasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("instance")
        super(PasswordChangeForm, self).__init__(*args, **kwargs)


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']


class RepositoryForm(ModelForm):
    class Meta:
        model = Repository
        fields = ['title']


class RepositoryProjectForm(ModelForm):
    """
    Excludes project field so it can be added in a view. Will replace RepositoryForm.
    """

    class Meta:
        model = Repository
        exclude = ['id', 'project']
