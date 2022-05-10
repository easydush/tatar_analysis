import datetime

import requests
import os

from core.models import Article
from parsers.pdf import parse_pdf
from tatar_analysis.settings import MEDIA_ROOT
from bs4 import BeautifulSoup

BASE_URL = 'https://shelly.kpfu.ru/pls/iias/student_diplom_g'
P_FACULTY = '9023'
MIN_YEAR = 2015


def get_page_with_works(finish_year, page):
    result = requests.post(
        "https://shelly.kpfu.ru/pls/iias/student_diplom_g",
        data={
            "p_faculty": P_FACULTY,
            "p_finish_year": str(finish_year),
            "p_page": str(page),
        },
    )
    return result


def get_list_students_on_page(finish_year, page):
    response = get_page_with_works(finish_year, page)
    soup = BeautifulSoup(response.text, "html.parser")
    students = (soup.findAll("tr", class_="konf_tr"))[1:]
    result = []
    for data in students:
        student_name = (data.find("td")).text
        theme = (data.find("a")).text
        link = (data.find("a"))["href"]
        result.append((student_name, theme, link))
    return result


def find_max_page(finish_year):
    response = get_page_with_works(finish_year, 1)
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        page = soup.findAll("a", attrs={"id": "class="})[-1].text
    except IndexError:
        page = 0
    return int(page)


def get_full_list_students(finish_year):
    page = find_max_page(finish_year)
    if not page:
        return None
    result = []
    for i in range(page):
        page_list = get_list_students_on_page(finish_year, i + 1)
        result += page_list
    return result


def download_file(url):
    response = requests.get(url)
    with open(os.path.join(MEDIA_ROOT, "uploads", "work.pdf"), "wb") as f:
        f.write(response.content)


def download_parse():
    for finish_year in range(MIN_YEAR, datetime.datetime.now().year):
        list_students = get_full_list_students(finish_year)
        if not list_students:
            continue
        else:
            for i in list_students:
                student_name = i[0]
                theme = i[1]
                url_link = i[2]
                download_file(url_link)
                print(url_link)
                out = parse_pdf(
                    os.path.join(MEDIA_ROOT, "uploads", "work.pdf")
                )

                article = Article.objects.create(author=student_name, title=theme, article_link=url_link, text=out)
                print(article.author)

