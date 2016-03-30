from core.decorators import check_project_member
from django.http import HttpResponse

# Create your views here.

# TODO: Testing only
@check_project_member()
def project_test(request, project_name):
    return HttpResponse("Hello from %s!" % project_name)
