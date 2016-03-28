from core.forms import UserProjectRoleForm
from core.models import UserProjectRole
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.

@permission_required('core.view_group')
def list_all(request):
    paginator = Paginator(UserProjectRole.objects.all(), 25)
    # Pagination page number check
    page = request.GET.get('page')
    try:
        user_project_roles = paginator.page(page)
    except PageNotAnInteger:
        user_project_roles = paginator.page(1)
    except EmptyPage:
        user_project_roles = paginator.page(paginator.num_pages)
    return render(request, 'user_project_role/list.html', {'user_project_roles': user_project_roles})


@permission_required(['core.view_userprojectrole', 'core.change_userprojectrole'])
def edit(request, user_project_role_id):
    if request.method == 'GET':
        user_project_role = get_object_or_404(UserProjectRole, pk=user_project_role_id)
        form = UserProjectRoleForm(instance=user_project_role)
        return render(request, 'user_project_role/edit.html', {'user_project_role': form})
    elif request.method == 'POST':
        form = UserProjectRoleForm(request.POST)
        # Doesn't have an id apparently
        form.instance.id = user_project_role_id
        if form.is_valid():
            user_project_role = form.save(commit=True)
            UserProjectRole.save(user_project_role)
            return redirect(list_all)
        else:
            # TODO: Front end validation
            return render(request, 'user_project_role/edit.html', {'user_project_role': form})
    else:
        return HttpResponseBadRequest


@permission_required(['core.view_userprojectrole', 'core.add_userprojectrole'])
def create(request):
    form = UserProjectRoleForm(request.POST)
    if request.method == 'GET':
        return render(request, 'user_project_role/create.html', {'user_project_role': form})
    else:
        if request.method == 'POST':
            if form.is_valid():
                user_project_role = form.save(commit=True)
                UserProjectRole.save(user_project_role)

                return redirect(list_all)


@permission_required(['core.view_userprojectrole', 'core.read_userprojectrole'])
def detail(request, user_project_role_id):
    groups = UserProjectRole.objects.get(pk=user_project_role_id)
    return render(request, 'user_project_role/detail.html', {'user_project_role': groups})


@permission_required(['core.view_userprojectrole', 'core.delete_userprojectrole'])
def delete(request, user_project_role_id):
    try:
        user_project_role_id = UserProjectRole.objects.get(pk=user_project_role_id)
        UserProjectRole.delete(user_project_role_id)
        return redirect(list_all)
    except:
        raise Http404("User project role doesn't exist.")
