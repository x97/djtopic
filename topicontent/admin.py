from django.contrib import admin
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from .models import *

admin.site.site_header = '移动社交平台管理'
# Register your models here.
@admin.register(Topicategory)
class Topicategory(admin.ModelAdmin):
    list_display = ['label']

@admin.register(Topicontent)
class TopicontentAdmin(admin.ModelAdmin):
    list_display = ['article', 'create_time', 'admin_article_status',
                    'star_count', 'collect_count', 'setbest', ]

    exclude = ['status', 'article_status', ]
    list_filter = ['create_time']
    readonly_fields = ['author', 'cover_image', 'star_count', 'comment_count',
                       'collect_count']

    def setview(self, request, id=None):
        obj = Topicontent.objects.get(id=id)
        obj.status = 1
        obj.save()
        info = self.model._meta.app_label, self.model._meta.model_name
        return HttpResponseRedirect(reverse('admin:%s_%s_changelist' % info))

    def get_urls(self):
        urls = super(TopicontentAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<id>\d+)/set/$', self.setview),
        ]
        return my_urls + urls

    def get_queryset(self, request):
        qs = super(TopicontentAdmin, self).get_queryset(request)
        return qs.filter(status=0)

@admin.register(Topicomment)
class TopicommentAdmin(admin.ModelAdmin):
    pass
@admin.register(ProhibitWord)
class ProhibitWordAdmin(admin.ModelAdmin):
    pass
@admin.register(ProxyTopicontent)
class ProxyTopicontentAdmin(admin.ModelAdmin):
    list_display = ['article', 'create_time', 'admin_article_status',
                    'star_count', 'collect_count', 'resetbest']
    exclude = ['status', 'article_status', ]
    list_filter = ['create_time']
    readonly_fields = ['author', 'cover_image', 'star_count', 'comment_count',
                       'collect_count']

    def resetview(self, request, id=None):
        obj = Topicontent.objects.get(id=id)
        obj.status = 0
        obj.save()
        info = self.model._meta.app_label, self.model._meta.model_name
        return HttpResponseRedirect(reverse('admin:%s_%s_changelist' % info))

    def get_urls(self):
        urls = super(ProxyTopicontentAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<id>\d+)/reset/$', self.resetview),
        ]
        return my_urls + urls
    def get_queryset(self, request):
        qs = super(ProxyTopicontentAdmin, self).get_queryset(request)
        return qs.filter(status=1)

# @admin.register(TopicRelation)
# class TopicRelationAdmin(admin.ModelAdmin):
#     pass