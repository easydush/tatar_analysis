# -*- coding: UTF-8 -*-
#!/usr/bin/python

from unittest import TestCase

from py_tat_morphan.morphan import Morphan
from py_tat_morphan.disambiguation import is_amtype_pattern


RULES = [[u'N|V+IMP_SG()', 
          [[[[3, u'V', 1, 1, u'and']], u'N'],
           [[[2, u'Type1', 1, 1, u'and']], u'V'],
           [[], u'N']],
          []],
        ]

SENTENCES = [[('Язгы', 'язгы+Adj;'),
              ('ташуларда', 'NR'),
              ('көймә', 'көй+V+NEG(мА)+IMP_SG();көймә+N+Sg+Nom;'),
              ('йөздерәбез', 'йөз+V+CAUS(ДЫр)+PRES(Й)+1PL(бЫз);йөздер+V+PRES(Й)+1PL(бЫз);'),
              ('.', 'Type1')],
             [('Язгы', 'язгы+Adj;'),
              ('ташуларда', 'NR'),
              ('көймә', 'көй+V+NEG(мА)+IMP_SG();көймә+N+Sg+Nom;'),
              ('көймә', 'көй+V+NEG(мА)+IMP_SG();көймә+N+Sg+Nom;'),
              ('.', 'Type1')],
            ]

class TestDisam(TestCase):
    def test_disambiguate_text(self):
        tatmorphan = Morphan()
        text = u'Язгы ташуларда көймә йөздерәбез.Язгы ташуларда көймә көймә.'
        expected = [[(u'\u042f\u0437\u0433\u044b', 
                      u'\u044f\u0437\u0433\u044b+Adj;'), 
                     (u'\u0442\u0430\u0448\u0443\u043b\u0430\u0440\u0434\u0430', 
                      u'\u0442\u0430\u0448\u0443+N+PL(\u041b\u0410\u0440)+LOC(\u0414\u0410);\u0442\u0430\u0448\u044b+V+VN_1(\u0443/\u04af/\u0432)+PL(\u041b\u0410\u0440)+LOC(\u0414\u0410);'), 
                     (u'\u043a\u04e9\u0439\u043c\u04d9', 
                      u'\u043a\u04e9\u0439\u043c\u04d9+N+Sg+Nom'), 
                     (u'\u0439\u04e9\u0437\u0434\u0435\u0440\u04d9\u0431\u0435\u0437',
                      u'\u0439\u04e9\u0437+V+CAUS(\u0414\u042b\u0440)+PRES(\u0419)+1PL(\u0431\u042b\u0437);\u0439\u04e9\u0437\u0434\u0435\u0440+V+PRES(\u0419)+1PL(\u0431\u042b\u0437);'), 
                     (u'.', 'Type1')],
                    [(u'\u042f\u0437\u0433\u044b', 
                      u'\u044f\u0437\u0433\u044b+Adj;'), 
                     (u'\u0442\u0430\u0448\u0443\u043b\u0430\u0440\u0434\u0430', 
                      u'\u0442\u0430\u0448\u0443+N+PL(\u041b\u0410\u0440)+LOC(\u0414\u0410);\u0442\u0430\u0448\u044b+V+VN_1(\u0443/\u04af/\u0432)+PL(\u041b\u0410\u0440)+LOC(\u0414\u0410);'), 
                     (u'\u043a\u04e9\u0439\u043c\u04d9', 
                      u'\u043a\u04e9\u0439\u043c\u04d9+N+Sg+Nom'), 
                     (u'\u043a\u04e9\u0439\u043c\u04d9', 
                      u'\u043a\u04e9\u0439+V+NEG(\u043c\u0410)+IMP_SG()'), 
                     (u'.', 'Type1')]
                   ]
        analysed = tatmorphan.disambiguate_text(text)
        self.assertEqual(analysed, expected)

    def test_is_amtype_pattern(self):
        self.assertEqual(is_amtype_pattern(u'V+NEG(мА)+IMP_SG()|N+Sg+Nom'), True)
        self.assertEqual(is_amtype_pattern(u'V+NEG+IMP_SG|N+Sg+Nom'), True)
        self.assertEqual(is_amtype_pattern(u'PROP|'), True)
        self.assertEqual(is_amtype_pattern(u'PROP'), False)
        self.assertEqual(is_amtype_pattern(u'PROP|Wrong_chain'), False)
