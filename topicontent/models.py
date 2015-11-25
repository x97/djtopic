from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


from django.db.models import F
from tuser.models import Tuser
# Create your models here.
class TopicategoryManager(models.Manager):
    pass

Topicategorys = TopicategoryManager

class Topicategory(models.Model):
    label = models.CharField(max_length=20, verbose_name="名称")
    objects = Topicategorys

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.label

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
        return Topicomment.filter(content_type=Topicontent, object_id=topic_id, status=1)

    def collect(self, instance):
        self.filter(pk=instance.pk).update(collect_count=F('collect_count')+1)

    def comment(self, instance):
        self.filter(pk=instance.pk).update(comment_count=F('comment_count')+1)

    def star(self, instance):
        self.filter(pk=instance.pk).update(star_count=F('star_count')+1)


Topicontents = TopicontentManager()

class Topicontent(models.Model):
    ARTICLE_STATUS = (
        ('0', '草稿'),
        ('1', '发布'),
        ('2', '隐藏'),
        ('3', '屏蔽'),
    )
    title = models.CharField(max_length=40, verbose_name="标题",)
    article = models.TextField(verbose_name="正文")
    author = models.ForeignKey(Tuser, verbose_name="作者")
    cover_image = models.ImageField(verbose_name="封面图片")
    article_status = models.CharField(max_length=1, verbose_name="状态", choices=ARTICLE_STATUS, blank=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, null=True)
    update_time = models.DateTimeField(verbose_name='更新时间', blank=True, null=True)
    label_category = models.ManyToManyField(Topicategory, verbose_name="标签", blank=True)
    comment_count = models.IntegerField(blank=True, null=True, default=0)
    star_count = models.IntegerField(verbose_name='点赞数', blank=True, null=True, default=0)
    collect_count = models.IntegerField(verbose_name='收藏数', blank=True, null=True, default=0)
    status = models.IntegerField(default=0)
    objects = Topicontents

    def admin_article_status(self):
        status_list = ['草稿', '发布', '隐藏', '屏蔽']
        return status_list[int(self.article_status)]
    admin_article_status.short_description = "状态"
    def setbest(self):
        return mark_safe('<a class="button" href="%s/set/">加精</a>' % self.id)
    setbest.allow_tags = True
    setbest.short_description = '动作'

    def resetbest(self):
        return mark_safe('<a class="button" href="%s/reset/">取消加精</a>' % self.id)
    resetbest.allow_tags = True
    resetbest.short_description = '动作'

    def admin_cover_image(self):
        if self.cover_image:
            return '<img height="150" src="/media/%s" />' % self.cover_image
        return ''
    admin_cover_image.allow_tags = True
    admin_cover_image.short_description = '用户照片'

    class Meta:
        verbose_name = verbose_name_plural = '所有话题'

    def __str__(self):
        return self.title

class TopicommentManager(models.Manager):

    def set_best_comment(self, id):
        self.get(id=id).update(status=1)

Topicomments = TopicommentManager

# class Topicomment(models.Model):
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.PositiveIntegerField()
#     origin_content_type = models.ForeignKey(ContentType, related_name='origin_comment', null=True)
#     origin_object_id = models.PositiveIntegerField(null=True)
#     author = models.ForeignKey(Tuser)
#     comment = GenericForeignKey('content_type', 'object_id')
#     comment_origin = GenericForeignKey('origin_content_type', 'origin_object_id')
#     content = models.CharField(max_length=150, null=True)
#     comment_time = models.DateTimeField(auto_now_add=True, blank=True)
#     star_count = models.PositiveIntegerField(blank=True, null=True, default=0)
#     status = models.IntegerField(blank=True, null=True, default=0)
#     objects = Topicomments
#
#     class Meta:
#         verbose_name = verbose_name_plural = '评论'
#
#     def __str__(self):
#         return self.content

class Topicomment(models.Model):

    author = models.ForeignKey(Tuser)
    content = models.CharField(max_length=150, null=True)
    topic = models.ForeignKey(Topicontent, blank=True, null=True, verbose_name="话题")
    review = models.ForeignKey('self', blank=True, null=True, verbose_name="评论")
    star_count = models.PositiveIntegerField(blank=True, null=True, default=0)
    status = models.IntegerField(blank=True, null=True, default=0)
    create_time = models.DateTimeField(blank=True, null=True)
    objects = Topicomments

    class Meta:
        verbose_name = verbose_name_plural = '评论'

    def __str__(self):
        return self.content

class CollectionsManager(models.Manager):
    def get_collections(self, user):
        return self.filter(user=user)

Collections = CollectionsManager
class TopicRelation(models.Model):

    RELATION = (
        (0, "收藏"),
        (1, "点赞"),
    )
    user = models.ForeignKey(Tuser, verbose_name="用户")
    topic = models.ForeignKey(Topicontent, verbose_name="话题")
    collect_time = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间")
    relation = models.IntegerField(default=0, choices=RELATION, verbose_name="关系")
    status = models.IntegerField(default=1, verbose_name="状态")
    objects = Collections

    class Meta:
        verbose_name = verbose_name_plural = '话题关系'
    # def __str__(self):
    #     return self.topic
# class StaredTopic(models.M)

class ProhibitWord(models.Model):
    word = models.CharField(max_length=20, verbose_name="关键字")

    class Meta:
        verbose_name = verbose_name_plural = '禁止关键字'

    def __str__(self):
        return self.word

class ProxyTopicontent(Topicontent):
    class Meta:
        proxy = True
        verbose_name = verbose_name_plural = '精选话题'
