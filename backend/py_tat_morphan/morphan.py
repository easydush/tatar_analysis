# -*- coding: UTF-8 -*-
#!/usr/bin/python

import re
import os
import sys
import logging

# python 3 porting
# if sys.version_info > (3, 0):
#     import hfst_lookup
#     CHFST = True
# else:
try:
    import hfst_lookup
    CHFST = True
except ImportError:
    from .shared import Header, Alphabet
    from .transducer import Transducer
    from .transducer import TransducerW
    CHFST = False

import pymorphy2
from pymorphy2.units.by_analogy import KnownSuffixAnalyzer, UnknownPrefixAnalyzer, DictionaryAnalyzer

from py_tat_morphan.disambiguation import disambiguate_word, load_disam_rules

logging.basicConfig(filename='log.log', level=logging.DEBUG)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_MORPHAN_FILE = os.path.join(BASE_DIR, 'files/tatar_last.hfstol')
WORDS_FILE = os.path.join(BASE_DIR, 'files/words.csv')
TOKENS_FILE = os.path.join(BASE_DIR, 'files/tokens.csv')
EXCEPTIONS_FILE = os.path.join(BASE_DIR, 'files/exceptions.txt')
DISAM_RULES_FILES = os.path.join(BASE_DIR, 'files/disam_rules.json')

PARAMS = {'sdelimiter': u'\t',
          'fdelimiter': u'\n',
          'ignore_newlines': True
         }

def fix(text):
    """
        Prepare text for analysis:
        - Corrects some errors of Tatar language texts
        - Unifies letters, e.g. 'ђ' -> 'ә'
    """
    if sys.version_info < (3, 0) and not isinstance(text, unicode):
        text = text.decode('utf-8')

    letters = {u'ђ':u'ә', u'њ':u'ү', u'ќ':u'җ', u'љ':u'ө', u'ћ':u'ң',
               u'џ':u'һ', u'Ә':u'ә', u'Ү':u'ү', u'Ө':u'ө', u'Җ':u'җ',
               u'Һ':u'һ', u'Ң':u'ң',
               u'Ђ': u'Җ',  #  - почему для ә и Җ используются один и тот де символ?
               u'Љ': u'Ө', u'Њ': u'ү', u'Ќ': u'Җ', u'Џ': u'һ', u'Ћ': u'Ң'}
    # some texts contains words with not right letters, need to replace to right
    for letter in letters:
        text = text.replace(letter, letters[letter])

    # replace some errors
    text = text.replace(u'-\r\n', u'').replace(u'-\n\r', u'')\
               .replace(u'-\n', u'').replace(u'-\r', u'')\
               .replace(u'¬', u'').replace(u'...', u'…')\
               .replace(u'!..', u'!').replace(u'?..', u'?')\
               .replace(u' -', u' - ').replace(u'- ', u' - ')\
               .replace(u'\xad', '').replace(u'\ufeff', '')\
               .replace(u'ª', '').replace(u'’', '')\
               .replace(u'´', '')

    return text


def tokenize(text):
    """
        Splits text into tokens
    """
    tokens = re.split(r"([ .,!?\n\r\t“”„‘«»≪≫\{\}\(\)\[\]:;\'\"+=*\—_^…\|\/\\ ]|[0-9]+)", text)

    # filtering all spaces
    # tokens = filter(lambda token: token not in [u' ', u' ', u'', u'\r', u'\t'], tokens)
    tokens = [token.strip('-') for token in tokens if token not in [' ', u' ', u'', u'\r', u'\t']]

    return tokens


def to_text(sentences, sdelimiter=u'\t', fdelimiter=u'\n'):
    """
        Joins result of morphan into plain text
    """
    result = []
    for sentence in sentences:
        for (token, tag) in sentence:
            result.append('%s%s%s' % (token, sdelimiter, tag))
    return fdelimiter.join(result)


