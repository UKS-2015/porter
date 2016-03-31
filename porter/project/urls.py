from django.conf.urls import url, include
from porter.project import views

urlpatterns = [
    url(r'^$', views.overview),
    url(r'^members/$', views.members),
    url(r'^members/(?P<user_id>\d+)/remove/$', views.remove_member),
    url(r'^members/add/$', views.add_member),
    # url(r'^issues/$', views.edit),
    # url(r'^milestones/$', views.edit),
    # url(r'^issue_log/', include(issue_log_urls)),
    # url(r'^(?P<repository_name>[A-Za-z]+)/$', views.project_test)
]
