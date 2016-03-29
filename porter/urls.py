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
from django.conf.urls import url, include
from django.contrib import admin
from porter.issue_log import urls as issue_log_urls
from porter.group import urls as group_urls
from porter.user_project_role import urls as user_project_role_urls
from porter.milestone import urls as milestone_urls
from porter.label import urls as label_urls
from porter.issue import urls as issue_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^issue_log/', include(issue_log_urls)),
    url(r'^group/', include(group_urls)),
    url(r'^user_project_role/', include(user_project_role_urls)),
    url(r'^milestone/', include(milestone_urls)),
    url(r'^label/', include(label_urls)),
    url(r'^issue/', include(issue_urls))
]
