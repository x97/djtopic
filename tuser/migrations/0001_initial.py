# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tuser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False, parent_link=True)),
                ('nickname', models.CharField(max_length=30)),
                ('avatar', models.ImageField(upload_to='')),
                ('sex', models.CharField(max_length=1, choices=[('1', '男'), ('0', '女')])),
                ('email_verified', models.CharField(max_length=1)),
                ('phone_verified', models.CharField(max_length=1)),
            ],
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=40, verbose_name='', blank=True)),
                ('province', models.CharField(max_length=40, verbose_name='', blank=True)),
                ('city', models.CharField(max_length=40, verbose_name='', blank=True)),
                ('birthday', models.DateField(verbose_name='', blank=True)),
                ('grade', models.IntegerField(verbose_name='')),
                ('followers_count', models.IntegerField(default=0, verbose_name='', blank=True)),
                ('following_count', models.IntegerField(default=0, verbose_name='', blank=True)),
                ('registed_time', models.DateTimeField(default=0, verbose_name='', blank=True)),
                ('User', models.OneToOneField(to='tuser.Tuser')),
            ],
        ),
    ]
