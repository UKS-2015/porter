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
from porter.issue import views

urlpatterns = [
    # ex: /issue/
    url(r'^$', views.list, name='list'),
    # ex: /issue/5/change
    url(r'^(?P<issue_id>\d+)/change/$', views.change, name='change'),
    # ex: /issue/5/
    url(r'^(?P<issue_id>\d+)/$', views.detail, name='detail'),
    # ex: /issue/add/
    url(r'^add/$', views.add, name='add'),
    # ex: /issue/5/delete/
    url(r'^(?P<issue_id>\d+)/delete/$', views.delete, name='delete'),
]