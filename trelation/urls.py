from django.conf.urls import include, url, patterns
from .rest import *
urlpatterns = patterns('',
    url(r'^create/$', RelationCreate.as_view(), name='relation_create'),
    url(r'^cancel/$', RelationCancel.as_view(), name='relation_cancel'),
    url(r'^following/$', FollowingList.as_view(), name='following'),
    url(r'^followers/$', FollowersList.as_view(), name='followers'),
    url(r'^blacklist/$', BalckList.as_view(), name='blacklist'),
)