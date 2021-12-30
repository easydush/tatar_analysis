import requests
from bs4 import BeautifulSoup


class YandexNewsTopics:
    def __init__(self):
        self.__url = 'https://yandex.ru/news/export'
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        self.__topics_url = []

    def get_topics(self):
        result = requests.get(self.__url, headers=self.__headers)
        result_page = result.text.encode('utf8')
        soup = BeautifulSoup(result_page, features='lxml')

        # find all items containing link to rss page
        all_items = soup.find_all('div', {'class': 'export__item'})

        # get links
        self.__topics_url = list(
            map(lambda wrapper_div: {'name': wrapper_div.a.text, 'url': wrapper_div.a['href']}, all_items))

        return self.__topics_url
