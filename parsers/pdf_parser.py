from django.conf import settings
from pdfminer.high_level import extract_text

from core.models import Article

text = extract_text('../res/test_diploma.pdf')

print(text)

article = Article.objects.create(text=text)
print(article)
