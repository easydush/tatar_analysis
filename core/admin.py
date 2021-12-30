from django.contrib import admin

from core.models import YandexNewsTopic, YandexNewsItem, TriggerPhrase, TriggerNews, VKSource, VKGroup, VKPost


@admin.register(YandexNewsTopic)
class YandexNewsTopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'rss_url']
    search_fields = ['name']
    ordering = ['name']


@admin.register(YandexNewsItem)
class YandexNewsItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'hash', 'link', 'pub_date', 'checked']
    search_fields = ['title', 'hash']
    list_filter = ['checked']


@admin.register(TriggerPhrase)
class TriggerPhraseAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class NewsTypeFilter(admin.SimpleListFilter):
    title = 'News type'
    parameter_name = 'news_type'

    def lookups(self, request, model_admin):
        return (
            ('YANDEX', 'YANDEX'),
            ('VK', 'VK'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'VK':
            return queryset.filter(news_type=TriggerNews.VK)
        elif value == 'YANDEX':
            return queryset.filter(news_type=TriggerNews.YANDEX)
        else:
            return queryset

@admin.register(TriggerNews)
class TriggerNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'article_link', 'last_update', 'news_type_value', 'tone_type_value', 'tone_value']
    list_filter = ['last_update', NewsTypeFilter]
    search_fields = ['title', 'description']
    ordering = ['last_update']

    def news_type_value(self, obj):
        if obj.news_type == TriggerNews.YANDEX:
            return 'YANDEX'
        else:
            return 'VK'

    def tone_type_value(self, obj):
        if obj.tone_type == TriggerNews.POSITIVE:
            return 'POSITIVE'
        elif obj.tone_type == TriggerNews.NEGATIVE:
            return 'NEGATIVE'
        else:
            return 'NEUTRAL'


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
    list_display = ['id', 'owner_id', 'address', 'likes', 'reposts', 'comments', 'checked']
    search_fields = ['id', 'owner_id', 'pub_date']
