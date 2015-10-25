# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tuser', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='User',
        ),
        migrations.AddField(
            model_name='tuser',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='tuser',
            name='city',
            field=models.CharField(max_length=40, blank=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='tuser',
            name='country',
            field=models.CharField(max_length=40, blank=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='tuser',
            name='followers_count',
            field=models.IntegerField(blank=True, default=0, verbose_name=''),
        ),
        migrations.AddField(
            model_name='tuser',
            name='grade',
            field=models.IntegerField(blank=True, default=0, verbose_name=''),
        ),
        migrations.AddField(
            model_name='tuser',
            name='province',
            field=models.CharField(max_length=40, blank=True, verbose_name=''),
        ),
        migrations.DeleteModel(
            name='Userinfo',
        ),
    ]
