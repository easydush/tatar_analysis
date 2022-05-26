# -*- coding: UTF-8 -*-
import time

if __name__ == '__build__':
    raise Exception


def canonize(source):
    stop_symbols = '.,!?:;-\n\r()'

    stop_words = (u'это', u'как', u'так',
                  u'и', u'в', u'над',
                  u'к', u'до', u'не',
                  u'на', u'но', u'за',
                  u'то', u'с', u'ли',
                  u'а', u'во', u'от',
                  u'со', u'для', u'о',
                  u'же', u'ну', u'вы',
                  u'бы', u'что', u'кто',
                  u'он', u'она')

    return ([x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)])


def genshingle(source):
    import binascii
    out = []
    for i in range(len(source) - (shingleLen - 1)):
        out.append(binascii.crc32(' '.join([x for x in source[i:i + shingleLen]]).encode('utf-8')))

    return out


def compaire(source1, source2):
    same = 0
    for i in range(len(source1)):
        if source1[i] in source2:
            same = same + 1

    return same * 2 / float(len(source1) + len(source2)) * 100


shingleLen = 3  # длина шингла


def main():
    time_req = time.time()
    with open('resources/full.txt', 'r', encoding="utf-8") as file1:
        with open('resources/part.txt', 'r', encoding="utf-8") as file2:
            text1 = file1.read()
            text2 = file2.read()
    cmp1 = genshingle(canonize(text1))
    cmp2 = genshingle(canonize(text2))
    print(canonize(text1))
    print(compaire(cmp1, cmp2), '%')
    time_req = time.time() - time_req
    print("Потрачено:", time_req, "секунд")


# Start program
main()
