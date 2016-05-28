from django.shortcuts import render, redirect, get_object_or_404
from core.models import User
from core.forms import UserForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def list(request):
    paginator = Paginator(User.objects.all(), 25)
    page = request.GET.get('page')

    try:
        user_list = paginator.page(page)
    except PageNotAnInteger:
        user_list = paginator.page(1)
    except EmptyPage:
        user_list = paginator.page(paginator.num_pages)

    return render(request, 'user/list.html', {'user_list': user_list})

def add(request):
    if request.method == 'POST':
        form = UserForm(request.POST, auto_id=True)
        if form.is_valid():
            User.save(form.instance)
            return redirect(list)
    else:
        form = UserForm()

    return render(request, 'user/add.html', {'user': form})

def detail(request, user_id):
    user = User.objects.get(pk=user_id)
    form = UserForm(instance = user)
    return render(request, 'user/profile.html', {'user': form.as_p()})

def change(request, user_id):
    if request.method == 'GET':
        user = get_object_or_404(User, pk=user_id)
        form = UserForm(instance=user)
        return render(request, 'user/change.html', {'user': form})
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.instance
            user.id = user_id
            User.save(user)
            return redirect(list)

def delete(request, user_id):
    if request.method == 'GET':
        user = get_object_or_404(User, pk=user_id)
        form = UserForm(instance=user)
        return render(request, 'user/delete.html', {'user': form})
    elif request.method == 'POST':
        user = User.objects.get(pk=user_id)
        User.delete(user)
        return redirect(list)
    else:
        redirect(list)
