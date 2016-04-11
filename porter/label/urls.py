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
from porter.label.views import LabelList, LabelCreate, LabelDetail, LabelUpdate, LabelDelete

app_name = 'label'

urlpatterns = [
    url(r'^$', LabelList.as_view(), name='list'),
    url(r'add/$', LabelCreate.as_view(), name='add'),
    url(r'(?P<pk>[0-9]+)/$', LabelDetail.as_view(), name='detail'),
    url(r'(?P<pk>[0-9]+)/update/$', LabelUpdate.as_view(), name='update'),
    url(r'(?P<pk>[0-9]+)/delete/$', LabelDelete.as_view(), name='delete'),
]