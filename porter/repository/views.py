from core.forms import RepositoryForm
from core.mixins import PorterAccessMixin, check_permissions
from core.models import Repository, Project, Issue, Milestone
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def _get_object(self):
    repository_title = self.kwargs['repository_title']
    project_title = self.kwargs['project_title']
    repository = Repository.objects.filter(title=repository_title, project__title=project_title)
    return repository


class RepositoryOverview(PorterAccessMixin, DetailView):
    model = Repository
    success_url = reverse_lazy('list')
    template_name = 'repository/overview.html'
    required_permissions = "view_repository"

    def get_object(self):
        return _get_object(self)

    def get_context_data(self, **kwargs):
        context = super(RepositoryOverview, self).get_context_data(**kwargs)
        context['project_title'] = self.kwargs['project_title']
        repository_title = self.kwargs['repository_title']
        repository = get_object_or_404(Repository, title=repository_title, project__title=self.kwargs['project_title'])
        context['repository'] = repository
        context['issues'] = [
            object for object in Issue.objects.filter(repository__title=repository_title,
                                                      repository__project__title=self.kwargs['project_title'])
            ]
        context['milestones'] = [
            object for object in Milestone.objects.filter(repository__title=repository_title,
                                                          repository__project__title=self.kwargs['project_title'])
            ]
        user = self.request.user
        context['view_repository'] = check_permissions(user, 'view_repository', **self.kwargs)
        context['change_repository'] = check_permissions(user, 'change_repository', **self.kwargs)
        context['delete_repository'] = check_permissions(user, 'delete_repository', **self.kwargs)
        context['add_milestone'] = check_permissions(user, 'add_milestone', **self.kwargs)
        context['view_milestone'] = check_permissions(user, 'view_milestone', **self.kwargs)
        context['change_milestone'] = check_permissions(user, 'change_milestone', **self.kwargs)
        context['delete_milestone'] = check_permissions(user, 'delete_milestone', **self.kwargs)
        context['add_issue'] = check_permissions(user, 'add_issue', **self.kwargs)
        context['change_issue'] = check_permissions(user, 'change_issue', **self.kwargs)
        context['delete_issue'] = check_permissions(user, 'delete_issue', **self.kwargs)
        return context


class RepositoryCreate(PorterAccessMixin, CreateView):
    model = Repository
    fields = RepositoryForm.Meta.fields
    template_name = 'repository/form.html'
    required_permissions = "add_repository"

    def get_object(self, queryset=None):
        return _get_object(self)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_title'] = self.kwargs['project_title']
        return context

    def post(self, request, project_title=None):
        # create a form instance and populate it with data from the request:
        form = RepositoryForm(request.POST, auto_id=True)
        # check whether it's valid:
        if form.is_valid():
            form.instance.project = Project.objects.get(title=project_title)
            form.save()
            self.kwargs['project_title'] = project_title
            return redirect(reverse('project:repository:list_all', kwargs={'project_title': project_title}))
        else:
            return HttpResponseBadRequest


class RepositoryUpdate(PorterAccessMixin, UpdateView):
    model = Repository
    fields = RepositoryForm.Meta.fields
    template_name = 'repository/form.html'
    required_permissions = "change_repository"
    success_url = reverse_lazy('list_all')
    project_title = 'project_title'

    # slug_field = 'repository_title'

    def get_object(self, queryset=None):
        return _get_object(self)

    def get(self, request, *args, **kwargs):
        repo = Repository.objects.get(title=kwargs['repository_title'], project__title=kwargs['project_title'])
        form = RepositoryForm(instance=repo)

        return render(request, 'repository/form.html', {'project_title': kwargs['project_title'], 'form': form})

    def post(self, request, *args, **kwargs):
        form = RepositoryForm(request.POST)
        if form.is_valid():
            form.instance.id = Repository.objects.get(title=kwargs['repository_title'],
                                                      project__title=kwargs['project_title']).id
            form.instance.project = Project.objects.get(title=kwargs['project_title'])

            form.save()
            # self.success_url = reverse('project:repository:list_all',
            #                            kwargs={'project_title': kwargs['project_title']})
            return redirect(
                reverse('project:repository:overview', kwargs={
                    'project_title': kwargs['project_title'],
                    'repository_title': form.instance.title
                })
            )
        else:
            return HttpResponseBadRequest


class RepositoryDelete(PorterAccessMixin, DeleteView):
    model = Repository
    template_name = 'repository/confirm-delete.html'
    required_permissions = "delete_repository"

    def get_object(self):
        return _get_object(self)

    def get_context_data(self, **kwargs):
        context = super(RepositoryDelete, self).get_context_data(**kwargs)
        context['project_title'] = self.kwargs['project_title']
        return context

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('project:repository:list_all',
                                   kwargs={'project_title': kwargs['project_title']})
        return super(RepositoryDelete, self).post(request, *args, **kwargs)


class RepositoryList(PorterAccessMixin, ListView):
    model = Repository
    template_name = 'repository/list.html'
    paginate_by = 10
    required_permissions = "view_repository"

    def get_context_data(self, **kwargs):
        context = super(RepositoryList, self).get_context_data(**kwargs)

        # Get project title from url params
        project_title = self.kwargs['project_title']
        context['repository_list'] = [
            object.to_dict() for object in Repository.objects.filter(project__title=project_title)
            ]
        context['project_title'] = project_title

        user = self.request.user

        context['project_title'] = self.kwargs['project_title']
        context['add_repository'] = check_permissions(user, 'add_repository', **self.kwargs)
        context['change_repository'] = check_permissions(user, 'change_repository', **self.kwargs)
        context['delete_repository'] = check_permissions(user, 'delete_repository', **self.kwargs)
        context['user'] = user

        return context
