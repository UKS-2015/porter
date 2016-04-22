from enum import Enum

from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from core.models import Issue, IssueLog
from core.forms import IssueForm
from django.core import serializers
from django.utils.datetime_safe import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy


class IssueLogType:
    CREATED = 'Created'
    UPDATED = 'Updated'
    OPENED = 'Opened'
    CLOSED = 'Closed'
    DELETED = 'Deleted'

    MESSAGES = {
        CREATED: "created the issue",
        UPDATED: "updated the issue",
        OPENED: "opened the issue",
        CLOSED: "closed the issue",
        DELETED: "deleted the issue"
    }


def create_issue_log(log_type, user, issue):
    """
    Creates an issue log for an issue.
    :param log_type: Content of issue log is based on its type. See IssueLogType.
    :param user: User that modified/created the issue
    :param issue:
    :return:
    """
    issue_log = IssueLog()
    issue_log.log_type = log_type

    issue_log.content = "{0} {1} {2}".format(user.name, IssueLogType.MESSAGES[log_type], issue.title)
    issue_log.subject_user = user
    issue_log.issue = issue
    issue_log.date_modified = datetime.now()
    IssueLog.save(issue)


class IssueCreate(CreateView):
    model = Issue
    fields = IssueForm.Meta.fields
    template_name = 'issue/form.html'

    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = IssueForm(request.POST, auto_id=True)
        # check whether it's valid:
        if form.is_valid():
            form.instance.creator = request.user
            form.save()
            return redirect('issue:list', self.args, self.kwargs)
        else:
            return HttpResponseBadRequest


class IssueUpdate(UpdateView):
    model = Issue
    fields = IssueForm.Meta.fields
    template_name = 'issue/form.html'
    success_url = reverse_lazy('issue:list')


class IssueDelete(DeleteView):
    model = Issue
    template_name = 'issue/confirm-delete.html'
    success_url = reverse_lazy('issue:list')


class IssueDetail(DetailView):
    model = Issue
    success_url = reverse_lazy('list')
    template_name = 'issue/detail.html'

    def get_context_data(self, **kwargs):
        context = super(IssueDetail, self).get_context_data(**kwargs)
        issue = Issue.objects.get(pk=self.kwargs['pk'])
        context['object'] = issue.to_dict()
        return context


class IssueList(ListView):
    model = Issue
    template_name = 'issue/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(IssueList, self).get_context_data(**kwargs)

        # Get project title from url params
        project_title = self.kwargs['project_title']

        # If url contains repo title param show only milestones for that repo
        if 'repository_title' in self.kwargs:
            repo_title = self.kwargs['repository_title']
            context['page_obj'] = [
                object.to_dict() for object in Issue.objects.filter(repository__title=repo_title)
                ]
        else:
            context['page_obj'] = [
                object.to_dict() for object in Issue.objects.filter(repository__project__title=project_title)
                ]

        return context
