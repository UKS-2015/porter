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
from porter.group.views import GroupList, GroupCreate, GroupDetail, GroupUpdate, GroupDelete

app_name = 'issue'

urlpatterns = [
    # ex: /group/
    url(r'^$', GroupList.as_view(), name='list'),
     # ex: /group/5/add/
    url(r'add/$', GroupCreate.as_view(), name='add'),
     # ex: /group/5/
    url(r'(?P<pk>[0-9]+)/$', GroupDetail.as_view(), name='detail'),
     # ex: /group/5/update/
    url(r'(?P<pk>[0-9]+)/update/$', GroupUpdate.as_view(), name='update'),
     # ex: /group/5/delete/
    url(r'(?P<pk>[0-9]+)/delete/$', GroupDelete.as_view(), name='delete'),
]