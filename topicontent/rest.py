from rest_framework import serializers, generics
from rest_framework import mixins, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework import generics, permissions, filters

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from . import models
from . import permission

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
            'pk', 'title', 'article', 'article_status', 'author', 'label_category', 'cover_image',
            'create_time', 'update_time', 'comment_count', 'star_count',
            'collect_count',
        )

class TopicommentSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Topicomment
        fields = (
            'pk', 'content_type', 'object_id', 'content',
        )

    def create(self, validated_data):
        validated_data['author_id'] = self._context['request'].user.pk
        return super(TopicommentSerializers, self).create(validated_data)

class TopicommentDetailSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Topicomment
        fields = (
            'pk', 'content_type', 'object_id', 'content',
        )

class TopicommentListSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Topicomment
        fields = '__all__'

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

class ListopicView(generics.ListAPIView):
    serializer_class = TopicSerializers
    def get_queryset(self):
        user_id = self.request.GET.get('user_id')
        if user_id:
            return models.Topicontent.objects.filter(author_id=user_id)
        else:
            if self.request.user and self.request.user.is_authenticated():
                return models.Topicontent.objects.filter(author=self.request.user)
            else:
                raise PermissionDenied

class CreatetopicView(generics.CreateAPIView):
    serializer_class = CreateTopicSerializers
    permission_classes = (permissions.IsAuthenticated,)
    # queryset = models.Topicontent.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TopicSerializers
        return self.serializer_class


class TopicView(generics.RetrieveAPIView, generics.DestroyAPIView,
                 generics.UpdateAPIView):
    queryset = models.Topicontent
    serializer_class = CreateTopicSerializers
    permission_classes = [permission.ISAuthorPermission, ]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return self.serializer_class
        return TopicSerializers

class TopicommentCreate(generics.CreateAPIView):
    serializer_class = TopicommentSerializers
    permission_classes = (permissions.IsAuthenticated, permission.RightContenttypePermission)
    create_serializer_class = TopicommentListSerializers


def get_contenttype(model):
    return ContentType.objects.get_for_model(model).pk

class TopicommentList(generics.ListAPIView):
    serializer_class = TopicommentListSerializers
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        object_id = self.request.GET.get('object_id')
        if object_id:
            return models.Topicomment.objects.filter(
                content_type=get_contenttype(models.Topicontent), object_id=object_id)
        else:
            return None
