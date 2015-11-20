# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topicontent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicontent',
            name='cover_image',
            field=models.ImageField(verbose_name='封面图片', upload_to=''),
        ),
        migrations.AlterField(
            model_name='topicontent',
            name='create_time',
            field=models.DateTimeField(auto_created=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='topicontent',
            name='update_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='更新时间'),
        ),
    ]
