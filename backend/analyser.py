from py_tat_morphan.morphan import Morphan

analyser = Morphan()

original = open('resources/part.txt', 'r', encoding='utf-8')
original = original.read()
print(original)
print(analyser.process_text(original))