from django.contrib import admin
from .models import Tuser
# Register your models here.

@admin.register(Tuser)
class TuserAdmin(admin.ModelAdmin):
    fields = ('nickname', 'avatar', 'sex','country', 'province',
              'city', 'birthday', 'followers_count', 'topic_count',
              'collection_count')
    readonly_fields = ('collection_count', 'followers_count', 'topic_count')