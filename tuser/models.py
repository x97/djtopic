from django.db import models
from django.contrib.auth.models import User

class TuserManager(models.Manager):
    pass


class Tuser(User):
    SEX_CHOICES = (
        (1, "男"),
        (0, "女")
    )
    nickname = models.CharField(max_length=30)
    avatar = models.ImageField()
    sex = models.CharField(choices=SEX_CHOICES)
    email_verified = models.IntegerField(max_length=1)
    phone_verified = models.IntegerField(max_length=1)

    class Meta:
        pass

class UserinfoManager(models.Manager):
    pass

class Userinfo(models.Model):
    User = models.OneToOneField(Tuser)
    country = models.CharField(verbose_name="", max_length=40, blank=True)
    province = models.CharField(verbose_name="", max_length=40, blank=True)
    city = models.CharField(verbose_name="", max_length=40, blank=True)
    birthday = models.DateField(verbose_name="", blank=True)
    grade = models.IntegerField(verbose_name="", max_length=2)
    followers_count = models.IntegerField(verbose_name="", blank=True,default=0)
    following_count = models.IntegerField(verbose_name="", blank=True, default=0)
    registed_time = models.DateTimeField(verbose_name='', blank=True, default=0)
