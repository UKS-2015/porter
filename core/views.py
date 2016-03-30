from core.decorators import check_project_member
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.

# TODO: Testing only
from django.shortcuts import redirect


@login_required()
@check_project_member()
def project_test(request, project_name):
    return HttpResponse("Hello from %s!" % project_name)


def logout_view(request):
    logout(request)
    return redirect('/')
