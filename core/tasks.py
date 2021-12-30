import logging
from functools import reduce
from itertools import chain

from django.db import IntegrityError
from django.db.models import Q

from core.models import YandexNewsTopic, YandexNewsItem, TriggerPhrase, TriggerNews, VKPost
from core.text_tone.TextToneAnalyser import TextToneAnalyser, POSITIVE, NEUTRAL, NEGATIVE
from core.util.SiteParser import SiteParser
from core.util.ArticleAnalyser import ArticleAnalyser
from core.vk.vk_parser import VKParser
from core.yandex_data_export.news_item import NewsItemDownloader
from tatar_analysis.celery import app
from operator import or_

# Get an instance of a logger
logger = logging.getLogger(__name__)


@app.task
def update_news_items():
    # get topics from db
    topics = []

    # test stuff
    # ToDo: add all topics
    topics = YandexNewsTopic.objects.all()
    # end test

    parser = NewsItemDownloader()

    for topic in topics:
        # get news from single rss page
        temp_news = parser.get_news_from_rss_page(rss_yandex_link=topic.rss_url)

        # creating news items
        for article in temp_news:
            news = YandexNewsItem(
                title=article.title,
                link=article.link,
                pub_date=article.pub_date,
                hash=article.hash
            )
            try:
                news.save()
                logger.info(f'Added: [{news.hash}] {news.title}')
            except IntegrityError:
                # handling re-adding news
                logger.info(f'Exist: [{news.hash}] {news.title}')


@app.task
def check_yandex_news_for_trigger_words():
    # todo: take all unchecked news
    news = YandexNewsItem.unchecked.all()[:10]  # all() [:5] for testing
    # init site parser
    parser = SiteParser()
    # init analyser
    analyser = ArticleAnalyser()
    # get all trigger words
    trigger_phrase = TriggerPhrase.objects.filter(is_active=True)
    # add keywords
    analyser.add_keywords(trigger_phrase)
    # text Tone Analyser
    tone = TextToneAnalyser()

    for article in news.iterator():
        # get raw article text and article name
        raw_text = parser.get_article_text(article.link)
        article_name = article.title

        article_keywords_found_list = analyser.check_text(raw_text)
        article_name_keywords_found_list = analyser.check_text(article_name)

        if article_keywords_found_list or article_name_keywords_found_list:
            # calculate tone
            tone_result = tone.get_text_tone([raw_text])
            tone_max_type = tone.get_max_text_tone_type(tone_result)

            # check news tone result
            if tone_max_type == POSITIVE:
                news_tone = TriggerNews.POSITIVE
            elif tone_max_type == NEGATIVE:
                news_tone = TriggerNews.NEGATIVE
            else:
                news_tone = TriggerNews.NEUTRAL

            trigger_news = TriggerNews(
                title=article.title,
                article_link=article.link,
                description='',
                rate=0,
                news_type=TriggerNews.YANDEX,
                tone_type=news_tone,
                tone_value=tone_result.get(tone_max_type)
            )
            trigger_news.save()
            if article_keywords_found_list:
                article_words = TriggerPhrase.objects.filter(
                    reduce(or_, [Q(name=word) for word in article_keywords_found_list]))
                for word in article_words:
                    trigger_news.trigger_word.add(word)
            if article_name_keywords_found_list:
                article_name_words = TriggerPhrase.objects.filter(
                    reduce(or_, [Q(name=word) for word in article_name_keywords_found_list]))
                for word in article_name_words:
                    trigger_news.trigger_word.add(word)
            trigger_news.save()

            logger.warning(f'Trigger: [{article.hash}] [{tone_max_type}] {article.title}')

        # update article
        article.checked = True
        article.save()
        logger.info(f'Checked: [{article.hash}] {article.title}')


@app.task
def update_vk_content():
    parser = VKParser()
    parser.parse_groups()
    logger.info(f'Updated VK groups')


@app.task
def check_vk_news_for_trigger_words():
    posts = VKPost.unchecked.all()
    # analyser = ArticleAnalyser()
    # get all trigger words
    trigger_phrase = TriggerPhrase.objects.filter(is_active=True)
    # add keywords
    # analyser.add_keywords(trigger_phrase)
    # text Tone Analyser
    tone = TextToneAnalyser()
    for post in posts.iterator():
        text = post.text
        # article_keywords_found_list = analyser.check_text(text)

        # calculate tone
        tone_result = tone.get_text_tone([text])

        trigger_news = TriggerNews(
            title=text[:200],
            article_link=post.address,
            description='',
            news_type=TriggerNews.VK,
            tone_type=TriggerNews.POSITIVE,
            tone_value='100%',
            last_update=post.pub_date
        )
        trigger_news.save()
        post.checked = True
        post.save()
        logger.info(f'VK: {post.id} has been checked')
