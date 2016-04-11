from django.shortcuts import redirect, get_object_or_404
from core.models import Issue
from core.forms import IssueForm
from django.core import serializers
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy

class IssueCreate(CreateView):
    model = Issue
    fields = IssueForm.Meta.fields
    template_name = 'issue/form.html'

    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = IssueForm(request.POST, auto_id=True )
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect('issue:list')

class IssueUpdate(UpdateView):
    model = Issue
    fields = IssueForm.Meta.fields
    template_name = 'issue/form.html'
    success_url = reverse_lazy('issue:list')

class IssueDelete(DeleteView):
    model = Issue
    template_name = 'issue/confirm-delete.html'
    success_url = reverse_lazy('issue:list')

class IssueDetail(DetailView):
    model = Issue
    success_url = reverse_lazy('list')
    template_name = 'issue/detail.html'

    def get_context_data(self, **kwargs):
        context = super(IssueDetail, self).get_context_data(**kwargs)
        issue = Issue.objects.get(pk=self.kwargs['pk'])
        context['object'] = issue.to_dict()
        return context

class IssueList(ListView):
    model = Issue
    template_name = 'issue/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(IssueList, self).get_context_data(**kwargs)
        context['page_obj'] = [object.to_dict() for object in Issue.objects.all()]
        return context
