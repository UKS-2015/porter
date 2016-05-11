from django.shortcuts import redirect
from core.models import UserProjectRole
from core.forms import UserProjectRoleForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy

class UserProjectRoleCreate(CreateView):
    model = UserProjectRole
    fields = UserProjectRoleForm.Meta.fields
    template_name = 'user_project_role/form.html'

    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = UserProjectRoleForm(request.POST, auto_id=True )
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect('user_project_role:list')

class UserProjectRoleUpdate(UpdateView):
    model = UserProjectRole
    fields = UserProjectRoleForm.Meta.fields
    template_name = 'user_project_role/form.html'
    success_url = reverse_lazy('user_project_role:list')

class UserProjectRoleDelete(DeleteView):
    model = UserProjectRole
    template_name = 'user_project_role/confirm-delete.html'
    success_url = reverse_lazy('user_project_role:list')

class UserProjectRoleDetail(DetailView):
    model = UserProjectRole
    success_url = reverse_lazy('list')
    template_name = 'user_project_role/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProjectRoleDetail, self).get_context_data(**kwargs)
        user_project_role = UserProjectRole.objects.get(pk=self.kwargs['pk'])
        context['object'] = user_project_role.to_dict()
        return context

class UserProjectRoleList(ListView):
    model = UserProjectRole
    template_name = 'user_project_role/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(UserProjectRoleList, self).get_context_data(**kwargs)
        context['page_obj'] = [object.to_dict() for object in UserProjectRole.objects.all()]
        return context
