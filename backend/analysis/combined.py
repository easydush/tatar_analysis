from collections import Counter

shingle_len = 5  # длина шингла


# генерация выборки
def get_sorted_recents(source):
    out = list(Counter(source).keys())
    out = sorted(out[:21])
    return out


# генерация шинглов
def get_shingles(source):
    import binascii
    out = []
    for i in range(len(source) - (shingle_len - 1)):
        filtered_shingles = ' '.join([x for x in source[i:i + shingle_len]])
        hashed = binascii.crc32(filtered_shingles.encode('utf-8'))
        out.append(hashed)
    return out


# сравнение выборок
def compare(source1, source2):
    same = list(set(source1) & set(source2))
    return len(same) * 2 / float(len(source1) + len(source2)) * 100


# главный метод
def combined(text1, text2):
    cmp1 = get_shingles(get_sorted_recents(text1))
    cmp2 = get_shingles(get_sorted_recents(text2))
    return compare(cmp1, cmp2)

