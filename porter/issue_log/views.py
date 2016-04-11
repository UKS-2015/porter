from django.shortcuts import redirect
from core.models import IssueLog
from core.forms import IssueLogForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy

class IssueLogCreate(CreateView):
    model = IssueLog
    fields = IssueLogForm.Meta.fields
    template_name = 'issue_log/form.html'

    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = IssueLogForm(request.POST, auto_id=True )
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect('issue_log:list')

class IssueLogUpdate(UpdateView):
    model = IssueLog
    fields = IssueLogForm.Meta.fields
    template_name = 'issue_log/form.html'
    success_url = reverse_lazy('issue_log:list')

class IssueLogDelete(DeleteView):
    model = IssueLog
    template_name = 'issue_log/confirm-delete.html'
    success_url = reverse_lazy('issue_log:list')

class IssueLogDetail(DetailView):
    model = IssueLog
    success_url = reverse_lazy('list')
    template_name = 'issue_log/detail.html'

    def get_context_data(self, **kwargs):
        context = super(IssueLogDetail, self).get_context_data(**kwargs)
        issue_log = IssueLog.objects.get(pk=self.kwargs['pk'])
        context['object'] = issue_log.to_dict()
        return context

class IssueLogList(ListView):
    model = IssueLog
    template_name = 'issue_log/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(IssueLogList, self).get_context_data(**kwargs)
        context['page_obj'] = [object.to_dict() for object in IssueLog.objects.all()]
        return context
