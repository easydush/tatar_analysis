import requests
from bs4 import BeautifulSoup


class SiteParser:
    """
    Class to download news from any page
    """

    def __init__(self):
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }

    def get_article_text(self, link):
        result = requests.get(link, headers=self._headers)
        result_page = result.text.encode('utf8')
        soup = BeautifulSoup(result_page, features='lxml')

        # get raw page text
        raw_text = soup.get_text()

        return raw_text
