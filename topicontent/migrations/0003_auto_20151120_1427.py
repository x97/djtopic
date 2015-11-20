# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topicontent', '0002_auto_20151120_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicontent',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True),
        ),
    ]
