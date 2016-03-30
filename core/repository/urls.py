from django.conf.urls import url
from core.repository import views

urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^(?P<repository_id>\d+)/change/$', views.change, name='change'),
    url(r'^(?P<repository_id>\d+)/$', views.detail, name='detail'),
    url(r'^add/$', views.add, name='add'),
    url(r'^(?P<repository_id>\d+)/delete/$', views.delete, name='delete')
]