class Morphan:
    def __init__(self, 
                 transducerfile=None, 
                 wordsfile=None, 
                 exceptionsfile=None, 
                 disamrulesfile=None,
                 tokensfile=None,
                 params={}):
        '''
            Initialize Morphan:
            - import transducer file from dir
            - import disam files
            - import exception file

        '''
        self.params = PARAMS
        if not transducerfile:
            transducerfile = DEFAULT_MORPHAN_FILE
        if not wordsfile:
            wordsfile = WORDS_FILE
        if not exceptionsfile:
            exceptionsfile = EXCEPTIONS_FILE
        if not disamrulesfile:
            disamrulesfile = DISAM_RULES_FILES
        if not tokensfile:
            tokensfile = TOKENS_FILE
        self.params.update(params)
            
        # if C hfst_lookup package installed
        if CHFST:
            logging.info('Import CHFST`s Transducer...')
            self.ctransducer = hfst_lookup.Transducer(transducerfile)
            self.transducer = None
        else:
            # else loads the simple transducer
            logging.info('Import Python HFST`s Transducer...')
            self.ctransducer = None
            handle = open(transducerfile, "rb")
            self.header = Header(handle)
            self.alphabet = Alphabet(handle, self.header.number_of_symbols)
            if self.header.weighted:
                self.transducer = TransducerW(handle, self.header, self.alphabet)
            else:
                self.transducer = Transducer(handle, self.header, self.alphabet)
            handle.close()

        # loads words and exceptions for better performance
        self.words = {}
        if not self.ctransducer:
            logging.info('Import Words list...')
            with open(wordsfile, 'rb') as stream:
                lines = stream.read().decode('UTF-8').split('\n')
            for line in lines:
                if not line:
                    continue
                word, morphcode = line.split('\t')
                self.words[word] = morphcode

        logging.info('Import Exceptional words list...')
        with open(exceptionsfile, 'rb') as stream:
            lines = stream.read().decode('UTF-8').split('\n')
            for line in lines:
                if not line:
                    continue
                word, morphcode = line.split('\t')
                self.words[word] = morphcode


        logging.info('Import tokens list...')
        self.tokens = {}
        with open(tokensfile, 'rb') as stream:
            lines = stream.read().decode('UTF-8').split('\n')
            for line in lines:
                if not line:
                    continue
                token, tag = line.split('\t')
                self.tokens[token] = tag

        logging.info('Import Russian Morphan (pymorphy2)...')
        self.rusmorphan = pymorphy2.MorphAnalyzer()

        logging.info('Import Contextual Rules for Disambiguation...')
        self.disam_rules = load_disam_rules(disamrulesfile)


    def lookup(self, token):
        '''
            Loads HFST Trancducer to tag the word
        '''
        if sys.version_info < (3, 0) and not isinstance(token, unicode):
            token = token.decode('UTF-8')

        if token.lower() in self.words:
            return self.words[token.lower()]

        if self.ctransducer:
            # python 3 porting
            if sys.version_info < (3, 0):
                token = token.encode('UTF-8')
            result = self.ctransducer.lookup(token)
            if not result:
                return None

            # delete '+' sign in the end of analysis
            # python 3 porting
            if sys.version_info < (3, 0):
                result = [row[0].decode('UTF-8') if row[0][-1] != '+' else row[0][:-1] 
                          for row in result]
            else:
                result = [row[0] if row[0][-1] != '+' else row[0][:-1] for row in result]

            # delete duplicates and sort, then join with ';' delimiter
            return ';'.join(sorted(list(set(result)))) + ';'
        else:
            if self.transducer.analyze(token):
                result = self.transducer.displayVector

                if not result:
                    return None
                # delete '+' sign in the end of analysis

                result = [row[0] if row[0][-1] != u'+' else row[0][:-1] for row in result]
                # delete duplicates and sort, then join with ';' delimiter
                return ';'.join(sorted(list(set(result)))) + ';'
        return None


    def analyse(self, token):
        """
            Tag word
        """
        if sys.version_info < (3, 0) and not isinstance(token, unicode):
            token = token.decode('UTF-8')

        token_lower = token.lower()
        if token_lower in self.tokens:
            result = self.tokens[token_lower]
        elif token in [u'\n', u'\n\r']:
            result = 'NL'
        elif token.isdigit():
            result = 'Num'
        elif re.match(u'^[a-zA-Z-]+$', token):
            result = 'Latin'
        elif re.match(u'^[^а-яА-ЯөүһңҗәҺҮӨҖҢӘЁё]$', token):
            result = 'Sign'
        elif (re.match(u'[а-яА-ЯөӨүҮһҺңҢҗҖәӘЁё]+$', token)) \
             or (re.match(u'[а-яА-ЯөӨүҮһҺңҢҗҖәӘЁё]+-[а-яА-ЯөӨүҮһҺңҢҗҖЁёәӘ]+$', token)):
            if token.count("-") > 1:
                result = 'Error'
            else:
                res = self.lookup(token)
                if not res:
                    res = self.lookup(token_lower)
                if not res and self.is_russian_word(token):
                    res = 'Rus'
                if not res:
                    result = 'NR'
                else:
                    result = res
        else:
            result = 'Error'

        return result


    def lemma(self, token):
        """
            Returns the lemma of the word
        """
        analysed = self.analyse(token)
        if analysed:
            return sorted(list(set([res.split(u'+')[0] for res in analysed.strip(';').split(';')])))


    def pos(self, token):
        """
            Returns the part-of-speech of the word
            !TODO
        """
        analysed = self.analyse(token)
        if analysed:
            return sorted(list(set([res.split(u'+')[1] for res in analysed.strip(';').split(';')])))


    def is_russian_word(self, word):
        """
            Parses word and check if word is russian
        """
        parses = self.rusmorphan.parse(word)
        for parse in parses:
            if 'UNKN' not in parse.tag and \
                not isinstance(parse.methods_stack[0][0], KnownSuffixAnalyzer.FakeDictionary) and\
                not isinstance(parse.methods_stack[1][0] if len(parse.methods_stack) > 1 else None,\
                                UnknownPrefixAnalyzer) and\
                isinstance(parse.methods_stack[0][0], DictionaryAnalyzer):
                return True
        return False


    def process_tokens(self, tokens):
        return dict([(token, self.analyse(token))
                     for token in set(tokens) 
                     if token not in [u'\n\r', u'\r']])


    def analyse_text(self, text):
        """
            Process text and return as list of words
        """
        if sys.version_info < (3, 0) and not isinstance(text, unicode):
            text = text.decode('utf-8')

        text = fix(text)
        tokens = tokenize(text)
        tagged_tokens = self.process_tokens(tokens)

        sentence = []
        sentences = []

        for i, token in enumerate(tokens):
            tag = tagged_tokens.get(token, 'Error')
            if tag == 'Type1':
                sentence.append((token, tag))
                sentences.append(sentence)
                sentence = []
            elif tag == 'NL': 
                if not self.params.get('ignore_newlines'):
                    sentence.append(('', 'NL'))
                    # if new line starts with uppercase, but prev line was not ended
                    if len(sentence) > 0 and i < len(tokens)-1 and tokens[i+1].istitle():
                        sentences.append(sentence)
                        sentence = []
            else:
                sentence.append((token, tag))

        if len(sentence) > 0:
            sentences.append(sentence)

        return len(tokens), len(tagged_tokens), len(sentences), sentences


    def process_text(self, text):
        """
            Takes plain text, tags and returns as plain text
        """
        if sys.version_info < (3, 0) and not isinstance(text, unicode):
            text = text.decode('utf-8')

        sdelimiter = self.params.get('sdelimiter', '\t')
        fdelimiter = self.params.get('fdelimiter', '\n')
        tokens_count, unique_tokens_count, sentences_count, sentences = self.analyse_text(text)

        result = []
        for sentence in sentences:
            for (token, tag) in sentence:
                result.append('%s%s%s' % (token, sdelimiter, tag))
        return fdelimiter.join(result)


    def disambiguate(self, text, disam_rules=None):
        """
            Parses text, analyses it and disambiguate morphological ambiguities
        """
        if not disam_rules:
            disam_rules = self.disam_rules
        tokens_count, unique_tokens_count, sentences_count, sentences = self.analyse_text(text)
        disamed_words_count = 0
        for sentence in sentences:
            for index, word in enumerate(sentence):
                if len(word[1].split(';')) >= 3:
                    # ambiguos word
                    result = disambiguate_word(sentence, index, disam_rules)
                    if result:
                        disamed_words_count += 1
                        sentence[index] = (word[0], result)
        return tokens_count, unique_tokens_count, sentences_count, disamed_words_count, sentences


    def disambiguate_text(self, text, disam_rules=None):
        """
            For Backward compatibility with older verions
        """
        tokens_count, unique_tokens_count, sentences_count, \
        disamed_words_count, sentences = self.disambiguate(text)
        return sentences
