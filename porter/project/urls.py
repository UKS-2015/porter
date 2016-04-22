from django.conf.urls import url, include
from porter.project.views import ProjectDetail, ProjectMembers, ProjectMemberRemove, ProjectMemberAdd
from porter.repository import urls as repository_urls
from porter.milestone import urls as milestone_urls
from porter.issue import urls as issue_urls

app_name = 'project'

urlpatterns = [
    url(r'^$', ProjectDetail.as_view(), name='overview'),
    url(r'^members/$', ProjectMembers.as_view(), name='members'),
    url(r'^members/(?P<user_id>\d+)/remove/$', ProjectMemberRemove.as_view(), name='remove_member'),
    url(r'^members/add/$', ProjectMemberAdd.as_view(), name='add_member'),
    url(r'^repository/', include(repository_urls), name='repositories'),
    # TODO: Modify issue application
    url(r'^issues/', include(issue_urls), name='issues'),
    url(r'^milestones/', include(milestone_urls), name='milestones'),
]
