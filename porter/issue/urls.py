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
from porter.issue.views import IssueList, IssueCreate, IssueOverview, IssueUpdate, IssueDelete

app_name = 'issues'

urlpatterns = [
    # ex: /issue/
    url(r'^$', IssueList.as_view(), name='list'),
    # ex: /issue/5/add/
    url(r'new/$', IssueCreate.as_view(), name='new'),
    # ex: /issue/5/update/
    url(r'(?P<pk>[^/\\]+)/change/$', IssueUpdate.as_view(), name='change'),
    # ex: /issue/5/delete/
    url(r'(?P<pk>[^/\\]+)/delete/$',IssueDelete.as_view(), name='delete'),
    # ex: /issue/5/
    url(r'(?P<pk>[^/\\]+)/$',IssueOverview.as_view(), name='overview'),
]
