from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Topicategory)
class Topicategory(admin.ModelAdmin):
    list_display = ['label']
