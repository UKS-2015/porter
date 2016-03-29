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
from porter.milestone import views

urlpatterns = [
    # ex: /milestone/
    url(r'^$', views.list, name='list'),
    # ex: /milestone/5/change
    url(r'^(?P<milestone_id>\d+)/change/$', views.change, name='change'),
    # ex: /milestone/5/
    url(r'^(?P<milestone_id>\d+)/$', views.detail, name='detail'),
    # ex: /milestone/add/
    url(r'^add/$', views.add, name='add'),
    # ex: /milestone/5/delete/
    url(r'^(?P<milestone_id>\d+)/delete/$', views.delete, name='delete'),
]