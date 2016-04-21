from django.conf.urls import url
from porter.repository import views

app_name = "repository"

urlpatterns = [
    url(r'^$', views.list_all, name='list_all'),
    url(r'^new/$', views.create, name='create'),
    # TODO: Changing repository name will break links - only allow deleting
    url(r'(?P<repository_title>[^/\\]+)/change/$', views.change, name='change'),
    url(r'(?P<repository_title>[^/\\]+)/delete/$', views.delete, name='delete'),
    url(r'(?P<repository_title>[^/\\]+)/$', views.overview, name='overview'),
]
