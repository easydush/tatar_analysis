from py_tat_morphan.morphan import Morphan

analyser = Morphan()

# part = open('resources/part.txt', 'r', encoding='utf-8')
# part = part.read()
# print(part)
# print(analyser.process_text(part))

original = open('resources/full1.txt', 'r', encoding='utf-8')
original = original.read().replace('-', ' ').replace('.', ' ').replace(',', ' ')
original = original.split()

lemmas = []
print(original)
for word in original:
    lemma = analyser.lemma(word)
    lemmas.append(lemma)
    print(lemma[0])