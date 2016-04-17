from django.shortcuts import redirect
from core.models import Project
from core.forms import ProjectForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy


class ProjectCreate(CreateView):
    model = Project
    template_name = 'project/form.html'

    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST, auto_id=True)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect('project:list')


class ProjectUpdate(UpdateView):
    model = Project
    template_name = 'project/form.html'
    success_url = reverse_lazy('project:list')


class ProjectDelete(DeleteView):
    model = Project
    template_name = 'project/confirm-delete.html'
    success_url = reverse_lazy('project:list')


class ProjectDetail(DetailView):
    model = Project
    success_url = reverse_lazy('project:overview')
    template_name = 'project/overview.html'

    def get_object(self):
        # Get project title from url params
        project_title = self.kwargs['project_title']
        return Project.objects.get(title=project_title)

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['project'] = self.get_object()
        return context

