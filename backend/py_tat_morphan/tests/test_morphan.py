# -*- coding: UTF-8 -*-
#!/usr/bin/python
from unittest import TestCase

from py_tat_morphan.morphan import Morphan

class TestMorphan(TestCase):
    def test_analyse(self):
        tatmorphan = Morphan()
        word = u'кеше'
        expected = u'кеше+N+Sg+Nom;'
        analysed = tatmorphan.analyse(word)
        self.assertEqual(analysed, expected)

        word = 'Кеше'
        expected = u'кеше+N+Sg+Nom;'
        analysed = tatmorphan.analyse(word)
        self.assertEqual(analysed, expected)

        word = 'урман'
        expected = u'урман+N+Sg+Nom;'
        analysed = tatmorphan.analyse(word)
        self.assertEqual(analysed, expected)

        word = u'Урман'
        expected = u'урман+N+Sg+Nom;'
        analysed = tatmorphan.analyse(word)
        self.assertEqual(analysed, expected)

        word = 'алма'
        expected = u'ал+V+NEG(мА)+IMP_SG();алма+N+Sg+Nom;'
        analysed = tatmorphan.analyse(word)
        self.assertEqual(analysed, expected)

        word = 'алмар'
        expected = u'Rus'
        analysed = tatmorphan.analyse(word)
        self.assertEqual(analysed, expected)

        word = '≫'
        expected = u'Type4'
        analysed = tatmorphan.analyse(word)
        self.assertEqual(analysed, expected)


    def test_lemma(self):
        tatmorphan = Morphan()
        word = u'кеше'
        expected = [u'кеше']
        analysed = tatmorphan.lemma(word)
        self.assertEqual(analysed, expected)

        word = u'алмалардай'
        expected = [u'алма']
        analysed = tatmorphan.lemma(word)
        self.assertEqual(analysed, expected)

        word = u'алма'
        expected = [u'ал', u'алма']
        analysed = tatmorphan.lemma(word)
        self.assertEqual(analysed, expected)

    def test_pos(self):
        tatmorphan = Morphan()
        word = u'кеше'
        expected = [u'N']
        analysed = tatmorphan.pos(word)
        self.assertEqual(analysed, expected)

        word = u'алмалардай'
        expected = [u'N']
        analysed = tatmorphan.pos(word)
        self.assertEqual(analysed, expected)

        word = u'алма'
        expected = [u'N', u'V']
        analysed = tatmorphan.pos(word)
        self.assertEqual(analysed, expected)

    def test_process_text(self):
        tatmorphan = Morphan(params={'sdelimiter': u'\n', 'ignore_newlines': False})
        text = 'Кеше , урман 3 dssdf\n Алмав леса ал-мап'
        expected = u'Кеше\nкеше+N+Sg+Nom;\n,\nType2\nурман\nурман+N+Sg+Nom;\n3\nNum\ndssdf\nLatin\n\nNL\nАлмав\nNR\nлеса\nRus\nал-мап\nNR'
        analysed = tatmorphan.process_text(text)
        self.assertEqual(analysed, expected)

        tatmorphan = Morphan(params={'sdelimiter': u'\n', 'ignore_newlines': True})
        text = 'Кеше , урман 3 dssdf\n Алмав леса ал-мап'
        expected = u'Кеше\nкеше+N+Sg+Nom;\n,\nType2\nурман\nурман+N+Sg+Nom;\n3\nNum\ndssdf\nLatin\nАлмав\nNR\nлеса\nRus\nал-мап\nNR'
        analysed = tatmorphan.process_text(text)
        self.assertEqual(analysed, expected)
