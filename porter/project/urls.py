from django.conf.urls import url, include
from porter.project import views
from porter.project.views_new import ProjectDetail
from porter.repository import urls as repository_urls
from porter.milestone import urls as milestone_urls

app_name = 'project'

urlpatterns = [
    url(r'^$', ProjectDetail.as_view(), name='overview'),
    url(r'^members/$', views.members, name='members'),
    url(r'^members/(?P<user_id>\d+)/remove/$', views.remove_member, name='remove_member'),
    url(r'^members/add/$', views.add_member, name='add_member'),
    url(r'^repository/', include(repository_urls), name='repositories'),
    # TODO: Modify issue application
    url(r'^issues/', views.overview, name='issues'),
    url(r'^milestones/', include(milestone_urls), name='milestones'),
]
