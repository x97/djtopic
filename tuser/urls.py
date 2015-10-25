from django.conf.urls import include, url, patterns
from .rest import *

urlpatterns = patterns('',
    url(r'^regist/$', CreateuserView.as_view(), name='regist'),
    url(r'^userinfo/(?P<pk>[0-9]+)/$', UserinfoView.as_view(), name='userinfo'),
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^logout/$', UserLogout.as_view(), name='logout'),
)