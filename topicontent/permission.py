from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.contrib.contenttypes.models import ContentType

class ISAuthorPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PUT']:
            if obj.author != request.user:
                raise PermissionDenied("不能修改不属于自己的文章")
        return True

class RightContenttypePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return True