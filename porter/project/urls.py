from django.conf.urls import url, include
from porter.project.views import ProjectDetail, ProjectMembers, \
    ProjectMemberRemove, ProjectMemberAdd, ProjectSettings, \
    ProjectDelete, ProjectAssignRole, ProjectMilestones, ProjectIssues
from porter.repository import urls as repository_urls
from porter.label import urls as label_urls

app_name = 'project'

urlpatterns = [
    url(r'^$', ProjectDetail.as_view(), name='overview'),
    url(r'^delete/$', ProjectDelete.as_view(), name='delete'),
    url(r'^settings/$', ProjectSettings.as_view(), name='settings'),
    url(r'^members/$', ProjectMembers.as_view(), name='members'),
    url(r'^members/(?P<user_id>\d+)/remove/$', ProjectMemberRemove.as_view(),
        name='remove_member'),
    url(r'^members/add/$', ProjectMemberAdd.as_view(), name='add_member'),
    url(r'^members/assign_role/$', ProjectAssignRole.as_view(),
        name='assign_role'),
    # TODO: Modify issue application
    url(r'^issues/$', ProjectIssues.as_view(), name='all_issues'),
    url(r'^labels/', include(label_urls), name='label'),
    url(r'^repository/', include(repository_urls), name='repository'),
    url(r'^milestones/$', ProjectMilestones.as_view(), name='all_milestones')

]
