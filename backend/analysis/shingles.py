shingle_len = 5  # длина шингла


# генерация шинглов
def get_shingles(source):
    import binascii
    out = []
    for i in range(len(source) - (shingle_len - 1)):
        filtered_shingles = ' '.join([x for x in source[i:i + shingle_len]])
        hashed = binascii.crc32(filtered_shingles.encode('utf-8'))
        out.append(hashed)
    return out


# генерация шинглов
def get_unique_shingles(source):
    import binascii
    out = []
    for i in range(0, len(source), shingle_len):
        filtered_shingles = ' '.join([x for x in source[i:i + shingle_len]])
        out.append(binascii.crc32(filtered_shingles.encode('utf-8')))
    return out


# сравнение выборок
def compare(source1, source2):
    same = list(set(source1) & set(source2))

    return len(same) * 2 / float(len(source1) + len(source2)) * 100


# метод шинглов
def shingles(text1, text2):
    cmp1 = get_shingles(text1)
    cmp2 = get_shingles(text2)
    print(cmp1, cmp2)
    return compare(cmp1, cmp2)


# метод уникальных шинглов
def unique_shingles(text1, text2):
    cmp1 = get_shingles(text1)
    cmp2 = get_shingles(text2)
    return compare(cmp1, cmp2)
