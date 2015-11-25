from django.db import models
from django.contrib.auth.models import User
from django.db.models import F

class TuserManager(models.Manager):

    def follows(self, instance):
        self.filter(pk=instance.pk).update(followers_count=F('followers_count')+1)

    def following(self, instance):
        print(self.filter(pk=instance.pk))
        self.filter(pk=instance.pk).update(following_count=F('following_count')+1)

    def unfollows(self, instance):
        print(instance.pk)
        print(self.filter(pk=instance.pk))
        self.filter(pk=instance.pk).update(followers_count=F('followers_count')-1)

    def unfollowing(self, instance):
        self.filter(pk=instance.pk).update(following_count=F('following_count')-1)

tusers = TuserManager()

class Tuser(User):
    SEX_CHOICES = (
        ('1', "男"),
        ('0', "女")
    )
    nickname = models.CharField(max_length=30, blank=True, verbose_name="昵称")
    avatar = models.ImageField(blank=True, null=True, verbose_name="头像")
    sex = models.CharField(choices=SEX_CHOICES, max_length=1, default='0', verbose_name="性别")
    email_verified = models.CharField(max_length=1, default='0', verbose_name="邮箱验证")
    phone_verified = models.CharField(max_length=1, default='0', verbose_name="手机验证")
    country = models.CharField(verbose_name="国家", max_length=40, blank=True)
    province = models.CharField(verbose_name="省份", max_length=40, blank=True)
    city = models.CharField(verbose_name="城市", max_length=40, blank=True)
    birthday = models.DateField(verbose_name="生日", blank=True, null=True)
    grade = models.IntegerField(verbose_name="等级", blank=True, default=0)
    followers_count = models.IntegerField(verbose_name="粉丝数量", blank=True, default=0)
    following_count = models.IntegerField(verbose_name="关注数量", blank=True, default=0)
    topic_count = models.IntegerField(verbose_name="话题数量", blank=True, default=0)
    collection_count = models.IntegerField(verbose_name="收藏数量", blank=True, default=0)

    objects = tusers

    class Meta:
        verbose_name = verbose_name_plural = '用户信息'

