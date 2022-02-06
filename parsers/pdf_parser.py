import pdfplumber
import re


def parse_pdf(path):
    with pdfplumber.open(path) as pdf:
        text = ''.join([page.extract_text() for page in pdf.pages])
    print(text)
    return text
