from django.shortcuts import redirect
from core.models import Group
from core.forms import GroupForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormMixin

class GroupCreate(CreateView):
    model = Group
    fields = GroupForm.Meta.fields
    template_name = 'group/form.html'

    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = GroupForm(request.POST, auto_id=True )
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect('group:list')

class GroupUpdate(UpdateView):
    model = Group
    fields = GroupForm.Meta.fields
    template_name = 'group/form.html'
    success_url = reverse_lazy('group:list')

class GroupDelete(DeleteView):
    model = Group
    template_name = 'group/confirm-delete.html'
    success_url = reverse_lazy('group:list')

class GroupDetail(DetailView):
    model = Group
    success_url = reverse_lazy('list')
    template_name = 'group/detail.html'

    def get_context_data(self, **kwargs):
        context = super(GroupDetail, self).get_context_data(**kwargs)
        group = Group.objects.get(pk=self.kwargs['pk'])
        context['object'] = group.to_dict()
        return context

class GroupList(ListView, FormMixin):
    model = Group
    template_name = 'issue/list.html'
    paginate_by = 10
    form_class = GroupForm

    def get_context_data(self, **kwargs):
        context = super(GroupList, self).get_context_data(**kwargs)
        context['page_obj'] = [{'id':object.id} for object in Group.objects.all()]
        return context
