from django.core.management import BaseCommand

from core.models import YandexNewsTopic
from core.yandex_data_export.news_topics import YandexNewsTopics


class Command(BaseCommand):
    """
    Command to get topics from yandex news page
    """
    def handle(self, *args, **options):
        parser = YandexNewsTopics()
        topics = parser.get_topics()

        YandexNewsTopic.objects.bulk_create(list(
            map(lambda topic: YandexNewsTopic(name=topic['name'], rss_url=topic['url']), topics)
        ))
