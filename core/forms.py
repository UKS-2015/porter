from core.models import IssueLog
from django import forms
from django.contrib.auth.models import Group


class IssueLogForm(forms.ModelForm):
    class Meta:
        model = IssueLog
        fields = ['content', 'content', 'log_type', 'object_user', 'subject_user', 'issue']


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']
