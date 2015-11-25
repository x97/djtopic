from rest_framework import serializers, generics
from rest_framework import mixins, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotAcceptable
from rest_framework import generics, permissions, filters
from rest_framework import status

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from . import models
from . import permission

import functools
import logging
import re

now = timezone.now()

topic = models.Topicontents

def replace_prohibit_word(context):
    words = models.ProhibitWord.objects.all()
    for word in words:
        temp = context.replace(word.word, "*" * len(word.word))
        context = temp
    return temp

def get_contentype_name(model):
    return ContentType.objects.get(model=model)

def get_contentype_id(model):
    return ContentType.objects.get_for_model(model).pk

def get_instance_for_contentype(model, **kwargs):
    return model.get_object_for_this_type(**kwargs)

class TopicSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Topicontent
        fields = (
            'pk', 'title', 'article', 'article_status', 'author', 'label_category', 'cover_image',
            'create_time', 'update_time', 'comment_count', 'star_count',
            'collect_count',
        )
        depth = 1

class TopicommentSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Topicomment
        fields = (
            'pk', 'topic', 'content',
        )

    def create(self, validated_data):
        validated_data['author_id'] = self._context['request'].user.pk
        validated_data['create_time'] = now
        instance = super(TopicommentSerializers, self).create(validated_data)
        topic.comment(instance.topic)
        return instance

class TopicommentReviewSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Topicomment
        fields = (
            'pk', 'review', 'content',
        )

    def create(self, validated_data):
        validated_data['author_id'] = self._context['request'].user.pk
        validated_data['topic'] = validated_data['review'].topic
        validated_data['create_time'] = now
        instance = super(TopicommentReviewSerializers, self).create(validated_data)
        topic.comment(instance.topic)
        return instance

class TopicommentListSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Topicomment
        # fields = '__all__'
        depth = 1

class BaseCollectionSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.TopicRelation
        fields = ('topic',)

    def create(self, validated_data):
        validated_data['collect_time'] = now
        validated_data['user_id'] = self._context['request'].user.pk
        return super(BaseCollectionSerializers, self).create(validated_data)

class CollectionCreateSerializers(BaseCollectionSerializers):

    def create(self, validated_data):
        instance = super(CollectionCreateSerializers, self).create(validated_data)
        topic.collect(instance.topic)
        return instance

class StarCreateSerializers(BaseCollectionSerializers):

    def create(self, validated_data):
        validated_data['relation'] = 1
        instance = super(StarCreateSerializers, self).create(validated_data)
        topic.star(instance.topic)
        return instance

class CollectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.TopicRelation
        fields = '__all__'
        depth = 1

class CreateTopicSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Topicontent
        fields = (
            'pk', 'title', 'article', 'article_status', 'label_category', 'cover_image'
        )

    def create(self, validated_data):
        validated_data['update_time'] = now
        validated_data['article'] = replace_prohibit_word(validated_data['article'])
        validated_data['author_id'] = self._context['request'].user.pk
        return super(CreateTopicSerializers, self).create(validated_data)

class ListopicView(generics.ListAPIView):
    serializer_class = TopicSerializers
    def get_queryset(self):
        user_id = self.request.GET.get('user_id')
        status = self.request.GET.get("status")
        if user_id:
            return models.Topicontent.objects.filter(author_id=user_id, article_status=1).order_by('create_time')
        if self.request.user and self.request.user.is_authenticated() and status and int(status) != 2:
            return models.Topicontent.objects.filter(author=self.request.user,
                                                     article_status=status).order_by('create_time')
        else:
            return models.Topicontent.objects.filter(author=self.request.user,
                                                     article_status=1).order_by('create_time')
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

class TopicommentReviewCreate(generics.CreateAPIView):
    serializer_class = TopicommentReviewSerializers
    permission_classes = (permissions.IsAuthenticated, permission.RightContenttypePermission)
    create_serializer_class = TopicommentListSerializers

class TopicommentList(generics.ListAPIView):
    serializer_class = TopicommentListSerializers
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        id = self.request.GET.get('id')
        if id:
            return models.Topicomment.objects.filter(topic_id=id)
        return models.Topicomment.objects.filter(author=self.request.user)

class CollectionCreate(generics.CreateAPIView):

    serializer_class = CollectionCreateSerializers
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        collection = models.TopicRelation.objects.filter(user=request.user, topic=request.data['topic'], relation=0)
        if collection:
            raise NotAcceptable("已经收藏过该话题")
        return super(CollectionCreate, self).create(request, *args, **kwargs)

class StarCreate(generics.CreateAPIView):
    serializer_class = StarCreateSerializers
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        collection = models.TopicRelation.objects.filter(user=request.user, topic=request.data['topic'], relation=1)
        if collection:
            raise NotAcceptable("已经点赞过该话题")
        return super(StarCreate, self).create(request, *args, **kwargs)

class CollectionList(generics.ListAPIView):
    serializer_class = CollectionSerializers
    permissions = (permissions.IsAuthenticated)

    def get_queryset(self):
        return models.TopicRelation.objects.filter(user=self.request.user, relation=0).order_by('collect_time')

class StarList(generics.ListAPIView):
    serializer_class = CollectionSerializers
    permissions = (permissions.IsAuthenticated)

    def get_queryset(self):
        return models.TopicRelation.objects.filter(user=self.request.user, relation=1).order_by('collect_time')

# class UserRelationTopicList(generics.ListAPIView):
#     serializer_class = CollectionSerializers
#     permissions = (permissions.IsAuthenticated)
#
#     def get_queryset(self):
#         return models.Topicontent.objects.filter()

class TopicRecentList(generics.ListAPIView):
    serializer_class = TopicSerializers
    permissions = (permissions.IsAuthenticated)

    def get_queryset(self):
        return models.Topicontent.objects.filter(article_status=1).order_by('create_time')


