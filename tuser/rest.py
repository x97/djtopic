from rest_framework import serializers, generics
from rest_framework import mixins, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied

from . import models
from .models import Tuser

import functools

def login_required(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        if not self.request.user or not self.request.user.pk:
            raise PermissionDenied
        return f(self, *args, **kwargs)
    return wrapper

class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Tuser
        fields = ('pk', 'username', 'email', 'avatar', 'sex',
                  'country', 'province', 'city', 'birthday',
                  'followers_count', 'grade')

class UserCreateuserializers(serializers.ModelSerializer):

    class Meta:
        model = models.Tuser
        fields = ('username', 'email', 'password',)

    def create(self, validated_data):
        # 密码处理
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserCreateuserializers, self).create(validated_data)

class Loginserializers(serializers.Serializer):

    username = serializers.CharField(label='帐号')
    password = serializers.CharField(label='密码')

    def get_user(self):
        return authenticate(username='hello', password='123456')

    user = None

class UserinfoGetserializers(serializers.ModelSerializer):

    class Meta:
        model = models.Tuser
        fields = ('pk', 'email', 'avatar', 'sex',
                  'country', 'province', 'city', 'birthday',
                  'followers_count', 'grade')

class UserinfoCreateserializers(serializers.ModelSerializer):

    class Meta:
        model = models.Tuser
        fields = ('email', 'avatar', 'sex',
                  'country', 'province', 'city', 'birthday',)
class CreateuserView(generics.CreateAPIView):
    serializer_class = UserCreateuserializers

class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(label='帐号')
    password = serializers.CharField(label='密码')

    user = None
    def validate_username(self, value):
        if value:
            if not Tuser.objects.filter(username=value).exists():
                raise ValidationError('此用户不存在')
        return value

    def validate_password(self, value):
        username = self.initial_data['username']
        if value and username:
            self.user = authenticate(username=username, password=value)
            if not self.user:
                raise ValidationError('密码不正确')
        return value

class UserLoginView(generics.GenericAPIView):

    queryset = Tuser.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.user:
            login(request, serializer.user)
        return Response({
            "succ": bool(getattr(serializer.user, 'pk')),
            "userid": getattr(serializer.user, "pk", None),
        })

class UserLogout(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status.HTTP_200_OK)

class UserinfoView(generics.RetrieveUpdateAPIView):
    serializer_class = UserinfoGetserializers
    queryset = Tuser

    def get_serializer_class(self):
        if self.request.method != 'GET':
            return UserinfoCreateserializers
        return self.serializer_class

    @login_required
    def put(self, request, *args, **kwargs):
        if str(request.user.id) == str(kwargs.get('pk')):
            return self.update(request, *args, **kwargs)
        else:
            return Response(status.HTTP_403_FORBIDDEN)