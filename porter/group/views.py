from core.forms import GroupForm
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.

def list_all(request):
    paginator = Paginator(Group.objects.all(), 25)
    # Pagination page number check
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)
    return render(request, 'group/list.html', {'groups': groups})


def edit(request, group_id):
    if request.method == 'GET':
        group = get_object_or_404(Group, pk=group_id)
        form = GroupForm(instance=group)
        return render(request, 'group/edit.html', {'group': form})
    elif request.method == 'POST':
        form = GroupForm(request.POST)
        group = form.instance
        # Doesn't have an id apparently
        group.id = group_id
        if form.is_valid():
            Group.save(group)
            return redirect(list_all)
        else:
            # TODO: Front end validation
            return render(request, 'group/edit.html', {'group': form})
    else:
        return HttpResponseBadRequest


def create(request):
    form = GroupForm(request.POST)
    if request.method == 'GET':
        return render(request, 'group/create.html', {'group': form})
    else:
        if request.method == 'POST':
            form = GroupForm(request.POST)
        if form.is_valid():
            groups = form.instance
            Group.save(groups)
            return redirect(list_all)


def detail(request, group_id):
    groups = Group.objects.get(pk=group_id)
    return render(request, 'group/detail.html', {'group': groups})


def delete(request, group_id):
    try:
        group = Group.objects.get(pk=group_id)
        Group.delete(group)
        return redirect(list_all)
    except:
        raise Http404("Issue log doesn't exist.")
