from django.shortcuts import redirect,render
from core.models import Label,Project
from core.forms import LabelForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy,reverse
from core.mixins import PorterAccessMixin,check_permissions
from django.db.models import Q
class LabelCreate(PorterAccessMixin, CreateView):
    model = Label
    fields = LabelForm.Meta.fields
    template_name = 'label/form.html'
    required_permissions = "change_label"

    def get_object(self, queryset=None):
        label = Label.objects.get(pk=self.kwargs['pk'])
        return label

    def get(self, request, *args, **kwargs):
        form = LabelForm()
        return render(request, 'label/form.html', {'project_title':kwargs['project_title'], 'form':form})

    def get_context_data(self, **kwargs):
        context = super(LabelCreate, self).get_context_data(**kwargs)
        context['project_title'] = self.kwargs['project_title']
        user = self.request.user
        context['change_label'] = check_permissions(user, 'change_label', **self.kwargs)
        return context

    def post(self, request, **kwargs):
        # create a form instance and populate it with data from the request:
        form = LabelForm(request.POST, auto_id=True)

        # check whether it's valid:
        if form.is_valid():
            project = Project.objects.get(title = kwargs['project_title'])
            form.instance.project = project
            form.save()
            return redirect(reverse('project:label:list', kwargs={'project_title': kwargs['project_title']}))
        else:
            return HttpResponseBadRequest


class LabelUpdate(PorterAccessMixin, UpdateView):
    model = Label
    fields = LabelForm.Meta.fields
    template_name = 'label/form.html'
    success_url = reverse_lazy('project:label:list')
    required_permissions = "change_label"

    def get_object(self):
        pk = self.kwargs['pk']
        return Label.objects.get(pk=pk)

    def get_context_data(self, **kwargs):
        context = super(LabelUpdate, self).get_context_data(**kwargs)
        context['project_title'] = self.kwargs['project_title']
        user = self.request.user
        context['change_label'] = check_permissions(user, 'change_label', **self.kwargs)
        return context

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('project:label:list',
                                   kwargs={'project_title': kwargs['project_title']})
        return super(LabelUpdate, self).post(request, *args, **kwargs)


class LabelDelete(DeleteView):
    model = Label
    template_name = 'label/confirm-delete.html'
    success_url = reverse_lazy('project:label:list')

class LabelDetail(PorterAccessMixin, DetailView):
    model = Label
    success_url = reverse_lazy('list')
    template_name = 'label/profile.html'

    def get_object(self):
        project_title = self.kwargs['project_title']
        pk = self.kwargs['pk']
        return Label.objects.get(pk=pk)

        return Project.objects.get(title=project_title)
    def get_context_data(self, **kwargs):
        context = super(LabelDetail, self).get_context_data(**kwargs)
        label = Label.objects.get(pk=self.kwargs['pk'])
        context['object'] = label.to_dict()
        return context

class LabelList(PorterAccessMixin, ListView):
    model = Label
    template_name = 'label/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(LabelList, self).get_context_data(**kwargs)
        user = self.request.user
        context['project_title'] = self.kwargs['project_title']
        context['label_list'] = Label.objects.filter(Q(project__title=self.kwargs['project_title']) | Q(project=None))
        context['change_label'] = check_permissions(user, 'change_label', **self.kwargs)
        return context
