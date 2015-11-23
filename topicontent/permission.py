from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError, PermissionDenied

class ISAuthorPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PUT']:
            if obj.author != request.user:
                raise PermissionDenied("不能修改不属于自己的文章")
        return True
