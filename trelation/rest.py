from rest_framework import serializers
from rest_framework import generics
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from rest_framework.exceptions import  NotAcceptable, NotFound
from rest_framework import status
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
now = timezone.now()

from . import models
from tuser.models import tusers

class RelationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Relation
        fields = ('relation_user', 'relation')

    def create(self, validated_data):
        validated_data['create_time'] = now
        validated_data['user_id'] = self._context['request'].user.pk
        if validated_data['relation'] == 0:
            return super(RelationCreateSerializer, self).create(validated_data)
        instance = super(RelationCreateSerializer, self).create(validated_data)
        tusers.follows(instance.relation_user)
        tusers.following(instance.user)
        return instance

class RelationCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Relation
        fields = ('relation_user', 'relation')

class RelationDeatilSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Relation
        depth = 1

class RelationFollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Relation
        fields = ('user',)
        depth = 1

class RelationFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Relation
        fields = ('relation_user',)
        depth = 1

class RelationCreate(generics.CreateAPIView):   #关注/拉黑
    serializer_class = RelationCreateSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        relation = models.Relation.objects.filter(user=request.user, relation_user=request.data['relation_user'],
                                                        relation=self.request.data['relation'])
        if relation:
            raise NotAcceptable("已经关注/拉黑过该用户")
        return super(RelationCreate, self).create(request, *args, **kwargs)

class RelationCancel(generics.CreateAPIView):  # 取消关注/拉黑
    serializer_class = RelationCancelSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        try:
            return models.Relation.objects.get(user=self.request.user, relation_user=self.request.data['relation_user'],
                                                relation=self.request.data['relation'])
        except ObjectDoesNotExist:
            raise NotFound("您还没有关注/拉黑该用户")

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.relation == 0:
            tusers.unfollows(instance.relation_user)
            tusers.unfollowing(instance.user)
        instance.delete()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT, headers=headers)

class BaseRelationList(generics.ListAPIView):
    serializer_class = RelationDeatilSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def base_queryset(self, **kwargs):
        return models.Relation.objects.filter(status=1, **kwargs)

class FollowingList(BaseRelationList): # 关注列表

    serializer_class = RelationFollowingSerializer
    def get_queryset(self):
        user_id = self.request.GET.get("user_id")
        if user_id:
            return super(FollowingList, self).base_queryset(user_id=user_id, relation=0)
        return super(FollowingList, self).base_queryset(user_id=self.request.user.id, relation=0)

class FollowersList(BaseRelationList): #粉丝列表

    serializer_class = RelationFollowersSerializer
    def get_queryset(self):
        user_id = self.request.GET.get("user_id")
        if user_id:
            return super(FollowersList, self).base_queryset(relation_user_id=user_id, relation=0)
        return super(FollowersList, self).base_queryset(relation_user_id=self.request.user.id, relation=0)

class BalckList(BaseRelationList):
    serializer_class = RelationFollowingSerializer
    def get_queryset(self):
        return super(BalckList, self).base_queryset(user_id=self.request.user.id, relation=1)
