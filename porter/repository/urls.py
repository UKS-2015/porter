from django.conf.urls import url
from porter.repository import views

urlpatterns = [
    url(r'^$', views.list_all, name='repo_list_all'),
    url(r'^new/$', views.create, name='repo_create'),
    # TODO: Changing repository name will break links - only allow deleting
    url(r'(?P<repository_title>[^/\\]+)/change/$', views.change, name='repo_change'),
    url(r'(?P<repository_title>[^/\\]+)/delete/$', views.delete, name='repo_delete'),
    url(r'(?P<repository_title>[^/\\]+)/$', views.overview, name='repo_overview'),
]
