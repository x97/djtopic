from django.conf.urls import include, url, patterns
from .rest import *

urlpatterns = patterns('',
    url(r'^create/$', CreatetopicView.as_view(), name='topic_create'),
    url(r'^get/(?P<pk>[0-9]+)/$', GetopicView.as_view(), name='topic_get'),
    url(r'^update/(?P<pk>[0-9]+)/$', UpdatetopicView.as_view(), name='topic_update'),
)