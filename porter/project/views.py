from django.contrib.auth.models import User
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, request
from django.shortcuts import redirect, get_object_or_404, render
from core.models import Project
from core.forms import ProjectForm
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy, reverse


class ProjectCreate(CreateView):
    model = Project
    template_name = 'project/form.html'

    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST, auto_id=True)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect('project:overview')


class ProjectUpdate(UpdateView):
    model = Project
    template_name = 'project/form.html'
    success_url = reverse_lazy('project:overview')


class ProjectDelete(DeleteView):
    model = Project
    template_name = 'project/confirm-delete.html'
    success_url = reverse_lazy('project:overview')


class ProjectMembers(DetailView):
    model = Project
    success_url = reverse_lazy('project:overview')
    template_name = 'project/members.html'

    def get_object(self):
        # Get project title from url params
        project_title = self.kwargs['project_title']
        return Project.objects.get(title=project_title)

    def get_context_data(self, **kwargs):
        project_title = self.kwargs['project_title']
        context = super(ProjectMembers, self).get_context_data(**kwargs)
        context['users'] = self.get_object().users.all()
        context['project_title'] = project_title
        return context


class ProjectMemberRemove(View):
    def get(self, request, *args, **kwargs):
        project_title = kwargs['project_title']
        user_id = kwargs['user_id']
        project = Project.objects.get(title=project_title)
        user = User.objects.get(pk=user_id)
        project.users.remove(user)

        return redirect(reverse('project:members', kwargs={'project_title': project_title}))


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


class ProjectMemberAdd(View):
    def get_paginator(self, request):
        paginator = Paginator(User.objects.all(), 25)
        page = request.GET.get('page')

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        return users

    def get(self, request, *args, **kwargs):
        project_title = kwargs['project_title']
        users = self.get_paginator(request)
        return render(request, 'project/members_add.html', {'project_title': project_title, 'users': users})


    def post(self, request, *args, **kwargs):
        project_title = kwargs['project_title']
        user_id = request.POST.get('user_id')

        project = get_object_or_404(Project, title=project_title)
        user = get_object_or_404(User, pk=user_id)
        project.users.add(user)

        return redirect(reverse('project:members', kwargs={'project_title': project_title}))

