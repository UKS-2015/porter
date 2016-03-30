from django.conf.urls import url
from core.project import views

urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^(?P<project_id>\d+)/change/$', views.change, name='change'),
    url(r'^(?P<project_id>\d+)/$', views.detail, name='detail'),
    url(r'^add/$', views.add, name='add'),
    url(r'^(?P<project_id>\d+)/delete/$', views.delete, name='delete')
]
