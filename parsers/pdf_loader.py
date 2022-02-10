import requests
import os


from core.models import Article
from parsers.pdf_parser import parse_pdf
from tatar_analysis.settings import MEDIA_ROOT
from bs4 import BeautifulSoup


def get_page_with_works(faculty, finish_year, page, p_qt, p_ks):
    result = requests.post(
        "https://shelly.kpfu.ru/pls/iias/student_diplom_g",
        data={
            "p_faculty": str(faculty),
            "p_finish_year": str(finish_year),
            "p_poisk": "1",
            "p_speciality": "6344",
            "p_page": str(page),
            "p_qt": p_qt,
            "p_ks": p_ks,
        },
    )
    return result


def get_list_students_on_page(faculty, finish_year, page, p_qt, p_ks):
    response = get_page_with_works(faculty, finish_year, page, p_qt, p_ks)
    soup = BeautifulSoup(response.text, "html.parser")
    students = (soup.findAll("tr", class_="konf_tr"))[1:]
    result = []
    for data in students:
        student_name = (data.find("td")).text
        theme = (data.find("a")).text
        link = (data.find("a"))["href"]
        result.append((student_name, theme, link))
    return result


def find_max_page(faculty, finish_year, p_qt, p_ks):
    response = get_page_with_works(faculty, finish_year, 1, p_qt, p_ks)
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        page = soup.findAll("a", attrs={"id": "class="})[-1].text
    except IndexError:
        page = 0
    return int(page)


def get_full_list_students(faculty, finish_year, p_qt, p_ks):
    page = find_max_page(faculty, finish_year, p_qt, p_ks)
    if not page:
        return None
    result = []
    for i in range(page):
        page_list = get_list_students_on_page(faculty, finish_year, i + 1, p_qt, p_ks)
        result += page_list
    return result


def download_file(url):
    response = requests.get(url)
    with open(os.path.join(MEDIA_ROOT, "uploads", "work.pdf"), "wb") as f:
        f.write(response.content)


def download_parse(faculty, finish_year):
    for p_qt in range(1, 3):
        for p_ks in range(1, 2):
            list_students = get_full_list_students(faculty, finish_year, p_qt, p_ks)
            if not list_students:
                continue
            else:
                for i in list_students:
                    student_name = i[0]
                    theme = i[1]
                    url_link = i[2]
                    download_file(url_link)

                    out = parse_pdf(
                        os.path.join(MEDIA_ROOT, "uploads", "work.pdf")
                    )
                    article = Article.objects.create(author=student_name, title=theme, article_link=url_link, text=out)
                    print(article.author)
