from selenium import webdriver
from selenium.webdriver.common.by import By
from decouple import config

SEARCH_QUERIES = ['Академия наук Республики Татарстан']
PDF_LINKS = []
driver = webdriver.Chrome()


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
    return driver.find_elements(By.XPATH, '//a[starts-with(@href,"/item.asp")]')


def exctract_all_links():
    links = extract_links_from_page()
    return links


def parse_page(link):
    link.click()
    file = driver.find_element(By.XPATH, '//*[text()="Полный текст"]')
    file.click()
    print(driver.current_url)
    new_window =driver.current_window_handle
    PDF_LINKS.append(driver.current_url)


if __name__ == '__main__':
    authorize()
    get_anrt_page()
    links = exctract_all_links()

    for link in links:
        parse_page(link)
