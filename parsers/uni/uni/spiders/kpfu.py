import scrapy
from selenium import webdriver

# class KpfuSpider(scrapy.Spider):
#     name = 'kpfu'
#     allowed_domains = ['kpfu.ru']
#     driver = webdriver.Chrome('C://Users/easy/Downloads/chromedriver.exe')
#     url = 'https://kpfu.ru/philology-culture/uchebnyj-process/diplomnye-raboty'
#
#     def extract_links(self):
#         pass
#
#     def next_page(self):
#         pass
#
#     def choose_profile(self):
#         pass
#
#     def parse(self, response):
#         self.driver.get(self.url)
#         print(self.driver.page_source)
driver = webdriver.Chrome('C://Users/easy/Downloads/chromedriver.exe')
url = 'https://kpfu.ru/philology-culture/uchebnyj-process/diplomnye-raboty'
driver.get(url)
print(driver.page_source)
