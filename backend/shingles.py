# -*- coding: UTF-8 -*-
import time

from py_tat_morphan.morphan import Morphan

if __name__ == '__build__':
    raise Exception

analyser = Morphan()

def canonize(source):
    stop_symbols = '.,!?:;-\n\r()'

    stop_words = (u'həм', u'əгəр', u'гəрчə',
                  u'чөнки', u'гүя', u'хəтта',
                  u'ягъни', u'мəсəлəн', u'хосусəн',
                  u'ə', u'әллә', u'әмма',
                  u'бәлки', u'белән', u'вә',
                  u'я', u'да', u'гүяки',
                  u'дә', u'ләкин', u'мәгәр',
                  u'нәкъ', u'ни', u'та',
                  u'тик', u'һәр', u'яисә',
                  u'яки', u'гына', u'бары')

    return ([analyser.lemma(x)[0] for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)])


def genshingle(source):
    import binascii
    out = []
    for i in range(len(source) - (shingle_len - 1)):
        out.append(binascii.crc32(' '.join([x for x in source[i:i + shingle_len]]).encode('utf-8')))

    return out


def compaire(source1, source2):
    same = 0
    for i in range(len(source1)):
        if source1[i] in source2:
            same = same + 1

    return same * 2 / float(len(source1) + len(source2)) * 100


shingle_len = 5  # длина шингла


def main():
    time_req = time.time()
    with open('resources/full2.txt', 'r', encoding="utf-8") as file1:
        with open('resources/mixed15.txt', 'r', encoding="utf-8") as file2:
            text1 = file1.read()
            text2 = file2.read()
    cmp1 = genshingle(canonize(text1))
    print(cmp1)
    cmp2 = genshingle(canonize(text2))
    print(canonize(text1))
    print(compaire(cmp1, cmp2), '%')
    time_req = time.time() - time_req
    print("Потрачено:", time_req, "секунд")


# Start program
main()
