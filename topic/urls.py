"""topic URL Configuration

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
from django.conf import settings

import tuser.urls
import topicontent.urls

from .views import index
urlpatterns = [
    url(r'^(?P<path>favicon\.ico)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}, name="favicon"),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    #
    url(r'^admin/', include(admin.site.urls)),
    url('^api/$', index),
    url('^$', index),
    url(r'^api/user/', include(tuser.urls)),
    url(r'^api/topic/', include(topicontent.urls))
]
