from core.forms import IssueWithRepoForm, IssueFormWithMilestone, CommentForm, IssueForm
from core.mixins import PorterAccessMixin, check_permissions
from core.models import Issue, IssueLog, Repository, PorterUser, Comment, Label, Milestone
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect,render
from django.utils.datetime_safe import datetime
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.base import View

class IssueLogType():

    CREATED = 'Created'
    UPDATED = 'Updated'
    OPENED = 'Opened'
    CLOSED = 'Closed'
    DELETED = 'Deleted'
    ASSIGNED = 'Assigned'

    MESSAGES = {
        CREATED: "created the issue",
        UPDATED: "updated the issue",
        OPENED: "opened the issue",
        CLOSED: "closed the issue",
        DELETED: "deleted the issue",
        ASSIGNED: "assigned the issue"
    }

    @classmethod
    def to_num(cls, name):
        if name == cls.CREATED:
            return 1
        elif name == cls.UPDATED:
            return 2
        elif name == cls.OPENED:
            return 3
        elif name == cls.CLOSED:
            return 4
        elif name == cls.DELETED:
            return 5


def create_issue_log(issue, log_type, s_user, o_user):
    """
    Creates an issue log for an issue.
    :param log_type: Content of issue log is based on its type. See IssueLogType.
    :param s_user: User that do an action on the the issue
    :param o_user: User that is connected with an issue on some other way
    (e.g. issue assignee)
    :param issue:
    :return:
    """
    issue_log = IssueLog()
    issue_log.log_type = IssueLogType.to_num(log_type)

    issue_log.content = "{0} {1} {2}".format(s_user.username,
                                             IssueLogType.MESSAGES[log_type],
                                             issue.title)
    issue_log.subject_user = s_user
    issue_log.object_user = o_user
    issue_log.issue = issue
    issue_log.date_modified = datetime.now()
    issue_log.save()

def delete_with_issue_log(method):
    """Decorator that wraps POST method of IssueDelete to extend it with issue
    log creation"""
    def decorated_delete(request, *args, **kwargs):
        issue = Issue.objects.get(pk=kwargs['pk'])
        ret_val = method(request, *args, **kwargs)
        create_issue_log(issue, IssueLogType.DELETED, issue.creator,
                         issue.assignee)
        return ret_val
    return decorated_delete

