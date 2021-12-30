import re

from flashtext import KeywordProcessor
from pymorphy2 import MorphAnalyzer


class ArticleAnalyser:
    def __init__(self):
        self._keyword_processor = KeywordProcessor()
        self._morph = MorphAnalyzer()

    def add_keywords(self, trigger_words):
        self._keyword_processor.add_keywords_from_list(list(trigger_word.name for trigger_word in trigger_words))

    def clean_text(self, text):
        return re.sub(r'\W+', ' ', text)

    def get_word_with_normal_form(self, word):
        return self._morph.parse(word)[0].normal_form

    def check_text(self, text):
        text_clean_copy = self.clean_text(text)
        text_clean_copy = text_clean_copy.split()
        words_list = list(
            map(
                lambda word: self.get_word_with_normal_form(word), text_clean_copy
            )
        )
        clean_text = ' '.join(words_list)
        return self._keyword_processor.extract_keywords(clean_text)
