from py_tat_morphan.morphan import Morphan

class Lemmatizer:
    def __init__(self):
        self.morphan = Morphan()

    def clean(self):
        pass

    def lemmatize(self):
        pass

morphan = Morphan()

print(morphan.lemma('мишәрләр'))