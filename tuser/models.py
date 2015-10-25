from django.db import models
from django.contrib.auth.models import User

class TuserManager(models.Manager):
    pass


class Tuser(User):
    SEX_CHOICES = (
        ('1', "男"),
        ('0', "女")
    )
    nickname = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(blank=True)
    sex = models.CharField(choices=SEX_CHOICES, max_length=1, default='0')
    email_verified = models.CharField(max_length=1, default='0')
    phone_verified = models.CharField(max_length=1, default='0')
    country = models.CharField(verbose_name="", max_length=40, blank=True)
    province = models.CharField(verbose_name="", max_length=40, blank=True)
    city = models.CharField(verbose_name="", max_length=40, blank=True)
    birthday = models.DateField(verbose_name="", blank=True, null=True)
    grade = models.IntegerField(verbose_name="", blank=True, default=0)
    followers_count = models.IntegerField(verbose_name="", blank=True, default=0)

    class Meta:
        pass

