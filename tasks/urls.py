"""tasks URL Configuration

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
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.all, name='all tasks'),
    url(r'^today$', views.today, name='today'),
    url(r'^([0-9]+)', views.detail, name='task detail'),
    url(r'^delete$', views.delete, name='delete task'),
    url(r'^updatetag', views.update_tag, name='update tag'),
    url(r'^managetags', views.manage_tags, name='manage tags'),
]
