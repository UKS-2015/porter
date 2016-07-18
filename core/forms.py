from bootstrap3 import forms
from core.models import IssueLog, UserProjectRole, \
    Milestone, Label, Issue, User, Project, Repository, PorterUser, Comment
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.forms import ModelForm, inlineformset_factory

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
    def __init__(self, *args, **kwargs):
        super(MilestoneForm, self).__init__(*args, **kwargs)
        print(self.fields['repository'].queryset)
        self.initial['repository'] = Repository.objects.filter(project__title='Projekat')

    class Meta:
        model = Milestone
        fields = ['title', 'description', 'repository']


class MilestoneWithRepoForm(ModelForm):
    class Meta:
        model = Milestone
        fields = ['title', 'description']


class LabelForm(ModelForm):
    class Meta:
        model = Label
        fields = '__all__'


class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'assignee', 'repository', 'labels']


class IssueWithRepoForm(ModelForm):
    def __init__(self, project_title=None, post_form=None,  **kwargs):
        super().__init__(post_form, **kwargs)
        if project_title:
            self.fields['assignee'].queryset = Project.objects.get(
                title=project_title).users

    class Meta:
        model = Issue
        fields = ['title', 'description', 'assignee', 'labels']


class IssueFormWithMilestone(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'assignee', 'milestone', 'labels']


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
        fields = '__all__'


class RepositoryForm(ModelForm):
    class Meta:
        model = Repository
        fields = ['title', 'description']


class RepositoryProjectForm(ModelForm):
    """
    Excludes project field so it can be added in a view. Will replace RepositoryForm.
    """

    class Meta:
        model = Repository
        exclude = ['id', 'project']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
