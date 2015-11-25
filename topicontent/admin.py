from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Topicategory)
class Topicategory(admin.ModelAdmin):
    list_display = ['label']

@admin.register(Topicontent)
class TopicontentAdmin(admin.ModelAdmin):
    pass

@admin.register(Topicomment)
class TopicommentAdmin(admin.ModelAdmin):
    pass

# @admin.register(TopicRelation)
# class TopicRelationAdmin(admin.ModelAdmin):
#     pass