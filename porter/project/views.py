from core.mixins import PorterAccessMixin, check_permissions
from django.contrib.auth.models import User, Group
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, request
from django.shortcuts import redirect, get_object_or_404, render
from core.models import Project, UserProjectRole
from core.forms import ProjectForm
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy, reverse

GUEST_ROLE = 'Guest'

def _get_object(self):
    # Get project title from url params
    project_title = self.kwargs['project_title']
    return Project.objects.get(title=project_title)


class ProjectCreate(PorterAccessMixin, CreateView):
    model = Project
    template_name = 'project/form.html'
    required_permissions = 'create_project'

    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST, auto_id=True)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect('project:overview')


class ProjectSettings(PorterAccessMixin, UpdateView):
    model = Project
    fields = ProjectForm.Meta.fields
    template_name = 'project/form.html'
    success_url = reverse_lazy('project:overview')
    required_permissions = 'change_project'

    def get_object(self):
        return _get_object(self)

    def get_context_data(self, **kwargs):
        context = super(ProjectSettings, self).get_context_data(**kwargs)
        context['project'] = self.get_object()

        user = self.request.user
        context['change_project'] = check_permissions(user, 'change_project', **self.kwargs)
        context['delete_repository'] = check_permissions(user, 'delete_repository', **self.kwargs)
        return context


class ProjectDelete(PorterAccessMixin, DeleteView):
    model = Project
    template_name = 'project/confirm-delete.html'
    success_url = reverse_lazy('project:overview')


class ProjectMembers(PorterAccessMixin, DetailView):
    model = Project
    success_url = reverse_lazy('project:overview')
    template_name = 'project/members.html'
    required_permissions = 'add_member'

    def get_object(self):
        # Get project title from url params
        project_title = self.kwargs['project_title']
        return Project.objects.get(title=project_title)

    def get_context_data(self, **kwargs):
        project_title = self.kwargs['project_title']
        context = super(ProjectMembers, self).get_context_data(**kwargs)
        users = []

        uprs = UserProjectRole.objects.filter(project__title=project_title).all()

        # Make it easier to get user roles
        # A little bit of monkey patching never hurt nobody
        for upr in uprs:
            user = upr.user
            user.role = upr.role
            users.append(user)

        context['users'] = users
        context['project_title'] = project_title
        context['roles'] = Group.objects.all()
        return context


class ProjectMemberRemove(PorterAccessMixin, View):
    required_permissions = 'remove_member'

    def get_object(self):
        return _get_object(self)

    def get(self, request, *args, **kwargs):
        project_title = self.kwargs['project_title']
        user = User.objects.get(pk=self.kwargs['user_id'])
        upr = UserProjectRole.objects.get(project__title=project_title, user=user)
        UserProjectRole.delete(upr)
        return redirect(reverse('project:members', kwargs={'project_title': project_title}))


class ProjectAssignRole(PorterAccessMixin, View):
    required_permissions = 'assign_role'

    def post(self, request, *args, **kwargs):
        project_title = self.kwargs['project_title']
        user = User.objects.get(pk=request.POST.get('user_id'))
        upr = UserProjectRole.objects.get(project__title=project_title, user=user)
        upr.role = Group.objects.get(pk=request.POST.get('role_id'))
        UserProjectRole.save(upr)
        project_title = kwargs['project_title']
        return redirect(reverse('project:members', kwargs={'project_title': project_title}))


class ProjectDetail(PorterAccessMixin, DetailView):
    model = Project
    success_url = reverse_lazy('project:overview')
    template_name = 'project/overview.html'
    required_permissions = None

    def get_object(self):
        # Get project title from url params
        project_title = self.kwargs['project_title']
        return Project.objects.get(title=project_title)

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['project'] = self.get_object()
        context['change_project'] = check_permissions(self.request.user, 'change_project', **self.kwargs)
        return context


class ProjectMemberAdd(PorterAccessMixin, View):
    required_permissions = 'add_member'

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
        upr = UserProjectRole()

        upr.role = Group.objects.get(name=GUEST_ROLE)
        upr.user = user
        upr.project = project
        UserProjectRole.save(upr)

        return redirect(reverse('project:members', kwargs={'project_title': project_title}))
