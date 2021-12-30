import logging
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import hashlib

from core.util.SiteParser import SiteParser


class NewsItem:
    """
    Temporary storage to news item
    """

    def __init__(self, title, description, link, pub_date):
        self.__title = title
        self.__description = description
        self.__link = link
        self.__date_time_pattern = '%d %b %Y %H:%M:%S %z'
        self.__pub_date = datetime.strptime(pub_date, self.__date_time_pattern)
        # hash - news version control
        self.__hash = hashlib.md5(
            (self.__title + self.__link + self.__pub_date.__str__()).encode()
        ).hexdigest()

    @property
    def date_time_pattern(self):
        return self.__date_time_pattern

    @date_time_pattern.setter
    def date_time_pattern(self, new_pattern):
        self.__date_time_pattern = new_pattern

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def link(self):
        return self.__link

    @property
    def pub_date(self):
        return self.__pub_date

    @property
    def hash(self):
        return self.__hash

    def __str__(self):
        return f'{self.__title} - [{self.__pub_date}]  - [{self.__hash}]'


class NewsItemDownloader(SiteParser):
    """
    Class to download news from rss page
    """

    def __init__(self):
        super(NewsItemDownloader, self).__init__()
        self.__recursion_depth = 5

    def get_link_to_news_page(self, yandex_news_link, recursion_step=0):
        result = requests.get(yandex_news_link, headers=self._headers)
        result_page = result.text.encode('utf8')
        soup = BeautifulSoup(result_page, features='lxml')
        # init news link
        try:
            # get title
            story_name = soup.find('h1', {'class': 'story__head'})
            # get link
            news_link = story_name.find('a')['href']

            # new way
            # doc_content = soup.find('div', {'class': 'story__main'})
            # news_link = doc_content.a['href']
        except AttributeError:
            if recursion_step < self.__recursion_depth:
                news_link = self.get_link_to_news_page(yandex_news_link, recursion_step + 1)
            else:
                news_link = yandex_news_link
        return news_link

    def get_news_from_rss_page(self, rss_yandex_link):
        result = requests.get(rss_yandex_link, headers=self._headers)
        result_page = result.text.encode('utf8')
        soup = BeautifulSoup(result_page, features='lxml')

        # get all items
        items_list = soup.find_all('item')
        # parse each item
        news_list = list(
            map(lambda item: NewsItem(
                title=item.title.text,
                description=item.description.text,
                link=self.get_link_to_news_page(item.guid.text),
                pub_date=item.pubdate.text
            ), items_list)
        )
        return news_list
