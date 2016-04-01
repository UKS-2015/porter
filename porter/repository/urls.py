from django.conf.urls import url
from porter.repository import views

urlpatterns = [
    # TODO: Changing repository name will break links - only allow deleting
    # url(r'(?P<repository_title>[A-Za-z]+)/change/$', views.change),
    url(r'^new/$', views.create),
    url(r'(?P<repository_title>[A-Za-z]+)/$', views.overview),
]
