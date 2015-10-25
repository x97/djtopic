# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tuser', '0002_auto_20151025_0238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tuser',
            name='avatar',
            field=models.ImageField(upload_to='', blank=True),
        ),
        migrations.AlterField(
            model_name='tuser',
            name='email_verified',
            field=models.CharField(default='0', max_length=1),
        ),
        migrations.AlterField(
            model_name='tuser',
            name='nickname',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='tuser',
            name='phone_verified',
            field=models.CharField(default='0', max_length=1),
        ),
        migrations.AlterField(
            model_name='tuser',
            name='sex',
            field=models.CharField(choices=[('1', '男'), ('0', '女')], default='0', max_length=1),
        ),
    ]
