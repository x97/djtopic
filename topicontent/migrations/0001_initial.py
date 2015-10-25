# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collect_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topicategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=20, verbose_name='名称')),
            ],
            options={
                'verbose_name_plural': '标签',
                'verbose_name': '标签',
            },
        ),
        migrations.CreateModel(
            name='Topicomment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('comment_time', models.DateTimeField()),
                ('star_count', models.PositiveIntegerField(default=0, null=True, blank=True)),
                ('status', models.IntegerField(null=True, blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('review_comment', models.ForeignKey(to='topicontent.Topicomment', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topicontent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='标题')),
                ('article', models.TextField(verbose_name='正文')),
                ('cover_image', models.ImageField(upload_to='/media/topic/cover/', verbose_name='封面图片')),
                ('article_status', models.CharField(max_length=1, verbose_name='状态', blank=True, choices=[('0', '草稿'), ('1', '发布'), ('2', '隐藏')])),
                ('create_time', models.DateTimeField(verbose_name='创建时间', blank=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', blank=True)),
                ('comment_count', models.IntegerField(default=0, null=True, blank=True)),
                ('star_count', models.IntegerField(default=0, null=True, blank=True)),
                ('collect_count', models.IntegerField(default=0, null=True, blank=True)),
                ('author', models.ForeignKey(verbose_name='作者', to=settings.AUTH_USER_MODEL)),
                ('label_category', models.ManyToManyField(verbose_name='标签', to='topicontent.Topicategory', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='collection',
            name='topic',
            field=models.ForeignKey(to='topicontent.Topicontent'),
        ),
        migrations.AddField(
            model_name='collection',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
