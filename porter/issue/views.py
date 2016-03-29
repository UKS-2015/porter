from django.shortcuts import get_object_or_404, render, redirect
from core.models import Issue
from core.forms import IssueForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def list(request):
    paginator = Paginator(Issue.objects.all(), 25)
    # Pagination page number check
    page = request.GET.get('page')
    try:
        issue_list = paginator.page(page)
    except PageNotAnInteger:
        issue_list = paginator.page(1)
    except EmptyPage:
        issue_list = paginator.page(paginator.num_pages)

    context = {'issue_list': issue_list}
    return render(request, 'issue/list.html', context)

def add(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = IssueForm(request.POST, auto_id=True)
        # check whether it's valid:
        if form.is_valid():
            Issue.save(form.instance)
            return redirect(list)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = IssueForm()

    return render(request, 'issue/add.html', {'issue': form})

def detail(request, issue_id):
    issue = Issue.objects.get(pk=issue_id)
    form = IssueForm(instance = issue)
    return render(request, 'issue/detail.html', {'issue': form.as_p()})

def change(request, issue_id):
    if request.method == 'GET':
        issue = get_object_or_404(Issue, pk=issue_id)
        form = IssueForm(instance=issue)
        return render(request, 'issue/change.html', {'issue': form})
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = IssueForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            issue = form.instance
            issue.id = issue_id
            Issue.save(issue)
            # redirect to a new URL:
            return redirect(list)

    return render(request, 'issue/change.html', {'form': form})

def delete(request, issue_id):
    if request.method == 'GET':
        issue = get_object_or_404(Issue, pk=issue_id)
        form = IssueForm(instance=issue)
        return render(request, 'issue/delete.html', {'issue': form})
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        issue = Issue.objects.get(pk=issue_id)
        Issue.delete(issue)
        return redirect(list)
    return redirect(list)