class IssueCreate(PorterAccessMixin, CreateView):
    model = Issue
    fields = IssueWithRepoForm.Meta.fields
    template_name = 'issue/form.html'
    required_permissions = "add_issue"

    def get_context_data(self, **kwargs):
        context = super(IssueCreate, self).get_context_data(**kwargs)
        context['project_title'] = self.kwargs['project_title']
        form = IssueWithRepoForm(project_title=self.kwargs['project_title'])
        context['form'] = form
        user = self.request.user
        context['change_label'] = check_permissions(user, 'change_label', **self.kwargs)
        context['form'] = IssueWithRepoForm(project_title=
                                            context['project_title'])
        return context

    def post(self, request, *args, **kwargs):

        # create a form instance and populate it with data from the request:
        form = IssueWithRepoForm(post_form=request.POST, auto_id=True)
        # check whether it's valid:
        if form.is_valid():
            form.instance.creator = request.user
            form.instance.repository = Repository.objects.get(
                title=kwargs['repository_title'],
                project__title=kwargs['project_title'])

            if form.instance.assignee:
                form.instance.status = 'Assigned'

            form.save()
            create_issue_log(form.instance, IssueLogType.CREATED,
                             form.instance.creator, form.instance.assignee)
            return redirect(reverse('project:repository:issue:list', kwargs={
                'project_title': kwargs['project_title'],
                'repository_title': kwargs['repository_title']}))
        else:
            return HttpResponseBadRequest


    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(IssueCreate, self).form_valid(form)


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
        context['issue'] = self.kwargs['pk']
        instance = Issue.objects.get(pk=self.kwargs['pk'])
        form = IssueFormWithMilestone(instance=instance, project_title=self.kwargs['project_title'],repository_title=self.kwargs['repository_title'])
        context['form'] = form
        user = self.request.user
        context['change_label'] = check_permissions(user, 'change_label', **self.kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = IssueFormWithMilestone(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.instance.repository = Repository.objects.get(
                title=kwargs['repository_title'],
                project__title=kwargs['project_title'])

            if form.instance.assignee:
                form.instance.status = 'Assigned'

            form.instance.id = kwargs['pk']
            form.instance.creator = Issue.objects.get(id=kwargs['pk']).creator
            form.save()
            create_issue_log(form.instance, IssueLogType.UPDATED,
                             form.instance.creator, form.instance.assignee)

            if kwargs['repository_title']:
                return redirect(
                    reverse('project:repository:issue:list',
                            kwargs={'project_title': kwargs['project_title'],
                                    'repository_title': kwargs['repository_title']}))
            else:
                reverse('project:issues:list',
                        kwargs={'project_title': kwargs['project_title']})
        else:
            return HttpResponseBadRequest


class IssueDelete(PorterAccessMixin, DeleteView):
    model = Issue
    template_name = 'issue/confirm-delete.html'
    required_permissions = "delete_issue"

    def get_success_url(self):
        return reverse_lazy(
            'project:all_issues',
            kwargs={'project_title': self.object.repository.project.title})

    post = delete_with_issue_log(DeleteView.post)


class IssueChangeStatus(PorterAccessMixin, View):
    def get(self, request, *args, **kwargs):

        return reverse_lazy('project:issues:list',
                            args=[self.object.repository.project.title])

    def post(self, request, *args, **kwargs):
        issue = Issue.objects.get(pk=kwargs['pk'])
        if issue.status == 'Closed':
            if issue.assignee:
                issue.status = 'Assigned'
                create_issue_log(issue, IssueLogType.ASSIGNED, issue.creator,
                                 issue.assignee)
            else:
                issue.status = 'Opened'
                create_issue_log(issue, IssueLogType.OPENED, issue.creator,
                                 issue.assignee)
        else:
            issue.status = 'Closed'
            issue.save()
            create_issue_log(issue, IssueLogType.CLOSED, issue.creator,
                             issue.assignee)
            return redirect(
                reverse('project:repository:issue:list',
                        kwargs={'project_title': kwargs['project_title'],
                                'repository_title': kwargs[
                                    'repository_title']}))


class IssueOverview(PorterAccessMixin, DetailView):
    model = Issue
    success_url = reverse_lazy('list')
    template_name = 'issue/detail.html'
    required_permissions = "view_issue"

    def get_context_data(self, **kwargs):
        context = super(IssueOverview, self).get_context_data(**kwargs)
        issue = Issue.objects.get(pk=self.kwargs['pk'])

        user = self.request.user
        porteruser = PorterUser.objects.get(user=user)

        comments = []

        for comment in Comment.objects.filter(issue=issue):
            comment.porteruser = PorterUser.objects.get(user=comment.user)
            comments.append(comment)

        context['comments'] = comments
        context['porteruser'] = porteruser
        context['project_title'] = self.kwargs['project_title']
        context['repository_title'] = self.kwargs['repository_title']
        context['object'] = issue
        return context

    # Only comments are posted from this view
    def post(self, request, *args, **kwargs):
        print(request.POST)
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST, auto_id=True)
        # check whether it's valid:
        if form.is_valid():
            form.instance.user = request.user
            form.instance.issue = Issue.objects.get(pk=self.kwargs['pk'])
            form.save()
            return redirect(
                reverse('project:repository:issue:overview',
                        kwargs={
                            'project_title': kwargs['project_title'],
                            'repository_title': kwargs['repository_title'],
                            'pk': kwargs['pk']
                        }
                )
            )
        else:
            return HttpResponseBadRequest


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
                object for object in
                Issue.objects.filter(repository__title=repo_title,
                                     repository__project__title=project_title)
            ]
        else:
            context['issue_list'] = [
                object for object in Issue.objects.filter(
                    repository__project__title=project_title)
            ]

        user = self.request.user
        context['view_issue'] = check_permissions(user, 'view_issue',
                                                  **self.kwargs)
        context['change_issue'] = check_permissions(user, 'change_issue',
                                                    **self.kwargs)
        context['delete_issue'] = check_permissions(user, 'delete_issue',
                                                    **self.kwargs)
        context['add_issue'] = check_permissions(user, 'add_issue',
                                                 **self.kwargs)
        return context
