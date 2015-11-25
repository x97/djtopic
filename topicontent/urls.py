from django.conf.urls import include, url, patterns
from .rest import *
from .views import _login
urlpatterns = patterns('',
    url(r'^(?P<pk>[0-9]+)/$', TopicView.as_view(), name='topic_update'),
    url(r'^create/$', CreatetopicView.as_view(), name='topic_create'),
    url(r'^list/$', ListopicView.as_view(), name='topic_list'),
    url(r'^recentlist/$', TopicRecentList.as_view(), name='recent_list'),
    url(r'^comment/create/$', TopicommentCreate.as_view(), name='comment_create'),
    url(r'^comment/list/$', TopicommentList.as_view(), name='comment_list'),
    url(r'^comment/review/$', TopicommentReviewCreate.as_view(), name='comment_review'),
    url(r'^collection/create/$', CollectionCreate.as_view(), name='collection_create'),
    url(r'^collection/list/$', CollectionList.as_view(), name='collection_list'),
    url(r'^star/create/$', StarCreate.as_view(), name='star_create'),
    url(r'^star/list/$', StarList.as_view(), name='star_list'),
)