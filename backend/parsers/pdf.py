import pdfplumber


def parse_pdf(path):
    with pdfplumber.open(path) as pdf:
        text = ''.join([page.extract_text() for page in pdf.pages])
    return text
