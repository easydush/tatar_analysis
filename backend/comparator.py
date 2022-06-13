# -*- coding: UTF-8 -*-
import time
from collections import Counter

from analysis.combined import combined
from analysis.recents import recents
from analysis.shingles import shingles, unique_shingles
from py_tat_morphan.morphan import Morphan

if __name__ == '__build__':
    raise Exception

analyser = Morphan()


def canonize(source):
    stop_symbols = '.,!?:;-\n\r()«—»[]'

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
    return [lemma for lemma in lemmas if lemma != 'NR']


def get_sorted_recents(source):
    out = list(Counter(source).keys())
    out = sorted(out[:21])
    return out


shingle_len = 5  # длина шингла


def main():
    with open('resources/full3.txt', 'r', encoding="utf-8") as file1:
        with open('resources/mixed50.txt', 'r', encoding="utf-8") as file2:
            text1 = file1.read()
            text2 = file2.read()
    text1 = canonize(text1)
    text2 = canonize(text2)

    print('Метод шинглов/n')
    time_req = time.time()
    print(shingles(text1, text2), '%')
    time_req = time.time() - time_req
    print("Потрачено:", time_req, "секунд")

    print('Метод уникальных шинглов/n')
    time_req = time.time()
    print(unique_shingles(text1, text2), '%')
    time_req = time.time() - time_req
    print("Потрачено:", time_req, "секунд")

    print('Метод сравнения наиболее встречающихся/n')
    time_req = time.time()
    print(recents(text1, text2), '%')
    time_req = time.time() - time_req
    print("Потрачено:", time_req, "секунд")

    print('Комбинация методов/n')
    time_req = time.time()
    print(combined(text1, text2), '%')
    time_req = time.time() - time_req
    print("Потрачено:", time_req, "секунд")


# Start program
main()
