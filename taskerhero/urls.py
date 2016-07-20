"""taskerhero URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from taskerhero import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='home'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    url(r'^tasks/', include('tasks.urls')),
    url(r'^user/', include('userprofile.urls')),
    # TODO: Customize password change form so it matches the template of the rest of the site
    url(r'^password/', auth_views.password_change, name='change password'),
    url(r'^passworddone/', auth_views.password_change_done, name='password_change_done'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)