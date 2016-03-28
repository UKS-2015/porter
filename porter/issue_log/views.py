from core.forms import IssueLogForm
from core.models import IssueLog
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect, get_object_or_404


def list_all_test(user):
    return True


""" Views require both view permission, which allows them to access this application,
and their operation specific permissions. I.e. editing requires view and change permissions.
"""


@permission_required('core.view_issuelog')
def list_all(request):
    user = request.user
    for permission in user.get_all_permissions():
        print(permission)
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


@permission_required(['core.view_issuelog', 'core.change_issuelog'])
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


@permission_required(['core.view_issuelog', 'core.add_issuelog'])
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


@permission_required(['core.view_issuelog', 'core.read_issuelog'])
def detail(request, issue_log_id):
    issue_log = IssueLog.objects.get(pk=issue_log_id)
    return render(request, 'issue_log/detail.html', {'issue_log': issue_log})


@permission_required(['core.view_issuelog', 'core.delete_issuelog'])
def delete(request, issue_log_id):
    try:
        issue_log = IssueLog.objects.get(pk=issue_log_id)
        IssueLog.delete(issue_log)
        return redirect(list_all)
    except:
        raise Http404("Issue log doesn't exist.")
