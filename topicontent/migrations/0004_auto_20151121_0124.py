# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topicontent', '0003_auto_20151120_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topicomment',
            name='review_comment',
        ),
        migrations.AddField(
            model_name='topicomment',
            name='content',
            field=models.CharField(max_length='150', null=True),
        ),
        migrations.AlterField(
            model_name='topicomment',
            name='comment_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
