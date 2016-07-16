from core.forms import ProjectForm, MilestoneForm, IssueForm
from core.mixins import PorterAccessMixin, check_permissions
from core.models import Project, UserProjectRole, Milestone, Repository, Issue
from django.contrib.auth.models import User, Group
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseBadRequest

GUEST_ROLE = 'Guest'
OWNER_ROLE = 'Project owner'
LEAD_ROLE = 'Project lead'


def _get_object(self):
    # Get project title from url params
    project_title = self.kwargs['project_title']
    return Project.objects.get(title=project_title)


class ProjectCreate(PorterAccessMixin, CreateView):
    model = Project
    fields = ProjectForm.Meta.fields
    template_name = 'project/form.html'
    required_permissions = 'create_project'
    success_url = reverse_lazy('user_projects')

    def get_context_data(self, **kwargs):
        context = super(ProjectCreate, self).get_context_data(**kwargs)
        return context

    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST, auto_id=True)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            form.instance.users = [request.user]
            group = Group.objects.get(name='owner')
            user_project_role = UserProjectRole(role=group, user=request.user, project=form.instance)
            user_project_role.save()
            return redirect(reverse('user_projects'))
        else:
            return HttpResponseBadRequest


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
    required_permissions = 'view_member'

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

        current_user = self.request.user

        context['users'] = users
        context['project_title'] = project_title
        context['roles'] = Group.objects.all()
        context['assign_role'] = check_permissions(current_user, 'assign_role', **self.kwargs)
        context['remove_member'] = check_permissions(current_user, 'remove_member', **self.kwargs)
        context['add_member'] = check_permissions(current_user, 'add_member', **self.kwargs)
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

    def get(self, request, *args, **kwargs):
        project_title = kwargs['project_title']
        project = get_object_or_404(Project, title=project_title)
        all_users =[user for user in User.objects.all() if user not in project.users.all()]
        paginator = Paginator(all_users, 25)
        page = request.GET.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

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

class ProjectMilestones(PorterAccessMixin, DetailView):
    model = Project
    success_url = reverse_lazy('project:overview')
    template_name = 'milestone/list.html'
    required_permissions = 'view_milestone'

    def get_object(self):
        # Get project title from url params
        project_title = self.kwargs['project_title']
        return Project.objects.get(title=project_title)

    def get_context_data(self, **kwargs):
        project_title = self.kwargs['project_title']
        context = super(ProjectMilestones, self).get_context_data(**kwargs)
        context['milestone_list'] = Milestone.objects.filter(repository__project__title=project_title).all()
        print(context['milestone_list'])
        print()
        print()
        current_user = self.request.user
        context['project_title'] = project_title
        context['remove_milestone'] = check_permissions(current_user, 'remove_milestone', **self.kwargs)
        context['change_milestone'] = check_permissions(current_user, 'change_milestone', **self.kwargs)
        context['delete_milestone'] = check_permissions(current_user, 'change_milestone', **self.kwargs)

        return context

class ProjectIssues(PorterAccessMixin, DetailView):
    model = Project
    template_name = 'issue/list.html'
    success_url = reverse_lazy('project:overview')
    paginate_by = 10
    required_permissions = "view_issue"

    def get_object(self):
        # Get project title from url params
        project_title = self.kwargs['project_title']
        return Project.objects.get(title=project_title)

    def get_context_data(self, **kwargs):
        context = super(ProjectIssues, self).get_context_data(**kwargs)
        # Get project title from url params
        project_title = self.kwargs['project_title']
        context['project_title'] = self.kwargs['project_title']
        context['issue_list'] = Issue.objects.filter(repository__project__title=project_title)
        user = self.request.user
        context['view_issue'] = check_permissions(user, 'view_issue', **self.kwargs)
        context['change_issue'] = check_permissions(user, 'change_issue', **self.kwargs)
        context['delete_issue'] = check_permissions(user, 'delete_issue', **self.kwargs)
        return context