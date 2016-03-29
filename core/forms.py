from core.models import IssueLog, UserProjectRole, Milestone, Label, Issue
from django.forms import ModelForm
from django.contrib.auth.models import Group


class IssueLogForm(ModelForm):
    class Meta:
        model = IssueLog
        fields = ['content', 'content', 'log_type', 'object_user', 'subject_user', 'issue']


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']


class UserProjectRoleForm(ModelForm):
    class Meta:
        model = UserProjectRole
        fields = ['role', 'user', 'repository']

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
        fields = '__all__'