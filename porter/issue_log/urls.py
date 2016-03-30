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
from porter.issue_log import views

urlpatterns = [
    url(r'^$', views.list_all),
    url(r'^(?P<issue_log_id>[0-9]+)/edit$', views.edit),
    url(r'^(?P<issue_log_id>[0-9]+)/$', views.detail),
    url(r'^new/$', views.create),
    url(r'^(?P<issue_log_id>[0-9]+)/delete/$', views.delete),
]