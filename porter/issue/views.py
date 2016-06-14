from core.forms import IssueForm, IssueWithRepoForm, IssueFormWithMilestone
from core.mixins import PorterAccessMixin, check_permissions
from core.models import Issue, IssueLog, Repository, Project
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils.datetime_safe import datetime
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

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

class IssueCreate(PorterAccessMixin, CreateView):
    model = Issue
    fields = IssueWithRepoForm.Meta.fields
    template_name = 'issue/form.html'
    required_permissions = "add_issue"

    def get_context_data(self, **kwargs):
        context = super(IssueCreate, self).get_context_data(**kwargs)
        context['project_title'] = self.kwargs['project_title']
        return context

    def post(self, request, *args, **kwargs):

        # create a form instance and populate it with data from the request:
        form = IssueWithRepoForm(request.POST, auto_id=True)
        # check whether it's valid:
        if form.is_valid():
            form.instance.creator = request.user

            try:
                form.instance.repository
            except AttributeError:
                form.instance.repository = Repository.objects.get(
                    project=Project.objects.get(title=kwargs['project_title']))

            form.save()
            return redirect(reverse('project:issues:list', kwargs={'project_title': kwargs['project_title']}))
        else:
            return HttpResponseBadRequest


class IssueUpdate(PorterAccessMixin, UpdateView):
    model = Issue
    fields = IssueFormWithMilestone.Meta.fields
    template_name = 'issue/form.html'
    success_url = reverse_lazy('list')
    required_permissions = "change_issue"
    project_title = 'project_title'

    def get_object(self, queryset=None):
        issue = Issue.objects.get(pk=self.kwargs['pk'])
        return issue

    def get_context_data(self, **kwargs):
        context = super(IssueUpdate, self).get_context_data(**kwargs)
        context['project_title'] = self.kwargs['project_title']
        return context

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('project:issues:list',
                                   kwargs={'project_title': kwargs['project_title']})
        return super(IssueUpdate, self).post(request, *args, **kwargs)

class IssueDelete(PorterAccessMixin, DeleteView):
    model = Issue
    template_name = 'issue/confirm-delete.html'
    required_permissions = "delete_issue"

    def get_success_url(self):
        return reverse_lazy('project:issues:list',
                            args=[self.object.repository.project.title])

class IssueOverview(PorterAccessMixin, DetailView):
    model = Issue
    success_url = reverse_lazy('list')
    template_name = 'issue/detail.html'
    required_permissions = "view_issue"

    def get_context_data(self, **kwargs):
        context = super(IssueOverview, self).get_context_data(**kwargs)
        issue = Issue.objects.get(pk=self.kwargs['pk'])
        context['project_title'] = self.kwargs['project_title']
        context['object'] = issue
        return context

class IssueList(PorterAccessMixin, ListView):
    model = Issue
    template_name = 'issue/list.html'
    paginate_by = 10
    required_permissions = "view_issue"

    def get_context_data(self, **kwargs):
        context = super(IssueList, self).get_context_data(**kwargs)

        # Get project title from url params
        project_title = self.kwargs['project_title']
        context['project_title'] = self.kwargs['project_title']
        # If url contains repo title param show only milestones for that repo
        if 'repository_title' in self.kwargs:
            repo_title = self.kwargs['repository_title']
            context['issue_list'] = [
                object for object in Issue.objects.filter(repository__title=repo_title)
            ]
        else:
            context['issue_list'] = [
                object for object in Issue.objects.filter(repository__project__title=project_title)
            ]

        user = self.request.user
        context['view_issue'] = check_permissions(user, 'view_issue', **self.kwargs)
        context['change_issue'] = check_permissions(user, 'change_issue', **self.kwargs)
        context['delete_issue'] = check_permissions(user, 'delete_issue', **self.kwargs)
        context['add_issue'] = check_permissions(user, 'add_issue', **self.kwargs)
        return context
