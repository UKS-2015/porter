from core.models import IssueLog, UserProjectRole, \
    Milestone, Label, Issue, User, Project, Repository
from django.contrib.auth.models import Group
from django.forms import ModelForm


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
    def __init__(self, repository_title=None, **kwargs):
        super(ModelForm, self).__init__(**kwargs)
        # Repository is through view
        if repository_title:
            self.fields.pop('repository', None)

    class Meta:
        model = Issue
        fields = ['title', 'assignee', 'repository', 'milestone', 'labels']


class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ['id']


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['id']


class RepositoryForm(ModelForm):
    class Meta:
        model = Repository
        exclude = ['id']


class RepositoryProjectForm(ModelForm):
    """
    Excludes project field so it can be added in a view. Will replace RepositoryForm.
    """
    class Meta:
        model = Repository
        exclude = ['id', 'project']
