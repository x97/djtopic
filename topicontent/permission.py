from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAcceptable, PermissionDenied
from django.contrib.contenttypes.models import ContentType

from . import models
class ISAuthorPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PUT']:
            if obj.author != request.user:
                raise PermissionDenied("不能修改不属于自己的文章")
        return True

class RightContenttypePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return True

class RepeatCollection(BasePermission):
    def has_object_permission(self, request, view, obj):
        collection = models.TopicRelation.objects.filter(user=request.user, topic=obj.topic)
        if collection:
            print(obj.topic)
            raise NotAcceptable("已经收藏过该话题")
        return True