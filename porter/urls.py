"""porter URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from core import views
from core.forms import UserPasswordForm
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login, password_change
from porter import settings
from porter.project import urls as new_project_urls
from porter.user.views import UserProfile, UserChange, UserPassword, UserDetail
from porter.project.views import ProjectCreate

app_name = 'porter'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', login),
    url(r'^porter/login/$', login),
    url(r'^porter/logout/$', logout_then_login, name='logout'),
    url(r'^porter/profile/$', UserProfile.as_view(), name='profile'),
    url(r'^porter/profile/change/$', UserChange.as_view(), name='profile_change'),
    url(r'^porter/user/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user_profile'),
    url(r'^porter/profile/password/$', UserPassword.as_view(), name='password_change'),
    url(r'^porter/projects/$', views.user_projects, name='user_projects'),
    url(r'^porter/projects/new/$', ProjectCreate.as_view(), name='new_project'),
    url(r'^porter/issues/$', views.user_issues, name='user_issues'),
    url(r'^porter/(?P<project_title>[^/\\]+)/', include(new_project_urls)),
    url(r'^porter/$', views.user_dashboard, name='user_dashboard'),

    # Allow media (such as pictures)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
