from django.urls import path

from core.views import NewsView, KeyWords, YandexNewsSource, ToggleActiveKey, VKNewsSource

app_name = 'core'
urlpatterns = [
    path('', NewsView.as_view(), name='news'),
    path('key-words/', KeyWords.as_view(), name='key_words'),
    path('yandex-source/', YandexNewsSource.as_view(), name='yandex_source'),
    path('vk-source/', VKNewsSource.as_view(), name='vk_source'),

    # ajax
    path('toggle_active_key/', ToggleActiveKey.as_view(), name='toggle_active_key')
]
