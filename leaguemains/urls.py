"""LeagueMains URL Configuration

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
from django.conf.urls import url

from leaguemains import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register_user, name='register_user'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^create/championlist/$', views.create_championlist, name='create_championlist'),
    url(r'^save/championlist/$', views.save_championlist, name='save_championlist'),
    url(r'^delete/championlist/$', views.delete_championlist, name='delete_championlist'),
    url(r'^championlist/$', views.championlist, name='championlist'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^test', views.test, name='test'),
]