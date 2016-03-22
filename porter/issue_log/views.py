from core.forms import IssueLogForm
from core.models import IssueLog
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.

def list_all(request):
    paginator = Paginator(IssueLog.objects.all(), 25)
    # Pagination page number check
    page = request.GET.get('page')
    try:
        issue_logs = paginator.page(page)
    except PageNotAnInteger:
        issue_logs = paginator.page(1)
    except EmptyPage:
        issue_logs = paginator.page(paginator.num_pages)
    return render(request, 'issue_log/list.html', {'issue_logs': issue_logs})


def edit(request, issue_log_id):
    if request.method == 'GET':
        issue_log = get_object_or_404(IssueLog, pk=issue_log_id)
        form = IssueLogForm(instance=issue_log)
        return render(request, 'issue_log/edit.html', {'issue_log': form})
    elif request.method == 'POST':
        form = IssueLogForm(request.POST)
        issue_log = form.instance
        # Doesn't have an id apparently
        issue_log.id = issue_log_id
        if form.is_valid():
            IssueLog.save(issue_log)
            return redirect(list_all)
        else:
            # TODO: Front end validation
            return render(request, 'issue_log/edit.html', {'issue_log': form})
    else:
        return HttpResponseBadRequest


def create(request):
    form = IssueLogForm(request.POST)
    if request.method == 'GET':
        return render(request, 'issue_log/create.html', {'issue_log': form.as_table()})
    elif request.method == 'POST':
        form = IssueLogForm(request.POST)
        if form.is_valid():
            issue_log = form.instance
            IssueLog.save(issue_log)
            return redirect(list_all)
        else:
            return HttpResponseBadRequest


def detail(request, issue_log_id):
    issue_log = IssueLog.objects.get(pk=issue_log_id)
    return render(request, 'issue_log/detail.html', {'issue_log': issue_log})


def delete(request, issue_log_id):
    try:
        issue_log = IssueLog.objects.get(pk=issue_log_id)
        IssueLog.delete(issue_log)
        return redirect(list_all)
    except:
        raise Http404("Issue log doesn't exist.")
