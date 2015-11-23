from django.conf.urls import include, url, patterns
from .rest import *

urlpatterns = patterns('',
    url(r'^create/$', CreatetopicView.as_view(), name='topic_create'),
    url(r'^list/$', ListopicView.as_view(), name='topic_list'),
    url(r'^(?P<pk>[0-9]+)/$', TopicView.as_view(), name='topic_update'),
    url(r'^comment/create/$', TopicommentCreate.as_view(), name='comment_create'),
    # url(r'^comment/llist/$', TopicommentCreate.as_view(), name='comment_create'),
)