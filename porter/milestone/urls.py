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
from porter.milestone.views import MilestoneList, MilestoneCreate, MilestoneDetail, MilestoneUpdate, MilestoneDelete

app_name = 'milestone'

urlpatterns = [
    url(r'^$', MilestoneList.as_view(), name='list'),
    url(r'new/$', MilestoneCreate.as_view(), name='new'),
    url(r'(?P<pk>[^/\\]+)/change/$', MilestoneUpdate.as_view(), name='change'),
    url(r'(?P<pk>[^/\\]+)/delete/$',MilestoneDelete.as_view(), name='delete'),
    url(r'(?P<pk>[^/\\]+)/$',MilestoneDetail.as_view(), name='overview'),

]