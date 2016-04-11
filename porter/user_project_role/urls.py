"""porter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from porter.user_project_role.views import UserProjectRoleList, UserProjectRoleCreate, UserProjectRoleDetail, UserProjectRoleUpdate, UserProjectRoleDelete

app_name = 'user_project_role'

urlpatterns = [
    url(r'^$', UserProjectRoleList.as_view(), name='list'),
    url(r'add/$', UserProjectRoleCreate.as_view(), name='add'),
    url(r'(?P<pk>[0-9]+)/$', UserProjectRoleDetail.as_view(), name='detail'),
    url(r'(?P<pk>[0-9]+)/update/$', UserProjectRoleUpdate.as_view(), name='update'),
    url(r'(?P<pk>[0-9]+)/delete/$', UserProjectRoleDelete.as_view(), name='delete'),
]