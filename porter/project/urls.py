from django.conf.urls import url, include
from porter.project import views
from porter.repository import urls as repository_urls

urlpatterns = [
    url(r'^$', views.overview, name='project_overview'),
    url(r'^members/$', views.members, name='project_members'),
    url(r'^members/(?P<user_id>\d+)/remove/$', views.remove_member, name='project_remove_member'),
    url(r'^members/add/$', views.add_member, name='project_add_member'),
    url(r'^repository/', include(repository_urls), name='project_repositories'),
    # TODO: Modify issue application
    url(r'^issues/', views.overview, name='project_issues'),
]
