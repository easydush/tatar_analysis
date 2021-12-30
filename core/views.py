import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView

from core.models import TriggerNews, TriggerPhrase, YandexNewsTopic, VKGroup


# class HomeView(LoginRequiredMixin, TemplateView):
#     """
#     Main page with all main information
#     """
#     template_name = 'core/home.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         context_data['main_page'] = True
#         return context_data


class NewsView(LoginRequiredMixin, ListView):
    """
    Main page with all main information
    """
    template_name = 'core/news.html'
    model = TriggerNews
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['news_page'] = True
        return context_data

    def get_queryset(self):
        queryset = TriggerNews.objects.all()
        filter_word = self.request.GET.get('filter_word', None)
        if filter_word:
            queryset = queryset.filter(trigger_word__name=filter_word)

        filter_news_type = self.request.GET.get('filter_news_type', None)
        if filter_news_type:
            queryset = queryset.filter(news_type__in=filter_news_type.split(','))

        return queryset


class KeyWords(LoginRequiredMixin, ListView):
    """
    Page with all key words
    """
    template_name = 'core/key_words.html'
    model = TriggerPhrase
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['key_words_page'] = True
        return context_data


class YandexNewsSource(LoginRequiredMixin, ListView):
    """
    Page with yandex news sources
    """

    template_name = 'core/yandex_news.html'
    model = YandexNewsTopic
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['yandex_source'] = True
        return context_data


class VKNewsSource(LoginRequiredMixin, ListView):
    """
    Page with vk news sources
    """

    template_name = 'core/vk_news.html'
    model = VKGroup
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['vk_source'] = True
        return context_data


class ToggleActiveKey(LoginRequiredMixin, View):
    """
    Toggle trigger word
    """

    def post(self, request):
        if request.is_ajax():
            key_id = request.POST.get('key_id', None)
            key_type = request.POST.get('type', None)
            is_active = request.POST.get('is_active', None)
            keyword = None
            if key_type == 'word':
                keyword = TriggerPhrase.objects.get(id=key_id)
            elif key_type == 'yandex':
                keyword = YandexNewsTopic.objects.get(id=key_id)
            elif key_type == 'vk':
                keyword = VKGroup.objects.get(id=key_id)
            try:
                keyword.is_active = is_active
                keyword.save()
            except AttributeError:
                pass
            data = {'status': 'ok'}
            return HttpResponse(json.dumps(data), content_type='application/json')
