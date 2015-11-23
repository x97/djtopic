# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topicontent', '0004_auto_20151121_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicomment',
            name='content',
            field=models.CharField(null=True, max_length=150),
        ),
    ]
