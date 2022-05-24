import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from decouple import config
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SEARCH_QUERIES = ['Академия наук Республики Татарстан']
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
pdf_file = open("pdfs.txt", "w")

def authorize():
    driver.get('http://www.elibrary.ru')
    login = driver.find_element(By.ID, 'login')
    login.send_keys(config('ELIB_USER'))
    password = driver.find_element(By.ID, 'password')
    password.send_keys(config('ELIB_PASS'))
    enter = driver.find_element(By.XPATH, '//*[text()="Вход"]')
    enter.click()


def get_anrt_page():
    search = driver.find_element(By.ID, 'ftext')
    search.send_keys(SEARCH_QUERIES[0])
    submit = driver.find_element(By.XPATH, '//*[text()="Найти"]')
    submit.click()


def extract_links_from_page():
    elems = driver.find_elements(By.XPATH, '//a[starts-with(@href,"/item.asp")]')
    return [elem.get_attribute('href') for elem in elems]


def extract_all_links():
    all_links = extract_links_from_page()

    next_page = driver.find_element(By.XPATH, '//a[text()=">>"]')
    while next_page:
        time.sleep(5)
        next_page.click()
        all_links += extract_links_from_page()
        try:
            next_page = driver.find_element(By.XPATH, '//a[text()=">>"]')
        except NoSuchElementException:
            return all_links


def parse_page(link):
    driver.get(link)
    try:
        file = driver.find_element(By.XPATH, '//*[starts-with(text(),"Полный текст")]')
    except NoSuchElementException:
        return
    file.click()
    pdf_file.write(f'{driver.current_url}\n')
    time.sleep(5)


if __name__ == '__main__':
    authorize()

    get_anrt_page()
    links = extract_all_links()

    with open("links.txt", "w") as txt_file:
        for link in links:
            txt_file.write(f'{link}\n')

    # links = []
    #
    # with open("links.txt", "r") as txt_file:
    #     links = txt_file.readlines()
    #
    # for link in links:
    #     parse_page(link.replace('\n', ''))
