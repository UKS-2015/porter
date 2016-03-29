from django.shortcuts import get_object_or_404, render, redirect
from core.models import Label
from core.forms import LabelForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def list(request):
    paginator = Paginator(Label.objects.all(), 25)
    # Pagination page number check
    page = request.GET.get('page')
    try:
        label_list = paginator.page(page)
    except PageNotAnInteger:
        label_list = paginator.page(1)
    except EmptyPage:
        label_list = paginator.page(paginator.num_pages)

    context = {'label_list': label_list}
    return render(request, 'label/list.html', context)

def add(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LabelForm(request.POST, auto_id=True)
        # check whether it's valid:
        if form.is_valid():
            Label.save(form.instance)
            return redirect(list)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LabelForm()

    return render(request, 'label/add.html', {'label': form})

def detail(request, label_id):
    label = Label.objects.get(pk=label_id)
    form = LabelForm(instance = label)
    return render(request, 'label/detail.html', {'label': form})

def change(request, label_id):
    if request.method == 'GET':
        label = get_object_or_404(Label, pk=label_id)
        form = LabelForm(instance=label)
        return render(request, 'label/change.html', {'label': form})
    if request.method == 'POST':
        form = LabelForm(request.POST)
        if form.is_valid():
            label = form.instance
            label.id = label_id
            Label.save(label)
            return redirect(list)

    return render(request, 'milestone/change.html', {'form': form})

def delete(request, label_id):
    if request.method == 'GET':
        label = get_object_or_404(Label, pk=label_id)
        form = LabelForm(instance=label)
        return render(request, 'label/delete.html', {'label': form})
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        label = Label.objects.get(pk=label_id)
        Label.delete(label)
        return redirect(list)
    return redirect(list)