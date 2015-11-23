from django.conf.urls import include, url, patterns
from .rest import *
from .views import _login
urlpatterns = patterns('',
    url(r'^create/$', CreatetopicView.as_view(), name='topic_create'),
    url(r'^list/$', ListopicView.as_view(), name='topic_list'),
    url(r'^(?P<pk>[0-9]+)/$', TopicView.as_view(), name='topic_update'),
    url(r'^comment/create/$', TopicommentCreate.as_view(), name='comment_create'),
    url(r'^_login$', _login, name='_login'),
    url(r'^comment/list/$', TopicommentList.as_view(), name='comment_list'),
)