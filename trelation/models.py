from django.db import models
from tuser.models import Tuser
# Create your models here.

class Relation(models.Model):
    RELATION_STATUS = (
        (0, '关注'),
        (1, '拉黑'),
    )
    #         (2, '互相关注'),
    user = models.ForeignKey(Tuser, verbose_name="用户", related_name="user")
    relation_user = models.ForeignKey(Tuser, verbose_name="关联用户", related_name="relation_user")
    relation = models.IntegerField(verbose_name="关系", choices=RELATION_STATUS, default=0)
    create_time = models.DateTimeField(verbose_name="创建时间", blank=True, null=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.user