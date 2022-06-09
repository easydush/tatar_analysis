from collections import Counter


# генерация выборки
def get_recents(source):
    out = list(Counter(source).keys())
    return out[:int(len(source) * 0.3)]


# сравнение выборок
def compare_recents(selection1, selection2):
    same = list(set(selection1) & set(selection2))

    return len(same) * 2 / float(len(selection1) + len(selection2)) * 100


# главный метод
def recents(text1, text2):
    cmp1 = get_recents(text1)
    cmp2 = get_recents(text2)
    return compare_recents(cmp1, cmp2)
