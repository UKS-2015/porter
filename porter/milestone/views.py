from django.shortcuts import redirect
from core.models import Milestone, Repository
from core.forms import MilestoneForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy


class MilestoneCreate(CreateView):
    model = Milestone
    fields = MilestoneForm.Meta.fields
    template_name = 'milestone/form.html'

    def post(self, request, **kwargs):
        # create a form instance and populate it with data from the request:
        form = MilestoneForm(request.POST, auto_id=True)
        # check whether it's valid:
        if form.is_valid():
            repository_title = kwargs['repository_title']
            repository = Repository.objects.find(repository_title=repository_title)
            form.instance.repository = repository
            form.save()
            return redirect('milestone:list')


class MilestoneUpdate(UpdateView):
    model = Milestone
    fields = MilestoneForm.Meta.fields
    template_name = 'milestone/form.html'
    success_url = reverse_lazy('milestone:list')


class MilestoneDelete(DeleteView):
    model = Milestone
    template_name = 'milestone/confirm-delete.html'
    success_url = reverse_lazy('milestone:list')


class MilestoneDetail(DetailView):
    model = Milestone
    success_url = reverse_lazy('list')
    template_name = 'milestone/detail.html'

    def get_context_data(self, **kwargs):
        context = super(MilestoneDetail, self).get_context_data(**kwargs)
        issue = Milestone.objects.get(pk=self.kwargs['pk'])
        context['object'] = issue.to_dict()
        return context


class MilestoneList(ListView):
    model = Milestone
    template_name = 'milestone/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(MilestoneList, self).get_context_data(**kwargs)

        # Get project title from url params
        project_title = self.kwargs['project_title']

        # If url contains repo title param show only milestones for that repo
        if 'repository_title' in self.kwargs:
            repo_title = self.kwargs['repository_title']
            context['page_obj'] = [
                object.to_dict() for object in Milestone.objects.filter(repository__title=repo_title)
                ]
        else:
            context['page_obj'] = [
                object.to_dict() for object in Milestone.objects.filter(repository__project__title=project_title)
                ]

        return context
