from rest_framework import serializers, generics
from rest_framework import mixins, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions, filters

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from . import models

import functools
import re

now = timezone.now()

def login_required(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        if not self.request.user or not self.request.user.pk:
            raise PermissionDenied
        return f(self, *args, **kwargs)
    return wrapper

class TopicSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Topicontent
        fields = (
            'pk', 'title', 'article', 'article_status', 'label_category', 'cover_image',
            'create_time', 'update_time', 'comment_count', 'star_count',
            'collect_count',
        )

class CreateTopicSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Topicontent
        fields = (
            'pk', 'title', 'article', 'article_status', 'label_category', 'cover_image'
        )

    def create(self, validated_data):
        validated_data['update_time'] = now
        validated_data['author_id'] = self._context['request'].user.pk
        return super(CreateTopicSerializers, self).create(validated_data)



class UserinfoGetserializers(serializers.ModelSerializer):

    class Meta:
        model = models.Tuser
        fields = ('pk', 'username', 'email', 'avatar', 'sex', 'nickname',
                  'country', 'province', 'city', 'birthday',
                  'followers_count', 'grade')

class UserinfoCreateserializers(serializers.ModelSerializer):

    class Meta:
        model = models.Tuser
        fields = ('email', 'avatar', 'sex', 'nickname',
                  'country', 'province', 'city', 'birthday',)

class CreatetopicView(generics.CreateAPIView):
    serializer_class = CreateTopicSerializers
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method != 'GET':
            return CreateTopicSerializers
        return TopicSerializers

class GetopicView(generics.RetrieveAPIView,):
    queryset = models.Topicontent
    serializer_class = TopicSerializers

class UpdatetopicView(generics.UpdateAPIView):
    queryset = models.Topicontent
    serializer_class = CreateTopicSerializers