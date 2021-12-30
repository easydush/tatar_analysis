import datetime
import hashlib
from django.test import TestCase
from core.models import TriggerPhrase
from core.util.ArticleAnalyser import ArticleAnalyser
from core.yandex_data_export.news_item import NewsItemDownloader, NewsItem
from core.yandex_data_export.news_topics import YandexNewsTopics


class TestTextAnalysis(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.ARTICLE_ANALYSER = ArticleAnalyser()

    def test_cleaning_text(self):
        text = "Roses (are) red, violets are blue!"
        self.assertEqual(self.ARTICLE_ANALYSER.clean_text(text), 'Roses are red violets are blue ')

    def test_normalizing_text(self):
        self.assertEqual(self.ARTICLE_ANALYSER.get_word_with_normal_form('Розы'), 'роза')
        self.assertEqual(self.ARTICLE_ANALYSER.get_word_with_normal_form('Делают'), 'делать')


    def test_checking_text(self):
        TriggerPhrase.objects.create(name='КФУ')
        self.ARTICLE_ANALYSER.add_keywords(TriggerPhrase.objects.all())
        self.assertEqual(
            self.ARTICLE_ANALYSER.check_text('день рождения КФУ'), ['КФУ'])

class YandexNewsTopicsTest(TestCase):
    def setUp(self):
        self.parser = YandexNewsTopics()

    def test_downloading_page(self):
        topics = self.parser.get_topics()
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 153)


class NewsItemDownloaderTest(TestCase):
    def setUp(self):
        self.parser = NewsItemDownloader()
        self.test_yandex_rss_url = 'https://news.yandex.ru/auto.rss'

    def test_get_news_from_rss_page(self):
        news = self.parser.get_news_from_rss_page(self.test_yandex_rss_url)
        self.assertIsNotNone(news)
        for i in news:
            self.assertIsNotNone(i.link)


class NewsItemTest(TestCase):
    def test_hash(self):
        news_item = NewsItem(
            title='title',
            description='description',
            link='link',
            pub_date='03 Aug 2020 15:09:43 +0000'
        )
        self.assertIsNotNone(news_item.hash)
        self.assertEqual(news_item.hash, hashlib.md5(
            (news_item.title + news_item.link + news_item.pub_date.__str__()).encode()
        ).hexdigest())

