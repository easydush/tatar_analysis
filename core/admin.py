from django.contrib import admin

from core.models import Article, VKSource, VKGroup, VKPost


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'article_link', 'text']
    search_fields = ['title', 'text']
    ordering = ['author']


@admin.register(VKSource)
class VKSourceAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(VKGroup)
class VKGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'members_count', 'site']
    search_fields = ['name']


@admin.register(VKPost)
class VKPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner_id', 'address']
    search_fields = ['id', 'owner_id']
