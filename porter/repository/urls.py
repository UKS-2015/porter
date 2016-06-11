from django.conf.urls import url, include
from porter.issue import urls as issue_urls
from porter.milestone import urls as milestone_urls
from porter.repository.views import RepositoryOverview, RepositoryCreate, RepositoryDelete, RepositoryUpdate, \
    RepositoryList

app_name = "repository"

urlpatterns = [
    url(r'^$', RepositoryList.as_view(), name='list_all'),
    url(r'^new/$', RepositoryCreate.as_view(), name='create'),
    # TODO: Changing repository name will break links - only allow deleting
    url(r'(?P<repository_title>[^/\\]+)/change/$', RepositoryUpdate.as_view(), name='change'),
    url(r'(?P<repository_title>[^/\\]+)/delete/$', RepositoryDelete.as_view(), name='delete'),
    url(r'(?P<repository_title>[^/\\]+)/issues/$', include(issue_urls), name='issues'),
    url(r'(?P<repository_title>[^/\\]+)/milestones/', include(milestone_urls), name='milestone'),
    url(r'(?P<repository_title>[^/\\]+)/$', RepositoryOverview.as_view(), name='overview'),
]
