from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from tuser.models import *
# Create your models here.
class TopicategoryManager(models.Manager):
    pass

Topicategorys = TopicategoryManager

class Topicategory(models.Model):
    label = models.CharField(max_length=20, verbose_name="名称")
    objects = Topicategorys

    class Meta:
        verbose_name = verbose_name_plural = '标签'

class TopicontentManager(models.Manager):

    def topic_modify(self, user):
        return self.filter(author=user, article_status=0)

    def topic_publish(self, user):
        return self.filter(author=user, article_status=1)

    def drop_topic(self, user, topic_id):
        self.get(author=user, id=topic_id).update(article_status=2)

    def topic_comments(self, topic_id):
        return Topicomment.filter(content_type=Topicontent, object_id=topic_id)

    def best_topic_comments(self, topic_id):
        return Topicomment.filter(content_type=Topicontent, object_id=topic_id, status=2)

Topicontents = TopicontentManager

class Topicontent(models.Model):
    ARTICLE_STATUS = (
        (0, '草稿'),
        (1, '发布'),
        (2, '隐藏'),
    )
    title = models.CharField(max_length=40, verbose_name="标题",)
    article = models.TextField(verbose_name="正文")
    author = models.ForeignKey(User, verbose_name="作者")
    cover_image = models.ImageField(verbose_name="封面图片", upload_to="/media/topic/cover/")
    article_status = models.CharField(verbose_name="状态", choices=ARTICLE_STATUS, blank=True)
    create_time = models.DateTimeField(verbose_name="创建时间", blank=True)
    update_time = models.DateTimeField(verbose_name='更新时间', blank=True)
    label_category = models.ManyToManyField(Topicategory, verbose_name="标签", blank=True)
    comment_count = models.IntegerField(blank=True, null=True, default=0)
    star_count = models.IntergerField(blank=True, null=True, default=0)
    collect_count = models.IntegerField(blank=True, null=True, default=0)

    objects = Topicontents

class TopicommentManager(models.Manager):

    def set_best_comment(self, id):
        self.get(id=id).update(status=2)

Topicomments = TopicommentManager

class Topicomment(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    review_comment = models.ForeignKey('self', blank=True, null=True)
    author = models.ForeignKey(User)
    content = GenericForeignKey('content_type', 'object_id')
    comment_time = models.DateTimeField()
    status = models.IntegerField(max_length=1, blank=True, null=True)
    star_count = models.IntergerField(blank=True, null=True, default=0)
    objects = Topicomments

class CollectionsManager(models.Manager):
    def get_collections(self, user):
        return self.filter(user=user)

Collections = CollectionsManager
class Collection(models.Model):
    user = models.ForeignKey(User)
    topic = models.ForeignKey(Topicontent)
    collect_time = models.DateTimeField(auto_now_add=True)
    objects = Collections