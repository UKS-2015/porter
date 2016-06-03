from core.mixins import PorterAccessMixin, check_permissions
from django.shortcuts import redirect
from core.models import Milestone, Repository
from core.forms import MilestoneForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseBadRequest


class MilestoneCreate(PorterAccessMixin, CreateView):
    model = Milestone
    fields = MilestoneForm.Meta.fields
    template_name = 'milestone/form.html'
    required_permissions = "add_milestone"

    def get_context_data(self, **kwargs):
        context = super(MilestoneCreate, self).get_context_data(**kwargs)
        context['project_title'] = self.kwargs['project_title']
        return context

    def post(self, request, **kwargs):
        # create a form instance and populate it with data from the request:
        form = MilestoneForm(request.POST, auto_id=True)
        # check whether it's valid:
        if form.is_valid():
            repository_title = kwargs['repository_title']
            repository = Repository.objects.get(repository_title=repository_title)
            form.instance.repository = repository
            form.save()
            return redirect(reverse('project:milestone:list', kwargs={'project_title': kwargs['project_title']}))
        else:
            return HttpResponseBadRequest


class MilestoneUpdate(PorterAccessMixin, UpdateView):
    model = Milestone
    fields = MilestoneForm.Meta.fields
    template_name = 'milestone/form.html'
    success_url = reverse_lazy('list')
    required_permissions = "change_milestone"

    def get_object(self, queryset=None):
        milestone = Milestone.objects.get(pk=self.kwargs['pk'])
        return milestone

    def get_context_data(self, **kwargs):
        context = super(MilestoneUpdate, self).get_context_data(**kwargs)
        context['project_title'] = self.kwargs['project_title']
        return context

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('project:milestones:list',
                                   kwargs={'project_title': kwargs['project_title']})
        return super(MilestoneUpdate, self).post(request, *args, **kwargs)

class MilestoneDelete(PorterAccessMixin, DeleteView):
    model = Milestone
    template_name = 'milestone/confirm-delete.html'
    success_url = reverse_lazy('milestone:list')
    required_permissions = "delete_milestone"


class MilestoneDetail(PorterAccessMixin, DetailView):
    model = Milestone
    success_url = reverse_lazy('list')
    template_name = 'milestone/detail.html'
    required_permissions = "view_milestone"

    def get_context_data(self, **kwargs):
        context = super(MilestoneDetail, self).get_context_data(**kwargs)
        milestone = Milestone.objects.get(pk=self.kwargs['pk'])
        context['object'] = milestone.to_dict()
        context['project_title'] = self.kwargs['project_title']
        return context


class MilestoneList(PorterAccessMixin, ListView):
    model = Milestone
    template_name = 'milestone/list.html'
    paginate_by = 10
    required_permissions = "view_milestone"

    def get_context_data(self, **kwargs):
        context = super(MilestoneList, self).get_context_data(**kwargs)

        # Get project title from url params
        context['project_title'] = self.kwargs['project_title']

        # If url contains repo title param show only milestones for that repo
        if 'repository_title' in self.kwargs:
            repo_title = self.kwargs['repository_title']
            context['page_obj'] = [
                object.to_dict() for object in Milestone.objects.filter(repository__title=repo_title)
                ]
        else:
            context['page_obj'] = [
                object.to_dict() for object in Milestone.objects.filter(repository__project__title=self.kwargs['project_title'])
                ]
        user = self.request.user
        context['view_milestone'] = check_permissions(user, 'view_milestone', **self.kwargs)
        context['change_milestone'] = check_permissions(user, 'change_milestone', **self.kwargs)
        context['delete_milestone'] = check_permissions(user, 'delete_milestone', **self.kwargs)
        context['add_milestone'] = check_permissions(user, 'add_milestone', **self.kwargs)

        return context
