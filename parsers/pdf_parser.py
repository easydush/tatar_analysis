import pdfplumber
import re


def parse_pdf(path):
    with pdfplumber.open(path) as pdf:
        text = pdf.extract_text()
        print(text)
        first_page = pdf.pages[3].extract_text()
        specialty = re.search(r"\d+[.]\s?\d+[.]\s?\d+\s([-, –, —]\s?)?\w+\s\w+\s", first_page)[0].rstrip()
        # три разных тире
        if not ("-" in specialty or "–" in specialty or "—" in specialty):
            specialty = specialty.replace(" ", " – ", 1)
        if "-" in specialty or "—" in specialty:
            specialty = specialty.replace("-", "–") if "-" in specialty else specialty.replace("—", "–")
        if specialty[: specialty.find("–") - 1].count(" ") > 0:
            index = specialty.find("–")
            specialty = specialty[: index - 1].replace(" ", "") + specialty[index - 1 :]
        if specialty[specialty.find("–") + 1] != " ":
            index = specialty.find("–")
            specialty = specialty[: index + 1] + " " + specialty[index + 1 :]
        group_number = re.search(r"([Г, г]руппы)\D+\d+\s?[-, –]\s?\d+\s?", first_page)[0][6:].rstrip()
        group_number = re.search(r"\d+\s?[-, –]\s?\d+\s?", group_number)[0]
        if " " in group_number:
            group_number = group_number.replace(" ", "")
        if "–" in group_number:
            group_number = group_number.replace("–", "-")
        scientific_director = re.findall(r"[А-Я]\w+\s[А-Я][.]\s?[А-Я][.]?", first_page)[1]
        if not scientific_director.endswith("."):
            scientific_director += "."
        if scientific_director.count(" ") > 1:
            index = scientific_director.rfind(" ")
            scientific_director = scientific_director[:index] + scientific_director[index + 1 :]

    return specialty, group_number, scientific_director, text
