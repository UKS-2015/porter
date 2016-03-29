from django.shortcuts import get_object_or_404, render, redirect
from core.models import Milestone
from core.forms import MilestoneForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def list(request):
    paginator = Paginator(Milestone.objects.all(), 25)
    # Pagination page number check
    page = request.GET.get('page')
    try:
        milestone_list = paginator.page(page)
    except PageNotAnInteger:
        milestone_list = paginator.page(1)
    except EmptyPage:
        milestone_list = paginator.page(paginator.num_pages)

    context = {'milestone_list': milestone_list}
    return render(request, 'milestone/list.html', context)

def add(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MilestoneForm(request.POST, auto_id=True)
        # check whether it's valid:
        if form.is_valid():
            Milestone.save(form.instance)
            return redirect(list)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MilestoneForm()

    return render(request, 'milestone/add.html', {'milestone': form})

def detail(request, milestone_id):
    milestone = Milestone.objects.get(pk=milestone_id)
    form = MilestoneForm(instance = milestone)
    return render(request, 'milestone/detail.html', {'milestone': form.as_p()})

def change(request, milestone_id):
    if request.method == 'GET':
        milestone = get_object_or_404(Milestone, pk=milestone_id)
        form = MilestoneForm(instance=milestone)
        return render(request, 'milestone/change.html', {'milestone': form})
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MilestoneForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            milestone = form.instance
            milestone.id = milestone_id
            Milestone.save(milestone)
            # redirect to a new URL:
            return redirect(list)

    return render(request, 'milestone/change.html', {'form': form})

def delete(request, milestone_id):
    if request.method == 'GET':
        milestone = get_object_or_404(Milestone, pk=milestone_id)
        form = MilestoneForm(instance=milestone)
        return render(request, 'milestone/delete.html', {'milestone': form})
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        milestone = Milestone.objects.get(pk=milestone_id)
        Milestone.delete(milestone)
        return redirect(list)
    return redirect(list)