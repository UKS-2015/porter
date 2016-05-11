from django.shortcuts import redirect
from core.models import Label
from core.forms import LabelForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy

class LabelCreate(CreateView):
    model = Label
    fields = LabelForm.Meta.fields
    template_name = 'label/form.html'

    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = LabelForm(request.POST, auto_id=True )
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect('label:list')

class LabelUpdate(UpdateView):
    model = Label
    fields = LabelForm.Meta.fields
    template_name = 'label/form.html'
    success_url = reverse_lazy('label:list')

class LabelDelete(DeleteView):
    model = Label
    template_name = 'label/confirm-delete.html'
    success_url = reverse_lazy('label:list')

class LabelDetail(DetailView):
    model = Label
    success_url = reverse_lazy('list')
    template_name = 'label/profile.html'

    def get_context_data(self, **kwargs):
        context = super(LabelDetail, self).get_context_data(**kwargs)
        label = Label.objects.get(pk=self.kwargs['pk'])
        context['object'] = label.to_dict()
        return context

class LabelList(ListView):
    model = Label
    template_name = 'label/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(LabelList, self).get_context_data(**kwargs)
        context['page_obj'] = [object.to_dict() for object in Label.objects.all()]
        return context
