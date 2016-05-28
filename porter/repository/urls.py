from django.conf.urls import url
from porter.repository import views
from porter.repository.views import RepositoryOverview, RepositoryCreate, RepositoryDelete, RepositoryUpdate, \
    RepositoryList

app_name = "repository"

urlpatterns = [
    url(r'^$', RepositoryList.as_view(), name='list_all'),
    url(r'^new/$', RepositoryCreate.as_view(), name='create'),
    # TODO: Changing repository name will break links - only allow deleting
    url(r'(?P<repository_title>[^/\\]+)/change/$', RepositoryUpdate.as_view(), name='change'),
    url(r'(?P<repository_title>[^/\\]+)/delete/$', RepositoryDelete.as_view(), name='delete'),
    url(r'(?P<repository_title>[^/\\]+)/$', RepositoryOverview.as_view(), name='overview'),
]
