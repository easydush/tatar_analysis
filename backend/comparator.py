# -*- coding: UTF-8 -*-
import time
from collections import Counter

from py_tat_morphan.morphan import Morphan

if __name__ == '__build__':
    raise Exception

analyser = Morphan()


def canonize(source):
    stop_symbols = '.,!?:;-\n\r()'

    stop_words = (u'həм', u'əгəр', u'ə', u'әллә', u'әмма',
                  u'чөнки', u'гүя', u'хəтта', u'гəрчə',
                  u'ягъни', u'мəсəлəн', u'хосусəн',
                  u'бәлки', u'белән', u'кебек', u'вә',
                  u'шикелле', u'сыман', u'сымак', u'аркылы',
                  u'хакында', u'хакта', u'өчен', u'сәбәпле',
                  u'я', u'да', u'дә', u'та', u'тә', u'гүяки',
                  u'ләкин', u'мәгәр', u'нәкъ', u'ни', u'янә',
                  u'тик', u'һәр', u'яисә', u'яки',
                  u'гына', u'бары', u'фәкать')
    lemmas = [analyser.lemma(x)[0] for x in [y.strip(stop_symbols) for y in source.lower().split()] if
             x and (x not in stop_words)]
    return [lemma for lemma in lemmas if lemma!= 'NR']


def get_shingles(source):
    import binascii
    out = []
    for i in range(len(source) - (shingle_len - 1)):
        out.append(binascii.crc32(' '.join([x for x in source[i:i + shingle_len]]).encode('utf-8')))
    return out


def get_unique_shingles(source):
    import binascii
    out = []
    for i in range(0, len(source), shingle_len):
        out.append(binascii.crc32(' '.join([x for x in source[i:i + shingle_len]]).encode('utf-8')))
    return out

def get_recents(source):
    out = list(Counter(source).keys())
    return out[:int(len(source) * 0.3)]

def get_sorted_recents(source):
    out = list(Counter(source).keys())
    out = sorted(out[:21])
    return out

def compaire(source1, source2):
    same = 0
    for i in range(len(source1)):
        if source1[i] in source2:
            same = same + 1

    return same * 2 / float(len(source1) + len(source2)) * 100


shingle_len = 5  # длина шингла


def main():
    with open('resources/full1.txt', 'r', encoding="utf-8") as file1:
        with open('resources/mixed15.txt', 'r', encoding="utf-8") as file2:
            text1 = file1.read()
            text2 = file2.read()
    text1 = canonize(text1)
    text2 = canonize(text2)

    print('Метод шинглов/n')
    time_req = time.time()
    cmp1 = get_shingles(text1)
    cmp2 = get_shingles(text2)
    print(compaire(cmp1, cmp2), '%')
    time_req = time.time() - time_req
    print("Потрачено:", time_req, "секунд")

    print('Метод уникальных шинглов/n')
    time_req = time.time()
    cmp1 = get_unique_shingles(text1)
    cmp2 = get_unique_shingles(text2)
    print(compaire(cmp1, cmp2), '%')
    time_req = time.time() - time_req
    print("Потрачено:", time_req, "секунд")

    print('Метод сравнения наиболее встречающихся/n')
    time_req = time.time()
    cmp1 = get_recents(text1)
    cmp2 = get_recents(text2)
    print(compaire(cmp1, cmp2), '%')
    time_req = time.time() - time_req
    print("Потрачено:", time_req, "секунд")

    print('Комбинация методов/n')
    time_req = time.time()
    cmp1 = get_sorted_recents(text1)
    cmp2 = get_sorted_recents(text2)
    print(compaire(cmp1, cmp2), '%')
    time_req = time.time() - time_req
    print("Потрачено:", time_req, "секунд")


# Start program
main()
